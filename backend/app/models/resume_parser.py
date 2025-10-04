import spacy
import pdfplumber
from docx import Document
import re
from typing import Dict, List, Any
import dateparser
from datetime import datetime

class ResumeParser:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Downloading spaCy model...")
            from spacy.cli import download
            download("en_core_web_sm")
            self.nlp = spacy.load("en_core_web_sm")
        
        self.skill_patterns = self._load_skill_patterns()
    
    def _load_skill_patterns(self) -> List[str]:
        """Load common skill patterns"""
        return [
            # Programming languages
            r'\b(python|java|javascript|typescript|c\+\+|c#|go|rust|swift|kotlin|r|sql)\b',
            # Frameworks
            r'\b(react|angular|vue|django|flask|spring|express|laravel|rails|tensorflow|pytorch)\b',
            # Tools
            r'\b(docker|kubernetes|aws|azure|gcp|git|jenkins|ansible|terraform)\b',
            # Soft skills
            r'\b(leadership|communication|teamwork|problem-solving|critical thinking|adaptability)\b'
        ]
    
    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """Parse resume file and extract information"""
        text = self._extract_text(file_path)
        doc = self.nlp(text)
        
        return {
            "raw_text": text,
            "skills": self._extract_skills(doc, text),
            "experience": self._extract_experience(doc, text),
            "education": self._extract_education(doc, text),
            "projects": self._extract_projects(text),
            "personal_info": self._extract_personal_info(doc),
            "summary": self._extract_summary(text)
        }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        if file_path.lower().endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        doc = Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def _extract_skills(self, doc, text: str) -> List[str]:
        """Extract skills using patterns and NER"""
        skills = set()
        
        # Pattern matching
        for pattern in self.skill_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                skills.add(match.group().title())
        
        # NER-based extraction
        for ent in doc.ents:
            if ent.label_ in ["ORG", "PRODUCT", "TECH"]:
                skills.add(ent.text)
        
        return sorted(list(skills))
    
    def _extract_experience(self, doc, text: str) -> List[Dict]:
        """Extract work experience"""
        experience = []
        
        # Look for experience sections
        experience_patterns = [
            r'experience.*?(?=education|projects|skills|$)',
            r'work.*?(?=education|projects|skills|$)',
            r'employment.*?(?=education|projects|skills|$)'
        ]
        
        for pattern in experience_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                exp_section = match.group()
                jobs = self._parse_jobs(exp_section)
                experience.extend(jobs)
        
        return experience
    
    def _parse_jobs(self, text: str) -> List[Dict]:
        """Parse individual job entries"""
        jobs = []
        
        # Simple job parsing - can be enhanced
        lines = text.split('\n')
        current_job = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for job title patterns
            if re.search(r'(senior|junior|lead|manager|director|engineer|developer|analyst)', line.lower()):
                if current_job:
                    jobs.append(current_job)
                    current_job = {}
                
                # Try to extract dates
                dates = self._extract_dates(line)
                current_job = {
                    "title": line,
                    "company": "",
                    "dates": dates,
                    "description": []
                }
            elif current_job and len(line) > 10:
                current_job["description"].append(line)
        
        if current_job:
            jobs.append(current_job)
        
        return jobs
    
    def _extract_dates(self, text: str) -> List[str]:
        """Extract dates from text"""
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}',
            r'\b\d{1,2}/\d{4}',
            r'\b\d{4}'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                dates.append(match.group())
        
        return dates
    
    def _extract_education(self, doc, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        education_patterns = [
            r'education.*?(?=experience|projects|skills|$)',
            r'academic.*?(?=experience|projects|skills|$)'
        ]
        
        for pattern in education_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                edu_section = match.group()
                institutions = self._parse_education_institutions(edu_section)
                education.extend(institutions)
        
        return education
    
    def _parse_education_institutions(self, text: str) -> List[Dict]:
        """Parse education institutions"""
        institutions = []
        lines = text.split('\n')
        
        current_edu = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Look for degree patterns
            if re.search(r'\b(B\.?S\.?|B\.?A\.?|M\.?S\.?|M\.?A\.?|PhD|Bachelor|Master|Doctorate)', line, re.IGNORECASE):
                if current_edu:
                    institutions.append(current_edu)
                
                current_edu = {
                    "degree": line,
                    "institution": "",
                    "dates": self._extract_dates(line),
                    "details": []
                }
            elif current_edu and len(line) > 5:
                current_edu["details"].append(line)
        
        if current_edu:
            institutions.append(current_edu)
        
        return institutions
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract projects"""
        projects = []
        
        project_patterns = [
            r'projects.*?(?=experience|education|skills|$)',
            r'portfolio.*?(?=experience|education|skills|$)'
        ]
        
        for pattern in project_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                project_section = match.group()
                projects.extend(self._parse_project_entries(project_section))
        
        return projects
    
    def _parse_project_entries(self, text: str) -> List[Dict]:
        """Parse individual project entries"""
        projects = []
        lines = text.split('\n')
        
        current_project = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Project title pattern (usually short and descriptive)
            if len(line) < 100 and not line.startswith(('-', '•')):
                if current_project:
                    projects.append(current_project)
                
                current_project = {
                    "name": line,
                    "description": []
                }
            elif current_project and len(line) > 10:
                current_project["description"].append(line)
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_personal_info(self, doc) -> Dict[str, str]:
        """Extract personal information"""
        personal_info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, doc.text)
        if emails:
            personal_info["email"] = emails[0]
        
        # Extract phone numbers
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, doc.text)
        if phones:
            personal_info["phone"] = phones[0]
        
        # Extract name (first entity that looks like a person)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                personal_info["name"] = ent.text
                break
        
        return personal_info
    
    def _extract_summary(self, text: str) -> str:
        """Extract summary/objective section"""
        summary_patterns = [
            r'summary.*?(?=experience|education|skills|$)',
            r'objective.*?(?=experience|education|skills|$)',
            r'profile.*?(?=experience|education|skills|$)'
        ]
        
        for pattern in summary_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                return match.group().strip()
        
        # If no summary found, return first few lines
        lines = text.split('\n')
        return '\n'.join([line for line in lines[:3] if len(line.strip()) > 10])