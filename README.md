# Introduction

[SimBin](http://simbin.siteladon.com/) is a service, inspired by [httpbin](http://httpbin.org/), to dynamically create combinations of HTML pages with specific HTTP headers for the purpose of testing crawlers or tools that need to be able to handle potentially misleading signals. You can use SimBin to deliberately generate pages with technical issues in order to verify how a crawler handles those scenarios.

SimBin accepts a list of flags in the URL which toggle various directives and HTTP responses. For example, you can simulate a page with a noindex tag, by using the `meta_noindex` flag:

	http://simbin.siteladon.com/meta_noindex/
	<meta name=“robots” content=“noindex” />

You can add a (self referencing) canonical tag to the page using the `html_canonical_self` flag:

	http://simbin.siteladon.com/html_canonical_self/
	<link rel=“canonical” href=“http://simbin.siteladon.com/html_canonical_self/” />

The power of SimBin comes when you start combining the various flags to allow you to generate the sorts of issues you are likely to encounter when doing any sort of technical audit.

For example, by combining a `response_301` flag with an `html_canonical_next_block` flag, you can simulate a canonical tag that references a page that subsequently 301’s. This is surprisingly common and whilst typically not disastrous, it is something that can and should be fixed. You see this sort of issue with automatic redirects setup to handle things like redirecting http -> https or automatically appending trailing slashes if they don’t exist.

Full documentation is available at [simbin.siteladon.com](http://simbin.siteladon.com/).

# Contributing

See CONTRIBUTING file.

# License

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License

See LICENSE file.