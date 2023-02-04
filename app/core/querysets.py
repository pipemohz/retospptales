from app.database import query_database, write_database, \
    clear_commissions_table
from abc import ABC, abstractmethod
from datetime import datetime as dt


class BaseQuerySet(ABC):
    @abstractmethod
    def get(self, **kwargs):
        """
        Method to get data from database connection.
        """
        pass


class ProductListQuerySet(BaseQuerySet):
    def get(self, **kwargs) -> dict:
        today = dt.today()
        query = f'exec [dbo].[SP_ListarProductos] {today.month},\
             {today.year},\
             {kwargs.get("id")}'

        records = query_database(query)
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

        records = query_database(query)

        data = [{
            'product': r[0],
            'gross_commission': '{:,}'.format(int(r[2])).replace(',', '.'),
            'total_sale': '{:,}'.format(int(r[1])).replace(',', '.')
        }
            for r in records
        ]

        return data


class CommissionsQuerySet(BaseQuerySet):
    def __init__(self) -> None:
        self._daily = DailyCommissionQuerySet()
        self._staggered = StaggeredCommissionQueryset()
        self._aguinaldo = AguinaldoQueryset()

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

        records = query_database(query)

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

        write_database(kwargs.get('id'), kwargs.get('products'))

        query = f"exec SP_RetoEscalonada {kwargs.get('year')},\
            {kwargs.get('month')},\
            '{kwargs.get('id')}'"

        records = query_database(query)

        clear_commissions_table()

        if not records or not records[0][0]:
            return {}

        commission_total = {
            'commission': f'{int(records[0][0])}'
        }

        return commission_total


class AguinaldoQueryset(BaseQuerySet):
    def get(self, **kwargs) -> dict:

        query = f"exec SP_RetoAguinaldo {kwargs.get('year')},\
            {kwargs.get('month')},\
            '{kwargs.get('id')}'"

        records = query_database(query)

        if not records or not records[0][0]:
            return {}

        commission_total = {
            'commission': f'{int(records[0][0])}'
        }

        return commission_total
