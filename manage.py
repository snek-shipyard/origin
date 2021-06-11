"""Django's command-line utility for administrative tasks."""
import os
import sys


# run!
def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "esite.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
