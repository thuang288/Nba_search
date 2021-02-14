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
    
    return render(
        request, 
        'nba/base.html', 
        context
    )

def delete(request, player_name):
    Player.objects.get(name=player_name).delete()
    return redirect('home')


def post_detail(request, pk):
    player = Player.objects.get(pk = pk)

    url = 'https://www.balldontlie.io/api/v1/players/?search={}'
    r = requests.get(url.format(player.name)).json()
    id = r['data'][0]['id']
    
    player_avg = 'https://www.balldontlie.io/api/v1/season_averages?player_ids[]={}'
    p = requests.get(player_avg.format(id)).json()
    
    player_detail = {
        'name': r['data'][0]['first_name'],
        'last_name': r['data'][0]['last_name'],
        'pk': player.pk,
        # 'season': p['data'][0].get('season'),
        #'games_played': p['data'][0]['games_played'],
        #'points': p['data'][0]['pts'],
        'post': r['data'][0]['position'],
        'current_team':r['data'][0]['team']['full_name'],
        'height': r['data'][0]['height_inches'],
        'weight':r['data'][0]['weight_pounds'],
    }
    if not p['data']:
        player_detail['season'] = ''
        player_detail['points'] = ''
    else:
        player_detail['season'] = p['data'][0]['season']
        player_detail['points'] = p['data'][0]['pts']
    
    return render (
        request,
        'nba/post_detail.html',
        {'player': player_detail}
    )

''' 
    class PostDetailView(DetailView):
    model = Player
    template_name = 'nba/post_detail.html'
    queryset = Player.objects.all()
'''   