import re
from typing import Dict, List, Any
from .optimizer import ResumeOptimizer

class LinkedInGenerator:
    def __init__(self):
        self.optimizer = ResumeOptimizer()
    
    def generate_suggestions(self, parsed_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate LinkedIn optimization suggestions"""
        return {
            "headline": self._generate_headline(parsed_data),
            "summary": self._generate_linkedin_summary(parsed_data),
            "skills": self._suggest_linkedin_skills(parsed_data["skills"]),
            "keywords": self._suggest_linkedin_keywords(parsed_data),
            "about_section": self._generate_about_section(parsed_data)
        }
    
    def _generate_headline(self, parsed_data: Dict[str, Any]) -> List[str]:
        """Generate LinkedIn headline suggestions"""
        headlines = []
        
        name = parsed_data["personal_info"].get("name", "").split()[0] if parsed_data["personal_info"].get("name") else "Professional"
        top_skills = parsed_data["skills"][:3]
        
        # Template-based headline generation
        templates = [
            f"{parsed_data.get('current_title', 'Professional')} | {', '.join(top_skills)}",
            f"Experienced {parsed_data.get('current_title', 'Professional')} | {', '.join(top_skills[:2])}",
            f"Passionate {parsed_data.get('current_title', 'Professional')} | Open to New Opportunities",
            f"{name} | {parsed_data.get('current_title', 'Professional')} | {top_skills[0] if top_skills else 'Technology'}",
        ]
        
        # Add custom headlines based on experience
        if parsed_data["experience"]:
            latest_job = parsed_data["experience"][0]
            job_title = latest_job.get("title", "")
            headlines.append(f"{job_title} | {', '.join(top_skills)}")
        
        headlines.extend(templates)
        return headlines[:5]  # Return top 5 headlines
    
    def _generate_linkedin_summary(self, parsed_data: Dict[str, Any]) -> str:
        """Generate LinkedIn summary section"""
        summary_parts = []
        
        # Professional introduction
        if parsed_data["personal_info"].get("name"):
            summary_parts.append(f"Results-driven {parsed_data.get('current_title', 'professional')} with expertise in:")
        else:
            summary_parts.append("Results-driven professional with expertise in:")
        
        # Key skills
        top_skills = parsed_data["skills"][:5]
        if top_skills:
            skills_text = ", ".join(top_skills)
            summary_parts.append(f"• {skills_text}")
        
        # Experience highlights
        if parsed_data["experience"]:
            summary_parts.append("\nProfessional Experience:")
            for job in parsed_data["experience"][:2]:  # Latest 2 jobs
                job_title = job.get("title", "")
                if job_title:
                    summary_parts.append(f"• {job_title}")
        
        # Call to action
        summary_parts.append("\nOpen to new opportunities and collaborations.")
        
        return "\n".join(summary_parts)
    
    def _suggest_linkedin_skills(self, skills: List[str]) -> List[str]:
        """Suggest skills for LinkedIn profile"""
        # LinkedIn allows up to 50 skills, suggest most relevant ones
        linkedin_skills = skills.copy()
        
        # Add commonly searched skills if missing
        common_linkedin_skills = [
            "Problem Solving", "Communication", "Leadership", 
            "Project Management", "Teamwork", "Adaptability"
        ]
        
        for common_skill in common_linkedin_skills:
            if common_skill.lower() not in [s.lower() for s in linkedin_skills]:
                linkedin_skills.append(common_skill)
        
        return linkedin_skills[:15]  # Suggest top 15 most relevant skills
    
    def _suggest_linkedin_keywords(self, parsed_data: Dict[str, Any]) -> List[str]:
        """Suggest keywords for LinkedIn profile optimization"""
        keywords = set()
        
        # Add skills as keywords
        for skill in parsed_data["skills"]:
            keywords.add(skill.lower())
        
        # Add job titles and roles
        for job in parsed_data["experience"]:
            title = job.get("title", "")
            if title:
                # Extract key terms from job title
                terms = re.findall(r'[A-Za-z]+', title)
                keywords.update(term.lower() for term in terms if len(term) > 3)
        
        # Add industry terms
        industry_terms = [
            "technology", "software", "development", "engineering",
            "management", "analysis", "strategy", "optimization",
            "innovation", "solutions", "consulting", "leadership"
        ]
        
        keywords.update(industry_terms)
        
        return sorted(list(keywords))[:20]
    
    def _generate_about_section(self, parsed_data: Dict[str, Any]) -> str:
        """Generate detailed About section for LinkedIn"""
        about_parts = []
        
        # Professional summary
        about_parts.append("## Professional Summary")
        about_parts.append(self._generate_professional_summary(parsed_data))
        
        # Core competencies
        about_parts.append("\n## Core Competencies")
        about_parts.append(self._generate_competencies_section(parsed_data["skills"]))
        
        # Career highlights
        about_parts.append("\n## Career Highlights")
        about_parts.append(self._generate_career_highlights(parsed_data["experience"]))
        
        return "\n".join(about_parts)
    
    def _generate_professional_summary(self, parsed_data: Dict[str, Any]) -> str:
        """Generate professional summary for About section"""
        experience_years = self._estimate_experience_years(parsed_data["experience"])
        
        summary = f"Seasoned professional with {experience_years}+ years of experience "
        summary += f"specializing in {', '.join(parsed_data['skills'][:3])}. "
        summary += "Proven track record of delivering innovative solutions and driving business growth through technology and strategic leadership."
        
        return summary
    
    def _estimate_experience_years(self, experience: List[Dict]) -> int:
        """Estimate total years of experience"""
        if not experience:
            return 3  # Default assumption
        
        # Simple estimation based on number of positions
        # In a real implementation, you would parse dates
        base_years = max(2, len(experience) * 2)
        return min(base_years, 30)  # Cap at 30 years
    
    def _generate_competencies_section(self, skills: List[str]) -> str:
        """Generate competencies section"""
        if not skills:
            return "• Strategic Planning • Problem Solving • Team Leadership"
        
        # Group skills into categories for better presentation
        technical_skills = [s for s in skills if self._is_technical_skill(s)]
        soft_skills = [s for s in skills if not self._is_technical_skill(s)]
        
        competencies = []
        
        if technical_skills:
            competencies.append("Technical: " + ", ".join(technical_skills[:5]))
        
        if soft_skills:
            competencies.append("Professional: " + ", ".join(soft_skills[:3]))
        
        return "• " + "\n• ".join(competencies)
    
    def _is_technical_skill(self, skill: str) -> bool:
        """Check if a skill is technical"""
        technical_indicators = [
            'python', 'java', 'javascript', 'sql', 'aws', 'docker', 'kubernetes',
            'react', 'angular', 'machine learning', 'ai', 'data', 'cloud',
            'devops', 'backend', 'frontend', 'fullstack', 'database'
        ]
        
        skill_lower = skill.lower()
        return any(indicator in skill_lower for indicator in technical_indicators)
    
    def _generate_career_highlights(self, experience: List[Dict]) -> str:
        """Generate career highlights section"""
        if not experience:
            return "• Successfully led multiple projects from conception to completion\n• Consistently exceeded performance targets\n• Recognized for innovative problem-solving abilities"
        
        highlights = []
        
        for job in experience[:3]:  # Latest 3 positions
            title = job.get("title", "Professional")
            highlights.append(f"• {title}: Delivered significant results through strategic initiatives and effective execution")
        
        return "\n".join(highlights)