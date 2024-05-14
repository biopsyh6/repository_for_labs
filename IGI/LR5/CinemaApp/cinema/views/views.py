from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound

from django.urls import reverse
from ..models import *
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.views.generic import *
from django.urls import reverse_lazy
from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from cinema.forms import ReviewForm


# def index(request):
#     return HttpResponse("Hello, World!")

# Genres*****************************

def index_genres(request):
    """
    Get Genre objects from database.
    """
    genres = Genre.objects.all()
    return render(request, "index.html", {"genres": genres})

def create_genre(request):
    """
    Create Genre object and save in database.
    """
    if request.method == "POST":
        genre = Genre()
        genre.name = request.POST.get("name")
        genre.save()
    return HttpResponseRedirect("/")

def edit_genre(request, id):
    """
    Edit Genre object from database.
    """
    try:
        genre = Genre.objects.get(id=id)

        if request.method == "POST":
            genre.name = request.POST.get("name")
            genre.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"genre": genre})
    except Genre.DoesNotExist:
        return HttpResponseNotFound("<h2>Genre not found</h2>")
    
def delete_genre(request, id):
    """
    Delete Genre object from database.
    """
    try:
        genre = Genre.objects.get(id=id)
        genre.delete()
        return HttpResponseRedirect("/")
    except Genre.DoesNotExist:
        return HttpResponseNotFound("<h2>Genre not found</h2>")
    
# Movies*****************************  

def index_movies(request):
    """
    Get Movie objects from database.
    """
    movies = Movie.objects.all()
    return render(request, "index.html", {"movies": movies})

def create_movie(request):
    """
    Create Movie object and save in database.
    """
    if request.method == "POST":
        movie = Movie()
        movie.title = request.POST.get("title")
        movie.country = request.POST.get("country")
        movie.genre = request.POST.get("genre")
        movie.duration = request.POST.get("duration")
        movie.budget = request.POST.get("budget")
        movie.poster = request.POST.get("poster")
        movie.description = request.POST.get("description")
        movie.rating = request.POST.get("rating")
        movie.save()
    return HttpResponseRedirect("/")

def edit_movie(request, id):
    """
    Edit Movie object from database.
    """
    try:
        movie = Movie.objects.get(id=id)

        if request.method == "POST":
            movie.title = request.POST.get("title")
            movie.country = request.POST.get("country")
            movie.genre = request.POST.get("genre")
            movie.duration = request.POST.get("duration")
            movie.budget = request.POST.get("budget")
            movie.poster = request.POST.get("poster")
            movie.description = request.POST.get("description")
            movie.rating = request.POST.get("rating")
            movie.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"movie": movie})
    except Movie.DoesNotExist:
        return HttpResponseNotFound("<h2>Movie not found</h2>")

def delete_movie(request, id):
    """
    Delete Movie object from database. 
    """
    try:
        movie = Movie.objects.get(id=id)
        movie.delete()
        return HttpResponseRedirect("/")
    except Movie.DoesNotExist:
        return HttpResponseNotFound("<h2>Movie not found</h2>")
    
# Halls*****************************

def index_halls(request):
    """
    Get Hall objects from database.
    """
    halls = Hall.objects.all()
    return render(request, "index.html", {"halls": halls})

def create_hall(request):
    """
    Create Hall object and save in database.
    """
    if request.method == "POST":
        hall = Hall()
        hall.name = request.POST.get("name")
        hall.save()
    return HttpResponseRedirect("/")

def edit_hall(request, id):
    """
    Edit Hall object from database.
    """
    try:
        hall = Hall.objects.get(id=id)

        if request.method == "POST":
            hall.name = request.POST.get("name")
            hall.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"hall": hall})
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")
    
def delete_hall(request, id):
    """
    Delete Hall object from database.
    """
    try:
        hall = Hall.objects.get(id=id)
        hall.delete()
        return HttpResponseRedirect("/")
    except Hall.DoesNotExist:
        return HttpResponseNotFound("<h2>Hall not found</h2>")
    
# Session*****************************

def index_sessions(request):
    """
    Get Session objects from database.
    """
    sessions = Session.objects.all()
    return render(request, "index.html", {"sessions": sessions})

def index_last_session(request):
    """
    Get the latest Session object from database.
    """
    latest_session = Session.objects.order_by('-start_time').first()
    return render(request, "cinema/main.html", {"session": latest_session})

def create_session(request):
    """
    Create Session object and save in database.
    """
    if request.method == "POST":
        session = Session()
        session.movie = request.POST.get("movie")
        session.hall = request.POST.get("hall")
        session.start_time = request.POST.get("start_time")
        session.save()
    return HttpResponseRedirect("/")

def edit_session(request, id):
    """
    Edit Session object from database.
    """
    try:
        session = Session.objects.get(id=id)

        if request.method == "POST":
            session.movie = request.POST.get("movie")
            session.hall = request.POST.get("hall")
            session.start_time = request.POST.get("start_time")
            session.save()
            return HttpResponseRedirect("/")
        else:
            return render(request, "edit.html", {"session": session})
    except Session.DoesNotExist:
        return HttpResponseNotFound("<h2>Session not found</h2>")

def delete_session(request, id):
    """
    Delete Session object from database.
    """
    try:
        session = Session.objects.get(id=id)
        session.delete()
        return HttpResponseRedirect("/")
    except Session.DoesNotExist:
        return HttpResponseNotFound("<h2>Session not found</h2>")
    
def about_company(request):
    """
    Get CompanyInfo objects from database. 
    """
    company_info = CompanyInfo.objects.first()
    logging.info(f'Company info: {company_info.text}')
    return render(request, "cinema/about_company.html", {"company_info": company_info})

def terms(request):
    """
    Get DictionaryOfTerms objects from database.
    """
    all_terms = DictionaryOfTerms.objects.all()
    logging.info("Get the questions and answers")
    return render(request, "cinema/faq.html", {"all_terms": all_terms})

def contacts(request):
    """
    Get Employee objects from database.
    """
    all_employees = Employee.objects.all()
    logging.info("Get contacts")
    return render(request, "cinema/contacts.html", {"all_employees": all_employees})

def vacancies(request):
    """
    Get Vacancy objects from database.
    """
    all_vacancies = Vacancy.objects.all()
    logging.info("Get vacancies")
    return render(request, "cinema/vacancies.html", {"all_vacancies": all_vacancies})

def reviews(request):
    """
    Get Review objects from database.
    """
    all_reviews = Review.objects.all()
    logging.info("Get reviews")
    is_auth = request.user.is_authenticated
    return render(request, "cinema/reviews.html", {"all_reviews": all_reviews, "is_auth": is_auth})

def add_review(request):
    """
    Add Review object to database.
    """
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            review.sender = request.user.client
            review.save()
            return HttpResponseRedirect(reverse('reviews'))
        else:
            return render(request, "cinema/add_review.html", {"form": form})
    else:
        form = ReviewForm()
        return render(request, "cinema/add_review.html", {"form": form})
    
def coupons(request):
    """
    Get Coupons objects from database.
    """
    coupons = Coupon.objects.all()
    used_coupons = UsedCoupons.objects.all()
    return render(request, "cinema/coupons.html", {"coupons": coupons, "used_coupons": used_coupons})