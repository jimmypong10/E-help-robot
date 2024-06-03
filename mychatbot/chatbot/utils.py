import requests

def find_patient_id_by_identifier(server_url, identifier_value):
    # 設置URL
    url = f"{server_url}/Patient?identifier=http://example.org/identifiers|{identifier_value}"

    # 發送GET請求查詢Patient資源
    response = requests.get(url)

    # 檢查響應狀態碼
    if response.status_code == 200:
        print("Patient resources found successfully.")
        # 解析響應JSON
        patients = response.json().get('entry', [])
        if patients:
            # 提取符合條件的病患ID
            patient_id = patients[0].get('resource', {}).get('id')
            return identifier_value, patient_id
        else:
            print("No patient found with the specified identifier.")
            return None, None
    else:
        print(f"Failed to find Patient resources: {response.status_code}")
        print(response.json())
        return None, None

# # 測試根據身分證號查詢病患ID
server_url = "http://localhost:8080/fhir"
# identifier_value = "Z111222333"

# # 調用函數
# identifier, patient_id = find_patient_id_by_identifier(server_url, identifier_value)
# print("身分證號:", identifier)
# print("病患編號:", patient_id)
