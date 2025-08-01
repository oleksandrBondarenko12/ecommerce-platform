#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # It tells your project where to find main settings (config/settings.py)
    # This is the "brain" of the application.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # It takes the command you give it (e.g. runserver, migrate etc) and
    # passes it to Django's core machinery to execute.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
