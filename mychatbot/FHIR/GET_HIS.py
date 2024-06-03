import requests
import re
def get_patient_records(server_url, patient_id):
    # 設置查詢URL
    url = f"{server_url}/Composition?subject=Patient/{patient_id}"

    # 發送GET請求查詢Composition資源
    response = requests.get(url)

    # 檢查響應狀態碼
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve patient records: {response.status_code}")
        return None
def extract_text_from_div(div_text):
    # 使用正則表達式提取<div>標籤內的文字
    match = re.search(r'<div[^>]*>(.*?)</div>', div_text)
    return match.group(1) if match else div_text

def display_patient_records(patient_records):
    # 遍歷查詢結果中的每個Composition資源
    for entry in patient_records.get('entry', []):
        composition = entry.get('resource')
        if composition:
            date = composition.get('date', 'N/A')
            author_reference = composition.get('author', [{}])[0].get('reference', 'N/A')
            author_id = author_reference.split('/')[-1]  # 獲取醫生ID
            patient_reference = composition.get('subject', {}).get('reference', 'N/A')
            patient_id = patient_reference.split('/')[-1]  # 獲取患者ID

            diagnoses = []
            for section in composition.get('section', []):
                diagnosis_html = section.get('text', {}).get('div', 'N/A')
                diagnosis_text = extract_text_from_div(diagnosis_html)
                diagnoses.append(diagnosis_text)

            # 顯示提取的信息
            print(f"Date: {date}")
            print(f"Doctor ID: {author_id}")
            print(f"Patient ID: {patient_id}")
            print(f"Diagnoses: {', '.join(diagnoses)}")
            print('---')

# 設置FHIR服務器的URL和相關ID
fhir_server_url = "http://localhost:8080/fhir"
patient_id = "55"

# 獲取患者病歷記錄
patient_records = get_patient_records(fhir_server_url, patient_id)

# 顯示患者病歷記錄
if patient_records:
    display_patient_records(patient_records)
else:
    print("No patient records found.")
