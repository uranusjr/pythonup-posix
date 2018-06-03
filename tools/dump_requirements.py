import sys

import pipfile
import requirementslib


def main():
    p = pipfile.load(sys.argv[1])
    try:
        indexes = p.data['_meta']['sources']
    except KeyError:
        indexes = []
    for k, v in p.data['default'].items():
        r = requirementslib.Requirement.from_pipfile(
            name=k, indexes=indexes, pipfile=v,
        )
        print(r.as_line())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: {cmd} Pipfile'.format(cmd=sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    main()
