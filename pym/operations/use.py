import click

from pym.conf import settings
from pym.versions import Version

from .common import check_installation, version_command
from .link import use_versions


@version_command(plural=True)
def use(versions, add):
    used_names = settings.get('using', [])
    if add is None and not versions:
        # Bare "use": Display active versions.
        names = used_names
        if names:
            click.echo(' '.join(names))
        else:
            click.echo('Not using any versions', err=True)
        return

    # Remove duplicate inputs (keep first apperance).
    versions = list(dict((v.name, v) for v in versions).values())

    for version in versions:
        check_installation(version)

    # Add new versions to the back of existing versions.
    used_versions = [Version.parse(name) for name in used_names]
    if add:
        new_versions = []
        for v in versions:
            if v in used_versions:
                click.echo('Already using {}'.format(v), err=True)
            else:
                new_versions.append(v)
        versions = used_versions + new_versions

    if used_versions == versions:
        click.echo('No version changes', err=True)
        return
    if versions:
        click.echo('Using: {}'.format(', '.join(v.name for v in versions)))
    elif not add:
        click.echo('Not using any versions')
    else:
        click.echo('No active versions', err=True)
        click.get_current_context().exit(1)

    use_versions(versions)
