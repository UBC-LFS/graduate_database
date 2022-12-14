import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as AuthLogin, logout as AuthLogout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control, never_cache
from django.views.decorators.http import require_http_methods

from ldap3 import ALL_ATTRIBUTES, SUBTREE, Server, Connection
from ldap3.core.exceptions import LDAPBindError
import json

from .forms import LocalLoginForm
from gp_admin import api
from core.auth import loggedin_user

def ldap_auth(username, password):
    server = Server(settings.GRAD_DB_LDAP_URI)

    try:
        auth_conn = Connection(
            server,
            user = "uid={},{}".format(username, settings.GRAD_DB_LDAP_MEMBER_DN),
            password = password,
            authentication = 'SIMPLE',
            check_names = True,
            client_strategy = 'SYNC',
            auto_bind = True,
            raise_exceptions = False
        )

        is_valid = auth_conn.bind()
        if not is_valid:
            return False

        conn = Connection(
            server,
            user = settings.GRAD_DB_LDAP_AUTH_DN,
            password = settings.GRAD_DB_LDAP_AUTH_PASSWORD,
            authentication = 'SIMPLE',
            check_names = True,
            client_strategy = 'SYNC',
            auto_bind = True,
            raise_exceptions = False
        )

        conn.bind()

        conn.search(
            search_base = "uid={0},{1}".format(username, settings.GRAD_DB_LDAP_MEMBER_DN),
            search_filter = settings.GRAD_DB_LDAP_SEARCH_FILTER,
            search_scope = SUBTREE,
            attributes = ALL_ATTRIBUTES
        )

        entries = json.loads(conn.response_to_json())['entries']

        if len(entries) == 0:
            return False

        data = entries[0]['attributes']

        sn = data['sn'][0]
        cn = data['cn'][0]
        user = {
            'last_name': sn,
            'first_name': cn.split(sn)[0].strip()
        }
        return user

    except LDAPBindError:
        return False


class Login(View):
    ''' Login page '''

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/login.html')

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None).strip()
        password = request.POST.get('password', None).strip()

        if username and password:
            ldap_info = ldap_auth(username, password)
            if ldap_info:
                user = None
                u = User.objects.filter(username=username)

                if u.exists():
                    user = u.first()
                else:
                    user = api.create_user(username, ldap_info['first_name'], ldap_info['last_name'])

                AuthLogin(request, user)
                roles = api.get_roles(user)

                if len(roles) == 0:
                    messages.error(request, 'An error occurred. Users must have at least one role.')
                else:
                    request.session['loggedin_user'] = {
                        'id': user.id,
                        'username': user.username,
                        'roles': roles
                    }
                    redirect_to = api.redirect_to_index_page(roles)

                    return HttpResponseRedirect(redirect_to)

        messages.error(request, 'An error occurred. Please check your username or password, then try again.')
        return redirect('accounts:login')


@login_required(login_url=settings.LOGIN_URL)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@require_http_methods(['GET'])
@loggedin_user
def logout(request):
    request.session.flush()
    AuthLogout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('accounts:login')


class LocalLogin(View):
    ''' Local login '''

    @method_decorator(require_GET)
    def get(self, request, *args, **kwargs):
        if 'loggedin_user' in request.session.keys():
            roles = request.session['loggedin_user']['roles']
            redirect_to = api.redirect_to_index_page(roles)
            return HttpResponseRedirect(redirect_to)

        return render(request, 'accounts/local_login.html', {
            'form': LocalLoginForm()
        })

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        form = LocalLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                AuthLogin(request, user)
                roles = api.get_roles(user)
                if roles == None:
                    messages.error(request, 'An error occurred. Users must have at least one role.')
                else:
                    request.session['loggedin_user'] = {
                        'id': user.id,
                        'username': user.username,
                        'roles': roles
                    }
                    redirect_to = api.redirect_to_index_page(roles)
                    return HttpResponseRedirect(redirect_to)
            else:
                messages.error(request, 'An error occurred. Please check your username and password, then try again.')
        else:
            messages.error(request, 'An error occurred. Form is invalid. Please check your inputs.')

        return redirect('accounts:local_login')
