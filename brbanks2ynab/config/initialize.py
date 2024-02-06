import base64
import json
import os
from datetime import datetime

import inquirer

SUPPORTED_BANKS = ['Nubank', 'Itaú']


def validate_nubank_cert(_, path: str):
    return os.path.exists(path)


def validate_date(_, date: str):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def init_config(console=None):
    questions = [
        inquirer.Text('ynab_token', 'Qual o seu token do YNAB ?'),
        inquirer.Text('ynab_budget', 'Qual o nome do orçamento no YNAB ?'),
        inquirer.Checkbox('banks', 'Quais bancos você irá importar os dados', choices=SUPPORTED_BANKS),
        inquirer.Text('start_import_date', 'A partir de qual data deseja importar as transações ? (YYYY-MM-DD)',
                      validate=validate_date),
        # TODO: Fazer no futuro
        # inquirer.Password('encrypt_password', 'Senha para criptografar o arquivo de configuração')
    ]

    answers = inquirer.prompt(questions, console)

    if 'Nubank' in answers['banks']:
        questions = [
            inquirer.Text('nubank_login', 'Qual o seu CPF ? (Somente numeros)'),
            inquirer.Password('nubank_token', message='Qual o seu refresh token ? (Obtido pelo pynubank)'),
            inquirer.Text('nubank_cert', 'Qual o caminho para o seu certificado ? (Obtido pelo pynubank)',
                          validate=validate_nubank_cert),
            inquirer.Text('nubank_credit_card_account',
                          'Qual o nome da conta cadastrada no YNAB para o cartão de crédito'),
            inquirer.Text('nubank_checking_account', 'Qual o nome da conta cadastrada no YNAB para a Nuconta'),
        ]

        nubank_answers = inquirer.prompt(questions, console)

        with open(nubank_answers['nubank_cert'], 'rb') as f:
            nubank_answers['nubank_cert'] = base64.b64encode(f.read()).decode('utf-8')

        answers = {**answers, **nubank_answers}

    if 'Itaú' in answers['banks']:
        questions = [
            inquirer.Text('itau_branch', 'Qual a sua agência ?'),
            inquirer.Text('itau_account_no', 'Qual o número da sua conta corrente ?'),
            inquirer.Text('itau_checking_account_name',
                          'Qual o nome da conta cadastrada no YNAB para a conta corrente'),
            inquirer.Text('itau_credit_card_account_name',
                          'Qual o nome da conta cadastrada no YNAB para o cartão de crédito'),
            inquirer.Password('itau_password', message='Qual a sua senha do internet banking ?'),
        ]

        itau_answers = inquirer.prompt(questions, console)
        answers = {**answers, **itau_answers}

    with open('./brbanks2ynab.json', 'w') as f:
        json.dump(answers, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    init_config()
