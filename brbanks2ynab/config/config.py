from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NubankConfig:
    login: str
    token: str
    cert: str
    credit_card_account: str
    checking_account: str

    @staticmethod
    def from_json(data: dict) -> 'NubankConfig':
        return NubankConfig(
            data['nubank_login'],
            data['nubank_token'],
            data['nubank_cert'],
            data['nubank_credit_card_account'],
            data['nubank_checking_account'],
        )


@dataclass
class BradescoConfig:
    branch: str
    account_no: str
    account_digit: str
    web_password: str
    credit_card_account: str
    checking_account: str

    @staticmethod
    def from_json(data: dict) -> 'BradescoConfig':
        return BradescoConfig(
            data['bradesco_branch'],
            data['bradesco_account_no'],
            data['bradesco_account_digit'],
            data['bradesco_web_password'],
            data['bradesco_credit_card_account'],
            data['bradesco_checking_account'],
        )


@dataclass
class ImporterConfig:
    ynab_token: str
    ynab_budget: str
    banks: List[str]
    start_import_date: str
    bradesco: Optional[BradescoConfig]
    nubank: Optional[NubankConfig]

    @staticmethod
    def from_json(json_data: dict) -> 'ImporterConfig':
        bradesco_config = BradescoConfig.from_json(json_data) if json_data.get('bradesco_branch') else None
        nubank_config = NubankConfig.from_json(json_data) if json_data.get('nubank_login') else None
        return ImporterConfig(
            json_data['ynab_token'],
            json_data['ynab_budget'],
            json_data['banks'],
            json_data['start_import_date'],
            bradesco_config,
            nubank_config,
        )
