#!/usr/bin/python3

import os
import sys

python_version = sys.version_info[:2]

if python_version < (3, 9):
    sys.exit(f"Error: Sentry Rate Limit requires at least Python 3.9 ({python_version})")

from setuptools import find_packages, setup

ROOT = os.path.dirname(os.path.abspath(__file__))

VERSION = "0.0.2"

def get_requirements():
    with open(f"requirements.txt") as fp:
        return [x.strip() for x in fp.read().split("\n") if not x.startswith("#")]

setup(
    name = "sentry_rate_limit",
    version = VERSION,
    author = "Anton Turko",
    author_email = "anton_turko@mail.ru",
    url = "https://github.com/antohhh93/sentry-rate-limit",
    description = "Rate limiter for the sentry.",
    long_description = open(os.path.join(ROOT, "README.md")).read(),
    long_description_content_type = "text/markdown",
    packages = find_packages(),
    zip_safe = False,
    install_requires = get_requirements(),
    entry_points={
        "console_scripts": [
            "sentry-rate-limit = ratelimit.cli:main"
        ],
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
    ],
)
