from django.shortcuts import render, redirect

def index(request):
    ''' App index page '''
    
    return redirect('accounts:login')
