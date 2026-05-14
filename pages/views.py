# Copyright 2015 Distilled
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

import json
import logging

from django.http import JsonResponse
from django.shortcuts import render

from pages.helpers_directive import canonical_directives
from pages.helpers_directive import delay_directives
from pages.helpers_directive import h1_directive
from pages.helpers_directive import handle_redirect
from pages.helpers_directive import index_follow_directives
from pages.helpers_directive import title_tag_directive
from pages.helpers_directive import vary_directives
from pages.helpers_url import get_directives_from_random_matching_block

logger = logging.getLogger('simbin.pages.views')

_STATUS_ANNOTATIONS = {
    200: ('Success - content will be processed by crawlers', 'info'),
    301: ('Permanent redirect - crawler follows Location to destination', 'warning'),
    302: ('Temporary redirect - crawler follows Location but may re-crawl this URL', 'warning'),
    303: ('See Other redirect - typically used after POST', 'warning'),
    307: ('Temporary redirect (method-preserving)', 'warning'),
    308: ('Permanent redirect (method-preserving)', 'warning'),
    400: ('Bad Request - malformed request', 'critical'),
    401: ('Unauthorized - authentication required; crawlers typically cannot authenticate', 'critical'),
    403: ('Forbidden - access denied', 'critical'),
    404: ('Not Found - URL treated as non-existent; signals removal to crawlers', 'critical'),
    410: ('Gone - URL permanently removed; stronger removal signal than 404', 'critical'),
    418: ("I'm a teapot - RFC 2324 easter egg; crawlers will treat as an error", 'info'),
    500: ('Internal Server Error - temporary failure; crawlers will retry', 'critical'),
    503: ('Service Unavailable - crawlers should back off and retry later', 'critical'),
}

_HEADER_ANNOTATIONS = {
    'X-Robots-Tag': lambda v: (
        'HTTP-level robots directive. Authoritative for non-HTML resources; takes precedence over meta tags for bots that honour it.',
        'critical' if any(x in v for x in ('noindex', 'none', 'nofollow')) else 'info',
    ),
    'Link': lambda v: (
        'HTTP-level canonical. Most crawlers honour this ahead of the HTML <link rel="canonical">.',
        'info',
    ),
    'Vary': lambda v: (
        f'Response content varies by: {v}. Crawlers that cache may store separate copies per variant.',
        'warning' if any(x in v for x in ('User-Agent', 'Cookie')) else 'info',
    ),
    'Location': lambda v: (
        'Redirect target URL. Crawler follows this on 3xx responses.',
        'warning',
    ),
    'WWW-Authenticate': lambda v: (
        'Authentication challenge. Crawlers cannot authenticate and will treat this as a hard block.',
        'critical',
    ),
}


def _build_http_signals(status_code, headers):
    annotation, impact = _STATUS_ANNOTATIONS.get(
        status_code,
        ('Non-standard status code', 'critical' if status_code >= 400 else 'warning'),
    )
    # Status is baseline unless a directive changed it
    signals = [{'name': 'Status', 'value': f'HTTP/1.1 {status_code}', 'annotation': annotation, 'impact': impact, 'active': status_code != 200}]
    for name, value in headers.items():
        annotate = _HEADER_ANNOTATIONS.get(name)
        if annotate:
            ann, imp = annotate(value)
        else:
            ann, imp = f'{name} header', 'info'
        # All non-status headers are directive-set
        signals.append({'name': name, 'value': f'{name}: {value}', 'annotation': ann, 'impact': imp, 'active': True})
    return signals


def _build_head_signals(context, directives):
    signals = []

    title = context.get('title', '')
    if 'random_title' in directives:
        signals.append({
            'name': '<title>',
            'value': f'<title>{title}</title>',
            'annotation': 'Randomly chosen on each request - crawlers may see inconsistent titles across recrawls',
            'impact': 'warning',
            'active': True,
        })
    else:
        signals.append({
            'name': '<title>',
            'value': f'<title>{title}</title>',
            'annotation': 'Page title as seen by crawlers and browser tabs',
            'impact': 'info',
            'active': False,  # default title, no directive modified it
        })

    meta_str = context.get('meta_follow_index_string', '')
    if meta_str:
        has_noindex = 'noindex' in meta_str
        has_nofollow = 'nofollow' in meta_str
        if has_noindex and has_nofollow:
            ann = 'Blocks both indexing and link-following. Page will be dropped from index.'
            imp = 'critical'
        elif has_noindex:
            ann = 'Blocks page from being indexed. Crawler reads content but does not store it.'
            imp = 'critical'
        elif has_nofollow:
            ann = 'Links on this page will not be followed or crawled.'
            imp = 'warning'
        else:
            ann = 'Explicit allow directive - redundant unless overriding a prior signal.'
            imp = 'info'
        signals.append({'name': '<meta name="robots">', 'value': f'<meta name="robots" content="{meta_str}">', 'annotation': ann, 'impact': imp, 'active': True})

    canonical_map = [
        ('canonical_self',       'Self-referential canonical - confirms this URL as the preferred version'),
        ('canonical_home',       'Canonical points to homepage - tells crawlers to attribute signals to homepage instead'),
        ('canonical_next_block', 'Canonical points to the previous URL block in the path'),
        ('canonical_random',     'Canonical points to a randomly chosen URL - unpredictable; may cause signal churn'),
    ]
    for key, ann in canonical_map:
        val = context.get(key, '')
        if val:
            imp = 'warning' if key in ('canonical_home', 'canonical_random') else 'info'
            signals.append({'name': '<link rel="canonical">', 'value': f'<link rel="canonical" href="{val}">', 'annotation': ann, 'impact': imp, 'active': True})

    return signals


def _build_body_signals(context):
    h1 = context.get('h1', '')
    if h1 == 'off':
        return [{'name': '<h1>', 'value': '(absent)', 'annotation': 'No H1 tag - missing primary heading signal for crawlers', 'impact': 'warning', 'active': True}]
    if h1 == 'multiple':
        return [{'name': '<h1>', 'value': '<h1>SimBin</h1>  <h1>Another title</h1>', 'annotation': 'Multiple H1 tags - ambiguous primary heading; crawlers may pick either', 'impact': 'warning', 'active': True}]
    return [{'name': '<h1>', 'value': '<h1>SimBin</h1>', 'annotation': 'Single H1 present - unambiguous primary heading signal', 'impact': 'info', 'active': False}]


def index(request):
    return render(request, 'pages/index.html')


def scenarios(request):
    return render(request, 'pages/scenarios.html')


def robots(request):
    response = render(request, "pages/robots.txt")
    response['Content-Type'] = "text/plain; charset=UTF-8"
    return response


def handle(request, url):
    url_parts = url.split("/")
    last_part = url_parts[-1]
    previous_parts = url_parts[:-1]
    directives = get_directives_from_random_matching_block(
        last_part,
        user_agent=request.META['HTTP_USER_AGENT']
    )

    base_url = '{scheme}://{host}'.format(scheme=request.scheme, host=request.get_host())
    current_url = '{base}{path}'.format(base=base_url, path=request.path)

    path = '/'.join(pp for pp in previous_parts)
    previous_parts_url = (
        '{base}/{path}/'.format(base=base_url, path=path) if path
        else '{base}/'.format(base=base_url)
    )

    page_title = " + ".join(
        flag.replace("_", " ").title() for flag in last_part.split("+") if flag
    )
    context = {'url': url, 'previous_parts_url': previous_parts_url, 'directives': directives, 'page_title': page_title}
    headers = {}

    h1_context, h1_headers = h1_directive(directives)
    context.update(h1_context)
    headers.update(h1_headers)

    title_tag_context, title_tag_headers = title_tag_directive(directives)
    context.update(title_tag_context)
    headers.update(title_tag_headers)

    index_follow_context, index_follow_headers = index_follow_directives(directives)
    context.update(index_follow_context)
    headers.update(index_follow_headers)

    canonical_context, canonical_headers = canonical_directives(
        directives, base_url, current_url, previous_parts_url
    )
    context.update(canonical_context)
    headers.update(canonical_headers)

    vary_context, vary_headers = vary_directives(directives)
    context.update(vary_context)
    headers.update(vary_headers)

    delay_context, delay_headers = delay_directives(directives)
    context.update(delay_context)
    headers.update(delay_headers)

    response_context, response_headers, status_code = handle_redirect(
        directives, previous_parts_url
    )
    context.update(response_context)
    headers.update(response_headers)

    context['status_code'] = status_code
    context['http_signals'] = _build_http_signals(status_code, headers)
    context['head_signals'] = _build_head_signals(context, directives)
    context['body_signals'] = _build_body_signals(context)

    jsonld = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": current_url,
        "name": f"SimBin: /{url}/",
        "additionalProperty": (
            [{"@type": "PropertyValue", "name": s['name'], "value": s['value'], "description": s['annotation']}
             for s in context['http_signals'] + context['head_signals'] + context['body_signals']]
        ),
    }
    context['jsonld_data'] = json.dumps(jsonld)

    response = render(request, "pages/template.html", context, status=status_code)
    for header_key, header_val in headers.items():
        response[header_key] = header_val
    return response


def health_check(request):
    return JsonResponse({'status': 'healthy', 'message': 'Simbin is running'})
