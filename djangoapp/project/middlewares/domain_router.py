from django.shortcuts import redirect

class DomainRouterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().lower()
        path = request.path

        if 'souterceirizado.com' in host and not path.startswith('/programa'):
            return redirect('/programa' + path)

        return self.get_response(request)
