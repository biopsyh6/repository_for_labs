from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages

def to_tickets(request):
    return render(request, "cinema/client/movies.html")

def index_client_movies(request):
    movies = Movie.objects.all()
    return render(request, "cinema/client/movies.html", {"movies": movies})

@login_required
def movie_tickets(request, pk):
    movie = Movie.objects.get(pk=pk)
    tickets = Ticket.objects.filter(session__movie=movie)
    return render(request, "cinema/client/tickets.html", {"tickets": tickets, "movie": movie})


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
    finish_price = ticket.price
    return redirect("success_ticket", pk=ticket_selling.pk)

def success_ticket(request, pk):
    ticket_selling = TicketSelling.objects.get(pk=pk)
    return render(request, "cinema/client/success_ticket.html", {"ticket": ticket_selling.ticket, "promo_code": ticket_selling.promo_code})

def index_information_tickets(request):
    ticket_sellings = TicketSelling.objects.filter(client=request.user.client)
    return render(request, "cinema/client/info_tickets.html", {"ticket_sellings": ticket_sellings})


# @require_POST
# def use_coupon(request, pk):
#     coupon = Coupon.objects.get(pk=pk)
#     coupon.is_available = False
#     coupon.save()
#     UsedCoupons.objects.create(coupon=coupon, user=request.user.client)
#     return redirect('coupons')
