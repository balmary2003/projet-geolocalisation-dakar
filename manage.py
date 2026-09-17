#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

if os.name == 'nt':
    os.environ['PATH'] = r'C:\OSGeo4W\bin' + ';' + os.environ.get('PATH', '')
    os.environ['GDAL_DATA'] = r'C:\OSGeo4W\share\gdal'
    os.environ['PROJ_LIB'] = r'C:\OSGeo4W\share\proj'
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet_Geolocalisation.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
