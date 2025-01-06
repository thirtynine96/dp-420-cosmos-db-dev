#
#  먼저, pip install azure-cosmos 명령어로 Python용 Azure Cosmos 패키지를 설치합니다.
#
import json
from azure.cosmos import CosmosClient, PartitionKey

# (1) Cosmos DB 연결 설정 (직접 문자열 입력)
COSMOS_ENDPOINT = "https://<YOUR_COSMOS_ENDPOINT>.documents.azure.com:443/"
COSMOS_KEY = "<YOUR_COSMOS_KEY>"

# (2) DB, 컨테이너 이름 설정
DATABASE_NAME = "MyDatabase"
CONTAINER_NAME = "MyContainer"

# (3) CosmosClient 생성
client = CosmosClient(url=COSMOS_ENDPOINT, credential=COSMOS_KEY)

# (4) 데이터베이스 생성(혹은 이미 존재한다면 가져오기)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

# (5) 컨테이너 생성(혹은 이미 존재한다면 가져오기)
#    partition_key 파라미터: 보통 /category, /department 등 실제 파티션 키 경로에 맞게 변경
container = database.create_container_if_not_exists(
    id=CONTAINER_NAME,
    partition_key=PartitionKey(path="/categoryId"),
    offer_throughput=400  # 필요에 따라 조정
)

print("[INFO] Database & Container 준비 완료")

# (6) 예시 아이템 정의
#     실제 시나리오에서는 사용자 입력, JSON 파일, 혹은 다른 소스에서 불러올 수 있음
item_to_create = {
    "id": "item1",            # Cosmos DB에서 id는 고유 식별자
    "categoryId": "cat1",     # 파티션 키로 사용
    "name": "Sample Item",
    "description": "This is a sample item for CRUD operations.",
    "price": 99.99
}

##
# CREATE
##

# (7) 아이템 생성
try:
    created_item = container.create_item(body=item_to_create)
    print(f"[CREATE] 아이템 생성 완료. ID: {created_item['id']}")
except Exception as e:
    print("[CREATE] 에러 발생:", e)


##
# READ
##

# (8) 아이템 읽기 (Read)
try:
    # id와 파티션 키를 지정하여 문서를 읽을 수 있음
    read_item = container.read_item(
        item=item_to_create["id"],
        partition_key=item_to_create["categoryId"]
    )
    print(f"[READ] 아이템 읽기 완료. 내용: {read_item}")
except Exception as e:
    print("[READ] 에러 발생:", e)


##
# QUERY
##

# (9) 쿼리 - SQL 질의 형태로 아이템 목록 조회
try:
    query = "SELECT * FROM c WHERE c.categoryId = @catId"
    parameters = [
        {"name": "@catId", "value": "cat1"}
    ]
    items = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True  # 파티션 분산 쿼리를 허용
        )
    )
    print(f"[QUERY] cat1 파티션의 아이템 목록 (총 {len(items)}개):")
    for it in items:
        print(" -", it)
except Exception as e:
    print("[QUERY] 에러 발생:", e)


##
# UPDATE (Replace)
##

# (10) 아이템 수정(Replace)
#      upsert_item()을 사용해도 되지만, 여기서는 replace_item() 사용 예시를 보임
try:
    # 우선 기존 아이템을 읽어온 후, 특정 필드를 업데이트
    item_to_update = container.read_item(
        item=item_to_create["id"],
        partition_key=item_to_create["categoryId"]
    )
    item_to_update["price"] = 79.99
    item_to_update["description"] = "Updated item description"

    updated_item = container.replace_item(
        item=item_to_create["id"],       # 혹은 item_to_update
        body=item_to_update
    )
    print(f"[UPDATE] 아이템 갱신 완료. 새로운 가격: {updated_item['price']}")
except Exception as e:
    print("[UPDATE] 에러 발생:", e)


##
# DELETE
##

# (11) 아이템 삭제(Delete)
try:
    container.delete_item(
        item=item_to_create["id"],
        partition_key=item_to_create["categoryId"]
    )
    print("[DELETE] 아이템 삭제 완료")
except Exception as e:
    print("[DELETE] 에러 발생:", e)
