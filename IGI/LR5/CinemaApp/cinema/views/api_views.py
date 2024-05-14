from cinema.models import News
import requests
import tmdbsimple as tmdb
from django.shortcuts import render
import random

tmdb.API_KEY = '25beca1b44784cf99bb97d69d991690f'
# tmdb.REQUESTS_TIMEOUT = 1
tmdb.REQUESTS_SESSION = requests.Session()

def update_news():
    """
    Film API
    """
    url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

    headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyNWJlY2ExYjQ0Nzg0Y2Y5OWJiOTdkNjlkOTkxNjkwZiIsInN1YiI6IjY2M2ZhNjEzNTU5NjAxOWE1ZDdlODg3ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.g_0r8-miSVpWL27lVBt25nK3HE07FYEkg8QBxnAvQQ4"
    }
    response = requests.get(url, headers=headers)
    response = response.json()
    films = response['results']
    for film in films:
        try:
            temp = News.objects.get(title=film['original_title'])
            in_db = True
        except:
            in_db = False
        if not in_db:
            news_obj = News()
            news_obj.title = film['original_title']
            news_obj.description = film['overview']
            # news_obj.url = film['url']
            news_obj.image_url = 'https://image.tmdb.org/t/p/w500' + film['poster_path']
            news_obj.save_image_from_url()
            news_obj.save()
    return

def news(request):
    update_news()
    news_data = News.objects.all()
    data = {'news': reversed(news_data)}
    return render(request, 'cinema/news.html', context=data)


def cats(request):
    page = random.randint(1, 34)
    response = requests.get(f'https://catfact.ninja/facts?page={page}')
    response = response.json()
    data = response['data']
    facts = list()
    for i in range(len(data)):
        facts.append(data[i]["fact"])
    return render(request, 'cinema/cat_facts.html', {"facts": facts})



# database = tmdb()
# movies = database.movies().top_rated()

