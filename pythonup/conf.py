import contextlib
import json

from . import paths


def safe_load(f):
    try:
        return json.load(f)
    except json.JSONDecodeError:
        return {}


class Settings:

    @property
    def config(self):
        path = paths.get_root_dir().joinpath('config')
        if not path.exists():
            path.touch(mode=0o644, exist_ok=True)
        return path

    def __getitem__(self, key):
        with self.config.open() as f:
            return safe_load(f)[key]

    def __setitem__(self, key, value):
        with contextlib.ExitStack() as stack:
            try:
                f = stack.enter_context(self.config.open('w+'))
            except FileNotFoundError:
                data = {}
            else:
                data = safe_load(f)
            data[key] = value
            json.dump(data, f, indent=4)

    def get(self, key, default=None):
        with self.config.open() as f:
            return safe_load(f).get(key, default)


settings = Settings()
