from django.shortcuts import redirect

from accounts.middleware.whitelisted_routes import whitelisted_urls


class RouterMiddleware:
    def __init__(self, get_response):
        # self.whitelisted_urls = '/dashboard/factual/limiting/(?P<token>[^/]+)\\Z'
        self.whitelisted_urls = '/accounts/confirm-email/(?P<token>[^/]+)\\Z'

        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            return self.utilityfunc(request, response)
        return response

    def utilityfunc(self, request, response):
        for p in whitelisted_urls(request):
            if request.path == p:
                print(request.path)
                print("whitelisted=> ", request.path)
                return response
        print(request.path)
        return redirect('welcome')

    def utilityfunc_wl(self, rpath):
        return redirect(rpath)