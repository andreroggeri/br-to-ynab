import logging
from functools import reduce
from typing import List

from ynab_sdk.api.models.responses.accounts import Account
from ynab_sdk.api.models.responses.budget_detail import Budget


def find_budget_by_name(budgets: List[Budget], name) -> Budget:
    def lookup(budget: Budget):
        return budget.name == name

    budget = next(filter(lookup, budgets), None)

    if budget is None:
        logging.error(f'Budget "{name}" not found')
        raise Exception(f'Budget "{name}" not found')

    return budget


def find_account_by_name(accounts: List[Account], name) -> Account:
    def lookup(account: Account):
        return account.name == name

    account = next(filter(lookup, accounts), None)

    if account is None:
        logging.error(f'Account "{name}" not found')
        raise Exception(f'Account "{name}" not found')

    return account


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)