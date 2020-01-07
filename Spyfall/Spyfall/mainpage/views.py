from django.http import HttpResponse
from django.http import Http404
from django.urls import reverse
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from .models import Gametemp, Location, Room, Tempuser
from .forms import RoomForm, TempuserForm
from django.db.models import Max
import random


def index(request):
    all_temps = Gametemp.objects.all()
    # template = loader.get_template('mainpage/index.html')
    #if 'newgame' in request.POST:
    #    redirect(create_game(request))
    context = {
        'all_temps': all_temps,
    }
    # return HttpResponse(template.render(context, request))
    return render(request, 'mainpage/index.html', context)


def templist(request, temp_id):
    # all_temp = Gametemp.objects.all()
    # for i in all_temp:
    #    if(i.game_temp_name == temp_id):
    #        zmienna = i.id
    # try:
    #    one_temp = Gametemp.objects.get(pk=temp_id)
    # except Gametemp.DoesNotExist:
    #    raise Http404("Szablon nie istnieje")
    one_temp = get_object_or_404(Gametemp, pk=temp_id)
    all_loc = Location.objects.all()
    context = {
        'all_loc': all_loc,
        'game_temp': one_temp,
    }
    # return HttpResponse("<h1>List of locations of Template : " + game_temp_name + "</h1>")
    return render(request, 'mainpage/templist.html', context)


def join_game(request, nic):
    if request.method == "POST":
        form = TempuserForm(request.POST or None)
        if form.is_valid():
            nick = form.cleaned_data['nickname']
            temp_room = form.cleaned_data['room']
            temp_user = Tempuser.objects.create(nickname=nick, room_id=temp_room)
            gr = Tempuser.objects.all()
            request.session['user_id'] = temp_user.id
            request.session['room_id'] = temp_room
            return render(request, 'mainpage/wait_room.html', {'gracze': gr, 'liczba': temp_room})
    form = TempuserForm()
    return render(request, 'mainpage/join_game.html', {'form': form})


def fast_join(request):
    tuser = TempuserForm(request.POST or None)
    if tuser.is_valid():
        tuser.save()
        return redirect(join_game(request, 'alalalala'))
    return render(request, 'mainpage/index.html')


def create_game(request, nic):
    if request.method == "POST":
        form = RoomForm(request.POST or None)
        if form.is_valid():
            gt = form.cleaned_data['gt']
            rn = form.cleaned_data['room_name']
            ps = form.cleaned_data['password']
            nick = form.cleaned_data['nickname']
            temp_room = Room.objects.create(gametemp=gt, room_name=rn, status=0, password=ps )
            temp_id = temp_room.id
            user = Tempuser.objects.create(room_id=temp_id, nickname=nick)
            request.session['user_id']=user.id
            request.session['room_id'] = temp_id
            gr = Tempuser.objects.all()
            return render(request, 'mainpage/wait_room.html', {'gracze': gr, 'liczba': temp_id})
    form = RoomForm()
    return render(request, 'mainpage/creating_game.html', {'form': form})


def game(request):
    userid = request.session['user_id']
    roomid = request.session['room_id']
    szablon = Room.objects.get(pk=roomid)
    if 1 == szablon.status:

        #try:
        #    tmp = Room.objects.get(pk=roomid)
        #except Room.DoesNotExist:
        #    raise Http404("nie ma takiego pokoju")
        user = Tempuser.objects.get(pk=userid)
        users = Tempuser.objects.all().filter(room=roomid)
        szablon = Room.objects.get(pk=roomid)
        chosen_loc = szablon.current_location
        locations = Location.objects.all().filter(gametemp=szablon.gametemp)
        context = {
            'user': user,
            'users': users,
            'chosen_loc': chosen_loc,
            'locations': locations,
        }
        return render(request, 'mainpage/game.html', context)
    redirect(roles(request))


def vote_wait(request):
    this_user = request.session['user_id']
    user = Tempuser.objects.get(pk=this_user)
    user.ready = 1
    user.save()
    return render(request, 'mainpage/vote_wait.html',
                  {'wiad': "Poczekaj na resztę graczy i wciśnij Start voting"})


def result_wait(request):
    this_user = request.session['user_id']
    user = Tempuser.objects.get(pk=this_user)
    #try:
    #    selected_user = Tempuser.objects.get(pk=request.POST['user'])
    #except (KeyError, Tempuser.DoesNotExist):
    #    return render(request, 'mainpage/error.html', {'wiad': "Something went wrong"})
    #else:
    selected_user = Tempuser.objects.get(pk=request.POST['user'])
    if user.voted == 0:
        selected_user.voted_for= selected_user.voted_for + 1
        selected_user.save()
        user.voted = 1
        user.save()
    else:
        return render(request, 'mainpage/error.html', {'wiad': "Dont cheat. U allready voted"})
    return redirect('mainpage:count_votes')


def count_votes(request):

    most_votes = 0
    highest_vote_count = 0
    spy_id = 0
    chosen_player = 0
    this_room = request.session['room_id']
    this_user = request.session['user_id']
    room = Room.objects.get(pk=this_room)
    locations = Location.objects.all().filter(gametemp=room.gametemp)
    all_users = Tempuser.objects.all().filter(room=this_room)
    for users in all_users:
        if users.voted == 0:
            return render(request, 'mainpage/result_wait.html')
    for users in all_users:
        if users.role == 1:
            spy_id = users.id
        if users.voted_for > most_votes:
            most_votes = users.voted_for
    for users in all_users:
        if users.voted_for == most_votes:
            chosen_player = users.id
            highest_vote_count = highest_vote_count + 1
    user = Tempuser.objects.get(pk=this_user)
    spy = Tempuser.objects.get(pk=spy_id)
    most_voted = all_users.get(pk=chosen_player)
    if highest_vote_count == 1 and most_voted.role == 1:
        #szpieg zdemaskowany
        who_won = 0
    else:
        who_won = 1
    room = Room.objects.get(pk=this_room)
    loc = room.current_location
    context = {
        'who_won': who_won,
        'spy': spy,
        'this_location': loc,
        'locations': locations,
        'user': user
    }
    return render(request, 'mainpage/result.html', context)


def vote(request):
    room_id = request.session['room_id']
    all_ready = Tempuser.objects.all().filter(room=room_id)
    for users in all_ready:
        if users.ready == 0:
            return redirect(reverse('mainpage:vote_wait'))
    room = Room.objects.get(pk=room_id)
    context = {
        'room': room,
        'users': all_ready
    }
    return render(request, 'mainpage/vote.html', context)


def end_game(request):
    user = Tempuser.objects.get(pk=request.session['user_id'])
    user.delete()
    all_temps = Gametemp.objects.all()
    context = {
        'all_temps': all_temps,
    }
    del request.session['user_id']
    del request.session['room_id']
    return render(request, 'mainpage/index.html', context)


def play_again(request):
    user = Tempuser.objects.get(pk=request.session['user_id'])
    user.role = 0
    user.ready = 0
    user.voted = 0
    user.voted_for = 0
    user.save()
    gr = Tempuser.objects.all()
    temp_room = request.session['room_id']
    room = Room.objects.get(pk=temp_room)
    room.status = 0
    room.save()
    return render(request, 'mainpage/wait_room.html', {'gracze': gr, 'liczba': temp_room})


def roles(request):
    print("Uruchomienie roles")
    #user_id = request.session['user_id']
    room_id = request.session['room_id']
    szablon = Room.objects.get(pk=room_id)
    print("Room id = ", room_id)
    if szablon.status == 0:
        all_users = Tempuser.objects.all().filter(room=room_id)
        number_of_users = Tempuser.objects.filter(room=room_id).count()
        #print("Liczba użytkownikow", all_users.count())
        number_of_locations = Location.objects.filter(gametemp=szablon.gametemp).count()
        all_loc = Location.objects.all().filter(gametemp=szablon.gametemp)
        pick = random.randint(1,number_of_users)
        print("Pick =", pick)
        pick_l = random.randint(1, number_of_locations)
        print("Pick loc = ", pick_l)
        user_iterator = 1
        loc_iterator = 1
        for user in all_users:
            print("User iteration = ", user_iterator)
            if user_iterator == pick:
                print("User wylosowany")
                user.role = 1
                user.save()
                user_iterator = user_iterator + 1
            else:
                user_iterator = user_iterator + 1
                print(user_iterator)
        for loc in all_loc:
            print("location id = ", loc_iterator)
            if loc_iterator == pick_l:
                print("Lokacja wybrana")
                szablon.status = 1
                szablon.current_location = loc.location_name
                szablon.save()
                return redirect(reverse('mainpage:game'))

            else:
                loc_iterator = loc_iterator + 1

    return redirect('mainpage:game')































