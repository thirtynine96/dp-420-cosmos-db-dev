from azure.cosmos import CosmosClient, PartitionKey

# Cosmos DB 연결 설정

endpoint = "YOUR_ENDPOINT"
key = "YOUR_KEY"
database_name = "cosmicworks"
container_name = "products"

# 클라이언트 초기화
client = CosmosClient(endpoint, key)
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

# 모든 아이템 조회
query = "SELECT * FROM c"
items = list(container.query_items(query=query, enable_cross_partition_query=True))

# 각 아이템 삭제
for item in items:
    # 파티션 키 값을 지정하여 삭제
    partition_key = [item['category']['name'], item['category']['subCategory']['name']]
    container.delete_item(
        item=item,
        partition_key=partition_key
    )
