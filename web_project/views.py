from django.http import HttpResponse

def homeView(request):
    if request.method == 'GET':
        return HttpResponse("Hello World! This is a website for a book publisher")