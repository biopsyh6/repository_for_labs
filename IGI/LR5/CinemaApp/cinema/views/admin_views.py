from django.shortcuts import render, redirect, get_object_or_404
from cinema.forms import MovieForm, TicketForm, SessionForm
from cinema.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse



def session_new(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            session.save()
            return HttpResponseRedirect(reverse('index_admin_sessions'))
        else:
            return render(request, "cinema/admin/add_session_admin.html", {"form": form})
    else:
        form = SessionForm()
        return render(request, "cinema/admin/add_session_admin.html", {"form": form})
    

def session_edit(request):
    if request.method == "POST":
        session_pk = request.POST.get('session')
        session = Session.objects.get(pk=session_pk)
        form = SessionForm(request.POST, instance=session)
        if form.is_valid():
            new_session = form.save()
            new_session.save()
            # form.save()
            return HttpResponseRedirect(reverse("index_admin_sessions"))
        
    else:
        sessions = Session.objects.all()
        form = SessionForm()
        return render(request, 'cinema/admin/edit_session_admin.html', {"sessions": sessions, "form": form})
    

def session_delete(request):
    if request.method == "POST":
        try:
            session_pk = request.POST.get('session')
            session = Session.objects.get(pk=session_pk)
            session.delete()
            return HttpResponseRedirect(reverse("index_admin_sessions"))
        except Session.DoesNotExist:
            return HttpResponseNotFound("<h2>Session not found</h2>")
    else:
        sessions = Session.objects.all()
        return render(request, "cinema/admin/delete_session_admin.html", {"sessions": sessions})



def ticket_delete(request):
    if request.method == "POST":
        try:
            ticket_pk = request.POST.get('ticket')
            ticket = Ticket.objects.get(pk=ticket_pk)
            ticket.delete()
            return HttpResponseRedirect(reverse("index_admin_tickets"))
        except Ticket.DoesNotExist:
            return HttpResponseNotFound("<h2>Ticket not found</h2>")
    else:
        tickets = Ticket.objects.all()
        return render(request, "cinema/admin/delete_ticket_admin.html", {"tickets": tickets})



def ticket_edit(request):
    if request.method == "POST":
        ticket_pk = request.POST.get('ticket')
        ticket = Ticket.objects.get(pk=ticket_pk)
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            new_ticket = form.save()
            new_ticket.save()
            # form.save()
            return HttpResponseRedirect(reverse("index_admin_tickets"))
        
    else:
        tickets = Ticket.objects.all()
        form = TicketForm()
        return render(request, 'cinema/admin/edit_ticket_admin.html', {"tickets": tickets, "form": form})


def ticket_new(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            ticket.save()
            return HttpResponseRedirect(reverse('index_admin_tickets'))
        else:
            return render(request, "cinema/admin/add_ticket_admin.html", {"form": form})
    else:
        form = TicketForm()
        return render(request, "cinema/admin/add_ticket_admin.html", {"form": form})

def movie_new(request):
    if request.method == "POST":
        form = MovieForm(request.POST, files=request.FILES)
        if form.is_valid():
            movie = form.save()
            movie.save()
            return HttpResponseRedirect(reverse('index_admin_movies'))
        else:
            return render(request, "cinema/admin/add_movie_admin.html", {"form": form})
    else:
        form = MovieForm()
        return render(request, "cinema/admin/add_movie_admin.html", {"form": form})
    
    
def movie_edit(request):
    if request.method == "POST":
        movie_pk = request.POST.get('movie')
        movie = Movie.objects.get(pk=movie_pk)
        form = MovieForm(request.POST, instance=movie, files=request.FILES)
        if form.is_valid():
            new_movie = form.save()
            new_movie.save()
            # form.save()
            return HttpResponseRedirect(reverse("index_admin_movies"))
        
    else:
        movies = Movie.objects.all()
        form = MovieForm()
        return render(request, 'cinema/admin/edit_movie_admin.html', {"movies": movies, "form": form})

def movie_delete(request):
    if request.method == "POST":
        try:
            movie_pk = request.POST.get('movie')
            movie = Movie.objects.get(pk=movie_pk)
            movie.delete()
            return HttpResponseRedirect(reverse("index_admin_movies"))
        except Movie.DoesNotExist:
            return HttpResponseNotFound("<h2>Movie not found</h2>")
    else:
        movies = Movie.objects.all()
        return render(request, "cinema/admin/delete_movie_admin.html", {"movies": movies})
        

def to_admin(request):
    return render(request, "cinema/admin/home_admin.html")

def index_admin_movies(request):
    """
    Get Movie objects from database.
    """
    movies = Movie.objects.all()
    return render(request, "cinema/admin/list_movies_admin.html", {"movies": movies})

def index_admin_tickets(request):
    """
    Get Ticket objects from database.
    """
    tickets = Ticket.objects.all()
    return render(request, "cinema/admin/list_tickets_admin.html", {"tickets": tickets})

def index_admin_sessions(request):
    """
    Get Session objects from database.
    """
    sessions = Session.objects.all()
    return render(request, "cinema/admin/list_sessions_admin.html", {"sessions": sessions})

def index_admin_halls(request):
    """
    Get Hall objects from database.
    """
    halls = Hall.objects.all()
    return render(request, "cinema/admin/list_halls_admin.html", {"halls": halls})

def index_admin_employees(request):
    """
    Get Employee objects from database.
    """
    employees = Employee.objects.all()
    return render(request, "cinema/admin/list_employees_admin.html", {"employees": employees})


