from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from cinema.forms import MovieFilterForm, TicketFilterForm
from django.db import transaction
from django.urls import reverse

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


# @require_POST
# def buy_ticket(request, pk):

#     ticket = Ticket.objects.get(pk=pk)
#     amount = int(request.POST.get('amount', 1))

#     first_price = ticket.price
#     promo_code = request.POST.get('promo_code')
#     ticket_selling = TicketSelling.objects.create(ticket=ticket, client=request.user.client, promo_code=promo_code, amount=amount)
    
#     if promo_code:
#         promo = Coupon.objects.get(promo=promo_code)
#         ticket_selling.apply_promo(promo)
#         promo.is_available = False
#         promo.save()
    
#     ticket.amount -= amount
#     if ticket.amount == 0:
#         ticket.is_sold = True
#     ticket.save()

#     logger.info("Create ticket successfully")
#     return redirect("success_ticket", pk=ticket_selling.pk)

@require_POST
def buy_ticket(request):

    client = request.user.client
    cart_items = Cart.objects.filter(client=client)
    promo_code = request.POST.get('promo_code')
    total_price = 0
    promo = None

    with transaction.atomic():
        for item in cart_items:
            ticket = item.ticket
            amount = item.amount
            if ticket:
                ticket_selling = TicketSelling.objects.create(ticket=ticket, client=client, promo_code=promo_code, amount=amount)
            else:
                continue

            if promo_code:
                promo = Coupon.objects.get(promo=promo_code)
                ticket_selling.apply_promo(promo)

            ticket.amount -= amount
            if ticket.amount == 0:
                ticket.is_sold = True
            ticket.save()
            total_price += (ticket_selling.amount * ticket_selling.ticket.price)
        else:
            if promo != None:
                promo.is_available = False
                promo.save()
        
        cart_items.delete()

    return redirect(reverse('success_ticket', args=[total_price, promo_code or '']))



def success_ticket(request, total_price, promo):
    # ticket_selling = TicketSelling.objects.get(pk=pk)
    # logger.info("Get TicketSelling objects by pk successfully")
    # return render(request, "cinema/client/success_ticket.html", {"ticket": ticket_selling.ticket, "promo_code": ticket_selling.promo_code,
    #                                                              "price": ticket_selling.amount * ticket_selling.ticket.price})

    return render(request, "cinema/client/success_ticket.html", {"total_price": total_price, "promo": promo})

def index_information_tickets(request):
    ticket_sellings = TicketSelling.objects.filter(client=request.user.client)
    logger.info("Get TicketSelling objects by client successfully")
    return render(request, "cinema/client/info_tickets.html", {"ticket_sellings": ticket_sellings})

def add_cart(request, pk):
    
    # cart_item = Ticket.objects.get(pk=pk)
    # amount = int(request.POST.get('amount', 1))
    # return render(request, "cinema/client/cart.html", {"ticket": cart_item, "amount": amount})
    ticket = Ticket.objects.get(pk=pk)
    amount = int(request.POST.get('amount', 1))
    client = request.user.client

    cart_item, created = Cart.objects.get_or_create(client=client, ticket=ticket, defaults={'amount': amount})
    if not created:
        cart_item.amount += amount
        cart_item.save()

    # return render(request, "cinema/client/cart.html", {"ticket": cart_item, "amount": amount})
    return redirect("cart")

def cart(request):
    client = request.user.client
    cart_items = Cart.objects.filter(client=client)
    total_price = 0
    if cart_items:
        for item in cart_items:
            if item.ticket and item.ticket.price:
                total_price += (item.amount * item.ticket.price)
    return render(request, "cinema/client/cart.html", {"cart_items": cart_items, "total_price": total_price})

@require_POST
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, client=request.user.client)
    cart_item.delete()
    return redirect('cart')

