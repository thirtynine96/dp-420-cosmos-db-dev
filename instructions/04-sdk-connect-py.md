---
lab:
    title: 'Connect to Azure Cosmos DB for NoSQL with the SDK'
    module: 'Module 3 - Connect to Azure Cosmos DB for NoSQL with the SDK with Python'
---

## Prepare your development environment

If you have not already cloned the lab code repository for **DP-420** to the environment where you're working on this lab, follow these steps to do so. Otherwise, open the previously cloned folder in **Visual Studio Code**.

1. Start **Visual Studio Code**.

    > &#128221; If you are not already familiar with the Visual Studio Code interface, review the [Get Started guide for Visual Studio Code][code.visualstudio.com/docs/getstarted]

1. Open the command palette and run **Git: Clone** to clone the ``https://github.com/microsoftlearning/dp-420-cosmos-db-dev`` GitHub repository in a local folder of your choice.

    > &#128161; You can use the **CTRL+SHIFT+P** keyboard shortcut to open the command palette.

1. Once the repository has been cloned, open the local folder you selected in **Visual Studio Code**.

## Create an Azure Cosmos DB for NoSQL account

Azure Cosmos DB is a cloud-based NoSQL database service that supports multiple APIs. When provisioning an Azure Cosmos DB account for the first time, you will select which of the APIs you want the account to support (for example, **Mongo API** or **NoSQL API**). Once the Azure Cosmos DB for NoSQL account is done provisioning, you can retrieve the endpoint and key and use them to connect to the Azure Cosmos DB for NoSQL account using the Azure SDK for .NET or any other SDK of your choice.

1. In a new web browser window or tab, navigate to the Azure portal (``portal.azure.com``).

1. Sign into the portal using the Microsoft credentials associated with your subscription.

1. Select **+ Create a resource**, search for *Cosmos DB*, and then create a new **Azure Cosmos DB for NoSQL** account resource with the following settings, leaving all remaining settings to their default values:

    | **Setting** | **Value** |
    | ---: | :--- |
    | **Subscription** | *Your existing Azure subscription* |
    | **Resource group** | *Select an existing or create a new resource group* |
    | **Account Name** | *Enter a globally unique name* |
    | **Location** | *Choose any available region* |
    | **Capacity mode** | *Provisioned throughput* |
    | **Apply Free Tier Discount** | *Do Not Apply* |
    | **Limit the total amount of throughput that can be provisioned on this account** | *Unchecked* |

    > &#128221; Your lab environments may have restrictions preventing you from creating a new resource group. If that is the case, use the existing pre-created resource group.

1. Wait for the deployment task to complete before continuing with this task.

1. Go to the newly created **Azure Cosmos DB** account resource and navigate to the **Keys** pane.

1. This pane contains the connection details and credentials necessary to connect to the account from the SDK. Specifically:

    1. Notice the **URI** field. You will use this **endpoint** value later in this exercise.

    1. Notice the **PRIMARY KEY** field. You will use this **key** value later in this exercise.

1. Keep the browser tab open, as we will return to it later.


Azure Cosmos DB와 Python SDK를 사용하여 Python으로 이 핸즈온 실습을 진행할 수 있도록 내용을 Python 기반으로 변환. 
Microsoft의 Cosmos DB Python SDK를 사용한 예제 코드임.

Python SDK로 Azure Cosmos DB 연결 및 데이터 작업
# 1.	Python 환경 설정
Python SDK를 설치합니다.
 ```
pip install azure-cosmos
 ```

# 2.	Python 코드 작성
아래는 핸즈온에서 제공된 작업을 Python 코드로 변환한 예제입니다.
 ```
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

 ```

#	3.	Python 코드 실행
위 코드의 <YOUR_COSMOS_DB_ACCOUNT_URI>와 <YOUR_COSMOS_DB_PRIMARY_KEY>를 Azure 포털에서 가져와 대체한 후 실행합니다.

작업 설명
	•	Database 생성: create_database_if_not_exists를 사용해 데이터베이스를 생성합니다.
	•	Container 생성: create_container_if_not_exists로 컨테이너를 생성하며, 파티션 키를 설정합니다.
	•	데이터 삽입: create_item 메서드로 JSON 문서를 삽입합니다.
	•	쿼리 실행: SQL 형식의 쿼리문으로 데이터를 조회합니다.
