from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.utils.decorators import method_decorator
from django.urls import reverse

from gp_admin import api
from core.auth import supervisor_access_only


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@supervisor_access_only
def index(request):
    return render(request, 'gp_supervisor/index.html', {
        'info': {
            'href': reverse('gp_supervisor:get_grad_supervision')
        }
    })


@method_decorator([never_cache, login_required, supervisor_access_only], name='dispatch')
class Get_Grad_Supervision(View):

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'gp_supervisor/get_grad_supervision.html', {
            'prof': api.get_program_supervision_view(request.user.username),
            'info': {
                'href': reverse('gp_supervisor:index')
            },
            'tab': request.GET.get('t', 'students'),
            'tab_urls': {
                'students': api.build_tab_url(request.path, 'students')
            }
        })
