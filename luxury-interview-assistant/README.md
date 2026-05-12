# 💎 奢侈品行业AI面试助手

一个专为奢侈品行业设计的AI面试系统，帮助求职者准备LV、Chanel、Hermès等顶级品牌的面试。

## 🌟 核心功能

### 1. 品牌知识库与一致性评估 (RAG)
- 构建了奢侈品牌专属向量数据库
- 包含Louis Vuitton、Chanel、Hermès、Cartier、Gucci等品牌的详细信息
- 面试时根据上下文提出深度品牌认知问题
- 评估候选人对品牌DNA的理解

### 2. VIP高净值客群场景模拟
- 内置高端客户棘手场景Prompt模板
- 评估共情能力、措辞优雅度、专业素养
- 场景包括：限量品缺货、商品损坏、客户砍价等

### 3. 双语与语调测评
- 语音输入支持（开发中）
- 简单的语调分析（语速、情绪、措辞）
- 提供优雅表达建议

### 4. 简历"奢侈品化"改写
- 自动提取关键词并转换为奢侈品行业术语
- "负责销售" → "高净值客户个人顾问"
- "库存管理" → "精品库商品调拨与稀缺性维护"
- 根据简历推荐合适的品牌和职位

## 📁 项目结构

```
luxury-interview-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI主应用
│   ├── models.py            # SQLAlchemy数据模型
│   ├── schemas.py           # Pydantic模式
│   ├── resume_parser.py     # 简历解析模块
│   ├── interview_engine.py  # 面试引擎
│   └── luxury_knowledge_rag.py  # RAG知识库
├── frontend/
│   └── streamlit_app.py     # Streamlit前端
├── data/                    # 数据存储目录
├── luxury_knowledge_base/   # 品牌知识库
├── requirements.txt         # 依赖包
└── README.md
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- pip

### 安装依赖
```bash
cd luxury-interview-assistant
pip install -r requirements.txt
```

### 启动后端服务
```bash
cd luxury-interview-assistant
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端API文档将在 http://localhost:8000/docs 访问

### 启动前端界面
打开新的终端窗口：
```bash
cd luxury-interview-assistant/frontend
streamlit run streamlit_app.py
```

前端将在浏览器自动打开 http://localhost:8501

## 💡 使用流程

1. **上传简历**：输入或粘贴您的简历内容
2. **解析与改写**：系统自动解析并生成奢侈品化简历版本
3. **选择岗位**：选择目标品牌和职位
4. **开始面试**：AI会根据品牌知识和简历提出专业问题
5. **回答问题**：输入您的回答，AI会实时分析并给出反馈
6. **查看评估**：查看品牌匹配度、语气优雅度等评分

## 📊 数据模型

系统包含以下核心模型：
- **User** - 用户信息
- **LuxuryBrand** - 奢侈品牌信息
- **JobDescription** - 职位描述
- **Resume** - 简历信息（含奢侈品化版本）
- **Interview** - 面试记录
- **Round** - 面试轮次（问题、回答、分析）

## 🛠️ 技术栈

- **后端框架**：FastAPI (异步优先)
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **ORM**：SQLAlchemy + Alembic
- **前端**：Streamlit
- **向量数据库**：ChromaDB
- **嵌入式模型**：Sentence-Transformers

## 📝 核心Prompt模板

面试问题生成Prompt（结合品牌知识、简历、VIP场景）：

```
结合以下信息生成一个专业的奢侈品行业面试问题：

1. 岗位要求：{{job_requirement}}
2. 候选人简历：{{resume_summary}}
3. 品牌知识库：{{brand_knowledge}}
4. VIP场景：{{vip_scenario}}

问题应该：
- 深度考察品牌认知
- 模拟真实工作场景
- 评估表达优雅度
- 专业但不过于刁难
```

## 🎯 未来规划

- [ ] 集成OpenCV面部表情识别
- [ ] 实现真实的语音输入与分析
- [ ] 添加更多奢侈品牌到知识库
- [ ] 支持法语/英语双语面试
- [ ] 生成个性化面试报告

---

✨ 祝您在奢侈品行业的求职之路一帆风顺！
