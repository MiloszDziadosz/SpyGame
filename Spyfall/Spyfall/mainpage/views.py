from django.http import HttpResponse
from django.http import Http404
from django.template import loader
from django.shortcuts import render
from .models import Gametemp, Location


def index(request):
    all_temps = Gametemp.objects.all()
    #template = loader.get_template('mainpage/index.html')
    context = {
        'all_temps' : all_temps,
    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'mainpage/index.html', context)


def templist(request, temp_id):
    #all_temp = Gametemp.objects.all()
    #for i in all_temp:
    #    if(i.game_temp_name == temp_id):
    #        zmienna = i.id
    try:
        one_temp = Gametemp.objects.get(pk=temp_id)
    except Gametemp.DoesNotExist:
        raise Http404("Szablon nie istnieje")
    #all_loc = Location.objects.all()
    #context = {
    #    'all_loc': all_loc,
    #    'game_temp': one_temp,
    #}
    #return HttpResponse("<h1>List of locations of Template : " + game_temp_name + "</h1>")
    return render(request, 'mainpage/templist.html', context)