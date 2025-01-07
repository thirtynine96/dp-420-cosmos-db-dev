**Azure Cosmos DB SDK의 Python 버전을 사용하여 페이지네이션 쿼리를 구현**

**Python으로 페이지네이션 구현하기**

1. Cosmos 클라이언트 설정

Cosmos DB의 Python SDK를 사용하려면 azure-cosmos 패키지가 필요합니다. 먼저 클라이언트를 설정합니다.
```
from azure.cosmos import CosmosClient, PartitionKey

# Cosmos DB 클라이언트 초기화
url = "https://<your-account-name>.documents.azure.com:443/"
key = "<your-primary-key>"
client = CosmosClient(url, credential=key)

# 데이터베이스와 컨테이너 참조
database_name = "your-database-name"
container_name = "your-container-name"
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)
```
2. 쿼리 정의

SQL 쿼리를 문자열로 작성합니다.
```
sql_query = "SELECT * FROM products p WHERE p.price > @lower"
```
3. Query Options 설정

쿼리의 페이지 크기를 지정하려면 max_item_count를 설정합니다.
```
query_options = {
    "max_item_count": 100  # 한 페이지에서 반환할 최대 항목 수
}
```
4. FeedIterator 생성

Python SDK에서는 query_items 메서드를 사용하여 쿼리를 실행합니다. 이 메서드는 max_item_count를 포함하여 옵션을 설정할 수 있습니다.
```
parameters = [
    {"name": "@lower", "value": 500}  # 변수 설정
]

iterator = container.query_items(
    query=sql_query,
    parameters=parameters,
    enable_cross_partition_query=True,  # 분할된 데이터를 처리할 때 필요
    max_item_count=query_options["max_item_count"]
)
```
5. 페이지별로 결과 처리

iterator 객체는 by_page() 메서드를 통해 페이지 단위로 순회할 수 있습니다. 각 페이지의 데이터를 처리하려면 아래와 같이 작성합니다.
```
from azure.core.exceptions import AzureError

try:
    for page in iterator.by_page():
        items = list(page)
        for item in items:
            print(f"Product Name: {item['name']}, Price: {item['price']}")
except AzureError as e:
    print(f"An error occurred: {str(e)}")
```
요약
	1.	CosmosClient 설정: Python SDK를 사용해 Cosmos DB에 연결합니다.
	2.	쿼리 작성: SQL 쿼리와 매개변수를 정의합니다.
	3.	쿼리 옵션 지정: max_item_count를 설정하여 페이지 크기를 제어합니다.
	4.	FeedIterator 사용: query_items와 by_page를 통해 페이지별 데이터를 처리합니다.

이 코드는 Cosmos DB Python SDK를 사용하여 대규모 데이터셋을 페이지 단위로 처리할 수 있도록 설계되었습니다. 필요에 따라 max_item_count 값을 조정하여 성능을 최적화할 수 있습니다.
