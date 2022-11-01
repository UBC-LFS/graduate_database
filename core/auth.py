

def superadmin_access_only(view_func):
    ''' Only superadmins can access '''
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active and request.user.is_superuser and 'superadmin' in request.session['loggedin_user']['roles']:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def admin_access_only(view_func):
    ''' Only admins can access '''
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active and ('superadmin' in request.session['loggedin_user']['roles'] or 'admin' in request.session['loggedin_user']['roles']):
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def grad_advisor_access_only(view_func):
    ''' Only admins can access '''
    def wrap(request, *args, **kwargs):
        print(request.session['loggedin_user']['roles'])
        if request.user.is_authenticated and request.user.is_active and 'graduate-advisor' in request.session['loggedin_user']['roles']:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def supervisor_access_only(view_func):
    ''' Only admins can access '''
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active and 'supervisor' in request.session['loggedin_user']['roles']:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap


def guest_access_only(view_func):
    ''' Only admins can access '''
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active and 'guest' in request.session['loggedin_user']['roles']:
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrap