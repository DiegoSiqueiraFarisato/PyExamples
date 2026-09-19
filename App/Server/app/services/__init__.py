"""Every module named *_service in this package is a service.

A service module exposes:
  router            -> fastapi.APIRouter with its endpoints (required)
  register(broker)  -> optional; subscribe handlers to broker topics

Modules are discovered automatically at startup (see app/main.py), so adding a new
service means adding a file here - nothing else to wire up.
"""
