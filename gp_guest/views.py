from django.shortcuts import render

def index(request):
    print( request.session.get('loggedin_user') )
    
    return render(request, 'gp_guest/index.html')
