import os  # For handling file operations like basename for file name extraction
import json  # For parsing JSON data from request bodies
import requests  # For making HTTP requests, e.g., to download images or interact with APIs
from django.core.files.base import ContentFile  # For saving downloaded image content to a FileField
from django.http import JsonResponse  # For returning JSON responses
from django.shortcuts import render, redirect, get_object_or_404  # For rendering templates and handling object retrieval
from django.views import View  # To define class-based views
from django.utils.decorators import method_decorator  # To apply decorators like csrf_exempt
from django.views.decorators.csrf import csrf_exempt  # To exempt the view from CSRF validation
from django.utils import timezone  # For handling time-related operations like timestamps

# Import your models
from .models import Alert, Media  # Ensure these models are defined in your models.py

GOOGLE_MAPS_EMBED_API_KEY = 'AIzaSyDmQC5wO03CX1-NjiKlC20aHq3JuSuOIMA'

# Create your views here.
class Index(View):
    def get(self, request, alert=None):
        if request.user.is_authenticated:
            pass
        else:
            return redirect('login')
        context = {}
        alerts = Alert.objects.all()
        context['alerts'] = alerts
        if alert is not None:
            alertobj = Alert.objects.get(id = alert)
            context['alertobj'] = alertobj
        return render(request, 'dashboard/index.html', context)
    def post(self, request, alert=None):
        alertobj = get_object_or_404(Alert, id=alert)
        update_text = request.POST.get('update')

        if update_text:
            # Create a new update instance
            alertobj.updates.create(update=update_text, timestamp=timezone.now())
            return redirect('index', alert)  # Redirect back to the index or wherever you need

        return JsonResponse({'error': 'Update text cannot be empty.'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AlertView(View):
    def post(self, request, *args, **kwargs):
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Extract Alert fields
            alert_type = data.get('type')
            description = data.get('description')
            location_name = data.get('place')  # Place will be the location name
            priority = data.get('priority')
            media_data = data.get('media', [])

            # Validate required fields
            if not all([alert_type, description, location_name, priority]):
                return JsonResponse({'error': 'Missing required Alert fields.'}, status=400)

            # Get Embed URL from Google Maps
            place_embed_url = self.get_google_maps_embed_url(location_name)

            if not place_embed_url:
                return JsonResponse({'error': 'Unable to generate Google Maps embed URL.'}, status=400)

            # Create Alert object with the Embed URL
            alert = Alert.objects.create(
                type=alert_type,
                description=description,
                place=place_embed_url,  # Save the embed URL in the place field
                priority=priority
            )

            # Save media images if present
            if media_data:
                for media in media_data:
                    if 'image_url' in media:
                        image_url = media['image_url']  # Extract the actual URL
                        self.download_and_save_image(image_url, alert)

            return JsonResponse({'message': 'Alert created successfully.', 'alert_id': alert.id}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

    def get_google_maps_embed_url(self, location_name):
        """
        Generates a Google Maps Embed URL using the Google Maps Embed API.
        """
        try:
            embed_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_EMBED_API_KEY}&q={location_name}"
            response = requests.get(embed_url)

            # Return the embed URL if the request is successful
            if response.status_code == 200:
                return embed_url
            else:
                return None

        except requests.exceptions.RequestException as e:
            # Handle exceptions related to the HTTP request
            print(f"Error connecting to Google Maps API: {str(e)}")
            return None

    def download_and_save_image(self, media_url, alert):
        """
        Downloads an image from the provided URL and saves it to the Media model.
        """
        try:
            response = requests.get(media_url)
            if response.status_code == 200:
                # Get the file name from the URL
                file_name = os.path.basename(media_url)

                # Create a ContentFile from the downloaded content
                image_content = ContentFile(response.content)

                # Create a Media instance and save the image
                media_instance = Media.objects.create(
                    alert=alert,
                    image=None,  # Save the content to the ImageField
                    video=None  # You can add video handling here if needed
                )
                media_instance.image.save(file_name, image_content)

                print(f"Image saved successfully: {file_name}")

            else:
                print(f"Failed to download image: {media_url} - Status code: {response.status_code}")

        except Exception as e:
            print(f"Error downloading or saving image: {str(e)}")
