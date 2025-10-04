import re
from typing import Dict, List, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ATSScorer:
    def __init__(self):
        self.weights = {
            "skills_match": 0.35,
            "keywords": 0.25,
            "formatting": 0.15,
            "readability": 0.15,
            "grammar": 0.10
        }
        
        self.common_keywords = {
            "technical": ["python", "java", "javascript", "sql", "aws", "docker", "kubernetes"],
            "soft_skills": ["leadership", "communication", "teamwork", "problem-solving", "adaptability"],
            "action_verbs": ["managed", "developed", "implemented", "led", "created", "optimized"]
        }
    
    def calculate_score(self, parsed_data: Dict[str, Any], job_description: str = "") -> Dict[str, Any]:
        """Calculate comprehensive ATS score"""
        scores = {}
        
        # Skills match score
        if job_description:
            scores["skills_match"] = self._calculate_skills_match(parsed_data["skills"], job_description)
        else:
            skills_score = len(parsed_data["skills"]) / 20  # Normalize based on expected skills count
            scores["skills_match"] = min(skills_score * 40, 40)  # Scale to 40 points
        
        # Keywords score
        scores["keywords"] = self._calculate_keywords_score(parsed_data["raw_text"])
        
        # Formatting score
        scores["formatting"] = self._calculate_formatting_score(parsed_data)
        
        # Readability score
        scores["readability"] = self._calculate_readability_score(parsed_data["raw_text"])
        
        # Grammar score
        scores["grammar"] = self._calculate_grammar_score(parsed_data["raw_text"])
        
        # Calculate total score
        total_score = sum(
            score * self.weights[category] 
            for category, score in scores.items() 
            if category in self.weights
        )
        
        # Convert to 0-100 scale
        total_score = (total_score / sum(self.weights.values())) * 100
        
        return {
            "total_score": round(total_score, 1),
            "breakdown": {
                "Skills Match": {
                    "score": round(scores["skills_match"], 1),
                    "max_score": 40 if job_description else 40,
                    "details": self._get_skills_match_details(parsed_data["skills"], job_description)
                },
                "Keywords": {
                    "score": round(scores["keywords"], 1),
                    "max_score": 20,
                    "details": self._get_keywords_details(parsed_data["raw_text"])
                },
                "Formatting": {
                    "score": round(scores["formatting"], 1),
                    "max_score": 15,
                    "details": self._get_formatting_details(parsed_data)
                },
                "Readability": {
                    "score": round(scores["readability"], 1),
                    "max_score": 15,
                    "details": self._get_readability_details(parsed_data["raw_text"])
                },
                "Grammar": {
                    "score": round(scores["grammar"], 1),
                    "max_score": 10,
                    "details": self._get_grammar_details(parsed_data["raw_text"])
                }
            }
        }
    
    def _calculate_skills_match(self, skills: List[str], job_description: str) -> float:
        """Calculate skills match with job description"""
        if not job_description:
            return 0
        
        # Extract skills from job description
        job_skills = self._extract_skills_from_text(job_description)
        
        if not job_skills:
            return 0
        
        # Calculate match percentage
        matched_skills = set(skill.lower() for skill in skills) & set(job_skills)
        match_percentage = len(matched_skills) / len(job_skills)
        
        return min(match_percentage * 40, 40)  # Scale to 40 points
    
    def _extract_skills_from_text(self, text: str) -> List[str]:
        """Extract skills from text"""
        skills = set()
        text_lower = text.lower()
        
        # Common technical skills patterns
        tech_skills = [
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'sql', 'nosql', 'mongodb', 'postgresql', 'mysql',
            'react', 'angular', 'vue', 'django', 'flask', 'spring', 'node.js',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform',
            'machine learning', 'ai', 'data science', 'big data', 'tableau'
        ]
        
        for skill in tech_skills:
            if skill in text_lower:
                skills.add(skill)
        
        return list(skills)
    
    def _calculate_keywords_score(self, text: str) -> float:
        """Calculate keywords presence score"""
        score = 0
        text_lower = text.lower()
        
        # Check for action verbs
        action_verbs = self.common_keywords["action_verbs"]
        found_verbs = [verb for verb in action_verbs if verb in text_lower]
        score += (len(found_verbs) / len(action_verbs)) * 10
        
        # Check for quantifiable achievements
        quant_patterns = [
            r'increased by \d+%',
            r'reduced by \d+%',
            r'saved \$\d+',
            r'improved by \d+%',
            r'managed \$\d+'
        ]
        
        quant_count = 0
        for pattern in quant_patterns:
            quant_count += len(re.findall(pattern, text_lower))
        
        score += min(quant_count * 2, 10)  # Max 10 points for quantifiable results
        
        return min(score, 20)
    
    def _calculate_formatting_score(self, parsed_data: Dict[str, Any]) -> float:
        """Calculate formatting score"""
        score = 15  # Start with full points
        
        text = parsed_data["raw_text"]
        
        # Check section presence
        required_sections = ['experience', 'education', 'skills']
        missing_sections = []
        
        text_lower = text.lower()
        for section in required_sections:
            if section not in text_lower:
                missing_sections.append(section)
                score -= 2
        
        # Check for consistent bullet points
        bullet_pattern = r'^[\•\-\*]\s'
        lines = text.split('\n')
        bullet_lines = [line for line in lines if re.match(bullet_pattern, line.strip())]
        bullet_ratio = len(bullet_lines) / max(len([l for l in lines if len(l.strip()) > 10]), 1)
        
        if bullet_ratio < 0.3:  # Less than 30% bullet points
            score -= 2
        
        # Check for appropriate length
        word_count = len(text.split())
        if word_count < 200:
            score -= 2  # Too short
        elif word_count > 800:
            score -= 2  # Too long
        
        return max(score, 0)
    
    def _calculate_readability_score(self, text: str) -> float:
        """Calculate readability score using simple metrics"""
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return 0
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Calculate readability score (simplified)
        if avg_sentence_length <= 15:
            readability = 15  # Excellent
        elif avg_sentence_length <= 20:
            readability = 12  # Good
        elif avg_sentence_length <= 25:
            readability = 8   # Fair
        else:
            readability = 5   # Poor
        
        return readability
    
    def _calculate_grammar_score(self, text: str) -> float:
        """Calculate basic grammar score using pattern matching"""
        score = 10  # Start with full points
        
        # Check for common errors
        common_errors = [
            (r'\bi\s', 'Lowercase "I" should be capitalized'),  # lowercase i
            (r'\btheir\s', 'Potential their/there/they\'re error'),  # context needed
        ]
        
        error_count = 0
        for pattern, _ in common_errors:
            error_count += len(re.findall(pattern, text.lower()))
        
        # Simple check for consistent tense (basic implementation)
        past_tense = len(re.findall(r'\b(managed|developed|created|led)\b', text.lower()))
        present_tense = len(re.findall(r'\b(manage|develop|create|lead)\b', text.lower()))
        
        if past_tense > 0 and present_tense > 0:
            # Mixed tenses might indicate inconsistency
            error_count += 1
        
        # Deduct points for errors
        score -= min(error_count * 0.5, 5)
        
        return max(score, 0)
    
    def _get_skills_match_details(self, skills: List[str], job_description: str) -> List[str]:
        """Get detailed feedback for skills match"""
        details = []
        
        if job_description:
            job_skills = self._extract_skills_from_text(job_description)
            matched_skills = set(skill.lower() for skill in skills) & set(job_skills)
            missing_skills = set(job_skills) - set(skill.lower() for skill in skills)
            
            details.append(f"Matched {len(matched_skills)} out of {len(job_skills)} required skills")
            if missing_skills:
                details.append(f"Missing skills: {', '.join(missing_skills)}")
        else:
            details.append(f"Found {len(skills)} skills in resume")
            if len(skills) < 10:
                details.append("Consider adding more relevant skills")
        
        return details
    
    def _get_keywords_details(self, text: str) -> List[str]:
        """Get detailed feedback for keywords"""
        details = []
        text_lower = text.lower()
        
        # Action verbs
        action_verbs = self.common_keywords["action_verbs"]
        found_verbs = [verb for verb in action_verbs if verb in text_lower]
        details.append(f"Used {len(found_verbs)} action verbs")
        
        # Quantifiable achievements
        quant_patterns = [
            r'increased by \d+%',
            r'reduced by \d+%',
            r'saved \$\d+',
            r'improved by \d+%'
        ]
        
        quant_count = 0
        for pattern in quant_patterns:
            quant_count += len(re.findall(pattern, text_lower))
        
        details.append(f"Found {quant_count} quantifiable achievements")
        
        if quant_count < 2:
            details.append("Add more quantifiable results (e.g., 'increased efficiency by 25%')")
        
        return details
    
    def _get_formatting_details(self, parsed_data: Dict[str, Any]) -> List[str]:
        """Get detailed feedback for formatting"""
        details = []
        text = parsed_data["raw_text"]
        text_lower = text.lower()
        
        # Section check
        sections = ['experience', 'education', 'skills']
        missing_sections = [section for section in sections if section not in text_lower]
        
        if missing_sections:
            details.append(f"Missing sections: {', '.join(missing_sections)}")
        else:
            details.append("All essential sections present")
        
        # Bullet points
        lines = text.split('\n')
        bullet_lines = [line for line in lines if re.match(r'^[\•\-\*]\s', line.strip())]
        bullet_ratio = len(bullet_lines) / max(len([l for l in lines if len(l.strip()) > 10]), 1)
        
        if bullet_ratio < 0.3:
            details.append("Consider using more bullet points for readability")
        else:
            details.append("Good use of bullet points")
        
        # Length
        word_count = len(text.split())
        if 300 <= word_count <= 600:
            details.append("Appropriate resume length")
        elif word_count < 300:
            details.append("Resume might be too short - add more details")
        else:
            details.append("Resume might be too long - consider condensing")
        
        return details
    
    def _get_readability_details(self, text: str) -> List[str]:
        """Get detailed feedback for readability"""
        details = []
        sentences = re.split(r'[.!?]+', text)
        words = text.split()
        
        if len(sentences) == 0:
            return ["Unable to analyze readability"]
        
        avg_sentence_length = len(words) / len(sentences)
        
        if avg_sentence_length <= 15:
            details.append("Excellent sentence length")
        elif avg_sentence_length <= 20:
            details.append("Good sentence length")
        elif avg_sentence_length <= 25:
            details.append("Consider shortening some sentences")
        else:
            details.append("Some sentences are too long - break them up")
        
        return details
    
    def _get_grammar_details(self, text: str) -> List[str]:
        """Get detailed feedback for grammar"""
        details = ["Basic grammar check passed"]
        
        # Simple checks
        if re.search(r'\bi\s', text):
            details.append("Found lowercase 'I' - should be capitalized")
        
        return details
