from azure.cosmos import CosmosClient

# Cosmos DB 클라이언트 초기화
endpoint = "https://cosmos-dustin.documents.azure.com:443/"
key = "gaG1dj623kKqR90ZTYJL0xn6aXqVolyodzOrlpFl4feNn6bHzvbV7J8vv5eDirNGNirjU3hFzuSYACDbIFvPDA=="
client = CosmosClient(endpoint, key)

# 데이터베이스 참조
database = client.get_database_client("<database-name>")

# 처리량 확인
throughput = database.read_offer()
print(f"Database throughput: {throughput['content']['offerThroughput']} RU/s")


# 컨테이너 참조
database = client.get_database_client("<database-name>")
container = database.get_container_client("<container-name>")

# 처리량 확인
throughput = container.read_offer()
print(f"Container throughput: {throughput['content']['offerThroughput']} RU/s")