import base64
import json
import logging
from typing import TypedDict, List

from pybradesco import Bradesco
from pynubank import Nubank
from ynab_sdk import YNAB

from brbanks2ynab.importers.bradesco.bradesco_checking_account import BradescoCheckingAccount
from brbanks2ynab.importers.bradesco.bradesco_credit_card import BradescoCreditCard
from brbanks2ynab.importers.nubank.nubank_checking_account import NubankCheckingAccountData
from brbanks2ynab.importers.nubank.nubank_credit_card import NubankCreditCardData
from brbanks2ynab.util import find_budget_by_name, find_account_by_name
from brbanks2ynab.ynab.ynab_transaction_importer import YNABTransactionImporter


class ImporterConfig(TypedDict):
    ynab_token: str
    ynab_budget: str
    banks: List[str]
    start_import_date: str
    # Nubank
    nubank_login: str
    nubank_token: str
    nubank_cert: str
    nubank_card_account: str
    nubank_checking_account: str
    # Bradesco
    bradesco_branch: str
    bradesco_account_no: str
    bradesco_account_digit: str
    bradesco_web_password: str
    bradesco_credit_card_account: str
    bradesco_checking_account: str


def sync():
    logging.basicConfig()
    logger = logging.getLogger('brbanks2ynab')
    logger.setLevel(logging.DEBUG)

    importer_config: ImporterConfig = json.load(open('br_to_ynab.json'))

    ynab = YNAB(importer_config['ynab_token'])

    budget = find_budget_by_name(ynab.budgets.get_budgets().data.budgets, importer_config['ynab_budget'])
    ynab_accounts = ynab.accounts.get_accounts(budget.id).data.accounts

    ynab_importer = YNABTransactionImporter(ynab, budget.id, importer_config['start_import_date'])

    with open('cert.p12', 'wb') as f:
        cert_content = base64.b64decode(importer_config['nubank_cert'])
        f.write(cert_content)

    if 'Nubank' in importer_config['banks']:
        logger.info('[Nubank] Fetching data')
        # nu = Nubank(client=MockHttpClient())
        nu = Nubank()
        new_token = nu.authenticate_with_refresh_token(importer_config['nubank_token'], './cert.p12')

        importer_config['nubank_token'] = new_token

        if importer_config['nubank_card_account']:
            logger.info('[Nubank] Fetching card data')
            account = find_account_by_name(ynab_accounts, importer_config['nubank_card_account'])
            nu_card_data = NubankCreditCardData(nu, account.id)
            ynab_importer.get_transactions_from(nu_card_data)

        if importer_config['nubank_checking_account']:
            logger.info('[Nubank] Fetching checking account data')
            account = find_account_by_name(ynab_accounts, importer_config['nubank_checking_account'])
            nu_checking_account = NubankCheckingAccountData(nu, account.id)
            ynab_importer.get_transactions_from(nu_checking_account)

    if 'Bradesco' in importer_config['banks']:
        logger.info('[Bradesco] Fetching data')
        bradesco = Bradesco(preview=True)
        bradesco.prepare(importer_config['bradesco_branch'],
                         importer_config['bradesco_account_no'],
                         importer_config['bradesco_account_digit'])
        token = input('Digite o token > ')
        bradesco.authenticate(importer_config['bradesco_web_password'], token)

        if importer_config['bradesco_checking_account']:
            logger.info('[Bradesco] Fetching checking account data')
            account = find_account_by_name(ynab_accounts, importer_config['bradesco_checking_account'])
            ynab_importer.get_transactions_from(BradescoCheckingAccount(bradesco, account.id))

        if importer_config['bradesco_credit_card_account']:
            logger.info('[Bradesco] Fetching card data')
            account = find_account_by_name(ynab_accounts, importer_config['bradesco_credit_card_account'])
            ynab_importer.get_transactions_from(BradescoCreditCard(bradesco, account.id))

    response = ynab_importer.save()
    print(ynab_importer.transactions)
    print(response)

    with open('br_to_ynab.json', 'w') as f:
        json.dump(importer_config, f)
    # print(f'{len(response["importers"]["transaction_ids"])} new transactions imported')


if __name__ == '__main__':
    sync()
