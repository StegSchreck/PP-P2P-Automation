import datetime
import logging
import os
import time

EXPORTS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "exports"))
TIMESTAMP = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
CSV_HEADER = 'Datum,Wert,Buchungswährung,Typ,Notiz\n'


def wait_for_file_to_exist(filepath: str, seconds: int = 30):
    iteration = 0
    while iteration < seconds:
        iteration += 1
        try:
            with open(filepath, "rb") as file:
                return file
        except IOError:
            time.sleep(1)  # try every second
            continue
    raise IOError(f"Could not access {filepath} after {seconds} seconds")


def save_loan_transactions_to_csv(loan_transactions, folder, filename=TIMESTAMP + '_auxmoney.csv'):
    logging.info(
        '===== saving loan transactions to CSV\r\n'
        f'      folder: {folder}\r\n'
        f'      filename: {filename}\r\n'
        f'      number of entries: {len(loan_transactions)}\r\n'
    )
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder, filename), 'w+', encoding='UTF-8') as output_file:
        output_file.write(CSV_HEADER)
        for transaction in loan_transactions:
            output_file.write(convert_transaction_to_csv_row(transaction))


def convert_transaction_to_csv_row(transaction):
    transaction_csv_row = '' + transaction['date'] + ',' + \
                          '"' + str(transaction['value']).replace('.', ',') + '",' + \
                          'EUR,' + \
                          '' + transaction['type'] + ',' + \
                          '' + transaction['id'] + ',' + \
                          '\n'
    return transaction_csv_row
