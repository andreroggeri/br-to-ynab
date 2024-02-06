import requests


def send_notification(summary: dict, topic):
    message = f"""
{summary['transaction_count']} new transactions imported into YNAB

{summary['duplicated_count']} transactions were already imported.
    """

    payload = {
        'topic': topic,
        'title': f'💰 {summary["transaction_count"]} new transactions imported into YNAB',
        'message': message,
        'tags': ['cron', 'ynab'],
    }

    requests.post('https://ntfy.sh', json=payload)
