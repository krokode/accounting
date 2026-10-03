#!/usr/bin/env python
"""
Sole Enterprise Orchestrator - Automated AI/LLM Setup Wizard
Run: python setup_llm.py
"""
import os
import sys

def main():
    # Ensure Windows console handles UTF-8 strings gracefully
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            try:
                stream.reconfigure(encoding='utf-8', errors='replace')
            except Exception:
                pass

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core_erp.settings')
    try:
        import django
        django.setup()
        from django.core.management import call_command
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    try:
        call_command('configure_llm', *sys.argv[1:])
    except KeyboardInterrupt:
        print("\nSetup wizard exited by user.")
        sys.exit(0)

if __name__ == '__main__':
    main()
