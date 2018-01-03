import pathlib


def get_pym_root():
    root = pathlib.Path.home().joinpath('.pym')
    if not root.exists():
        root.mkdir()
    return root


def get_versions_root():
    root = get_pym_root().joinpath('versions')
    if not root.exists():
        root.mkdir()
    return root


def get_installation_root(name):
    return get_versions_root().joinpath(name)


def get_python(name):
    return get_installation_root(name).joinpath('bin', 'python')
