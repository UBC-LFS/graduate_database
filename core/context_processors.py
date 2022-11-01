def user_roles(request):
    user_roles = None
    if request.user.is_authenticated and 'loggedin_user' in request.session.keys():
        user_roles = request.session['loggedin_user']['roles']

    return {
        'user_roles': user_roles
    }
