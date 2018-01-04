import functools

import click

from pym import versions

from .common import check_installed


def install(name):
    check_installed(
        name, expect=False,
        on_exit=functools.partial(versions.link_cmd, name),
    )
    try:
        best = versions.find_best(name)
    except versions.VersionNotFoundError:
        click.echo(f'No such version: {name}', err=True)
        click.get_current_context().exit(1)
    versions.install(name, best)
    versions.link_cmd(name)


def uninstall(name):
    check_installed(
        name, expect=True,
        on_exit=functools.partial(versions.unlink_cmd, name),
    )
    click.echo(f'Uninstalling {name}...')
    versions.unlink_cmd(name)
    removed_path = versions.uninstall(name)
    click.echo(f'Removed {name} from {removed_path}')


def upgrade(name):
    check_installed(
        name, expect=False,
        on_exit=functools.partial(versions.link_cmd, name),
    )
    current = versions.get_full_version(name)
    best = versions.find_best(name)
    if current >= best:
        click.echo(f'{name} is up to date ({current} >= {best})')
        return
    click.echo(f'Upgrading {name} from {current} to {best}...')
    versions.install(name, best)
