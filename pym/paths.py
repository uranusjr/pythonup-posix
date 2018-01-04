import functools
import pathlib


def ensure_exists(directory=True):
    """Decorator to ensure the returning path exists.
    """
    def wrapper(f):

        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            path = f(*args, **kwargs)
            if not path.exists():
                if directory:
                    path.mkdir(parents=True)
                else:
                    path.parent.mkdir(parents=True)
                    path.touch()
            return path

        return wrapped

    return wrapper


@ensure_exists()
def get_pym_root():
    return pathlib.Path.home().joinpath('.pym')


@ensure_exists()
def get_versions_root():
    return get_pym_root().joinpath('versions')


@ensure_exists()
def get_pym_cmd():
    return get_pym_root().joinpath('cmd')


@ensure_exists()
def get_pym_bin():
    return get_pym_root().joinpath('bin')


def get_python_cmd(name):
    return get_pym_cmd().joinpath(f'python{name}')
