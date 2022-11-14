from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.decorators import method_decorator

from gp_admin import api
from core.auth import guest_access_only


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@guest_access_only
def index(request):
    return render(request, 'gp_guest/index.html')
