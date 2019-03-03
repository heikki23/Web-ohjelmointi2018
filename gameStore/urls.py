from django.urls import path
from django.conf.urls import url

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search', views.search, name='search'),
    path('login',auth_views.login,{'template_name' : 'login.html'} ,name = 'login'),
    path('logout', auth_views.logout, {'next_page': 'home'}, name='logout'),
    path('signup',views.signup,name = "signup"),
    path('user_profile',views.user_profile,name = 'user_profile'),
	# path('game_window', views.game_window, name = 'game_window'),
    path('game_window/<int:game_id>',views.game_window, name = 'game_window'),
	path('add_game', views.add_game, name = 'add_game'),
	path('your_games', views.your_games, name = 'your_games'),
    path('shopcart',views.shopcart, name = 'shopcart'),
    path('purchase', views.purchase, name = 'purchase'),
    path('purchaseResult',views.purchaseResult, name = 'purchaseResult'),
    path('statistic',views.statistic, name = 'statistic'),
    path('newhighscore',views.newhighscore, name = 'newhighscore'),
    path('modifygame/<int:game_id>',views.modify_game, name= 'modify_game'),
    path('account_activation_sent/', views.account_activation_sent, name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('deletegame/<int:game_id>', views.delete_game, name='delete_game'),
    path('removeShopCart',views.removeShopCart, name = 'removeShopCart')
]
