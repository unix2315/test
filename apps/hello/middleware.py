from apps.hello.models import RequestsLog


class RequestStore(object):

    def process_response(self, request, response):
        if not request.is_ajax():
            new_request = RequestsLog(
                method=request.method,
                path=request.path,
                status_code=response.status_code)
            new_request.save()
        return response
