import os
from pathlib import Path

from analyze_sessions import analyze_sessions


def main():
    filepath = os.path.join(os.path.dirname(__file__), '..', 'files', 'cdr.csv')

    path = Path(filepath)
    if not path.exists():
        print(f'Arquivo nao encontrado: {filepath}')
        exit(1)

    analyze_sessions(str(path))


if __name__ == '__main__':
    main()
