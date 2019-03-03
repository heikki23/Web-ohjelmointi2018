from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm, AddGameForm, GameSaveForm, GameScoreForm
from .models import Game, GameState, Sales, GameScore, User
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django import forms
from django.http import JsonResponse, HttpResponseRedirect
from hashlib import md5
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from gameStore.tokens import accountActivationToken


#Check that is user developer. Return TRUE if user is developer
def user_is_developer(user):
    if user.isDeveloper:
        return True
    else:
        return False

def user_is_player(user):
    if user.isPlayer:
        return True
    else:
        return False

#Home window
def home(request):
    games = {
     "all_games": Game.objects.all()
    }
    if not request.user.is_anonymous:
        games["user_games"] = request.user.games.all()

    return render(request,'home.html',games)

#Search-function
def search(request):
    if request.method == "GET":
        games = {
         "all_games": Game.objects.filter(name__icontains=request.GET.get('search_box', None))
        }
        if not request.user.is_anonymous:
            games["user_games"] = request.user.games.all()
        return render(request, 'search.html', games)
    else:
        return HttpResponse(status=405, content = "Invalid method.")

#Your games view
@login_required(login_url='/gamestore/login')
def your_games(request):
    if request.user.isPlayer:
        transactions = request.user.salesPlayer.filter(status = "ready")
        games = request.user.games.all()
        #Get dates when game is bougth and save them to dates
        dic = {}
        for game in games:
            for transaction in transactions:
                if game in transaction.games.all():
                    dic[game] = transaction.date
        return render(request,'your_games.html',{'data':dic})
    elif request.user.isDeveloper:
        games = request.user.games.all()
        return render(request,'your_games.html',{'data':games})

#statistic
@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_developer, login_url='/gamestore')
def statistic(request):
    if request.method == "POST":
        data = request.POST
        #If developer have not developed this game
        if not request.user.games.filter(name = data.get('game')):
            return HttpResponse(status=403, content = "You are not this games developer.")
        #Get all transactions, where the game was bought. Include only those transactions where status is ready
        transactions = Sales.objects.filter(games__in = request.user.games.filter(name = data.get('game'))).filter(status = "ready")
        return render(request,'statistic.html',{'data':data.get('game'), 'trans': transactions})
    else:
        return HttpResponse(status=405, content = "Invalid method.")


#This view adds games to the user's shopcart
@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def shopcart(request):
    #Check if the request method post
    if request.method == "POST":
        #Get the data from the reqyest
        data = request.POST
        #Only plyaers can do this
        if request.user.isPlayer:

            #Check if the game is already in shopcart or user owns that game
            if request.user.games.filter(name = data.get('game')):
                messages.error(request, 'You already own this game')
                return HttpResponseRedirect('/gamestore/')
            #Check if the game is in the database
            try:
                buyGame = Game.objects.get(name = data.get('game'))
            except ObjectDoesNotExist:
                messages.error(request, 'There is no game named like this in shop!')
                return HttpResponseRedirect('/gamestore/')

            #Add game to the user. First try to find existing shopacart. If that
            #fails, create new one.
            try:
                saleEvent = request.user.salesPlayer.get(status = "pending")
                if saleEvent.games.filter(name = buyGame.name):
                    messages.error(request, 'Game is already in shopcart')
                    return HttpResponseRedirect('/gamestore/')
                saleEvent.games.add(buyGame)
                saleEvent.totPrice = saleEvent.totPrice + buyGame.price
                saleEvent.save()
                messages.success(request, 'Game added to shopcart')
                return HttpResponseRedirect('/gamestore/')
            #There was no shopcart for this user, so create new one.
            except ObjectDoesNotExist:
                saleEvent = Sales.objects.create_sales(request.user, buyGame)
                messages.success(request, 'Game added to shopcart')
                return HttpResponseRedirect('/gamestore/')
        else:
            messages.error(request, 'Developer can not buy games')
            return HttpResponseRedirect('/gamestore/')

    else:
        #Try to get pending shopcart. If there is none, give empty template to
        try:
            event = request.user.salesPlayer.get(status = "pending")
            games = event.games.all()
            dataTemplate = {
            "all_games":games,
            "price":event.totPrice
            }
        except ObjectDoesNotExist:
            dataTemplate = {
            "all_games": "",
            "price":"0"
            }

        return render(request,'shopcart.html', dataTemplate)

#this view handes removing games from shopart
@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def removeShopCart(request):
    if request.method == "POST":
        #Get the data from the reqyest
        data = request.POST
        #check that user has pending shopart
        try:
            saleEvent = request.user.salesPlayer.get(status = "pending")
        except:
            messages.error(request, 'There is nothing in your shopcart!')
            return HttpResponseRedirect('/gamestore/shopcart')
        #Check that that game wanted to remove exist in shopacrt
        try:
            removedGame = saleEvent.games.get(name = data.get('game'))
        except ObjectDoesNotExist:
            messages.error(request, 'This game is not in your shopcart!')
            return HttpResponseRedirect('/gamestore/shopcart')

        saleEvent.totPrice -= removedGame.price
        saleEvent.games.remove(removedGame)
        #If there are no games left in shopcart, remove this saleEvent.
        if saleEvent.games.all().count() == 0:
            saleEvent.delete()
        else:
            saleEvent.save()
        return HttpResponseRedirect('/gamestore/shopcart')
    else:
        return HttpResponse(status=405, content = "Invalid method.")

#This view renders purchase view.
@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def purchase(request):
    if request.method == "GET":
        action = "https://simplepayments.herokuapp.com/pay/"
        try:
            event = request.user.salesPlayer.get(status = "pending")
        except ObjectDoesNotExist:
            messages.error(request, 'There is nothing in you shopcart!')
            return HttpResponseRedirect('/gamestore/')
        games = event.games.all()
        amount = event.totPrice
        #Always go to same view for handling the result
        successUrl = request.build_absolute_uri("purchaseResult")
        errorUrl =  request.build_absolute_uri("purchaseResult")
        cancelUrl =  request.build_absolute_uri("purchaseResult")
        #our sid and secret key!
        sid = "joniheidimatti123"
        secretKey = "fd295a60cd39246c9251a01eb4768335"
        pid = event.pk


        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secretKey)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        return render(request, 'purchase.html', {'user': request.user,
                                                       'all_games':  games,
                                                       'action': action,
                                                       'pid': pid,
                                                       'sid': sid,
                                                       'amount': amount,
                                                       'success_url': successUrl,
                                                       'cancel_url': cancelUrl,
                                                       'error_url': errorUrl,
                                                       'checksum': checksum})
        #This view can be used only with GET
    else:
        return HttpResponse(status=405, content = "Invalid method.")


#This view handels the payment result
@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def purchaseResult(request):
    if request.method == 'GET':
        result = request.GET['result']
        checksumReq = request.GET['checksum']
        pid = request.GET['pid']
        ref = request.GET['ref']
        #check the checksum
        sid = "joniheidimatti123"
        secretKey =  "fd295a60cd39246c9251a01eb4768335"
        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result, secretKey)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()
        if checksum != checksumReq:
            messages.error(request, 'Your payment is invalid ')
            return HttpResponseRedirect('/gamestore/purchase')

        #Check that there still is pending load_request
        try:
            saleEvent = request.user.salesPlayer.get(status = "pending")
        except ObjectDoesNotExist:
            messages.error(request, 'There is nothing in your shopcart ')
            return HttpResponseRedirect('/gamestore/')
        #check that orderid is same
        if int(pid) != saleEvent.pk:
            messages.error(request, "Your purchase was not succesfull. Try again!")
            return HttpResponseRedirect('/gamestore/purchase')
        #Check that user is same as in orderid
        if saleEvent.player.pk != request.user.pk:
            messages.error(request,"Order does not match to your account!")
            return HttpResponseRedirect('/gamestore/purchase')

        #Transaction was succesfull
        if result == "success":
            #add games to the user
            for game in saleEvent.games.all():
                request.user.games.add(game)
                saleEvent.status = "ready"
                saleEvent.date = timezone.now()
                saleEvent.save()
            return HttpResponseRedirect('/gamestore/your_games')

        #User canceled the transaction
        elif result == "cancel":
            messages.error(request, 'You canceled the payment')
            return HttpResponseRedirect('/gamestore/purchase')

        #There was an error
        elif result == "error":
            messages.error(request, 'Error occurred. Try again!')
            return HttpResponseRedirect('/gamestore/purchase')

        #Message result was something else
        else:
            messages.error(request, 'Error occurred. Try again!')
            return HttpResponseRedirect('/gamestore/purchase')
    else:
        return HttpResponse(status=405, content = "Invalid method.")

#user_profile request login. Redirects to the login page
@login_required(login_url='/gamestore/login')
def user_profile(request):
    return render(request,'user_profile.html')

#When signup done
def signup(request):
    if request.method == 'POST':
        #Displayes SignUpForm (founnd in forms.py)
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #Send email to the user. Email is sent to users console
            current_site = get_current_site(request)
            subject = 'Activate Your GameStore Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': accountActivationToken.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

#This view is called when activation links is used
def activate(request, uidb64, token):
    try:
        #Check the link and find the user
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    #If link was good and user exist, activate the user
    if user is not None and accountActivationToken.check_token(user, token):
        user.is_active = True
        user.emailConfirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')

#This is shown when account activation link was sent.
def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def game_window(request, game_id):
    current_game = get_object_or_404(Game, id=game_id)
    #Here we check again if the user owns the game and proceed if he/she/it has it
    owned = request.user.games.filter(id=game_id).exists()

    if not owned:
        messages.error(request, "You do not own this game!")
        return redirect('home')

    #Here we return the site when 1st called
    if request.method == 'GET':
        return render(request, 'game_window.html', {'game': current_game.to_dict(),
                                                    'player': request.user.username,
                                                    'url': current_game.game_url,
                                                    'top5': GameScore.objects.filter(game = current_game).order_by('-score').all()[:5]})

    #When this website uses ajax to post messages we come here
    elif request.is_ajax():
        #This is the response we return to the window
        response = {
            "error": None,
            "result": None,
            "game_id": None
        }
        #Here we snatch the 'messageType' from the request and use it to check
        #what the window wanted us to do
        message = request.POST.get('messageType',None)

        if message == None:
            response['error'] = 'Wrongly used message to parent window'
            return JsonResponse(status=400, data=response)

        #Score command, checks if score is player's new highscore and add's it
        elif message == 'SCORE':
            form = GameScoreForm(request.POST)
            if not form.is_valid():
                response['error'] = form.errors
                return JsonResponse(status=400, data=response)

            playerScore = GameScore.objects.update_or_create(game = current_game, player = request.user)[0]
            if playerScore.score > form.cleaned_data['score']:
                #Since player has higher score already, we do nothing
                return JsonResponse(status=201, data=response)

            playerScore.score = form.cleaned_data['score']
            playerScore.save()

            response['game_id'] = game_id
            # response['top5'] = GameScore.objects.filter(game = current_game).order_by('-score').all()[:5]

            return JsonResponse(status=201, data=response)

        #Save command, checks if gameState is valid and if it is saves the data
        #to database
        elif message == 'SAVE':
            form = GameSaveForm(request.POST)

            if not form.is_valid():
                response['error'] = form.errors
                return JsonResponse(status=400, data=response)

            saveState = GameState.objects.update_or_create(game = current_game, player = request.user)[0]
            saveState.gameState = form.cleaned_data['gameState']
            saveState.save()
            return JsonResponse(status=201, data=response)

        #Load_request checks if the user has gameState saved and returns it
        elif message == 'LOAD_REQUEST':
            saveState = GameState.objects.filter(game = current_game, player = request.user)
            if saveState.exists():
                response['result'] = saveState[0].gameState
                return JsonResponse(status=200, data=response)
            else:
                response['error'] = 'There are no saved games!'
                return JsonResponse(status=400, data=response)

        #If messageType is wrong or it doesn't exist we get here
        else:
            response['error'] = 'Invalid message type.'
            return JsonResponse(status=400, data=response)

    #If method is not GET or not using ajax we get here
    else:
        return HttpResponse(status=405, content="Invalid method")

@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_developer, login_url='/gamestore')
def add_game(request):
    #Create form for adding game and add it when it's ready
	if request.method == 'POST':
		form = AddGameForm(request.POST)
		if form.is_valid():
			game = form.save()
			request.user.games.add(game)
			return redirect('your_games')
	else:
		form = AddGameForm(initial={'developer_name':request.user.username})

	return render(request,'add_game.html',{'form': form})

@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_developer, login_url='/gamestore')
def modify_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    #If developer have not developed this game
    user_games = request.user.games.all()
    if not game in user_games:
        return HttpResponse(status=403, content = "You are not this games developer.")
    #GET will be called when we want to start modifying game
    if request.method == "GET":
        form = AddGameForm(instance=game)
        return render(request, 'modify_game.html', {'form':form})
    #POST will be called when we are done modifying game
    if request.method == "POST":
        form = AddGameForm(request.POST or None ,instance=game)
        if form.is_valid():
            form.save()
            return redirect('your_games')
        return render(request, 'modify_game.html', {'form':form})

@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_developer, login_url='/gamestore')
def delete_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    #If developer have not developed this game
    user_games = request.user.games.all()
    if not game in user_games:
        return HttpResponse(status=403, content = "You are not this games developer.")
    #Deleteting of the game
    if request.method == "POST":
        game.delete()
        return redirect('your_games')

@login_required(login_url='/gamestore/login')
@user_passes_test(user_is_player, login_url='/gamestore')
def newhighscore(request):
    game_id = int(request.GET['game_id'])
    game = get_object_or_404(Game, id=game_id)
    scores = GameScore.objects.filter(game = game).order_by('-score').all()[:5]
    return render(request, 'newhighscore.html', {'top5': scores})
