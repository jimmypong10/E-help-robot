import requests
import re
from .models import PatientRecord_Detail

def find_patient_id_by_identifier(server_url, identifier_value):
    url = f"{server_url}/Patient"
    params = {'identifier': identifier_value}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        bundle = response.json()
        if 'entry' in bundle:
            entry = bundle['entry'][0]
            resource = entry.get('resource', {})
            patient_id = resource.get('id', None)
            return identifier_value, patient_id
    return identifier_value, None

def get_patient_records(server_url, patient_id):
    url = f"{server_url}/Composition?subject=Patient/{patient_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def extract_text_from_div(div_text):
    match = re.search(r'<div[^>]*>(.*?)</div>', div_text)
    return match.group(1) if match else div_text

def save_patient_records(identifier, patient_id, records):
    for entry in records.get('entry', []):
        composition = entry.get('resource')
        if composition:
            date = composition.get('date', 'N/A')
            author_reference = composition.get('author', [{}])[0].get('reference', 'N/A')
            author_id = author_reference.split('/')[-1]
            diagnoses = [extract_text_from_div(section.get('text', {}).get('div', 'N/A')) for section in composition.get('section', [])]
            for diagnosis in diagnoses:
                # 檢查記錄是否已存在
                if not PatientRecord_Detail.objects.filter(patient_id=patient_id, date=date, doctor_id=author_id, diagnosis=diagnosis).exists():
                    PatientRecord_Detail.objects.create(
                        identifier=identifier,
                        patient_id=patient_id,
                        date=date,
                        doctor_id=author_id,
                        diagnosis=diagnosis
                    )