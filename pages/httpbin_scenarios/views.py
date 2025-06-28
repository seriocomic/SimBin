from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import json
import base64
import uuid

# Scenario: Status Codes
def status_code(request, code):
    return HttpResponse(status=code)

# Scenario: Redirects
def redirect(request):
    return HttpResponse(status=302, headers={'Location': '/new-location'})

# Scenario: Headers
def headers(request):
    return JsonResponse(dict(request.headers))

# Scenario: Cookies
def cookies(request):
    response = JsonResponse({'cookies': request.COOKIES})
    response.set_cookie('test_cookie', 'test_value')
    return response

# Scenario: JSON/XML
def json_response(request):
    return JsonResponse({'message': 'This is a JSON response'})

def xml_response(request):
    xml_content = """<?xml version='1.0' encoding='UTF-8'?>
    <response>
        <message>This is an XML response</message>
    </response>"""
    return HttpResponse(xml_content, content_type='application/xml')

# Scenario: Base64
def base64_decode(request, encoded_string):
    decoded = base64.b64decode(encoded_string).decode('utf-8')
    return JsonResponse({'decoded': decoded})

# Scenario: HTML
def html_response(request):
    html_content = "<html><body><h1>This is an HTML response</h1></body></html>"
    return HttpResponse(html_content, content_type='text/html')

# Scenario: Robots.txt
def robots_txt(request):
    content = "User-agent: *\nDisallow: /"
    return HttpResponse(content, content_type='text/plain')
