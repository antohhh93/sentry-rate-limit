import importlib.metadata

try:
    VERSION = importlib.metadata.version("sentry-rate-limit")
except importlib.metadata.PackageNotFoundError:
    VERSION = "unknown"

__version__ = VERSION
