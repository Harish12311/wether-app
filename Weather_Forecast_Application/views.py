from django.shortcuts import render
from django.contrib import messages
import datetime
import requests

def home(request):
    # Get the city name from the POST request, defaulting to "indore" if not provided
    city = request.POST.get('city', 'indore')

    # OpenWeatherMap API endpoint
    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=b862a9c036bb45eb9f61f2a4977100af'
    weather_params = {'units': 'metric'}

    # Google Programmable Search Engine API
    API_KEY = 'AIzaSyCPaPOYlJguaXyt-xBVMrLIU2ZPL0j9MVk'
    SEARCH_ENGINE_ID = '405bcde9d3bf24264'
    query = f"{city} 1920x1080"
    start = 1  # Set start to 1 to define the first page of results
    search_type = 'image'
    image_url = None

    try:
        # Fetch the image data from Google Custom Search
        city_url = (
            f"https://www.googleapis.com/customsearch/v1?key={API_KEY}"
            f"&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
            f"&searchType={search_type}&imgSize=xlarge"
        )
        image_response = requests.get(city_url)
        image_response.raise_for_status()
        image_data = image_response.json()
        search_items = image_data.get("items")

        if search_items:
            # Retrieve the first image link
            image_url = search_items[0]['link']
        else:
            # Set a default image URL or message if no images are found
            image_url = "https://example.com/default_image.jpg"

    except requests.exceptions.RequestException:
        # Handle errors if Google Custom Search API request fails
        messages.error(request, "Could not retrieve city image.")
        image_url = "https://example.com/default_image.jpg"  # Set a default image URL

    try:
        # Fetch weather data from OpenWeatherMap API
        response = requests.get(weather_url, params=weather_params)
        response.raise_for_status()
        weather_data = response.json()

        # Extract weather details from API response
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        # Pass all data to the template
        return render(request, 'index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'image_url': image_url,
            'exception_occurred': False
        })

    except requests.exceptions.RequestException:
        # Handle errors for OpenWeatherMap API request
        messages.error(request, 'Weather data for the entered city is not available.')
        day = datetime.date.today()

        # Render template with fallback values
        return render(request, 'index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'Maharashtra',
            'exception_occurred': True,
            'image_url': image_url
        })
