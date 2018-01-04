def safe_link(source, target):
    if target.exists():
        if source.samefile(target):
            return False
        target.unlink()
    target.symlink_to(source)
    return True


def safe_unlink(target):
    if target.exists():
        target.unlink()


def link_commands(version):
    installation = version.find_installation()
    for target in version.python_commands:
        safe_link(installation.python, target)
    for target in version.pip_commands:
        safe_link(installation.pip, target)


def unlink_commands(version):
    for target in version.python_commands:
        safe_unlink(target)
    for target in version.pip_commands:
        safe_unlink(target)
