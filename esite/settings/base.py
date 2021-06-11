"""
Django base settings for esite project.

For more information on this file, see
https://docs.djangoproject.com/en/stable/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/stable/ref/settings/
"""

import os
from datetime import timedelta

env = os.environ.copy()

# > Root Paths
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# > Application Definition
# A list of strings designating all applications that are enabled in this
# Django installation.
# See https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps
INSTALLED_APPS = [
    # Our own apps
    "esite.core",
    "esite.user",
    "esite.documents",
    "esite.images",
    "esite.sneklog_bot",
    "esite.jaen_cms",
    # Django core apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    # Wagtail core apps
    "wagtail.api.v2",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.settings",
    "wagtail.contrib.search_promotions",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    # Third party apps
    "wagtailmedia",
    "corsheaders",
    "django_filters",
    "modelcluster",
    "taggit",
    "captcha",
    "generic_chooser",
    "wagtailcaptcha",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "wagtailfontawesome",
    "pattern_library",
    # BIFROST SPECIFIC MODULES
    "bifrost",
    "graphene_django",
    "channels",
    "wagtail_headless_preview",
]

# > Middleware Definition
# In MIDDLEWARE, each middleware component is represented by a string: the full
# Python path to the middleware factory’s class or function name.
# https://docs.djangoproject.com/en/stable/ref/settings/#middleware
# https://docs.djangoproject.com/en/stable/topics/http/middleware/
MIDDLEWARE = [
    # Django core middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Wagtail core middleware
    "wagtail.contrib.legacy.sitemiddleware.SiteMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    # Third party middleware
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "esite.urls"

# > Template Configuration
# A list containing the settings for all template engines to be used with
# Django.
# See https://docs.djangoproject.com/en/stable/ref/settings/#templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "wagtail.contrib.settings.context_processors.settings",
                # This is a custom context processor that lets us add custom
                # global variables to all the templates.
                # "esite.utils.context_processors.global_vars",
            ],
            "builtins": ["pattern_library.loader_tags"],
        },
    }
]

# > CORS Origin
# If True, the whitelist will not be used and all origins will be accepted.
# See https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True

# > URL Configuration
# A string representing the full Python import path to your root URL configuration.
# See https://docs.djangoproject.com/en/stable/ref/settings/#root-urlconf
ROOT_URLCONF = "esite.urls"

# > Database Configuration
# This setting will use DATABASE_URL environment variable.
# https://docs.djangoproject.com/en/stable/ref/settings/#databases
# https://github.com/kennethreitz/dj-database-url
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# > Graphene Configuration
GRAPHENE = {
    "SCHEMA": "bifrost.api.schema.schema",
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}
GRAPHQL_JWT = {
    "JWT_ALLOW_ARGUMENT": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=5),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

ASGI_APPLICATION = "bifrost.asgi.application"

# > Password Validation
# The list of validators that are used to check the strength of passwords, see
# https://docs.djangoproject.com/en/stable/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "user.SNEKUser"
# AUTH_PROFILE_MODULE = "avatar.Avatar"

# > Authentication Backend
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# > Internationalization
# https://docs.djangoproject.com/en/stable/topics/i18n/
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Vienna"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# > Staticfile Directory
# This is where Django will look for static files outside the directories of
# applications which are used by default.
# https://docs.djangoproject.com/en/stable/ref/settings/#staticfiles-dirs
STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "static")]

# This is where Django will put files collected from application directories
# and custom direcotires set in "STATICFILES_DIRS" when
# using "django-admin collectstatic" command.
# https://docs.djangoproject.com/en/stable/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# This is the URL that will be used when serving static files, e.g.
# https://llamasavers.com/static/
# https://docs.djangoproject.com/en/stable/ref/settings/#static-url
STATIC_URL = "/static/"

# Where in the filesystem the media (user uploaded) content is stored.
# MEDIA_ROOT is not used when S3 backend is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# The URL path that media files will be accessible at. This setting won't be
# used if S3 backend is set up.
# Probably only relevant to the local development.
# https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = "/media/"

# > Wagtail Settings
# This name is displayed in the Wagtail admin.
WAGTAIL_SITE_NAME = "esite"

# > Search Configuration
# https://docs.wagtail.io/en/latest/topics/search/backends.html
WAGTAILSEARCH_BACKENDS = {
    "default": {"BACKEND": "wagtail.search.backends.db", "INDEX": "esite"}
}

# Custom document model
# https://docs.wagtail.io/en/stable/advanced_topics/documents/custom_document_model.html
WAGTAILDOCS_DOCUMENT_MODEL = "documents.SNEKDocument"

# Custom image model
# https://docs.wagtail.io/en/stable/advanced_topics/images/custom_image_model.html
WAGTAILIMAGES_IMAGE_MODEL = "images.SNEKImage"
WAGTAILIMAGES_FEATURE_DETECTION_ENABLED = False

# Rich text settings to remove unneeded features
# We normally don't want editors to use the images
# in the rich text editor, for example.
# They should use the image stream block instead
WAGTAILADMIN_RICH_TEXT_EDITORS = {
    "default": {
        "WIDGET": "wagtail.admin.rich_text.DraftailRichTextArea",
        "OPTIONS": {
            "features": [
                "bold",
                "italic",
                "underline",
                "strikethrough",
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "blockquote",
                "ol",
                "ul",
                "hr",
                "embed",
                "link",
                "superscript",
                "subscript",
                "document-link",
                "image",
                "code",
            ]
        },
    }
}

# Default size of the pagination used on the front-end
DEFAULT_PER_PAGE = 10

# The number of GET/POST parameters
DATA_UPLOAD_MAX_NUMBER_FIELDS = 999999999999999

# > Styleguide
PATTERN_LIBRARY_ENABLED = True
PATTERN_LIBRARY_TEMPLATE_DIR = os.path.join(
    PROJECT_DIR, "project_styleguide", "templates"
)

PASSWORD_REQUIRED_TEMPLATE = "patterns/pages/wagtail/password_required.html"

# > System Checks
# Wagtail forms not used so silence captcha warning
SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]

# > WAGTAIL_ALLOW_UNICODE_SLUGS Checks
# Set this to False to limit slugs to ASCII characters.
# Ref:https://docs.wagtail.io/en/stable/advanced_topics/settings.html#unicode-page-slugs
WAGTAIL_ALLOW_UNICODE_SLUGS = True

# > Bifrost settings
BIFROST_APPS = {
    "core": "",
    "documents": "",
    "images": "",
    "user": "",
    "sneklog_bot": "",
    "jaen_cms": "",
}

BIFROST_FILES = False

BIFROST_ADD_SEARCH_HIT = True

HEADLESS_PREVIEW_CLIENT_URLS = {"default": "http://localhost:8001/preview"}
HEADLESS_PREVIEW_LIVE = True

ASGI_APPLICATION = "bifrost.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [("localhost", 6379)]},
    }
}
# Private file storage
PRIVATE_STORAGE_ROOT = "private_media/"

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
