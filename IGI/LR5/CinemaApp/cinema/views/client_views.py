from django.shortcuts import render, redirect

def to_tickets(request):
    return render(request, "cinema/client/tickets.html")