from django.shortcuts import redirect

EXEMPT_PREFIXES = (
    "/admin/",
    "/accounts/",
    "/onboarding/profile/",
    "/static/",
    "/media/",
)

class RequireProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.nickname:
            if not request.path.startswith(EXEMPT_PREFIXES):
                return redirect("/onboarding/profile/")
        return self.get_response(request)
