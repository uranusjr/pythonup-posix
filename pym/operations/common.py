import click

from pym.versions import is_installed


def check_installed(name, *, expect=True, on_exit=None):
    if is_installed(name) == expect:
        return
    if expect:
        message = f'{name} is not installed'
    else:
        message = f'{name} is already installed'
    click.echo(message, err=True)
    if on_exit:
        on_exit()
    click.get_current_context().exit(1)
