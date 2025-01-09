from azure.cosmos import CosmosClient
import uuid
import time
import random

# Cosmos DB 연결 설정
endpoint = "YOUR_COSMOS_DB_ENDPOINT"
key = "YOUR_COSMOS_DB_KEY"
database_name = "YOUR_DATABASE_NAME"
container_name = "YOUR_CONTAINER_NAME"

# 카테고리 샘플 데이터
categories = [
    {"id": str(uuid.uuid4()), "name": "Components, Pedals"},
    {"id": str(uuid.uuid4()), "name": "Components, Wheels"},
    {"id": str(uuid.uuid4()), "name": "Accessories, Lights"},
    {"id": str(uuid.uuid4()), "name": "Clothing, Jerseys"},
    {"id": str(uuid.uuid4()), "name": "Components, Brakes"}
]

# 제품명 접두사 샘플
product_prefixes = ["Pro", "Elite", "Sport", "ML", "Ultra", "Premium"]
product_types = ["Road", "Mountain", "Racing", "Urban", "Touring"]
product_suffixes = ["Pedal", "Wheel", "Light", "Jersey", "Brake"]

def generate_sku():
    """SKU 생성 함수"""
    prefix = random.choice(["PD", "WH", "LT", "JS", "BR"])
    number = random.randint(100, 999)
    return f"{prefix}-R{number}"

def generate_product():
    """단일 제품 데이터 생성 함수"""
    category = random.choice(categories)
    product_name = f"{random.choice(product_prefixes)} {random.choice(product_types)} {random.choice(product_suffixes)}"
    
    return {
        "id": str(uuid.uuid4()),
        "categoryId": category["id"],
        "categoryName": category["name"],
        "sku": generate_sku(),
        "name": product_name,
        "price": round(random.uniform(20.0, 500.0), 2)
    }

try:
    # Cosmos DB 클라이언트 초기화
    client = CosmosClient(endpoint, key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    
    # 50개의 제품 데이터 생성 및 삽입
    for i in range(50):
        product = generate_product()
        container.create_item(body=product)
        print(f"제품 {i+1}/50 삽입 완료: {product['name']}")
        time.sleep(0.5)  # 0.5초 대기
        
    print("모든 샘플 데이터 삽입이 완료되었습니다.")

except Exception as e:
    print(f"오류 발생: {str(e)}")
