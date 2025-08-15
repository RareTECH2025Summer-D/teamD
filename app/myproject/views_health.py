from django.http import HttpResponse

def health(_request):
    return HttpResponse("ok\n", content_type="text/plain")