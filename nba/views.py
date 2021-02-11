import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from .models import Player
from .forms import PlayerForm

# Create your views here.
def index(request):
    url = 'https://www.balldontlie.io/api/v1/players/?search={}'

    error = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = PlayerForm(request.POST)

        if form.is_valid():
            new_player = form.cleaned_data['name']
            existing_player_count = Player.objects.filter(name=new_player).count()
            
            if existing_player_count == 0:                                              # check if the player is in the nba
                r = requests.get(url.format(new_player)).json()                   
                print(r)
                if r['meta']['total_pages'] != 0:
                    form.save()
                else:
                    error = 'Player does not exist in the NBA'
            else:
                error = 'Player is already in the database'
        return HttpResponseRedirect('/')
    
        if error:
            message = error
            message_class = 'is-danger'
        else:
            message = 'Player added successfully'
            message_class = 'is-success'

    form = PlayerForm()

    players = Player.objects.all()

    player_data = []

    for player in players:
        r = requests.get(url.format(player)).json()
        # print(r.text)
        
        nba_players = {
            'name': player.name,
            'id': player.id,
            'post': r['data'][0]['position'],
            'current_team':r['data'][0]['team']['full_name'],
            'height': r['data'][0]['height_inches'],
            'weight':r['data'][0]['weight_pounds'],
        }

        player_data.append(nba_players)
    

    context = {
        'player_data': player_data, 
        'form': form,
        'message' : message,
        'message_class' : message_class
    }
    return render(request, 'nba/base.html', context)

def delete(request, player_name):
    Player.objects.get(name=player_name).delete()
    return redirect('home')

class PostDetailView(DetailView):
    model = Player
    template_name = 'nba/post_detail.html'
    #queryset = Player.objects.all()
    