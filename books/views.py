from django.http import HttpResponse

# Create your views here.
def listBooksView(request):
    if request.method == 'GET':
        return HttpResponse("Successful")

def bookView(request, id=1):
    if request.method == 'GET':
        return HttpResponse("Will show book detail")