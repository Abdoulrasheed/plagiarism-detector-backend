import random
from django.views import View
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from copyleaks.copyleaks import Copyleaks, Products
from copyleaks.models.submit.document import UrlDocument
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.properties.scan_properties import ScanProperties

class LoginView(View):
    def get(self, request):
        try:
            response = Copyleaks.login(settings.COPYLEAKS_EMAIL_ID, settings.COPYLEAKS_API_KEY)
        except CommandError as ce:
            response = ce.get_response()
            print(f"An error occurred (HTTP status code {response.status_code}):")
            print(response.content)
            return JsonResponse({"error":"theres a problem"}, status=401)
        
        return JsonResponse(response)

class ScanURLView(View):
    def get(self, request, filename, token, issued, expires):
        scan_id = random.randint(100, 100000)

        print("scan_id")
        print(scan_id)
        print("scan_id")
        
        url_submission = UrlDocument()
        url_submission.set_url(f"https://bitsmss.s3.eu-west-2.amazonaws.com/{filename}")
        scan_properties = ScanProperties('http://cd0b0bfc85b4.ngrok.io/app/webhook/results?event={{STATUS}}')
        scan_properties.set_sandbox(True)
        url_submission.set_properties(scan_properties)
        tok = { "access_token": token,  ".issued": issued,  ".expires": expires }

        res = Copyleaks.submit_url(Products.EDUCATION, tok, scan_id, url_submission)
        print(res)

        return JsonResponse({"status": "success"})