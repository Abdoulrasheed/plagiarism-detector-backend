import random
import requests
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import os
import json

class ScanURLView(View):
    def get(self, request, filename):
        res = requests.post("https://api.unicheck.com/oauth/access-token", data={
            "grant_type": "client_credentials",
            "client_id": "d2a3ad3e1bf9a9e4e8ab",
            "client_secret": "3e1965ac5a36aa75463c1b795743fc88c551ef75"
        }, headers={"Content-Type" : "application/x-www-form-urlencoded"})

        access_token = res.json()['access_token']

        headers = {
            "Accept": "application/vnd.api+json",
            "Authorization": "Bearer " + access_token
        }

        filestring = f"https://bitsmss.s3.eu-west-2.amazonaws.com/{filename}"

        file = requests.get(filestring)
        
        file_path = os.path.join(settings.MEDIA_ROOT, filename)

        with open(file_path, 'wb') as f:
            f.write(file.content)

        upload_res = requests.post("https://api.unicheck.com/files", 
            files={'file': open(file_path, 'rb')}, 
            headers=headers
        )

        doc_id = upload_res.json()['data']['id']
        words_count = upload_res.json()['data']['attributes']['words_count']
        pages_count = upload_res.json()['data']['attributes']['pages_count']

        headers.update({"Content-Type": "application/vnd.api+json"})

        similarity_res = requests.post("https://api.unicheck.com/similarity/checks", data = json.dumps({ "data": {"type": "similarityCheck", "attributes": { "search_types": { "web": True, "library": False  }, "parameters": { "sensitivity": { "percentage": 0, "words_count": 8 } } } }, "relationships": { "file": { "data": { "id": doc_id, "type": "file" } } }}), headers = headers)

        check_id = similarity_res.json()['data']['id']

        return JsonResponse({
            "message": "success", 
            "scan_id": check_id, 
            "access_token": access_token,
            "pages_count": pages_count,
            "words_count": words_count
        })

@method_decorator(csrf_exempt, name='dispatch')
class CheckResult(View):
    def get(self, request, scan_id, access_token):
        headers = {
            "Accept": "application/vnd.api+json",
            "Authorization": "Bearer " + access_token
        }
        result_res = requests.get(f"https://api.unicheck.com/similarity/checks/{scan_id}", headers=headers)
        
        return JsonResponse(result_res.json())