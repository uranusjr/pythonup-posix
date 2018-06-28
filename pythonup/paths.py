import functools
import pathlib


def ensure_exists(*, directory=True):
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
def get_root_dir():
    """Return the root directory, as a :class:`pathlib.Path`.

    This tries to smart-detect the best location to host PythonUp. It tries
    `~/Library`, which likely only exists on Macs; if that does not exist, use
    the Linux standard `~/.local/share` instead.
    """
    macos_library = pathlib.Path.home().joinpath('Library')
    if macos_library.exists():
        return macos_library.joinpath('PythonUp')
    return pathlib.Path.home().joinpath('.local', 'share', 'pythonup')


@ensure_exists()
def get_versions_dir():
    return get_root_dir().joinpath('versions')


@ensure_exists()
def get_cmd_dir():
    return get_root_dir().joinpath('cmd')


@ensure_exists()
def get_bin_dir():
    return get_root_dir().joinpath('bin')
