import click

from pym import paths

from .common import check_installed


def where(version):
    check_installed(version, expect=True)
    click.echo(str(paths.get_python(version)))
