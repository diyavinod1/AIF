from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
from typing import Optional, Dict, Any

from .models.resume_parser import ResumeParser
from .models.ats_scorer import ATSScorer
from .models.optimizer import ResumeOptimizer
from .models.linkedin_generator import LinkedInGenerator
from .utils.file_handlers import FileHandler

app = FastAPI(title="AI Resume Optimizer", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize components
resume_parser = ResumeParser()
ats_scorer = ATSScorer()
resume_optimizer = ResumeOptimizer()
linkedin_generator = LinkedInGenerator()
file_handler = FileHandler()

@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """Handle resume file upload"""
    try:
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are allowed")
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        return {"filename": filename, "message": "File uploaded successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@app.post("/api/analyze-resume")
async def analyze_resume(
    filename: str = Form(...),
    job_description: Optional[str] = Form("")
):
    """Analyze resume and provide ATS scoring"""
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Parse resume
        parsed_data = resume_parser.parse_resume(file_path)
        
        # Calculate ATS score
        ats_score = ats_scorer.calculate_score(parsed_data, job_description)
        
        # Generate optimization suggestions
        optimization_suggestions = resume_optimizer.get_suggestions(parsed_data, job_description)
        
        # Generate LinkedIn suggestions
        linkedin_suggestions = linkedin_generator.generate_suggestions(parsed_data)
        
        return {
            "parsed_data": parsed_data,
            "ats_score": ats_score,
            "optimization_suggestions": optimization_suggestions,
            "linkedin_suggestions": linkedin_suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.post("/api/optimize-resume")
async def optimize_resume(
    filename: str = Form(...),
    job_description: str = Form(...),
    region: str = Form("US")
):
    """Generate optimized resume version"""
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="File not found")
        
        # Parse original resume
        parsed_data = resume_parser.parse_resume(file_path)
        
        # Generate optimized resume
        optimized_content = resume_optimizer.optimize_resume(parsed_data, job_description, region)
        
        # Save optimized version
        optimized_filename = f"optimized_{filename}"
        optimized_path = os.path.join(UPLOAD_DIR, optimized_filename)
        
        file_handler.save_resume(optimized_content, optimized_path, file_path)
        
        return {
            "optimized_filename": optimized_filename,
            "optimized_content": optimized_content
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error optimizing resume: {str(e)}")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Download optimized resume file"""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )

@app.get("/")
async def root():
    return {"message": "AI Resume Optimizer API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
