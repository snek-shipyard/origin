from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.core import hooks


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    # Add /static/css/custom.css to admin.
    return format_html('<link rel="stylesheet" href="{}">', static("core/custom.css"))


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    # Add /static/css/custom.css to admin.
    return format_html('<script src="{}"></script>', static("core/custom.js"))


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
