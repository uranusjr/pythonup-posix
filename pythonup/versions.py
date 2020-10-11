import dataclasses
import os
import re
import shutil
import subprocess
import sys

import packaging.version

from . import installations, paths


class VersionNotFoundError(ValueError):
    pass


def iter_installable_matches():
    """Iterate through CPython versions available for PythonUp to install.
    """
    output = subprocess.check_output(
        ['python-build', '--definitions'], encoding='ascii',
    )
    for name in output.splitlines():
        match = re.match(r'^(\d+\.\d+)\.\d+$', name)
        if match:
            yield match


@dataclasses.dataclass(order=True, frozen=True)
class Version:

    major: int
    minor: int

    @classmethod
    def parse(cls, name):
        match = re.match(r'^(?P<major>\d+)\.(?P<minor>\d+)$', name)
        if not match:
            raise VersionNotFoundError(name)
        return cls(
            major=int(match.group('major')),
            minor=int(match.group('minor')),
        )

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f'{self.major}.{self.minor}'

    @property
    def python_commands(self):
        return [paths.get_cmd_dir().joinpath(f'python{self.name}')]

    @property
    def pip_commands(self):
        return [paths.get_cmd_dir().joinpath(f'pip{self.name}')]

    def iter_matched_build_name(self):
        """Iterate through CPython version names matching this version.
        """
        for match in iter_installable_matches():
            if match.group(1) == self.name:
                yield match.group(0)

    def find_best_build_name(self):
        return max(
            self.iter_matched_build_name(),
            key=packaging.version.Version,
        )

    def install(self, *, build_name=None):
        if build_name is None:
            build_name = self.find_best_build_name()
        installation = self.find_installation(strict=False)
        env = os.environ.copy()
        if sys.platform == 'darwin':
            opts = env.get('PYTHON_CONFIGURE_OPTS', '').split()
            opts.append('--enable-framework')
            env['PYTHON_CONFIGURE_OPTS'] = ' '.join(opts)
        subprocess.check_call(
            ['python-build', build_name, str(installation.root)],
            env=env,
        )
        return installation

    def uninstall(self):
        root = self.find_installation().root
        shutil.rmtree(root)
        return root

    def find_installation(self, *, strict=True):
        return installations.Installation.find(self, strict=strict)


def iter_versions():
    exist_names = set()
    for match in iter_installable_matches():
        name = match.group(1)
        if name not in exist_names:
            exist_names.add(name)
            yield Version.parse(name)
