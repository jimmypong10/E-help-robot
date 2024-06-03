# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 22:09:26 2024

@author: tiffany
"""

import requests

def create_composition(server_url, patient_id, author_id, diagnoses, date):
    # 設置URL
    url = f"{server_url}/Composition"

    # 構建Composition資源
    composition = {
        "resourceType": "Composition",
        "status": "final",
        "type": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "11488-4",
                    "display": "Consult Note"
                }
            ]
        },
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "date": date,
        "author": [
            {
                "reference": f"Practitioner/{author_id}"
            }
        ],
        "title": "Consultation Note",
        "section": []
    }

    # 添加診斷內容
    for diagnosis in diagnoses:
        composition["section"].append({
            "title": "Diagnosis",
            "text": {
                "status": "generated",
                "div": f"<div xmlns=\"http://www.w3.org/1999/xhtml\">{diagnosis}</div>"
            }
        })

    # 發送POST請求創建Composition資源
    response = requests.post(url, json=composition)

    # 檢查響應狀態碼
    if response.status_code == 201:
        print("Composition resource created successfully.")
    else:
        print(f"Failed to create Composition resource: {response.status_code}")
        print(response.json())

# 設置FHIR服務器的URL和相關ID
fhir_server_url = "http://localhost:8080/fhir"
patient_id = "55"
author_id = "52"
diagnoses = ["B型流感"]
date = "2023-07-18"

# 創建Composition資源
create_composition(fhir_server_url, patient_id, author_id, diagnoses, date)
