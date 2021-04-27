import base64
import json
from typing import TypedDict, List

from pybradesco import Bradesco
from pynubank import Nubank
from ynab_sdk import YNAB
from ynab_sdk.utils.clients.cached_client import CachedClient
from ynab_sdk.utils.configurations.cached import CachedConfig

from br_to_ynab.data.bradesco.bradesco_checking_account import BradescoCheckingAccount
from br_to_ynab.data.bradesco.bradesco_credit_card import BradescoCreditCard
from br_to_ynab.data.nubank.nubank_checking_account import NubankCheckingAccountData
from br_to_ynab.data.nubank.nubank_credit_card import NubankCreditCardData
from br_to_ynab.util import find_budget_by_name, find_account_by_name
from br_to_ynab.ynab.ynab_transaction_importer import YNABTransactionImporter


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


if __name__ == '__main__':
    importer_config: ImporterConfig = json.load(open('br-to-ynab.json'))

    config = CachedConfig('localhost', 6379, api_key=importer_config['ynab_token'])
    client = CachedClient(config)
    ynab = YNAB(client=client)

    budget = find_budget_by_name(ynab.budgets.get_budgets().data.budgets, importer_config['ynab_budget'])
    ynab_accounts = ynab.accounts.get_accounts(budget.id).data.accounts

    ynab_importer = YNABTransactionImporter(ynab, budget.id, importer_config['start_import_date'])

    with open('cert.p12', 'wb') as f:
        cert_content = base64.b64decode(importer_config['nubank_cert'])
        f.write(cert_content)

    if 'Nubank' in importer_config['banks']:
        # nu = Nubank(client=MockHttpClient())
        nu = Nubank()
        nu.authenticate_with_refresh_token(importer_config['nubank_token'], './cert.p12')

        if importer_config['nubank_card_account']:
            account = find_account_by_name(ynab_accounts, importer_config['nubank_card_account'])
            nu_card_data = NubankCreditCardData(nu, account.id)
            ynab_importer.get_transactions_from(nu_card_data)

        if importer_config['nubank_checking_account']:
            account = find_account_by_name(ynab_accounts, importer_config['nubank_checking_account'])
            nu_checking_account = NubankCheckingAccountData(nu, account.id)
            ynab_importer.get_transactions_from(nu_checking_account)

    if 'Bradesco' in importer_config['banks']:
        bradesco = Bradesco()
        bradesco.prepare(importer_config['bradesco_branch'],
                         importer_config['bradesco_account_no'],
                         importer_config['bradesco_account_digit'])
        token = input('Digite o token > ')
        bradesco.authenticate(importer_config['bradesco_web_password'], token)

        if importer_config['bradesco_checking_account']:
            account = find_account_by_name(ynab_accounts, importer_config['bradesco_checking_account'])
            ynab_importer.get_transactions_from(BradescoCheckingAccount(bradesco, account.id))

        if importer_config['bradesco_credit_card_account']:
            account = find_account_by_name(ynab_accounts, importer_config['bradesco_credit_card_account'])
            ynab_importer.get_transactions_from(BradescoCreditCard(bradesco, account.id))

    response = ynab_importer.save()
    print(ynab_importer.transactions)
    print(response)

    # print(f'{len(response["data"]["transaction_ids"])} new transactions imported')
