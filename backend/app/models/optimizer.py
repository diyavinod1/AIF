import re
from typing import Dict, List, Any
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ResumeOptimizer:
    def __init__(self):
        try:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            # Fallback to simpler model or download
            self.model = None
        
        self.action_verbs = [
            "accelerated", "achieved", "administered", "advanced", "advised", "allocated",
            "analyzed", "assembled", "assessed", "assisted", "attained", "authored",
            "balanced", "boosted", "built", "calculated", "catalyzed", "chaired",
            "changed", "coached", "collaborated", "compiled", "completed", "conceived",
            "conducted", "consolidated", "constructed", "consulted", "controlled",
            "coordinated", "created", "decreased", "delivered", "designed", "developed",
            "devised", "directed", "drove", "edited", "eliminated", "engineered",
            "enhanced", "established", "evaluated", "executed", "expanded", "facilitated",
            "forecasted", "formed", "founded", "generated", "guided", "headed",
            "implemented", "improved", "increased", "influenced", "initiated", "innovated",
            "installed", "instituted", "integrated", "introduced", "invented", "launched",
            "led", "managed", "marketed", "mastered", "mediated", "mentored",
            "modernized", "monitored", "motivated", "negotiated", "operated", "optimized",
            "orchestrated", "organized", "originated", "overhauled", "oversaw", "performed",
            "pioneered", "planned", "prepared", "presented", "processed", "produced",
            "programmed", "projected", "promoted", "proposed", "provided", "published",
            "purchased", "recommended", "recruited", "reduced", "regulated", "reorganized",
            "researched", "restructured", "revamped", "reviewed", "revised", "saved",
            "scheduled", "secured", "selected", "simplified", "sold", "solved",
            "spearheaded", "started", "streamlined", "strengthened", "structured", "supervised",
            "supported", "surpassed", "targeted", "trained", "transformed", "translated",
            "trimmed", "unified", "upgraded", "utilized", "validated", "verified",
            "won", "wrote"
        ]
    
    def get_suggestions(self, parsed_data: Dict[str, Any], job_description: str = "") -> Dict[str, Any]:
        """Get optimization suggestions for resume"""
        suggestions = {
            "skills": self._suggest_skills(parsed_data["skills"], job_description),
            "experience": self._suggest_experience_improvements(parsed_data["experience"]),
            "summary": self._suggest_summary_improvements(parsed_data["summary"], job_description),
            "keywords": self._suggest_keywords(parsed_data["raw_text"], job_description),
            "bullet_points": self._suggest_bullet_point_improvements(parsed_data["experience"])
        }
        
        return suggestions
    
    def optimize_resume(self, parsed_data: Dict[str, Any], job_description: str, region: str = "US") -> Dict[str, Any]:
        """Generate optimized resume content"""
        optimized = parsed_data.copy()
        
        # Optimize summary
        optimized["summary"] = self._optimize_summary(parsed_data["summary"], job_description)
        
        # Optimize experience bullet points
        optimized["experience"] = self._optimize_experience(parsed_data["experience"])
        
        # Add missing skills from job description
        optimized["skills"] = self._enhance_skills(parsed_data["skills"], job_description)
        
        # Apply regional formatting
        optimized = self._apply_regional_formatting(optimized, region)
        
        return optimized
    
    def _suggest_skills(self, current_skills: List[str], job_description: str) -> List[str]:
        """Suggest skills to add based on job description"""
        if not job_description:
            return []
        
        # Extract skills from job description
        job_skills = self._extract_skills_from_jd(job_description)
        missing_skills = [skill for skill in job_skills if skill.lower() not in [s.lower() for s in current_skills]]
        
        return missing_skills[:5]  # Return top 5 missing skills
    
    def _extract_skills_from_jd(self, job_description: str) -> List[str]:
        """Extract skills from job description"""
        skills = set()
        jd_lower = job_description.lower()
        
        common_skills = [
            'python', 'java', 'javascript', 'typescript', 'sql', 'nosql',
            'react', 'angular', 'vue', 'django', 'flask', 'spring',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes',
            'machine learning', 'ai', 'data analysis', 'tableau',
            'agile', 'scrum', 'devops', 'ci/cd'
        ]
        
        for skill in common_skills:
            if skill in jd_lower:
                skills.add(skill.title())
        
        return list(skills)
    
    def _suggest_experience_improvements(self, experience: List[Dict]) -> List[Dict]:
        """Suggest improvements for experience section"""
        suggestions = []
        
        for job in experience:
            job_suggestions = {
                "title": job["title"],
                "suggestions": []
            }
            
            # Check for weak bullet points
            for bullet in job.get("description", []):
                weak_patterns = [
                    (r'responsible for', "Use action verbs instead of 'responsible for'"),
                    (r'duties included', "Start with action verbs"),
                    (r'helped with', "Be more specific about your contribution"),
                    (r'worked on', "Specify what you achieved")
                ]
                
                for pattern, suggestion in weak_patterns:
                    if re.search(pattern, bullet.lower()):
                        job_suggestions["suggestions"].append({
                            "original": bullet,
                            "suggestion": suggestion,
                            "improved": self._improve_bullet_point(bullet)
                        })
                        break
            
            if job_suggestions["suggestions"]:
                suggestions.append(job_suggestions)
        
        return suggestions
    
    def _suggest_summary_improvements(self, summary: str, job_description: str) -> List[str]:
        """Suggest improvements for summary section"""
        suggestions = []
        
        if not summary or len(summary.strip()) < 50:
            suggestions.append("Summary is too short. Add 2-3 sentences highlighting key achievements.")
        
        # Check for keywords
        if job_description:
            jd_keywords = self._extract_keywords(job_description)
            summary_keywords = self._extract_keywords(summary)
            missing_keywords = [kw for kw in jd_keywords if kw not in summary_keywords]
            
            if missing_keywords:
                suggestions.append(f"Consider adding these keywords: {', '.join(missing_keywords[:3])}")
        
        # Check for action-oriented language
        action_verb_count = sum(1 for verb in self.action_verbs if verb in summary.lower())
        if action_verb_count < 1:
            suggestions.append("Start with a strong action verb to make your summary more impactful")
        
        return suggestions
    
    def _suggest_keywords(self, resume_text: str, job_description: str) -> List[str]:
        """Suggest keywords to add"""
        if not job_description:
            return []
        
        jd_keywords = self._extract_keywords(job_description)
        resume_keywords = self._extract_keywords(resume_text)
        missing_keywords = [kw for kw in jd_keywords if kw not in resume_keywords]
        
        return missing_keywords[:10]
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        
        # Filter common words and get unique keywords
        common_words = {'with', 'this', 'that', 'have', 'from', 'they', 'were', 'their'}
        keywords = [word for word in words if word not in common_words]
        
        return list(set(keywords))
    
    def _suggest_bullet_point_improvements(self, experience: List[Dict]) -> List[Dict]:
        """Suggest specific bullet point improvements"""
        improvements = []
        
        for job in experience:
            for bullet in job.get("description", []):
                improved = self._improve_bullet_point(bullet)
                if improved != bullet:
                    improvements.append({
                        "original": bullet,
                        "improved": improved,
                        "reason": "Made more action-oriented and results-focused"
                    })
        
        return improvements[:5]  # Limit to top 5 improvements
    
    def _improve_bullet_point(self, bullet: str) -> str:
        """Improve a single bullet point"""
        original = bullet.lower().strip()
        
        # Remove weak phrases
        improvements = [
            (r'responsible for', ''),
            (r'duties included', ''),
            (r'helped with', ''),
            (r'worked on', ''),
            (r'was involved in', '')
        ]
        
        improved = original
        for pattern, replacement in improvements:
            improved = re.sub(pattern, replacement, improved)
        
        # Add action verb if missing
        if not any(verb in improved for verb in self.action_verbs):
            # Find a suitable action verb based on context
            context_verbs = {
                r'manage|lead|supervis': 'Managed',
                r'develop|create|build': 'Developed',
                r'analyze|research|evaluat': 'Analyzed',
                r'improv|optimiz|enhanc': 'Improved',
                r'implement|integrat|deploy': 'Implemented'
            }
            
            for pattern, verb in context_verbs.items():
                if re.search(pattern, improved):
                    improved = f"{verb} {improved}"
                    break
            else:
                # Default action verb
                improved = f"Managed {improved}"
        
        # Capitalize first letter
        improved = improved.capitalize()
        
        # Add quantifiable results if missing
        if not re.search(r'\d+%|\$\d+|\d+\s*(years|months)|increased|decreased|reduced', improved):
            # Suggest adding metrics
            improved += " - consider adding quantifiable results"
        
        return improved
    
    def _optimize_summary(self, summary: str, job_description: str) -> str:
        """Optimize the summary section"""
        if not summary:
            # Generate a basic summary
            return "Experienced professional seeking new opportunities to leverage skills and experience."
        
        # Ensure summary starts with a strong action verb
        first_word = summary.split()[0].lower() if summary.split() else ""
        if first_word not in [verb.lower() for verb in self.action_verbs]:
            # Prepend a strong action verb
            summary = "Accomplished " + summary.lower()
        
        # Ensure proper capitalization
        summary = summary[0].upper() + summary[1:] if summary else summary
        
        return summary
    
    def _optimize_experience(self, experience: List[Dict]) -> List[Dict]:
        """Optimize experience section"""
        optimized_experience = []
        
        for job in experience:
            optimized_job = job.copy()
            optimized_bullets = []
            
            for bullet in job.get("description", []):
                optimized_bullet = self._improve_bullet_point(bullet)
                # Remove the "consider adding" part for final version
                if "consider adding" in optimized_bullet:
                    optimized_bullet = optimized_bullet.replace(" - consider adding quantifiable results", "")
                optimized_bullets.append(optimized_bullet)
            
            optimized_job["description"] = optimized_bullets
            optimized_experience.append(optimized_job)
        
        return optimized_experience
    
    def _enhance_skills(self, current_skills: List[str], job_description: str) -> List[str]:
        """Enhance skills list based on job description"""
        enhanced_skills = current_skills.copy()
        
        if job_description:
            missing_skills = self._suggest_skills(current_skills, job_description)
            enhanced_skills.extend(missing_skills)
        
        # Remove duplicates while preserving case
        seen = set()
        unique_skills = []
        for skill in enhanced_skills:
            skill_lower = skill.lower()
            if skill_lower not in seen:
                seen.add(skill_lower)
                unique_skills.append(skill)
        
        return unique_skills
    
    def _apply_regional_formatting(self, resume_data: Dict[str, Any], region: str) -> Dict[str, Any]:
        """Apply regional formatting preferences"""
        # This is a simplified implementation
        # In a real application, you would handle date formats, spelling differences, etc.
        
        regional_changes = {
            "US": {"spelling": "color", "date_format": "MM/DD/YYYY"},
            "UK": {"spelling": "colour", "date_format": "DD/MM/YYYY"},
            "India": {"spelling": "colour", "date_format": "DD/MM/YYYY"}
        }
        
        region_info = regional_changes.get(region, regional_changes["US"])
        
        # Add regional info to resume data
        resume_data["regional_format"] = region_info
        
        return resume_data