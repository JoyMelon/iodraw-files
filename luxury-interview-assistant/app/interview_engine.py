import random
import re
from typing import Dict, List
import time

class InterviewEngine:
    def __init__(self):
        self.vip_scenarios = [
            {
                "scenario": "VIP客户想预订一款全球限量的手袋但已售罄，当场黑脸。",
                "evaluation_criteria": "考察候选人的共情能力、措辞优雅度、高净值客户维护的专业素养"
            },
            {
                "scenario": "客户在店内误摔贵重商品后情绪崩溃。",
                "evaluation_criteria": "考察候选人的应急处理能力、情绪安抚技巧、专业服务意识"
            },
            {
                "scenario": "客户试图大幅度砍价并质疑品牌价值。",
                "evaluation_criteria": "考察候选人对品牌价值的诠释能力、谈判技巧、优雅拒绝的艺术"
            },
            {
                "scenario": "VIP客户在试穿多套高级定制服装后，表示都不满意，表现出不耐烦。",
                "evaluation_criteria": "考察候选人的耐心、审美建议能力、客户需求洞察"
            },
            {
                "scenario": "客户要求在非营业时间安排私人购物体验。",
                "evaluation_criteria": "考察候选人的协调能力、VIP服务意识、品牌标准维护"
            }
        ]
        
        self.brand_question_templates = [
            "您说喜爱{brand}，请问您了解其{aspect}吗？",
            "请谈谈您对{brand}的{aspect}的理解？",
            "作为{brand}的{aspect}体现了什么品牌精神？"
        ]
        
        self.aspects = ["设计灵感", "品牌历史", "工艺特点", "经典产品", "品牌价值观"]
    
    def generate_interview_question(self, jd: str, resume: str, 
                                     brand_knowledge: List[Dict], 
                                     random_brand: str = None) -> Dict:
        question_type = random.choice(["brand", "vip_scenario", "general"])
        
        question_data = {}
        
        if question_type == "brand" and brand_knowledge:
            brand = random_brand or self._extract_brand_from_knowledge(brand_knowledge)
            aspect = random.choice(self.aspects)
            question = random.choice(self.brand_question_templates).format(brand=brand, aspect=aspect)
            question_data = {
                "type": "brand",
                "brand": brand,
                "question": question,
                "knowledge_context": brand_knowledge
            }
        
        elif question_type == "vip_scenario":
            scenario = random.choice(self.vip_scenarios)
            question = f"请模拟以下场景，展示您会如何处理：\n\n{scenario['scenario']}\n\n请详细描述您的应对方式。"
            question_data = {
                "type": "vip_scenario",
                "scenario": scenario,
                "question": question
            }
        
        else:
            question = f"结合您的简历和这个岗位，请谈谈您为什么适合这个奢侈品行业的职位？"
            question_data = {
                "type": "general",
                "question": question
            }
        
        return question_data
    
    def analyze_answer(self, answer: str, question_data: Dict, brand_knowledge: List[Dict] = None) -> Dict:
        tone_analysis = self._analyze_tone(answer)
        brand_match = self._analyze_brand_match(answer, question_data, brand_knowledge)
        
        analysis = self._generate_ai_analysis(answer, question_data, tone_analysis, brand_match)
        
        return {
            "ai_analysis": analysis,
            "emotion_score": tone_analysis["emotion_score"],
            "brand_match_score": brand_match["score"],
            "tone_score": tone_analysis["tone_score"],
            "tone_feedback": tone_analysis["feedback"]
        }
    
    def _analyze_tone(self, text: str) -> Dict:
        word_count = len(text.split())
        exclamation_count = text.count("!")
        question_count = text.count("?")
        
        emotion_score = 7.0 + random.uniform(-1.0, 1.5)
        tone_score = 7.5 + random.uniform(-1.0, 1.5)
        
        feedback = ""
        if "请" in text or "您好" in text or "感谢" in text:
            tone_score += 1.0
        
        if word_count > 50 and "请" in text:
            feedback = "您的语气非常优雅专业，继续保持。"
        elif word_count < 20:
            feedback = "建议回答可以更加详细一些，展现您的专业素养。"
        else:
            feedback = "语气良好，建议适当放慢语速，保持专业微笑语调。"
        
        emotion_score = min(emotion_score, 10.0)
        tone_score = min(tone_score, 10.0)
        
        return {
            "emotion_score": round(emotion_score, 1),
            "tone_score": round(tone_score, 1),
            "feedback": feedback
        }
    
    def _analyze_brand_match(self, answer: str, question_data: Dict, brand_knowledge: List[Dict]) -> Dict:
        score = 6.0 + random.uniform(0.5, 2.5)
        
        keywords = ["品牌", "工艺", "经典", "优雅", "专业", "客户", "服务", "品质"]
        match_count = sum(1 for kw in keywords if kw in answer)
        
        if match_count >= 3:
            score += 1.5
        elif match_count >= 1:
            score += 0.5
        
        score = min(score, 10.0)
        
        return {
            "score": round(score, 1),
            "match_level": "优秀" if score >= 8 else "良好" if score >= 6 else "需要提升"
        }
    
    def _generate_ai_analysis(self, answer: str, question_data: Dict, 
                             tone_analysis: Dict, brand_match: Dict) -> str:
        analysis_parts = []
        
        analysis_parts.append("您的回答展现了一定的专业素养。")
        
        if brand_match["score"] >= 7:
            analysis_parts.append("对品牌的理解很到位。")
        else:
            analysis_parts.append("建议加深对品牌文化和价值的理解。")
        
        if tone_analysis["tone_score"] >= 7:
            analysis_parts.append("语气优雅得体，符合奢侈品行业的服务标准。")
        else:
            analysis_parts.append("注意保持专业优雅的语气表达。")
        
        analysis_parts.append("继续努力，您有潜力成为一名优秀的奢侈品行业从业者！")
        
        return "\n".join(analysis_parts)
    
    def _extract_brand_from_knowledge(self, brand_knowledge: List[Dict]) -> str:
        if brand_knowledge:
            brands = list(set([k["brand"] for k in brand_knowledge]))
            return random.choice(brands)
        return "Louis Vuitton"
