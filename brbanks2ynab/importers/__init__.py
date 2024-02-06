import base64
import logging
from typing import List

from pyitau import Itau
from pynubank import Nubank
from ynab_sdk.api.models.responses.accounts import Account

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.itau.itau_checking_account import ItauCheckingAccount
from brbanks2ynab.importers.itau.itau_credit_card import ItauCreditCard
from brbanks2ynab.importers.nubank.nubank_checking_account import NubankCheckingAccountData
from brbanks2ynab.importers.nubank.nubank_credit_card import NubankCreditCardData
from brbanks2ynab.importers.transaction import Transaction
from brbanks2ynab.util import find_account_by_name

logger = logging.getLogger('brbanks2ynab')


def get_importers_for_bank(bank: str,
                           importer_config: ImporterConfig,
                           ynab_accounts: List[Account]) -> List[DataImporter]:
    if bank == 'Nubank':
        return get_nubank_importers(importer_config, ynab_accounts)
    elif bank == 'Itaú':
        return get_itau_importers(importer_config, ynab_accounts)


def get_nubank_importers(importer_config, ynab_accounts):
    logger.info('[Nubank] Fetching data')
    importers = []
    cert_content = base64.b64decode(importer_config.nubank.cert)
    nu = Nubank()
    # TODO: Implementar atualização do refresh token
    nu.authenticate_with_refresh_token(importer_config.nubank.token, cert_data=cert_content)
    if importer_config.nubank.credit_card_account:
        logger.info('[Nubank] Fetching card data')
        account = find_account_by_name(ynab_accounts, importer_config.nubank.credit_card_account)
        importers.append(NubankCreditCardData(nu, account.id))
    if importer_config.nubank.checking_account:
        logger.info('[Nubank] Fetching checking account data')
        logger.warn('[Nubank] Checking account data is currently disabled')
        # account = find_account_by_name(ynab_accounts, importer_config.nubank.checking_account)
        # importers.append(NubankCheckingAccountData(nu, account.id))

    return importers


def get_itau_importers(importer_config: ImporterConfig, ynab_accounts):
    logger.info('[Itaú] Fetching data')
    importers = []

    account_no = importer_config.itau.account_no[:-1]
    account_digit = importer_config.itau.account_no[-1]
    itau = Itau(importer_config.itau.branch, account_no, account_digit, importer_config.itau.password)
    logger.info('[Itaú] Authenticating')
    itau.authenticate()
    logger.info('[Itaú] Authenticated')
    # itau.login(importer_config.itau.branch, importer_config.itau.account_no, importer_config.itau.password)
    # credit_card_account_id = find_account_by_name(ynab_accounts, importer_config.itau.credit_card_account_name)
    checking_account_id = find_account_by_name(ynab_accounts, importer_config.itau.checking_account_name)
    importers.append(ItauCheckingAccount(itau, checking_account_id.id))
    # importers.append(ItauCreditCard(itau, credit_card_account_id.id))

    return importers
