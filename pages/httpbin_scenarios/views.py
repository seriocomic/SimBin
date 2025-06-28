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

# Scenario: User Agent
def user_agent(request):
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    return JsonResponse({'user-agent': user_agent})

# Scenario: IP Address
def ip_address(request):
    # Get IP from various headers in case of proxy/load balancer
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return JsonResponse({'origin': ip})

# Scenario: Cookie Management
def cookies_set(request, name, value):
    response = JsonResponse({'message': f'Cookie {name} set to {value}'})
    response.set_cookie(name, value)
    return response

def cookies_delete(request, name):
    response = JsonResponse({'message': f'Cookie {name} deleted'})
    response.delete_cookie(name)
    return response

# Scenario: HTTP Methods
def get_request(request):
    return JsonResponse({
        'method': 'GET',
        'args': dict(request.GET),
        'headers': dict(request.headers),
        'origin': request.META.get('REMOTE_ADDR'),
        'url': request.build_absolute_uri()
    })

def post_request(request):
    data = {}
    if request.content_type == 'application/json':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
    else:
        data = dict(request.POST)
    
    return JsonResponse({
        'method': 'POST',
        'args': dict(request.GET),
        'data': data,
        'files': {k: str(v) for k, v in request.FILES.items()},
        'form': dict(request.POST),
        'headers': dict(request.headers),
        'json': data if request.content_type == 'application/json' else None,
        'origin': request.META.get('REMOTE_ADDR'),
        'url': request.build_absolute_uri()
    })

def anything_request(request):
    data = {}
    if request.content_type == 'application/json' and request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
    
    return JsonResponse({
        'method': request.method,
        'args': dict(request.GET),
        'data': data,
        'files': {k: str(v) for k, v in request.FILES.items()},
        'form': dict(request.POST),
        'headers': dict(request.headers),
        'json': data if request.content_type == 'application/json' else None,
        'origin': request.META.get('REMOTE_ADDR'),
        'url': request.build_absolute_uri()
    })

# Scenario: Redirect Chains
def redirect_chain(request, count):
    count = int(count)
    if count <= 0:
        return JsonResponse({'message': 'Redirect chain complete'})
    
    next_count = count - 1
    if next_count > 0:
        from django.urls import reverse
        redirect_url = reverse('redirect_chain', args=[next_count])
        return HttpResponse(status=302, headers={'Location': redirect_url})
    else:
        return JsonResponse({'message': 'Final redirect destination reached'})
