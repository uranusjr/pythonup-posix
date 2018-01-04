import click

from pym import installations, versions

from .common import check_installation, version_command


@version_command()
def where(version):
    installation = check_installation(version, expect=True)
    click.echo(str(installation.python))


def list_(list_all):
    outputed = False
    for version in sorted(versions.iter_versions()):
        try:
            installation = version.find_installation()
        except installations.InstallationNotFoundError:
            installation = None
        # if name in active_names:
        #     marker = '*'
        if installation:
            marker = 'o'
            outputed = True
        else:
            if not list_all:
                continue
            marker = ' '
        click.echo(f'{marker} {version}')

    if not list_all and not outputed:
        click.echo(
            'No installed versions. Use --all to list all available versions '
            'for installation.',
            err=True,
        )
