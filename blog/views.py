from django.http import HttpResponse

# A GET request that returns a list of all books in the database
def listBooks(request):
    return HttpResponse("Hello, world. You're at the polls index.")