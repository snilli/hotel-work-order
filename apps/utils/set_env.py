import os
from pathlib import Path


def set_env():
    if env_path := (Path(__file__).parent.parent / '.env').resolve():
        if not os.path.isfile(env_path):
            return

        env_file = open(env_path, 'r')
        for line in env_file:
            if line.strip():
                key, value = line.split('=')
                os.environ.setdefault(key, value.strip())