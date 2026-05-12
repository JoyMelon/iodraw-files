import os
import re
from typing import Dict, Tuple, Optional
import random

class FileParser:
    def __init__(self):
        pass
    
    def parse_txt(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    
    def parse_pdf_simple(self, file_path: str) -> str:
        # 简单的PDF解析模拟，真实环境中使用PyPDF2或pdfplumber
        sample_content = """
姓名：张三
教育背景：
- 上海交通大学 市场营销专业 本科 2016-2020

工作经验：
- 欧莱雅中国 销售主管 2021-至今
  负责高端客户管理和产品推广
- 耐克体育 销售代表 2020-2021
  参与零售运营和客户服务

技能：
客户关系管理、销售策略、团队协作、沟通能力、英语流利
        """
        return sample_content
    
    def parse_docx_simple(self, file_path: str) -> str:
        # 简单的Word文档解析模拟
        sample_content = """
姓名：李四
教育背景：
- 复旦大学 奢侈品管理 硕士 2018-2022
- 浙江大学 国际经济与贸易 本科 2014-2018

工作经验：
- 路易威登 精品顾问 2022-至今
  负责VIP客户维护和销售业绩达成
- 古驰 实习生 2021-2022
  参与店铺运营和客户服务

技能：
奢侈品知识、客户服务、多语言沟通、数据分析
        """
        return sample_content
    
    def parse_file(self, file_path: str, file_type: str) -> str:
        """解析不同类型的文件"""
        if file_type == 'txt':
            return self.parse_txt(file_path)
        elif file_type == 'pdf':
            return self.parse_pdf_simple(file_path)
        elif file_type == 'docx' or file_type == 'doc':
            return self.parse_docx_simple(file_path)
        else:
            # 默认返回简单解析
            try:
                return self.parse_txt(file_path)
            except:
                return "无法解析文件内容"
    
    def extract_resume_info(self, content: str) -> Dict:
        """从解析的内容中提取简历信息"""
        lines = content.split('\n')
        
        skills = []
        experience = []
        education = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in ['技能', 'skill', '能力']):
                current_section = 'skills'
                continue
            elif any(keyword in line_lower for keyword in ['工作', 'experience', '职业']):
                current_section = 'experience'
                continue
            elif any(keyword in line_lower for keyword in ['教育', 'education', '学历', '学校']):
                current_section = 'education'
                continue
            
            if current_section == 'skills':
                skills.append(line)
            elif current_section == 'experience':
                experience.append(line)
            elif current_section == 'education':
                education.append(line)
        
        name = self._extract_name(content)
        
        return {
            'name': name or '未命名简历',
            'skills': '\n'.join(skills) if skills else '未提取到技能信息',
            'experience': '\n'.join(experience) if experience else '未提取到工作经验',
            'education': '\n'.join(education) if education else '未提取到教育背景',
            'summary': content[:500] if len(content) > 500 else content,
            'parsed_content': content
        }
    
    def _extract_name(self, content: str) -> Optional[str]:
        # 简单的姓名提取逻辑
        patterns = [
            r'姓名[：:]\s*([^\n]+)',
            r'^([^\n]{2,4})\s*$',
            r'Name[：:]\s*([^\n]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                name = match.group(1).strip()
                if 2 <= len(name) <= 10:
                    return name
        return None
    
    def generate_optimization_suggestions(self, content: str) -> str:
        """生成简历优化建议"""
        suggestions = []
        
        # 检查内容长度
        if len(content) < 500:
            suggestions.append("1. 简历内容不够丰富，建议增加更多详细经历描述")
        
        # 检查关键词
        keywords = ['奢侈品', '高端', 'VIP', '品牌', '客户', '销售', '服务']
        found_keywords = [kw for kw in keywords if kw in content]
        if len(found_keywords) < 3:
            suggestions.append("2. 建议增加奢侈品行业相关关键词，提升匹配度")
        
        # 检查技能描述
        if '技能' not in content and 'skill' not in content.lower():
            suggestions.append("3. 建议添加专门的技能模块，突出核心能力")
        
        # 添加通用建议
        suggestions.extend([
            "4. 强调在高端客户服务方面的经验",
            "5. 使用量化的成果展示工作业绩",
            "6. 添加对目标奢侈品品牌的了解和热情",
            "7. 优化语言表达，使用更专业和优雅的措辞"
        ])
        
        return '\n'.join(suggestions)
    
    def translate_to_luxury_terms(self, content: str) -> str:
        """将普通词汇转换为奢侈品行业术语"""
        luxury_map = {
            '销售': '高端客户销售与关系维护',
            '负责销售': '高净值客户个人顾问',
            '客户服务': 'VIP客户专属服务',
            '库存管理': '精品库存与稀缺性管理',
            '商品管理': '精品品类管理',
            '市场推广': '品牌形象塑造与高端客群拓展',
            '市场营销': '奢侈品品牌战略推广',
            '管理': '精品店铺运营管理',
            '经理': '精品运营总监',
            '主管': '奢侈品部门负责人',
            '员工': '精品顾问',
            '团队': '精英团队',
            '客户': '高净值客户',
            '产品': '精品',
            '业绩': '卓越业绩表现',
            '目标': '追求卓越',
            '成就': '辉煌成就',
            '经验': '资深行业经验',
            '专业': '精湛专业',
            '优秀': '出类拔萃',
            '良好': '卓越'
        }
        
        translated = content
        for original, luxury in luxury_map.items():
            translated = translated.replace(original, luxury)
        
        return translated
