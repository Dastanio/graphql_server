import psycopg2


def create_postgresql_connection(db_username, db_password, db_host, db_port, db_name):
    connection = psycopg2.connect(user=db_username, password=db_password, host=db_host, port=db_port, database=db_name)
    connection.autocommit = True
    return connection
