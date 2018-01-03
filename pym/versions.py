import re
import shutil
import subprocess

import packaging.version

from . import paths


class VersionNotFoundError(ValueError):
    pass


def iter_buildable_name():
    """Iterate through all definitions available in python-build.
    """
    output = subprocess.check_output(
        ['python-build', '--definitions'], encoding='ascii',
    )
    return iter(output.splitlines())


def iter_installable():
    """Iterate through CPython versions available for PYM to install.
    """
    exist_versions = set()
    for name in iter_buildable_name():
        match = re.match(r'^(\d+\.\d+)\.\d+$', name)
        if not match:
            continue
        version = packaging.version.parse(match.group(1))
        if (isinstance(version, packaging.version.Version) and
                version not in exist_versions):
            exist_versions.add(version)
            yield version


def iter_matched(name):
    """Iterate through CPython versions matching the given name.
    """
    for candidate in iter_buildable_name():
        if candidate.startswith(f'{name}.'):
            version = packaging.version.parse(candidate)
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
        str(paths.get_installation_root(name)),
    ])


def is_installed(name):
    return paths.get_installation_root(name).exists()


def uninstall(name):
    path = paths.get_installation_root(name)
    shutil.rmtree(path)
    return path


def get_full_version(name):
    output = subprocess.check_output(
        [str(paths.get_python(name)), '--version'], encoding='ascii',
    ).strip()
    match = re.match(r'^Python (\d+\.\d+\.\d+)$', output)
    return packaging.version.parse(match.group(1))


def iter_installed():
    for path in paths.get_versions_root().iterdir():
        version = packaging.version.parse(path.name)
        if isinstance(version, packaging.version.Version):
            yield version
