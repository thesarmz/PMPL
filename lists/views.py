from django.http import HttpResponse

# Create your views here.
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title><h1>Thesar Muhammad Zuhri</h1></html>')
