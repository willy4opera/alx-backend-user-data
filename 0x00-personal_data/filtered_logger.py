#!/usr/bin/env python3

'''Here, we defined A module for filtering logs.
'''
import os
import re
import logging
import mysql.connector
from typing import List


patterns = {
    'extract': lambda numx, numy: r'(?P<field>{})=[^{}]*'.format('|'.join(numx), numy),
    'replace': lambda numx: r'\g<field>={}'.format(numx),
}
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
        ) -> str:
    '''Here, we defined the filters a log line.
    '''

    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    '''Here, we created a new logger for user data.
    '''
    dev_logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    dev_logger.setLevel(logging.INFO)
    dev_logger.propagate = False
    dev_logger.addHandler(stream_handler)
    return dev_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''Here, we creates a connector to a database.
    '''
    datab_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    datab_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    connection = mysql.connector.connect(
        host=datab_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=datab_name,
    )
    return connection


def main():
    '''Here, we Loged information about the user records in a table.
    '''
    u_fields = "name,email,phone,ssn,password,ip,last_login,user_agent"
    columns = u_fields.split(',')
    query = "SELECT {} FROM users;".format(u_fields)
    info_logger = get_logger()
    connection = get_db()
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(x[0], x[1]),
                zip(columns, row),
            )
            message = '{};'.format('; '.join(list(record)))
            args = ("user_data", logging.INFO, None, None, message, None, None)
            log_record = logging.LogRecord(*args)
            info_logger.handle(log_record)


class RedactingFormatter(logging.Formatter):
    '''Here, we redacted the Formatter class
    '''

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    FORMAT_FIELDS = ('name', 'levelname', 'asctime', 'message')
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''formating the LogRecord.
        '''
        message = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return text


if __name__ == "__main__":
    main()
