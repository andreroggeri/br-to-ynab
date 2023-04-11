import base64
import json
import logging
import os
from argparse import ArgumentParser
from pathlib import Path

from brbanks2ynab.config.config import ImporterConfig
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
    sync_parser.add_argument('--config-file')
    sync_parser.add_argument('--config')
    sync_parser.add_argument('--dry', action='store_true', default=False)
    configure_parser = subparsers.add_parser('configure')

    result = parser.parse_args()

    if result.debug:
        logger.setLevel(logging.DEBUG)

    if result.cmd == 'configure':
        init_config()
    elif result.cmd == 'sync':
        if result.config_file and result.config or not result.config_file and not result.config:
            raise Exception('É necessário informar um arquivo de configuração ou uma string de configuração')

        if result.config_file:
            path = Path(result.config_file)
            if not path.exists():
                raise Exception(f'Arquivo de configuração "{path}" não encontrado')

            config = ImporterConfig.from_dict(json.loads(path.read_text()))
        else:
            config = ImporterConfig.from_dict(json.loads(base64.b64decode(result.config)))

        sync(config, result.dry)


if __name__ == '__main__':
    main()
