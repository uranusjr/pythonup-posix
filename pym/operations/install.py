import pathlib

import click

from pym import versions

from .common import check_installed


PYM_ROOT = pathlib.Path


def install(version):
    check_installed(version, expect=False)
    versions.install(version, versions.find_best(version))


def uninstall(version):
    check_installed(version, expect=True)
    click.echo(f'Uninstalling {version}...')
    removed_path = versions.uninstall(version)
    click.echo(f'Removed {version} from {removed_path}')


def upgrade(version):
    check_installed(version, expect=True)
    current = versions.get_full_version(version)
    best = versions.find_best(version)
    if current >= best:
        click.echo(f'{version} is up to date ({current} >= {best})')
        return
    click.echo(f'Upgrading {version} from {current} to {best}...')
    versions.install(version, best)
