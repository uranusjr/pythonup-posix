import functools

import click

from .. import installations, versions


def check_installation(version, *, expect=True, on_exit=None):
    try:
        installation = version.find_installation()
    except installations.InstallationNotFoundError:
        if not expect:
            return None
        message = f'{version} is not installed'
    else:
        if expect:
            return installation
        message = f'{version} is already installed'
    click.echo(message, err=True)
    if on_exit:
        on_exit()
    click.get_current_context().exit(1)


def parse_version(name):
    try:
        return versions.Version.parse(name)
    except versions.VersionNotFoundError:
        click.echo('No such version: {}'.format(name), err=True)
        click.get_current_context().exit(1)


def version_command(*, plural=False):
    """Decorator to convert version name arguments to actual version instances.
    """
    def decorator(f):

        @functools.wraps(f)
        def wrapped(*args, version, **kwargs):
            if plural:
                kwargs['versions'] = [parse_version(n) for n in version]
            else:
                kwargs['version'] = parse_version(version)
            return f(*args, **kwargs)

        return wrapped

    return decorator
