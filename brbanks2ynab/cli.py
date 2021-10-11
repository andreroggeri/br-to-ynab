import logging
import os
from argparse import ArgumentParser
from pathlib import Path

from brbanks2ynab.config.initialize import init_config
from brbanks2ynab.sync.sync import sync


def _default_config_path():
    return os.path.join(os.getcwd(), 'brbanks2ynab.json')


def main():
    logging.basicConfig()
    logger = logging.getLogger('brbanks2ynab')

    parser = ArgumentParser(description='Importador de transações de bancos brasileiros para o YNAB')
    parser.add_argument('--debug', action='store_true')

    subparsers = parser.add_subparsers(dest='cmd')

    sync_parser = subparsers.add_parser('sync')
    sync_parser.add_argument('--config', default=_default_config_path())
    configure_parser = subparsers.add_parser('configure')

    result = parser.parse_args()

    if result.debug:
        logger.setLevel(logging.DEBUG)

    if result.cmd == 'configure':
        init_config()
    elif result.cmd == 'sync':
        path = Path(result.config)
        sync(path)


if __name__ == '__main__':
    main()
