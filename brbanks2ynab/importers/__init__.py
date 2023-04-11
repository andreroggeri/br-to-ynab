import base64
import logging
from typing import List

from pybradesco import Bradesco
from pyitau import Itau
from pynubank import Nubank
from python_alelo.alelo import Alelo
from ynab_sdk.api.models.responses.accounts import Account

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers.alelo.alelo_alimentacao_card import AleloAlimentacaoImporter
from brbanks2ynab.importers.alelo.alelo_flex_card import AleloFlexImporter
from brbanks2ynab.importers.alelo.alelo_refeicao_card import AleloRefeicaoImporter
from brbanks2ynab.importers.bradesco.bradesco_checking_account import BradescoCheckingAccount
from brbanks2ynab.importers.bradesco.bradesco_credit_card import BradescoCreditCard
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
    elif bank == 'Bradesco':
        return get_bradesco_importers(importer_config, ynab_accounts)
    elif bank == 'Alelo':
        return get_alelo_importers(importer_config, ynab_accounts)
    elif bank == 'Itaú':
        return get_itau_importers(importer_config, ynab_accounts)


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
        account = find_account_by_name(ynab_accounts, importer_config.nubank.checking_account)
        importers.append(NubankCheckingAccountData(nu, account.id))

    return importers


def get_alelo_importers(importer_config, ynab_accounts):
    logger.info('[Alelo] Fetching data')
    importers = []

    alelo = Alelo(importer_config.alelo.login, importer_config.alelo.password)
    alelo.login()

    if importer_config.alelo.flex_account:
        logger.info('[Alelo] Fetching flex card data')
        account = find_account_by_name(ynab_accounts, importer_config.alelo.flex_account)
        importers.append(AleloFlexImporter(alelo, account.id))

    if importer_config.alelo.alimentacao_account:
        logger.info('[Alelo] Fetching alimentação card data')
        account = find_account_by_name(ynab_accounts, importer_config.alelo.alimentacao_account)
        importers.append(AleloAlimentacaoImporter(alelo, account.id))

    if importer_config.alelo.refeicao_account:
        logger.info('[Alelo] Fetching refeição card data')
        account = find_account_by_name(ynab_accounts, importer_config.alelo.refeicao_account)
        importers.append(AleloRefeicaoImporter(alelo, account.id))

    return importers


def get_itau_importers(importer_config: ImporterConfig, ynab_accounts):
    logger.info('[Itaú] Fetching data')
    importers = []

    itau = Itau()
    itau.login(importer_config.itau.branch, importer_config.itau.account_no, importer_config.itau.password)
    credit_card_account_id = find_account_by_name(ynab_accounts, importer_config.itau.credit_card_account_name)
    checking_account_id = find_account_by_name(ynab_accounts, importer_config.itau.checking_account_name)
    importers.append(ItauCheckingAccount(itau, checking_account_id.id))
    importers.append(ItauCreditCard(itau, credit_card_account_id.id))

    return importers
