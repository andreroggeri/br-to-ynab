import base64
import logging
from typing import List

from pybradesco import Bradesco
from pynubank import Nubank
from ynab_sdk.api.models.responses.accounts import Account

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers.bradesco.bradesco_checking_account import BradescoCheckingAccount
from brbanks2ynab.importers.bradesco.bradesco_credit_card import BradescoCreditCard
from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.nubank.nubank_checking_account import NubankCheckingAccountData
from brbanks2ynab.importers.nubank.nubank_credit_card import NubankCreditCardData
from brbanks2ynab.importers.transaction import Transaction
from brbanks2ynab.util import find_account_by_name

logger = logging.getLogger('brbanks2ynab')


def get_importers_for_bank(bank: str,
                           importer_config: ImporterConfig,
                           ynab_accounts: List[Account]) -> List[DataImporter]:
    importers: List[DataImporter] = []
    if bank == 'Nubank':
        importers.extend(get_nubank_importers(importer_config, ynab_accounts))

    elif bank == 'Bradesco':
        importers.extend(get_bradesco_importers(importer_config, ynab_accounts))

    return importers


def get_bradesco_importers(importer_config, ynab_accounts):
    logger.info('[Bradesco] Fetching data')
    importers = []
    bradesco = Bradesco(preview=True)
    bradesco.prepare(importer_config.bradesco.branch,
                     importer_config.bradesco.account_no,
                     importer_config.bradesco.account_digit)
    token = input('Digite o token > ')
    bradesco.authenticate(importer_config.bradesco.web_password, token)
    if importer_config.bradesco.checking_account:
        logger.info('[Bradesco] Fetching checking account data')
        account = find_account_by_name(ynab_accounts, importer_config.bradesco.checking_account)
        importers.append(BradescoCheckingAccount(bradesco, account.id))
    if importer_config.bradesco.credit_card_account:
        logger.info('[Bradesco] Fetching card data')
        account = find_account_by_name(ynab_accounts, importer_config.bradesco.credit_card_account)
        importers.append(BradescoCreditCard(bradesco, account.id))

    return importers


def get_nubank_importers(importer_config, ynab_accounts):
    logger.info('[Nubank] Fetching data')
    importers = []
    with open('cert.p12', 'wb') as f:
        cert_content = base64.b64decode(importer_config.nubank.cert)
        f.write(cert_content)
    nu = Nubank()
    # TODO: Implementar atualização do refresh token
    nu.authenticate_with_refresh_token(importer_config.nubank.token, './cert.p12')
    if importer_config.nubank.credit_card_account:
        logger.info('[Nubank] Fetching card data')
        account = find_account_by_name(ynab_accounts, importer_config.nubank.credit_card_account)
        importers.append(NubankCreditCardData(nu, account.id))
    if importer_config.nubank.checking_account:
        logger.info('[Nubank] Fetching checking account data')
        account = find_account_by_name(ynab_accounts, importer_config.nubank.checking_account)
        importers.append(NubankCheckingAccountData(nu, account.id))

    return importers
