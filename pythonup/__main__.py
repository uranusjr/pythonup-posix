import click


class PythonUpGroup(click.Group):
    """Force command name to show 'pythonup'.
    """
    def make_context(self, info_name, *args, **kwargs):
        return super().make_context('pythonup', *args, **kwargs)


@click.group(cls=PythonUpGroup, invoke_without_command=True)
@click.option('--version', is_flag=True, help='Print version and exit.')
@click.pass_context
def cli(ctx, version):
    if ctx.invoked_subcommand is None:
        if version:
            from . import __version__
            click.echo('PythonUp (macOS) {}'.format(__version__))
        else:
            click.echo(ctx.get_help(), color=ctx.color)
            ctx.exit(1)


@cli.command(help='Install a Python version.')
@click.argument('version')
@click.option('--use', is_flag=True, help='Use version after installation.')
def install(**kwargs):
    from .operations.install import install
    install(**kwargs)


@cli.command(help='Uninstall a Python version.')
@click.argument('version')
def uninstall(**kwargs):
    from .operations.install import uninstall
    uninstall(**kwargs)


@cli.command(help='Upgrade an installed Python version.')
@click.argument('version')
def upgrade(**kwargs):
    from .operations.install import upgrade
    upgrade(**kwargs)


@cli.command(help='Set active Python versions.')
@click.argument('version', nargs=-1)
@click.option(
    '--add/--reset', default=None, help='Add version to use without removing.',
)
def use(**kwargs):
    from .operations.use import use
    use(**kwargs)


@cli.command(
    help='Prints where the executable of Python version is.',
    short_help='Print python.exe location.',
)
@click.argument('version')
def where(**kwargs):
    from .operations.versions import where
    where(**kwargs)


@cli.command(name='list', help='List Python versions.')
@click.option(
    '--all', 'list_all', is_flag=True,
    help='List all versions (instead of only installed ones).',
)
def list_(**kwargs):
    from .operations.versions import list_
    list_(**kwargs)


if __name__ == '__main__':
    cli()
