# ref: https://gist.github.com/josuedjh3/38c521c9091b5c268f2a4d5f3166c497
import logging
import os
import re
# import traceback as tb
# from functools import wraps
from pathlib import Path

def get_env(key: str, default=None) -> str:
    """
    get environmnet variables
    """
    return os.environ.get(key, default)


class FilePermissionError(Exception):
    """The key file permissions are insecure."""
    pass


def load_env(path: Path):
    """
    >>>
    """
    quote_match = re.compile(r'''[^"]*"(.+)"''').match
    match_setting = re.compile(r'^(?P<name>[A-Z][A-Z_0-9]+)\s?=\s?(?P<value>.*)').match
    aliases = {
        'true': True, 'on': True,
        'false': False, 'off': False
    }

    if not path.exists():
        return

    path = path.resolve()

    if path.stat().st_mode != 0o100600:
        raise FilePermissionError(f"Insecure environment file permissions for {path}! Make it 600")

    content = path.read_text()

    for line in content.split('\n'):
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            continue
        match = match_setting(line)

        if not match:
            continue

        name, value = match.groups()
        quoted = quote_match(value)

        if quoted:
            # Convert 'a', "a" to a, a
            value = str(quoted.groups()[0])

        if name in aliases:
            value = aliases[name]

        # Replace placeholders like ${PATH}
        for match_replace in re.findall(r'(\${([\w\d\-_]+)})', value):
            replace, name = match_replace
            value = value.replace(replace, get_env(name, ''))

        # Set environment value
        os.environ[name] = value
