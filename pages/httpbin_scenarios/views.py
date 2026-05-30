import base64
import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

STATUS_DESCRIPTIONS = {
    100: "Continue",
    101: "Switching Protocols",
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    301: "Moved Permanently",
    302: "Found",
    303: "See Other",
    304: "Not Modified",
    307: "Temporary Redirect",
    308: "Permanent Redirect",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    410: "Gone",
    418: "I'm a teapot",
    429: "Too Many Requests",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
}


def status_code(request, code):
    description = STATUS_DESCRIPTIONS.get(code, "Unknown Status Code")
    return JsonResponse(
        {"status": code, "description": description},
        status=code,
    )


def redirect(request):
    from django.urls import reverse

    return HttpResponse(status=302, headers={"Location": reverse("get_request")})


def headers(request):
    return JsonResponse(dict(request.headers))


def cookies(request):
    response = JsonResponse({"cookies": request.COOKIES})
    response.set_cookie("test_cookie", "test_value")
    return response


def json_response(request):
    return JsonResponse({"message": "This is a JSON response"})


def xml_response(request):
    xml_content = (
        "<?xml version='1.0' encoding='UTF-8'?>\n"
        "<response>\n"
        "    <message>This is an XML response</message>\n"
        "</response>"
    )
    return HttpResponse(xml_content, content_type="application/xml")


def base64_decode(request, encoded_string):
    try:
        decoded = base64.b64decode(encoded_string).decode("utf-8")
    except Exception:
        return JsonResponse(
            {"error": "Invalid base64 encoding", "input": encoded_string},
            status=400,
        )
    return JsonResponse({"decoded": decoded})


def html_response(request):
    html_content = "<html><body><h1>This is an HTML response</h1></body></html>"
    return HttpResponse(html_content, content_type="text/html")


def robots_txt(request):
    content = "User-agent: *\nDisallow: /"
    return HttpResponse(content, content_type="text/plain")


def user_agent(request):
    ua = request.META.get("HTTP_USER_AGENT", "Unknown")
    return JsonResponse({"user-agent": ua})


def ip_address(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return JsonResponse({"origin": ip})


def cookies_set(request, name, value):
    response = JsonResponse({"message": f"Cookie {name} set to {value}"})
    response.set_cookie(name, value)
    return response


def cookies_delete(request, name):
    response = JsonResponse({"message": f"Cookie {name} deleted"})
    response.delete_cookie(name)
    return response


def get_request(request):
    return JsonResponse({
        "method": request.method,
        "args": dict(request.GET),
        "headers": dict(request.headers),
        "origin": request.META.get("REMOTE_ADDR"),
        "url": request.build_absolute_uri(),
    })


@csrf_exempt
def post_request(request):
    data = {}
    if request.content_type == "application/json":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}
    else:
        data = dict(request.POST)

    return JsonResponse({
        "method": request.method,
        "args": dict(request.GET),
        "data": data,
        "files": {k: str(v) for k, v in request.FILES.items()},
        "form": dict(request.POST),
        "headers": dict(request.headers),
        "json": data if request.content_type == "application/json" else None,
        "origin": request.META.get("REMOTE_ADDR"),
        "url": request.build_absolute_uri(),
    })


@csrf_exempt
def anything_request(request):
    data = {}
    if request.content_type == "application/json" and request.body:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = {}

    return JsonResponse({
        "method": request.method,
        "args": dict(request.GET),
        "data": data,
        "files": {k: str(v) for k, v in request.FILES.items()},
        "form": dict(request.POST),
        "headers": dict(request.headers),
        "json": data if request.content_type == "application/json" else None,
        "origin": request.META.get("REMOTE_ADDR"),
        "url": request.build_absolute_uri(),
    })


def redirect_chain(request, count):
    count = int(count)
    if count <= 0:
        return JsonResponse({"message": "Redirect chain complete"})

    next_count = count - 1
    if next_count > 0:
        from django.urls import reverse

        redirect_url = reverse("redirect_chain", args=[next_count])
        return HttpResponse(status=302, headers={"Location": redirect_url})
    else:
        return JsonResponse({"message": "Final redirect destination reached"})
