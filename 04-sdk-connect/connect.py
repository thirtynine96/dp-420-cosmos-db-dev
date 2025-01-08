from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Cosmos DB 연결 정보
endpoint = "https://cosmos-dustin.documents.azure.com:443/"
key = "@=="
database_name = "cosmicworks_python"
container_name = "products_new_python"

# 클라이언트 생성
client = CosmosClient(endpoint, key)

try:
    # 데이터베이스 생성
    database = client.create_database_if_not_exists(id=database_name)
    print(f"Database '{database_name}' created or already exists.")

    # 컨테이너 생성
    container = database.create_container_if_not_exists(
        id=container_name,
        partition_key=PartitionKey(path="/lastName"),
        offer_throughput=400,
    )
    print(f"Container '{container_name}' created or already exists.")

    # 데이터 삽입
    family_item = {
        "id": "AndersenFamily",
        "lastName": "Andersen",
        "parents": [
            {"firstName": "Thomas"},
            {"firstName": "Mary Kay"}
        ],
        "children": [
            {
                "firstName": "Henriette Thaulow",
                "gender": "female",
                "grade": 5,
                "pets": [{"givenName": "Fluffy"}]
            }
        ],
        "address": {"state": "WA", "county": "King", "city": "Seattle"},
        "isRegistered": True,
    }

    container.create_item(body=family_item)
    print("Item inserted successfully.")

    # 데이터 조회
    query = "SELECT * FROM c WHERE c.lastName='Andersen'"
    items = container.query_items(query=query, enable_cross_partition_query=True)

    for item in items:
        print(f"Item found: {item}")

except exceptions.CosmosHttpResponseError as e:
    print(f"An error occurred: {e.message}")
