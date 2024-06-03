from django.http import JsonResponse
from .models import PatientRecord_Detail

def help_input(request):
    identifier = request.user  # 假設用戶的唯一標識符儲存在user模型中
    diagnoses = PatientRecord_Detail.objects.filter(identifier=identifier).values('diagnosis', 'date', 'doctor_id')
    
    if diagnoses:
        diagnoses_list = list(diagnoses)
        return JsonResponse({'success': True, 'diagnoses': diagnoses_list})
    else:
        return JsonResponse({'success': False, 'message': 'No diagnosis records found.'})

# def get_patient_diagnoses(request):
#     patient_id = request.user.identifier  # 假設用戶的唯一標識符儲存在user模型中
#     diagnoses = PatientRecord_Detail.objects.filter(patient_id=patient_id).values('diagnosis', 'date', 'doctor_id')
    
#     if diagnoses:
#         diagnoses_list = list(diagnoses)
#         return JsonResponse({'success': True, 'diagnoses': diagnoses_list})
#     else:
#         return JsonResponse({'success': False, 'message': 'No diagnosis records found.'})