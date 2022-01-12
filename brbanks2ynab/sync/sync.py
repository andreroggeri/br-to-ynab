import asyncio
import json
import logging
from pathlib import Path

from actualbudget.actualbudget import ActualBudget

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers import get_importers_for_bank
from brbanks2ynab.ynab.ynab_transaction_importer import YNABTransactionImporter

logger = logging.getLogger('brbanks2ynab')


async def sync(config_file_path: Path, dry: bool):
    if not config_file_path.exists():
        raise Exception(f'Arquivo de configuração "{config_file_path}" não encontrado')

    importer_config = ImporterConfig.from_dict(json.loads(config_file_path.read_text()))

    actual = ActualBudget()
    await actual.connect()

    actual_accounts = await actual.get_accounts()

    actual_importer = YNABTransactionImporter(actual, importer_config.start_import_date)

    for bank in importer_config.banks:
        importers = await get_importers_for_bank(bank, importer_config, actual_accounts)

        for importer in importers:
            await actual_importer.get_transactions_from(importer)

    if dry:
        print(f'{len(actual_importer.transactions)} would be imported into YNAB')
    else:
        await actual_importer.save()
        print(f'transactions imported')


if __name__ == '__main__':
    asyncio.run(
        sync(
            Path('/Users/andrerc/Projects/personal/brbanks2ynab/brbanks2ynab.json'),
            False
        )
    )
