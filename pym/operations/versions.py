import click

from pym import paths, versions

from .common import check_installed


def where(version):
    check_installed(version, expect=True)
    click.echo(str(paths.get_python(version)))


def list_(list_all):
    if list_all:
        vers = sorted(versions.iter_installable())
    else:
        vers = sorted(versions.iter_installed())
    for v in vers:
        marker = ' '
        name = v.base_version
        # if name in active_names:
        #     marker = '*'
        if versions.is_installed(name):
            marker = 'o'
        click.echo(f'{marker} {name}')

    if not list_all and not vers:
        click.echo(
            'No installed versions. Use --all to list all available versions '
            'for installation.',
            err=True,
        )
