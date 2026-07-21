class CsrfExemptApiMiddleware:
    """Exenta endpoints /api/ da verificação CSRF.

    A API usa Token Authentication (header Authorization), não cookies,
    então CSRF não se aplica.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            request._dont_enforce_csrf_checks = True
        return self.get_response(request)
