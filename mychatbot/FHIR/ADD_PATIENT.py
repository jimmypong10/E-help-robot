# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 22:56:40 2024

@author: tiffany
"""

import requests
import json

def create_patient(server_url, name, birth_date, gender, identifier):
    # 設置URL
    url = f"{server_url}/Patient"

    # 構建Patient資源
    patient = {
        "resourceType": "Patient",
        "name": [
            {
                "use": "official",
                "family": name.get("family", ""),
                "given": [name.get("given", "")]
            }
        ],
        "gender": gender,
        "birthDate": birth_date,
        "identifier": [
            {
                "system": identifier.get("system", ""),
                "value": identifier.get("value", "")
            }
        ]
    }

    # 發送POST請求創建Patient資源
    response = requests.post(url, json=patient)

    # 檢查響應狀態碼
    if response.status_code == 201:
        print("Patient resource created successfully.")
        return response.json()
    else:
        print(f"Failed to create Patient resource: {response.status_code}")
        print(response.json())
        return None

# 測試新增病患資源
server_url = "http://localhost:8080/fhir"
name = {"family": "Smith", "given": "Tim"}
birth_date = "1989-03-21"
gender = "male"
identifier = {"system": "http://example.org/identifiers", "value": "Z111222333"}

created_patient = create_patient(server_url, name, birth_date, gender, identifier)
print(created_patient)
