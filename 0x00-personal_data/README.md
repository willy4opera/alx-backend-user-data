# PROJECT AUTHOR : ODIONYE OBIAJULU WILLIAMS
# PROJECT TITLE : Personal Data

The content of this project are tasks for learning to protect a user's personal data.

## Tasks Completed

+ Regex-ing

    filtered_logger.py contains a function called filter_datum that obfuscates the log message with the following requirements:
        Arguments:
            fields: a list of strings representing all fields to obfuscate.
            redaction: a string representing by what the field will be obfuscated.
            message: a string representing the log line.
            separator: a string representing by which character is separating all fields in the log line (message).
        The function uses a regex to replace occurrences of certain field values.
        filter_datum is less than 5 lines long and uses re.sub to perform the substitution with a single regex.

 Log formatter

    filtered_logger.py contains the following updates:

    python

    import logging

    class RedactingFormatter(logging.Formatter):
        """ Redacting Formatter class
        """

        REDACTION = "***"
        FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
        SEPARATOR = ";"

        def __init__(self, fields):
            super(RedactingFormatter, self).__init__(self.FORMAT)
            self.fields = fields

        def format(self, record: logging.LogRecord) -> str:
            for field in self.fields:
                record.msg = filter_datum(field, self.REDACTION, record.msg, self.SEPARATOR)
            return super().format(record)

        Updated the class to accept a list of strings fields constructor argument.
        Implemented the format method to filter values in incoming log records using filter_datum.
        format method is less than 5 lines long.

 Create logger

    filtered_logger.py contains:
        Used user_data.csv for this task.
        Implemented a get_logger function that returns a logging.Logger object named "user_data" and only logs up to logging.INFO level.
        The logger does not propagate messages to other loggers and has a StreamHandler with RedactingFormatter as formatter.
        Created a tuple PII_FIELDS constant at the root of the module containing the fields from user_data.csv that are considered PII.

 Connect to secure database

    filtered_logger.py contains the following updates:
        Implemented a get_db function that returns a connector to the database (mysql.connector.connection.MySQLConnection object).
        Used the os module to obtain credentials from the environment.
        Used the module mysql-connector-python to connect to the MySQL database.

 Read and filter data

    filtered_logger.py contains a main function that retrieves all rows in the users table from the database and displays each row under a filtered format.

    log

    [HOLBERTON] user_data INFO 2019-11-19 18:37:59,596: name=***; email=***; phone=***; ssn=***; password=***; ip=e848:e856:4e0b:a056:54ad:1e98:8110:ce1b; last_login=2019-11-14T06:16:24; user_agent=Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; KTXN);

        Filtered fields: name, email, phone, ssn, password.
        Only the main function runs when the module is executed.

 Encrypting passwords

    encrypt_password.py contains a script that meets the following requirements:
        Implemented a hash_password function that expects one string argument password and returns a salted, hashed password, which is a byte string.
        Used the bcrypt package to perform the hashing (with hashpw).

 Check valid password

    app.py contains an is_valid function that expects 2 arguments and returns a boolean:
        Arguments:
            hashed_password: bytes type.
            password: str type.
        Used bcrypt to validate that the provided password matches the hashed password.