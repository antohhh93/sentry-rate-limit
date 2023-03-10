import os
from peewee import *

from ratelimit.utils.types import Bool

env = os.environ.get

SENTRY_URL: str = env("SENTRY_URL") or "" 
BEARER_TOKEN: str = env("SENTRY_BEARER_TOKEN") or ""

SENTRY_API_URL: dict = {
    'organizations': '/api/0/organizations/',
    'organization': '/api/0/organizations/{organization_slug}/',
    'projects': '/api/0/projects/',
    'key': '/api/0/projects/{organization_slug}/{project_slug}/keys/',
    'key_id': '/api/0/projects/{organization_slug}/{project_slug}/keys/{key_id}/',
}

DATABASE = PostgresqlDatabase(
    env("POSTGRES_DB_NAME") or "postgres",
    user = env("POSTGRES_DB_USER") or "postgres",
    password = env("POSTGRES_DB_PASSWORD") or "",
    host = env("POSTGRES_HOST") or "localhost",
    port = env("POSTGRES_PORT") or "5432"
)

DEFAULT_LIMITS: list = [
    {"count": 1, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 300, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 400, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 500, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 600, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 700, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 800, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 900, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 1000, "window": 60, "description": 'Default reserved value', "fixed": False},
    {"count": 1100, "window": 60, "description": 'Default reserved value', "fixed": False},
]

DEFAULT_LIMIT_COUNT: int = int(env("DEFAULT_LIMIT_COUNT") or 300)
DEFAULT_LIMIT_WINDOW: int = int(env("DEFAULT_LIMIT_WINDOW") or 60)

MIN_LIMIT_COUNT: int = int(env("MIN_LIMIT_COUNT") or 60)

LOGGING_LEVEL: str = env("LOGGING_LEVEL") or "info"
LOGGING_ENABLE: bool = Bool(env("LOGGING_ENABLE", True))
LOGGING_FILE_NAME: str = env("LOGGING_FILE_NAME") or ""
