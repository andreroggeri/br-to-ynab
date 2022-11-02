from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AleloConfig:
    login: str
    password: str
    flex_account: str
    refeicao_account: str
    alimentacao_account: str

    @staticmethod
    def from_dict(data: dict) -> 'AleloConfig':
        return AleloConfig(
            data['alelo_login'],
            data['alelo_password'],
            data['alelo_flex_account'],
            data['alelo_refeicao_account'],
            data['alelo_alimentacao_account'],
        )


@dataclass
class NubankConfig:
    login: str
    token: str
    cert: str
    credit_card_account: str
    checking_account: str

    @staticmethod
    def from_dict(data: dict) -> 'NubankConfig':
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
class ItauConfig:
    branch: str
    account_no: str
    password: str
    checking_account_name: str
    credit_card_account_name: str

    @staticmethod
    def from_json(data: dict) -> 'ItauConfig':
        return ItauConfig(
            data['itau_branch'],
            data['itau_account_no'],
            data['itau_password'],
            data['itau_checking_account_name'],
            data['itau_credit_card_account_name'],
        )


@dataclass
class ImporterConfig:
    ynab_token: str
    ynab_budget: str
    banks: List[str]
    start_import_date: str
    bradesco: Optional[BradescoConfig]
    nubank: Optional[NubankConfig]
    alelo: Optional[AleloConfig]
    itau: Optional[ItauConfig]

    @staticmethod
    def from_dict(json_data: dict) -> 'ImporterConfig':
        bradesco_config = BradescoConfig.from_json(json_data) if json_data.get('bradesco_branch') else None
        nubank_config = NubankConfig.from_dict(json_data) if json_data.get('nubank_login') else None
        alelo_config = AleloConfig.from_dict(json_data) if json_data.get('alelo_login') else None
        itau_config = ItauConfig.from_json(json_data) if json_data.get('itau_branch') else None

        return ImporterConfig(
            json_data['ynab_token'],
            json_data['ynab_budget'],
            json_data['banks'],
            json_data['start_import_date'],
            bradesco_config,
            nubank_config,
            alelo_config,
            itau_config
        )
