import pynubank

from brbanks2ynab.config.config import ImporterConfig
from brbanks2ynab.importers import get_importers_for_bank, NubankCreditCardData, NubankCheckingAccountData


def test_should_get_only_nubank_card_importer(monkeypatch, config_for_nubank, ynab_account):
    monkeypatch.setattr('pynubank.nubank.HttpClient', pynubank.MockHttpClient)
    config = ImporterConfig.from_dict(config_for_nubank)
    config.nubank.checking_account = None
    ynab_account.name = config.nubank.credit_card_account
    accounts = [ynab_account]

    importers = get_importers_for_bank('Nubank', config, accounts)

    assert len(importers) == 1
    assert isinstance(importers[0], NubankCreditCardData)


def test_should_get_only_nubank_checking_account_importer(monkeypatch, config_for_nubank, ynab_account):
    monkeypatch.setattr('pynubank.nubank.HttpClient', pynubank.MockHttpClient)
    config = ImporterConfig.from_dict(config_for_nubank)
    config.nubank.credit_card_account = None
    ynab_account.name = config.nubank.checking_account
    accounts = [ynab_account]

    importers = get_importers_for_bank('Nubank', config, accounts)

    assert len(importers) == 1
    assert isinstance(importers[0], NubankCheckingAccountData)
