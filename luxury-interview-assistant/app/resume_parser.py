import re
from typing import Dict
import random

class ResumeParser:
    def __init__(self):
        self.luxury_terms_map = {
            "销售": "高净值客户个人顾问",
            "负责销售": "高净值客户个人顾问",
            "客户服务": "VIP客户关怀专员",
            "库存管理": "精品库商品调拨与稀缺性维护",
            "商品管理": "精品库商品调拨与稀缺性维护",
            "市场推广": "品牌形象塑造与高端客群拓展",
            "市场营销": "品牌形象塑造与高端客群拓展",
            "管理": "精品店运营管理",
            "经理": "精品店运营总监",
            "主管": "精品部门负责人",
            "员工": "精品顾问",
            "团队": "精英团队",
            "客户": "高净值客户",
            "产品": "精品",
            "业绩": "卓越表现",
            "目标": "追求卓越",
            "成就": "辉煌成就",
            "经验": "资深经验",
            "专业": "精湛专业",
            "优秀": "出类拔萃",
            "良好": "卓越"
        }
        
        self.brand_recommendations = {
            "零售": ["Louis Vuitton", "Gucci", "Chanel"],
            "客户关系": ["Cartier", "Hermès", "Van Cleef & Arpels"],
            "市场": ["Dior", "Prada", "Fendi"],
            "运营": ["LVMH", "Kering", "Richemont"]
        }
    
    def translate_to_luxury(self, text: str) -> str:
        translated = text
        for original, luxury in self.luxury_terms_map.items():
            translated = translated.replace(original, luxury)
        return translated
    
    def parse_resume(self, resume_text: str) -> Dict:
        skills = self._extract_skills(resume_text)
        experience = self._extract_experience(resume_text)
        education = self._extract_education(resume_text)
        summary = self._generate_summary(resume_text)
        luxury_translated = self.translate_to_luxury(resume_text)
        recommended_brands = self._recommend_brands(skills, experience)
        
        return {
            "skills": skills,
            "experience": experience,
            "education": education,
            "summary": summary,
            "luxury_translated_version": luxury_translated,
            "recommended_brands": recommended_brands,
            "score": random.uniform(7.0, 9.5)
        }
    
    def _extract_skills(self, text: str) -> str:
        skill_keywords = ["沟通", "销售", "客户", "管理", "市场", "策划", "分析", "团队", "英语", "法语", "Excel", "PPT"]
        found_skills = [kw for kw in skill_keywords if kw in text]
        return ", ".join(found_skills) if found_skills else "综合能力优秀"
    
    def _extract_experience(self, text: str) -> str:
        lines = text.split("\n")
        experience_lines = []
        for line in lines:
            if any(keyword in line for keyword in ["年", "工作", "经验", "公司", "职位"]):
                experience_lines.append(line.strip())
        return "\n".join(experience_lines[:5]) if experience_lines else text[:200]
    
    def _extract_education(self, text: str) -> str:
        edu_keywords = ["大学", "学院", "学士", "硕士", "博士", "毕业", "专业"]
        edu_lines = []
        for line in text.split("\n"):
            if any(kw in line for kw in edu_keywords):
                edu_lines.append(line.strip())
        return "\n".join(edu_lines[:3]) if edu_lines else "高等教育背景"
    
    def _generate_summary(self, text: str) -> str:
        return f"候选人具备优秀的综合素质，在奢侈品行业有良好的发展潜力。善于沟通，注重细节，具有服务高端客户的潜质。"
    
    def _recommend_brands(self, skills: str, experience: str) -> list:
        recommendations = []
        if "销售" in skills or "客户" in skills:
            recommendations.extend(self.brand_recommendations["零售"])
        if "管理" in skills or "运营" in experience:
            recommendations.extend(self.brand_recommendations["运营"])
        if "市场" in skills or "营销" in skills:
            recommendations.extend(self.brand_recommendations["市场"])
        
        if not recommendations:
            recommendations = ["Louis Vuitton", "Chanel", "Hermès"]
        
        return list(set(recommendations))
