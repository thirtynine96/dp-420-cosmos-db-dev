# 패키지 설치: 
# pip install azure-cosmos
# 실행방법: 
# python cosmos_query_pagination.py

from azure.cosmos import CosmosClient
from azure.core.exceptions import AzureError

# Cosmos DB 연결 정보
COSMOS_URL = "https://<your-account-name>.documents.azure.com:443/"
COSMOS_KEY = "<your-primary-key>"
DATABASE_NAME = "your-database-name"
CONTAINER_NAME = "your-container-name"

def main():
    try:
        # CosmosClient 초기화
        client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)

        # 데이터베이스와 컨테이너 참조
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # SQL 쿼리 정의
        sql_query = "SELECT * FROM products WHERE p.price > @lower"

        # 쿼리 매개변수와 옵션 설정
        parameters = [
            {"name": "@lower", "value": 500}  # 쿼리 필터 값
        ]
        query_options = {
            "max_item_count": 100  # 한 페이지에서 반환할 최대 항목 수
        }

        # FeedIterator 생성
        iterator = container.query_items(
            query=sql_query,
            parameters=parameters,
            enable_cross_partition_query=True,
            max_item_count=query_options["max_item_count"]
        )

        # 페이지별로 결과 처리
        print("Query results:")
        for page in iterator.by_page():
            items = list(page)
            for item in items:
                print(f"Product Name: {item['name']}, Price: {item['price']}")

    except AzureError as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
