import dataclasses
import json
import logging
from pathlib import Path

from ynab_sdk import YNAB

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers import get_importers_for_bank
from brbanks2ynab.util import find_budget_by_name
from brbanks2ynab.ynab.ynab_transaction_importer import YNABTransactionImporter

logger = logging.getLogger('brbanks2ynab')


def sync(config: ImporterConfig, dry: bool):
    ynab = YNAB(config.ynab_token)

    budget = find_budget_by_name(ynab.budgets.get_budgets().data.budgets, config.ynab_budget)
    ynab_accounts = ynab.accounts.get_accounts(budget.id).data.accounts

    ynab_importer = YNABTransactionImporter(ynab, budget.id, config.start_import_date)

    for bank in config.banks:
        importers = get_importers_for_bank(bank, config, ynab_accounts)

        for importer in importers:
            ynab_importer.get_transactions_from(importer)

    if dry:
        logger.warning('Dry running! No transactions will be imported into YNAB.')
        logger.info(f'{len(ynab_importer.transactions)} would be imported into YNAB')
        with open('import_result.json', 'w') as f:
            data = [dataclasses.asdict(t) for t in ynab_importer.transactions]
            json.dump(data, f)

    else:
        response = ynab_importer.save()
        logger.info(f'{len(response["data"]["transaction_ids"])} transactions imported')


if __name__ == '__main__':
    sync()
