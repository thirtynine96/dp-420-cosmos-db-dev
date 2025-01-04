Azure Cosmos DB와 Python SDK를 사용하여 Python으로 이 핸즈온 실습을 진행할 수 있도록 내용을 Python 기반으로 변환해 드리겠습니다.

아래는 Microsoft의 Cosmos DB Python SDK를 사용한 예제 코드입니다. Microsoft의 핸즈온 랩 구조에 맞춰 Python 버전을 작성하였습니다.

Python SDK로 Azure Cosmos DB 연결 및 데이터 작업
	1.	Python 환경 설정
Python SDK를 설치합니다.

pip install azure-cosmos


	2.	Python 코드 작성
아래는 핸즈온에서 제공된 작업을 Python 코드로 변환한 예제입니다.

from azure.cosmos import CosmosClient, PartitionKey, exceptions

# Cosmos DB 연결 정보
endpoint = "<YOUR_COSMOS_DB_ACCOUNT_URI>"
key = "<YOUR_COSMOS_DB_PRIMARY_KEY>"
database_name = "FamilyDatabase"
container_name = "FamilyContainer"

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


	3.	Python 코드 실행
위 코드의 <YOUR_COSMOS_DB_ACCOUNT_URI>와 <YOUR_COSMOS_DB_PRIMARY_KEY>를 Azure 포털에서 가져와 대체한 후 실행합니다.

핵심 작업 설명
	•	Database 생성: create_database_if_not_exists를 사용해 데이터베이스를 생성합니다.
	•	Container 생성: create_container_if_not_exists로 컨테이너를 생성하며, 파티션 키를 설정합니다.
	•	데이터 삽입: create_item 메서드로 JSON 문서를 삽입합니다.
	•	쿼리 실행: SQL 형식의 쿼리문으로 데이터를 조회합니다.
