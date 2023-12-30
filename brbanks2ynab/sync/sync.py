import dataclasses
import json
import logging
from typing import Optional

from ynab_sdk import YNAB
from ynab_sdk.api.models.responses.transactions import CreateTransactionResponse

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers import get_importers_for_bank
from brbanks2ynab.util import find_budget_by_name
from brbanks2ynab.utils.notification import send_notification
from brbanks2ynab.ynab.ynab_transaction_importer import YNABTransactionImporter

logger = logging.getLogger('brbanks2ynab')
logger.setLevel(logging.DEBUG)


def _build_summary(response: CreateTransactionResponse) -> dict:
    return {
        'transaction_count': len(response.transaction_ids),
        'duplicated_count': len(response.duplicate_import_ids),
        'total_amount': sum(t.amount for t in response.transactions) / 1000,
    }


def sync(config: ImporterConfig, dry: bool, ntfy_topic: Optional[str] = None):
    ynab = YNAB(config.ynab_token)
    
    budget = find_budget_by_name(ynab.budgets.get_budgets().data.budgets, config.ynab_budget)
    ynab_accounts = ynab.accounts.get_accounts(budget.id).data.accounts
    
    ynab_importer = YNABTransactionImporter(ynab, budget.id, config.start_import_date)
    
    for bank in config.banks:
        importers = get_importers_for_bank(bank, config, ynab_accounts)
        
        for importer in importers:
            ynab_importer.get_transactions_from(importer)
    
    if dry:
        logger.info('Dry running! No transactions will be imported into YNAB.')
        logger.info(f'{len(ynab_importer.transactions)} would be imported into YNAB')
        
        with open('import_result.json', 'w') as f:
            data = [dataclasses.asdict(t) for t in ynab_importer.transactions]
            json.dump(data, f)
    else:
        response = ynab_importer.save()
        logger.debug(f'YNAB response: \n {json.dumps(dataclasses.asdict(response), indent=2)}')
        
        summary = _build_summary(response)
        
        logger.info(f"""
        {summary['transaction_count']} new transactions imported into YNAB
        {summary['duplicated_count']} transactions were already imported.
        """)
        if ntfy_topic:
            send_notification(summary, ntfy_topic)


if __name__ == '__main__':
    sync()
