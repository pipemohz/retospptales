from app.core.processes import ComissionsProcess, SalesProcess
from app.settings.pyodbc import Connection


class SalesHandler:

    @staticmethod
    def run(request):
        with Connection() as conn:
            process = SalesProcess(conn, request)
            response = process.make()
        return response


class CommissionsHandler:

    @staticmethod
    def run(request):
        with Connection() as conn:
            process = ComissionsProcess(conn, request)
            response = process.make()
        return response
