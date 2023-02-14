from abc import ABC, abstractmethod
from datetime import datetime as dt
import logging


class BaseQuerySet(ABC):
    def __init__(self, conn) -> None:
        self.conn = conn

    @abstractmethod
    def get(self, **kwargs):
        """
        Method to get data from database connection.
        """
        pass

    def execute_query(self, query: str) -> list:
        """
        Make a query to fetch data from database.
        """

        with self.conn.cursor() as cursor:
            try:
                cursor.execute(query)
                results = cursor.fetchall()
            except Exception as e:
                results = []

        return results


class ProductListQuerySet(BaseQuerySet):
    def get(self, **kwargs) -> dict:
        today = dt.today()
        query = f'exec [dbo].[SP_ListarProductos] {today.month},\
             {today.year},\
             {kwargs.get("id")}'

        records = self.execute_query(query)
        if not records:
            return {}

        data = [{
            'code': str(r[0]),
            'product': str(r[1])
        }
            for r in records
        ]

        return data


class SalesQuerySet(BaseQuerySet):
    def get(self, **kwargs) -> list:

        query = f'Select Producto,\
            sum(VentaTotal) as VentaTotal,\
            sum(ComisionBruta) as ComisionBruta\
            from retos.tblVentasComisiones\
            where anno={kwargs.get("year")}\
            and NumMes={kwargs.get("month")}\
            and CedulaVendedor={kwargs.get("id")}\
            group by Producto'

        records = self.execute_query(query)

        data = [{
            'product': r[0],
            'gross_commission': '{:,}'.format(int(r[2])).replace(',', '.'),
            'total_sale': '{:,}'.format(int(r[1])).replace(',', '.')
        }
            for r in records
        ]

        return data


class CommissionsQuerySet(BaseQuerySet):
    def __init__(self, conn) -> None:
        self._daily = DailyCommissionQuerySet(conn)
        self._staggered = StaggeredCommissionQueryset(conn)
        self._aguinaldo = AguinaldoQueryset(conn)

    def get(self, **kwargs) -> dict:

        daily_commission = self._daily.get(**kwargs)
        staggered_commission = self._staggered.get(**kwargs)
        aguinaldo_commission = self._aguinaldo.get(**kwargs)

        if not daily_commission and (not staggered_commission
                                     or not aguinaldo_commission):
            return {}

        return {
            'daily': daily_commission,
            'escalonada': staggered_commission,
            'aguinaldo': aguinaldo_commission
        }


class DailyCommissionQuerySet(BaseQuerySet):
    def get(self, **kwargs) -> dict:

        query = f"Select c.CedulaVendedor,e.DiasBloqueado,c.CodProducto,\
            c.Producto,c.PorcentajeComision\
            from retos.tblPorcentajeComisionProducto c\
            left join retos.tblEstadoCartera e\
            on c.CedulaVendedor=e.CedulaVendedor\
            where c.CedulaVendedor like '{kwargs.get('id')}'\
            ORDER BY c.CodProducto ASC"

        records = self.execute_query(query)

        if not records:
            return {}

        status = records[-1][1]

        data = {
            str(r[2]): {
                'product': str(r[3]),
                'days_blocked': str(r[1]),
                'commission_percentage': float(r[4]) / 100
            }
            for r in records}

        commission_total = 0
        try:

            for index, product in enumerate(kwargs.get('products')):
                commission = data.get(str(product['code']))[
                    'commission_percentage'] * product['value']

                commission_total += commission

            commission_total = {
                'commission': f'{int(commission_total)}',
                'status_cartera': status
            }

        except TypeError:
            raise TypeError(f'Product {index + 1} code {product["code"]}')

        return commission_total


class StaggeredCommissionQueryset(BaseQuerySet):
    def get(self, **kwargs) -> dict:

        self.insert_products(kwargs['id'], kwargs['products'])

        records = self.exec_SP_RetoEscalonada(
            id=kwargs['id'],
            year=kwargs['year'],
            month=kwargs['month']
        )

        self.exec_SP_TruncaPronosticoComisionEscalonada()

        if not records or not records[0][0]:
            return {}

        commission_total = {
            'commission': f'{int(records[0][0])}'
        }

        return commission_total

    def insert_products(self, id: str, products: list[dict]):
        with self.conn.cursor() as cursor:
            try:
                for product in products:

                    insert = f"INSERT INTO retos.PronosticoComisionEscalonada \
                        (CedulaVendedor, CodProducto, VentaTotalMes)\
                        VALUES ({id}, \
                        {product.get('code')},\
                        {product.get('value')})"

                    cursor.execute(insert)

            except Exception as e:
                logging.info(f'Query has failed: {e}')

            else:
                self.conn.commit()

    def exec_SP_RetoEscalonada(self, **kwargs) -> list:
        query = f"exec SP_RetoEscalonada {kwargs.get('year')},\
            {kwargs.get('month')},\
            '{kwargs.get('id')}'"

        records = self.execute_query(query)

        return records

    def exec_SP_TruncaPronosticoComisionEscalonada(self):
        query = 'exec SP_TruncaPronosticoComisionEscalonada'
        with self.conn.cursor() as cursor:
            cursor.execute(query)


class AguinaldoQueryset(BaseQuerySet):
    def get(self, **kwargs) -> dict:

        query = f"exec SP_RetoAguinaldo {kwargs.get('year')},\
            {kwargs.get('month')},\
            '{kwargs.get('id')}'"

        records = self.execute_query(query)

        if not records or not records[0][0]:
            return {}

        commission_total = {
            'commission': f'{int(records[0][0])}'
        }

        return commission_total
