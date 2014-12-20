from Classes.models import Situation
from django.template import loader, Context
from django.http import HttpResponse
from django.template import RequestContext

def main(request):
    temp = loader.get_template("index.html")
    cont = RequestContext(request, {})
    return  HttpResponse(temp.render(cont))

def situations(request):
    temp = loader.get_template("scenarios.html")
    cont = RequestContext(request, {'scenarios': Situation.objects.all()})
    return  HttpResponse(temp.render(cont))
