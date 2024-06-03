from fhirclient import client

def get_fhir_client():
    settings = {
        'app_id': 'my_app',
        'api_base': 'http://localhost:8080/fhir'
    }
    return client.FHIRClient(settings=settings)