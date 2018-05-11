import dataclasses
import pathlib
import re
import subprocess

from . import paths


class InstallationNotFoundError(ValueError, FileNotFoundError):
    pass


@dataclasses.dataclass
class Installation:

    root: pathlib.Path

    @classmethod
    def find(cls, version, *, strict=True):
        path = paths.get_versions_dir().joinpath(version.name)
        try:
            path = path.resolve(strict=strict)
        except FileNotFoundError:
            raise InstallationNotFoundError(version)
        return cls(root=path)

    @property
    def python(self):
        return self.root.joinpath('bin', 'python')

    @property
    def pip(self):
        return self.root.joinpath('bin', 'pip')

    def get_build_name(self):
        process = subprocess.run(
            [str(self.python), '--version'], encoding='ascii',
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        # Newer versions use stdout, but older (mainly 2.7) use stderr.
        output = process.stdout.strip() or process.stderr.strip()
        match = re.match(r'^Python (\d+\.\d+\.\d+)$', output)
        return match.group(1)
