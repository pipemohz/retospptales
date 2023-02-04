from app.settings.database import Connection
import logging


def query_database(query: str) -> list:
    """
    Make a query to DB_NAME database of SQL Server DB_HOST.
    """

    with Connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
            except Exception as e:
                results = []

    return results


def clear_commissions_table() -> None:

    with Connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('exec SP_TruncaPronosticoComisionEscalonada;')


def write_database(_id: str, records: list[dict]) -> None:

    with Connection() as conn:
        with conn.cursor() as cursor:
            try:
                for record in records:

                    insert = f"INSERT INTO retos.PronosticoComisionEscalonada \
                        (CedulaVendedor, CodProducto, VentaTotalMes)\
                        VALUES ({_id}, \
                        {record.get('code')},\
                        {record.get('value')})"

                    cursor.execute(insert)

            except Exception as e:
                logging.info(f'Query has failed: {e}')

            else:
                conn.commit()
