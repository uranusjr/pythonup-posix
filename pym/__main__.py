import click


class PYMGroup(click.Group):
    """Force command name to show 'pym'.
    """
    def make_context(self, info_name, *args, **kwargs):
        return super().make_context('pym', *args, **kwargs)


@click.group(cls=PYMGroup, invoke_without_command=True)
@click.option('--version', is_flag=True, help='Print version and exit.')
@click.pass_context
def cli(ctx, version):
    if ctx.invoked_subcommand is None:
        if version:
            from . import __version__
            click.echo('PYM (macOS) {}'.format(__version__))
        else:
            click.echo(ctx.get_help(), color=ctx.color)
            ctx.exit(1)


@cli.command(help='Install a Python version.')
@click.argument('version')
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


# @cli.command(help='Set active Python versions.')
# @click.argument('version', nargs=-1)
# @click.option(
#     '--add/--reset', default=None, help='Add version to use without removing.',
# )
# @click.pass_context
# def use(ctx, **kwargs):
#     from .operations.link import use
#     use(ctx, **kwargs)


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


# @cli.command(
#     short_help='Link a command from active versions.',
#     help=('Link a command, or all commands available based on the currently '
#           'used Python version(s).'),
# )
# @click.argument('command', required=False)
# @click.option(
#     '--all', 'link_all', is_flag=True,
#     help='Link all available operations.',
# )
# @click.option(
#     '--overwrite',
#     type=click.Choice(['yes', 'no', 'smart']), default='yes',
#     help='What to do when the target exists.',
# )
# @click.pass_context
# def link(ctx, overwrite, **kwargs):
#     from .operations.link import link, Overwrite
#     link(ctx, overwrite=Overwrite[overwrite], **kwargs)


if __name__ == '__main__':
    cli()
