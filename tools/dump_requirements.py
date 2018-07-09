import sys

import requirementslib


def main():
    p = requirementslib.Pipfile.load(sys.argv[1])
    for s in p.sections:
        if s.name != 'packages':
            continue
        for r in s.requirements:
            print(r.as_line())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: {cmd} Pipfile'.format(cmd=sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    main()
