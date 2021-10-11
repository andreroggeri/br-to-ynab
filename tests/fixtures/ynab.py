import pytest
from ynab_sdk.api.models.responses.account import Account


@pytest.fixture
def ynab_account():
    return Account(
        'xxxx-yyyy',
        'AcctName',
        'Some?',
        True,
        False,
        None,
        123,
        124,
        0,
        'abc123',
        False
    )
