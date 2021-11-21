import json
import logging
from pathlib import Path

from ynab_sdk import YNAB

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers import get_importers_for_bank
from brbanks2ynab.util import find_budget_by_name
from brbanks2ynab.ynab.ynab_transaction_importer import YNABTransactionImporter

logger = logging.getLogger('brbanks2ynab')


def sync(config_file_path: Path, dry: bool):
    if not config_file_path.exists():
        raise Exception(f'Arquivo de configuração "{config_file_path}" não encontrado')

    importer_config = ImporterConfig.from_dict(json.loads(config_file_path.read_text()))

    ynab = YNAB(importer_config.ynab_token)

    budget = find_budget_by_name(ynab.budgets.get_budgets().data.budgets, importer_config.ynab_budget)
    ynab_accounts = ynab.accounts.get_accounts(budget.id).data.accounts

    ynab_importer = YNABTransactionImporter(ynab, budget.id, importer_config.start_import_date)

    for bank in importer_config.banks:
        importers = get_importers_for_bank(bank, importer_config, ynab_accounts)

        for importer in importers:
            ynab_importer.get_transactions_from(importer)

    if dry:
        print(f'{len(ynab_importer.transactions)} would be imported into YNAB')
    else:
        response = ynab_importer.save()
        print(f'{len(response["importers"]["transaction_ids"])} transactions imported')


if __name__ == '__main__':
    sync()
