"""esite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from bifrost import urls as api_urls
from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.contrib.sitemaps.views import sitemap
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.utils.urlpatterns import decorate_urlpatterns

# from esite.search import views as search_views


# Private URLs are not meant to be cached.
private_urlpatterns = [
    url(r"", include(api_urls)),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
]


# Public URLs that are meant to be cached.
urlpatterns = [
    # path("sitemap.xml", sitemap),
    # path("favicon.ico", favicon),
    # path("robots.txt", robots),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += [
        # Add views for testing 404 and 500 templates
        path(
            "test404/",
            TemplateView.as_view(template_name="patterns/pages/wagtail/404.html"),
        ),
        path(
            "test500/",
            TemplateView.as_view(template_name="patterns/pages/wagtail/500.html"),
        ),
    ]


# Style guide
if getattr(settings, "PATTERN_LIBRARY_ENABLED", False) and apps.is_installed(
    "pattern_library"
):
    private_urlpatterns += [path("pattern-library/", include("pattern_library.urls"))]


# Set public URLs to use the "default" cache settings.
#urlpatterns = decorate_urlpatterns(urlpatterns, get_default_cache_control_decorator())

# Set vary header to instruct cache to serve different version on different
# cookies, different request method (e.g. AJAX) and different protocol
# (http vs https).
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    vary_on_headers(
        "Cookie", "X-Requested-With", "X-Forwarded-Proto", "Accept-Encoding"
    ),
)

# Join private and public URLs.
urlpatterns = (
    private_urlpatterns
    + urlpatterns
    + [
        # Add Wagtail URLs at the end.
        # Wagtail cache-control is set on the page models's serve methods.
        path("", include(wagtail_urls))
    ]
)

# Error handlers
# handler404 = "esite.utils.views.page_not_found"
# handler500 = "esite.utils.views.server_error"

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
