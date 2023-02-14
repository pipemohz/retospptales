from app.common.validators import BaseValidator, CommissionsValidator
from app.common.querysets import SalesQuerySet, CommissionsQuerySet
from app.api.api_responser import ApiResponser
from pydantic import ValidationError
from flask import Response


class BaseProcess:

    def __init__(self, conn, request) -> None:
        self._conn = conn
        self._request = request

    def make(self) -> Response:

        try:
            kwargs = self._validator(**self._args)
            data = self._queryset.get(**kwargs.dict())
        except ValidationError as e:
            return ApiResponser.bad_request_response(e.json())
        except TypeError as e:
            return ApiResponser.not_found_response(e)
        except Exception as e:
            return ApiResponser.error_response(e)
        else:
            if data:
                return ApiResponser.success_response(data)
            else:
                return ApiResponser.empty_response(data)


class SalesProcess(BaseProcess):
    def __init__(self, conn, request) -> None:
        super().__init__(conn, request)
        self._args = self._request.args.to_dict()
        self._queryset = SalesQuerySet(conn)
        self._validator = BaseValidator


class ComissionsProcess(BaseProcess):
    def __init__(self, conn, request) -> None:
        super().__init__(conn, request)
        self._args = self._request.get_json()
        self._queryset = CommissionsQuerySet(conn)
        self._validator = CommissionsValidator


class SpecialProcess(BaseProcess):
    def __init__(self, conn, request) -> None:
        super().__init__(conn, request)
        self.form_to_json()
        self._queryset = CommissionsQuerySet(conn)
        self._validator = CommissionsValidator

    def form_to_json(self):
        data = {
            key: values[0] if len(values) == 1
            and key in ['id', 'month', 'year']
            else values
            for key, values in self._request.form.lists()
        }

        if all(map(lambda key: key in data.keys(), ['codes', 'values'])):

            data['products'] = [
                {'code': c, 'value': v}
                for c, v in zip(data['codes'], data['values'])
            ]

            data.pop('codes')
            data.pop('values')

        self._args = data
