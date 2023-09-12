from django.urls import path
from .views import home
from . import views

urlpatterns = [
    path('generate_predictions/', views.generate_predictions, name='generate_predictions'),
    # path('', views.home, name='home'),  # Uncomment this line
        path('add_facebook_username/', views.add_facebook_username, name='add_facebook_username'),  # The add_facebook_username view
    path('facebook/callback/', views.facebook_callback, name='facebook_callback'),
    path('share_prediction/<int:prediction_id>/', views.share_prediction_on_facebook, name='share_prediction'),
         path('twitter-authenticate/', views.twitter_authenticate, name='twitter_authenticate'),
            #  path('generate_gif/', views.generate_gif, name='generate_gif'),
    path('get_teams/<int:tournament_id>/', views.get_teams, name='get_teams'),    
            ]
