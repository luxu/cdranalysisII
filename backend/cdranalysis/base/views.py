from django.shortcuts import render


# login_not_required
def home(request):
    return render(request, 'base/home.html')
