from app.core.processes import ComissionsProcess, SalesProcess,\
    StaggeredCommissionProcess


class SalesHandler:

    @staticmethod
    def run(request):
        process = SalesProcess(request)
        response = process.make()
        return response


class CommissionsHandler:

    @staticmethod
    def run(request):
        process = ComissionsProcess(request)
        response = process.make()
        return response


class StaggeredCommisionHandler:
    @staticmethod
    def run(request):
        process = StaggeredCommissionProcess(request)
        response = process.make()
        return response
