import sys

import pipfile


def iter_lines(pairs):
    for k, v in pairs:
        if v == '*':
            yield k
        else:
            yield f'{k}{v}'


def main():
    p = pipfile.load(sys.argv[1])
    for line in iter_lines(p.data['default'].items()):
        print(line)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} Pipfile', file=sys.stderr)
        sys.exit(1)
    main()
