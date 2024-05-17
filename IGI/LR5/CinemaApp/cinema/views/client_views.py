from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from cinema.forms import MovieFilterForm, TicketFilterForm

logger = logging.getLogger('db_logger')

def to_tickets(request):
    logger.info(f"Go to /movies")
    return render(request, "cinema/client/movies.html")

def index_client_movies(request):
    movies = Movie.objects.all()
    if request.method == "GET":
        form = MovieFilterForm(request.GET)
        if form.is_valid():
            logger.info("MovieFilterForm is valid")
            if form.cleaned_data['genre']:
                movies = movies.filter(genre=form.cleaned_data['genre'])
            if form.cleaned_data['min_rating']:
                movies = movies.filter(rating__gte=form.cleaned_data['min_rating'])
            if form.cleaned_data['max_rating']:
                movies = movies.filter(rating__lte=form.cleaned_data['max_rating'])
    else:
        form = MovieFilterForm()
    return render(request, "cinema/client/movies.html", {"movies": movies, "form": form})

@login_required
def movie_tickets(request, pk):
    movie = Movie.objects.get(pk=pk)
    tickets = Ticket.objects.filter(session__movie=movie)
    if request.method == "GET":
        form = TicketFilterForm(request.GET)
        if form.is_valid():
            logger.info("TicketFilterForm is valid")
            if form.cleaned_data['min_price']:
                tickets = tickets.filter(price__gte=form.cleaned_data['min_price'])
            if form.cleaned_data['max_price']:
                tickets = tickets.filter(price__lte=form.cleaned_data['max_price'])
            if form.cleaned_data['date']:
                tickets = tickets.filter(session__start_time__date=form.cleaned_data['date'])
    else:
        form = TicketFilterForm()
    return render(request, "cinema/client/tickets.html", {"tickets": tickets, "movie": movie, "form":form})


@require_POST
def buy_ticket(request, pk):
    ticket = Ticket.objects.get(pk=pk)
    first_price = ticket.price
    promo_code = request.POST.get('promo_code')
    ticket_selling = TicketSelling.objects.create(ticket=ticket, client=request.user.client, promo_code=promo_code)
    if promo_code:
        promo = Coupon.objects.get(promo=promo_code)
        ticket_selling.apply_promo(promo)
        promo.is_available = False
        promo.save()
    ticket.is_sold = True
    ticket.save()
    logger.info("Create ticket successfully")
    finish_price = ticket.price
    return redirect("success_ticket", pk=ticket_selling.pk)

def success_ticket(request, pk):
    ticket_selling = TicketSelling.objects.get(pk=pk)
    logger.info("Get TicketSelling objects by pk successfully")
    return render(request, "cinema/client/success_ticket.html", {"ticket": ticket_selling.ticket, "promo_code": ticket_selling.promo_code})

def index_information_tickets(request):
    ticket_sellings = TicketSelling.objects.filter(client=request.user.client)
    logger.info("Get TicketSelling objects by client successfully")
    return render(request, "cinema/client/info_tickets.html", {"ticket_sellings": ticket_sellings})

