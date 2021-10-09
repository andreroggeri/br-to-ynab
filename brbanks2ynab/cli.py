from argparse import ArgumentParser

from brbanks2ynab.config.initialize import init_config
from brbanks2ynab.sync import sync


def main():
    parser = ArgumentParser(description='Importador de transações de bancos brasileiros para o YNAB')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--configure', action='store_true')
    group.add_argument('--sync', action='store_true')

    result = parser.parse_args()

    if result.configure:
        init_config()
    elif result.sync:
        sync()


if __name__ == '__main__':
    main()
