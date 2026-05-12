import chromadb
from chromadb.utils import embedding_functions
from typing import List, Dict
import os

class LuxuryKnowledgeRAG:
    def __init__(self, persist_directory: str = "./data/chroma_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.collection = self.client.get_or_create_collection(
            name="luxury_brands",
            embedding_function=self.embedding_function
        )
        
    def add_brand(self, brand_id: int, name: str, description: str, 
                  founding_story: str, signature_product: str, beliefs: str):
        documents = []
        metadatas = []
        ids = []
        
        if description:
            documents.append(description)
            metadatas.append({"brand": name, "type": "description", "brand_id": brand_id})
            ids.append(f"{brand_id}_desc")
        
        if founding_story:
            documents.append(founding_story)
            metadatas.append({"brand": name, "type": "founding_story", "brand_id": brand_id})
            ids.append(f"{brand_id}_story")
        
        if signature_product:
            documents.append(signature_product)
            metadatas.append({"brand": name, "type": "signature_product", "brand_id": brand_id})
            ids.append(f"{brand_id}_product")
        
        if beliefs:
            documents.append(beliefs)
            metadatas.append({"brand": name, "type": "beliefs", "brand_id": brand_id})
            ids.append(f"{brand_id}_beliefs")
        
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
    
    def query_brand_knowledge(self, query: str, brand_name: str = None, n_results: int = 3) -> List[Dict]:
        where_clause = {}
        if brand_name:
            where_clause = {"brand": brand_name}
        
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_clause if where_clause else None
        )
        
        knowledge = []
        if results['documents'] and results['metadatas']:
            for doc, meta in zip(results['documents'][0], results['metadatas'][0]):
                knowledge.append({
                    "content": doc,
                    "brand": meta['brand'],
                    "type": meta['type']
                })
        
        return knowledge
    
    def get_all_brand_names(self) -> List[str]:
        results = self.collection.get()
        if results['metadatas']:
            brands = list(set([meta['brand'] for meta in results['metadatas']]))
            return brands
        return []
    
    def initialize_sample_data(self):
        sample_brands = [
            {
                "id": 1,
                "name": "Louis Vuitton",
                "description": "Louis Vuitton是法国奢侈品品牌，由路易·威登于1854年创立，以其卓越品质和精湛工艺闻名于世。",
                "founding_story": "1854年，Louis Vuitton在巴黎Rue Neuve des Capucines开设了第一家店铺，革命性地推出了平顶行李箱设计，彻底改变了旅行方式。",
                "signature_product": "Monogram帆布系列、Neverfull手袋、Keepall旅行袋、Speedy手袋",
                "beliefs": "旅行的艺术、精湛工艺、传承与创新、追求卓越品质"
            },
            {
                "id": 2,
                "name": "Chanel",
                "description": "香奈儿是法国奢侈品品牌，由可可·香奈儿于1910年创立，以简约优雅的设计理念著称。",
                "founding_story": "1910年，Coco Chanel在巴黎开设了第一家女帽店，随后推出经典的小黑裙和N°5香水，彻底革新了女性时尚。",
                "signature_product": "2.55手袋、Classic Flap手袋、N°5香水、小黑裙、粗花呢外套",
                "beliefs": "简约即美、自由与独立、永恒优雅、打破传统"
            },
            {
                "id": 3,
                "name": "Hermès",
                "description": "爱马仕是法国奢侈品品牌，创立于1837年，以精湛的手工技艺和顶级材质闻名。",
                "founding_story": "Thierry Hermès于1837年在巴黎创立了马具工坊，为欧洲皇室贵族制造高级马具，后逐步转型为奢侈品品牌。",
                "signature_product": "Birkin手袋、Kelly手袋、丝巾、皮具、香水",
                "beliefs": "手工艺术、卓越品质、时间的价值、传承与匠心"
            },
            {
                "id": 4,
                "name": "Cartier",
                "description": "卡地亚是法国珠宝和腕表品牌，创立于1847年，被誉为'皇帝的珠宝商，珠宝商的皇帝'。",
                "founding_story": "Louis-François Cartier于1847年在巴黎创立品牌，其作品深受欧洲皇室喜爱，曾为多位国王和王后定制珠宝。",
                "signature_product": "Love手镯、Trinity戒指、Santos腕表、Ballon Bleu腕表、猎豹系列",
                "beliefs": "艺术与工艺、创新精神、优雅永恒、皇室荣耀"
            },
            {
                "id": 5,
                "name": "Gucci",
                "description": "古驰是意大利奢侈品品牌，创立于1921年，以双G标志和独特设计风格闻名。",
                "founding_story": "Guccio Gucci在佛罗伦萨创立品牌，最初制造高端行李箱和皮具，后发展成为全球顶级奢侈品集团。",
                "signature_product": "Dionysus手袋、Jackie 1961手袋、双G配饰、Ace运动鞋",
                "beliefs": "意大利传统、创新设计、自由表达、现代奢华"
            }
        ]
        
        for brand in sample_brands:
            self.add_brand(
                brand_id=brand["id"],
                name=brand["name"],
                description=brand["description"],
                founding_story=brand["founding_story"],
                signature_product=brand["signature_product"],
                beliefs=brand["beliefs"]
            )
