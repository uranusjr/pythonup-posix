import re
import shutil
import subprocess

import packaging.version

from .paths import get_installation_root, get_python


class VersionNotFoundError(ValueError):
    pass


def iter_matched(name):
    output = subprocess.check_output(
        ['python-build', '--definitions'], encoding='ascii',
    )
    for line in output.splitlines():
        if line.startswith(f'{name}.'):
            version = packaging.version.parse(line.strip())
            if isinstance(version, packaging.version.Version):
                yield version


def find_best(name):
    try:
        version = max(iter_matched(name))
    except ValueError:
        raise VersionNotFoundError(name)
    return version


def install(name, version):
    subprocess.check_call([
        'python-build',
        version.base_version,
        str(get_installation_root(name)),
    ])


def is_installed(name):
    return get_installation_root(name).exists()


def uninstall(name):
    path = get_installation_root(name)
    shutil.rmtree(path)
    return path


def get_full_version(name):
    output = subprocess.check_output(
        [str(get_python(name)), '--version'], encoding='ascii',
    ).strip()
    match = re.match(r'^Python (\d+\.\d+\.\d+)$', output)
    return packaging.version.parse(match.group(1))
