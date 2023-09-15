from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import auth_logout
from django.http import JsonResponse
from .forms import TeamSelectionForm
from social_django.models import UserSocialAuth
from random import randint
from .models import *
import tweepy
from django.conf import settings

def LogoutView(request):
    return auth_logout(request, next_page='login')

# def login(request):
#     return render(request, 'login.html')


def add_facebook_username(request):
    if request.method == 'POST':
        facebook_username = request.POST.get('facebook_username')
        request.user.profile.facebook_username = facebook_username
        request.user.profile.save()
    return redirect('home')


from social_django.models import UserSocialAuth
import logging

logger = logging.getLogger(__name__)

def facebook_callback(request):
    # Assuming you've configured the Facebook backend in your settings
    if request.user.is_authenticated and request.user.social_auth.filter(provider='facebook').exists():
        # User is logged in and has a Facebook social account
        facebook_social_account = request.user.social_auth.get(provider='facebook')

        # Now you can access the Facebook-related data
        facebook_data = facebook_social_account.extra_data
        facebook_id = facebook_data.get('id')
        facebook_username = facebook_data.get('username')
        
        # Update the user's social account with Facebook data
        facebook_social_account.extra_data['facebook_username'] = facebook_username
        facebook_social_account.save()

    return redirect('home')  # Redirect to your desired URL

def twitter_authenticate(request):
    # Set up Twitter API authentication using your Twitter API credentials from settings.py
    auth = tweepy.OAuthHandler(
        consumer_key=settings.TWITTER_API_KEY,
        consumer_secret=settings.TWITTER_API_SECRET,
        callback=settings.TWITTER_CALLBACK_URL,  # Redirect URL after Twitter authentication
    )
   
    # Get the authorization URL and request token
    try:
        redirect_url = auth.get_authorization_url()
        print(redirect_url)
        
        # Set session data for the request token
        request.session['request_token'] = auth.request_token
        print(  request.session['request_token'])
        return redirect(redirect_url)
    except Exception as e:
        print('Twitter authentication error:', e)
        # Handle the error gracefully, e.g., redirect to an error page or display a message.
        return redirect('home')

def home(request):
    if request.method == 'POST':
            content = request.POST.get('Content', '')

            if content:
            # Check if the user is authenticated with Twitter
             if not request.user.is_authenticated or not request.user.profile.twitter_access_token:
                return redirect('twitter_authenticate')  # Redirect to Twitter authentication

             auth = tweepy.OAuthHandler(
             consumer_key=settings.TWITTER_API_KEY,
             consumer_secret=settings.TWITTER_API_SECRET,
    )
            auth.set_access_token(
        request.user.profile.twitter_access_token,
        request.user.profile.twitter_access_token_secret,
    )

    # Create an API object
            api = tweepy.API(auth)

            try:
                api.update_status(content)
                print('Tweet posted successfully!')
            except Exception as e:
                print('Error posting tweet:', e)

    teams = Team.objects.all()
    predictions = Prediction.objects.all()
    description = "Check out this prediction!"
    facebook_username = None
    tournaments = Tournament.objects.all()

    selected_tournament_id = request.GET.get('selected_tournament_id')
    selected_teams = []

    if selected_tournament_id:
        try:
            selected_tournament = Tournament.objects.get(pk=selected_tournament_id)
            selected_teams = selected_tournament.teams.all()
        except Tournament.DoesNotExist:
            pass

    if request.user.is_authenticated:
        profile = request.user.profile
        facebook_username = profile.facebook_username

        if not profile.twitter_access_token:
            return redirect('twitter_authenticate')  # Redirect to Twitter authentication

        if not profile.facebook_username:
            return redirect('add_facebook_username')

    return render(request, 'home.html', {
        'teams': teams,
        'predictions': predictions,
        'description': description,
        'facebook_username': facebook_username,
        'tournaments': tournaments,
        'selected_teams': selected_teams,  # Pass selected teams to the template
    })
from django.http import JsonResponse

from django.http import JsonResponse

def get_teams(request, tournament_id):  # Add 'tournament_id' parameter
    try:
        selected_tournament = Tournament.objects.get(pk=tournament_id)
        selected_teams = selected_tournament.teams.all()
        team_data = [{'id': team.id, 'name': team.name, 'logo_url': team.logo.url} for team in selected_teams]

    except Tournament.DoesNotExist:
        team_data = []
    print(team_data) 
    return JsonResponse({'teams': team_data})


from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import imageio
import os
from random import randint
from .models import Team  # Make sure to import your Team model
from io import BytesIO  # Import BytesIO for working with image data
stop_predictions_flag = False

def generate_predictions(request):
    global stop_predictions_flag  # Access the global variable
    if request.method == 'POST' and 'team1_id' in request.POST and 'team2_id' in request.POST:
        try:
            team1_id = int(request.POST['team1_id'])
            team2_id = int(request.POST['team2_id'])
            
            team1 = Team.objects.get(pk=team1_id)
            team2 = Team.objects.get(pk=team2_id)

            selected_teams = {
                'team1_name': team1.name,
                'team2_name': team2.name,
            }

            predictions = []
            
            while not stop_predictions_flag and len(predictions) < 3:  # Generate random predictions until stopped or you have 3 predictions
                score1 = randint(0, 5)
                score2 = randint(0, 5)
                predictions.append({'team1': str(team1), 'team2': str(team2), 'score1': score1, 'score2': score2})

            # Reset the flag
            stop_predictions_flag = False

            # Convert team logos to bytes (assuming they are ImageField objects)
            team1_logo_bytes = team1.logo.read() if team1.logo else None
            team2_logo_bytes = team2.logo.read() if team2.logo else None
            
            # Generate and save the GIF using the modified function
            gif_filename = generate_match_gif(predictions, team1_logo_bytes, team2_logo_bytes)
            gif_url = os.path.join(settings.MEDIA_URL, gif_filename)
            return JsonResponse({'message': 'Predictions generated successfully', 'predictions': predictions, 'selected_teams': selected_teams, 'gif_url': gif_url})
        except Team.DoesNotExist:
            return JsonResponse({'message': 'Selected teams not found'}, status=400)
        except ValueError:
            return JsonResponse({'message': 'Invalid input'}, status=400)

    return JsonResponse({'message': 'Invalid request'}, status=400)

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image, ImageDraw, ImageFont
import os
from io import BytesIO
import imageio

def calculate_text_width(draw, text, font):
    _, _, width, _ = draw.textbbox((0, 0), text, font=font)
    return width

# Load the static background image outside of the function
background_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'images/uefa-champions-league-football-ball-stars-11562982790rnz67yryzj-removebg-preview.png')
background = Image.open(background_image_path)
background = background.resize((400, 250)) 

def generate_match_gif(predictions, team1_logo_bytes, team2_logo_bytes):
    images = []
    for prediction in predictions:
        img = Image.new('RGB', (400, 250), color='#1f044e')
        draw = ImageDraw.Draw(img)
        img.paste(background, (0, 0), background)
        
        # Load the fonts
        general_font_path = os.path.join(settings.STATICFILES_DIRS[0], 'fonts', 'times new roman bold italic.ttf')
        general_font = ImageFont.truetype(general_font_path, size=30)
        score_font = ImageFont.truetype(general_font_path, size=80)
        teamfont = ImageFont.truetype(general_font_path, size=15)
        website_font_path = os.path.join(settings.STATICFILES_DIRS[0], 'fonts', 'times new roman italic.ttf')
        website_font = ImageFont.truetype(website_font_path, size=15)  # Adjust the size as needed
        # Load team logos from BytesIO and paste them onto the image in the center
        team1_logo = Image.open(BytesIO(team1_logo_bytes)).convert("RGBA")
        team2_logo = Image.open(BytesIO(team2_logo_bytes)).convert("RGBA")
        logo_size = (100, 100)  # Set the logo size
        team1_logo = team1_logo.resize(logo_size)
        team2_logo = team2_logo.resize(logo_size)
        
        # Calculate the center positions for logos
        center_x1 = (img.width - team1_logo.width) // 5  # Left logo
        center_x2 = (img.width - team2_logo.width) * 4 // 5  # Right logo

        # Adjust the Y-coordinate for logo placement
        logo_y = 110  # Change this value as needed

        img.paste(team1_logo, (center_x1, logo_y), team1_logo)
        img.paste(team2_logo, (center_x2, logo_y), team2_logo)

        # Calculate the position to place scores on top of each team logo
        score1_x = center_x1 + (team1_logo.width - calculate_text_width(draw, str(prediction["score1"]), score_font)) // 2
        score2_x = center_x2 + (team2_logo.width - calculate_text_width(draw, str(prediction["score2"]), score_font)) // 2
        score_y = logo_y - 80  # Adjust this value as needed
        
        # Draw team scores on top of logos
        draw.text((score1_x, score_y), str(prediction["score1"]), fill='white', font=score_font)
        draw.text((score2_x, score_y), str(prediction["score2"]), fill='white', font=score_font)

        # Add your website link in the top left corner
        website_link = "www.ScoreGifs.com"
        website_x = 10
        website_y = 10
        draw.text((website_x, website_y), website_link, fill='white', font=website_font)

        # Add "Score Predictor" text in the middle with margin
        text_line1 = "   Score"
        text_line2 = "Predictor"
        text_width_line1 = calculate_text_width(draw, text_line1, general_font)
        text_width_line2 = calculate_text_width(draw, text_line2, general_font)
        text_x = (img.width - max(text_width_line1, text_width_line2)) // 2
        text_y_line1 = 10
        font_size = 30  # Adjust the font size as needed
        spacing = 5  # Adjust the vertical spacing between lines

        # Calculate the position of the second line based on font size and spacing
        text_y_line2 = text_y_line1 + font_size + spacing

        draw.text((text_x, text_y_line1), text_line1, fill='white', font=general_font)
        draw.text((text_x, text_y_line2), text_line2, fill='white', font=general_font)

        # Add team names and scores below the logos
        team1_text = f' {prediction["team1"]}   '
        team2_text = f'        {prediction["team2"]}'
        text_y = 215
        draw.text((center_x1, text_y), team1_text, fill='white', font=teamfont)
        draw.text((center_x2, text_y), team2_text, fill='white', font=teamfont)

        # Add larger-sized scores to the left and right of "Score Predictor" text
        # score1_text = str(prediction["score1"])
        # score2_text = str(prediction["score2"])
        # score1_x = text_x - calculate_text_width(draw, score1_text, score_font) - 100  # Margin to the left
        # score2_x = text_x + text_width_line1 + 100  # Margin to the right
        # score_y = 60  # Vertical alignment with "Score Predictor" text
        # draw.text((score1_x, score_y), score1_text, fill='white', font=score_font)
        # draw.text((score2_x, score_y), score2_text, fill='white', font=score_font)

        images.append(img)

    gif_path = os.path.join(settings.MEDIA_ROOT, 'match.gif')
    imageio.mimsave(gif_path, images, duration=0.8)

    return os.path.join(settings.MEDIA_URL, 'match.gif')

from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import Prediction

def share_prediction_on_facebook(request, prediction_id):
    prediction = get_object_or_404(Prediction, pk=prediction_id)
    
    # Update the prediction to indicate it's shared and capture the sharer's name
    prediction.shared = True
    prediction.sharer_name = request.user.username  # Assuming you're using the user's username
    prediction.save()
    
    # Your code to generate the Facebook share link (replace with actual implementation)
    # For example:
    facebook_share_link = f"https://www.facebook.com/sharer/sharer.php?u=https://example.com/prediction/{prediction_id}/"

    # Return a JSON response indicating success and the share link
    response_data = {
        'success': True,
        'facebook_share_link': facebook_share_link,
    }
    return JsonResponse(response_data)
