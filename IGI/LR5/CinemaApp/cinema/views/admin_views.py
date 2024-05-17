from django.shortcuts import render, redirect, get_object_or_404
from cinema.forms import MovieForm, TicketForm, SessionForm
from cinema.models import *
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse
from django.db.models import Sum, Avg, Count
from statistics import mode, median, mean
import plotly.graph_objs as draw
import datetime

logger = logging.getLogger('db_logger')

def session_new(request):
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            session.save()
            logger.info("Session create successfully")
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
            logger.info("Session edit successfully")
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
            logger.info("Session delete successfully")
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
            logger.info("Ticket delete successfully")
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
            logger.info("Ticket edit successfully")
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
            logger.info("Ticket create successfully")
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
            logger.info("Movie create successfully")
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
            logger.info("Movie edit successfully")
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
            logger.info("Movie delete successfully")
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
    logger.info("Get Movie objects successfully")
    return render(request, "cinema/admin/list_movies_admin.html", {"movies": movies})

def movie_admin_details(request, pk):
    movie = Movie.objects.get(pk=pk)
    logger.info("Get Movie object by pk")
    return render(request, "cinema/admin/details_movie_admin.html", {"movie": movie})

def index_admin_tickets(request):
    """
    Get Ticket objects from database.
    """
    tickets = Ticket.objects.all()
    logger.info("Get Ticket objects successfully")
    return render(request, "cinema/admin/list_tickets_admin.html", {"tickets": tickets})

def index_admin_sessions(request):
    """
    Get Session objects from database.
    """
    sessions = Session.objects.all()
    logger.info("Get Session objects successfully")
    return render(request, "cinema/admin/list_sessions_admin.html", {"sessions": sessions})

def index_admin_halls(request):
    """
    Get Hall objects from database.
    """
    halls = Hall.objects.all()
    logger.info("Get Hall objects successfully")
    return render(request, "cinema/admin/list_halls_admin.html", {"halls": halls})

def index_admin_employees(request):
    """
    Get Employee objects from database.
    """
    employees = Employee.objects.all()
    logger.info("Get Employee objects successfully")
    return render(request, "cinema/admin/list_employees_admin.html", {"employees": employees})


def statistics(request):
    #annotate is for agregation of data
    #total amount of tickets sold by day
    daily_sales = TicketSelling.objects.extra(select={'day':'date(date)'}).values('day').annotate(total_sales=Sum('ticket__price'))

    #total amount of ticket sold by session
    session_sales = TicketSelling.objects.values('ticket__session').annotate(total_sales=Sum('ticket__price'))

    #total amount of ticket sold by movie
    movie_sales = TicketSelling.objects.values('ticket__session__movie__title').annotate(total_sales=Sum('ticket__price'))

    #alphabetical order
    movies_alpha = Movie.objects.all().order_by('title')

    #total sales
    total_sales = TicketSelling.objects.aggregate(total_sales=Sum('ticket__price'))['total_sales']

    #mean, mode, median for total sales
    sales = TicketSelling.objects.values_list('ticket__price', flat=True)
    # average_sales = sales.aggregate(average_sales=Avg('ticket__price'))['average_sales']
    mean_sales = mean(sales)
    mode_sales = mode(sales)
    median_sales = median(sales)

    #mean, median for client ages
    clients = Client.objects.all()
    ages = [((date.today() - client.birth_date).days // 365) for client in clients]
    mean_age = mean(ages)
    median_age = median(ages)

    #popular genre of movie
    popular_genre = Genre.objects.annotate(num_movies=Count('movie')).order_by('-num_movies').first()

    #profitable genre of movie
    profitable_genre = Genre.objects.annotate(total_sales=Sum('movie__session__ticket__ticketselling__ticket__price')).order_by('-total_sales').first()

    #diagram
    age_groups = [(18, 30), (31, 60), (61, 100)]
    for client in clients:
        if client.age == 0:
            birth = client.birth_date
            today = datetime.date.today()
            client.age = int((today - birth).days / 365)
            client.save()

    clients_groups = [
        Client.objects.filter(age__range=(lower_range, upper_range)).count()
        for lower_range, upper_range in age_groups
    ]
    labels = ["Young(18-30)", "Adults(31, 60)", "Old(61-100)"]
    values = clients_groups

    fig = draw.Figure(data=[draw.Pie(labels=labels, values=values)])
    chart = fig.to_html(full_html=False)


    return render(request, "cinema/admin/statistics.html", {"daily_sales": daily_sales, "session_sales": session_sales, "movie_sales": movie_sales, 
                                                            "movies_alpha": movies_alpha, "total_sales": total_sales, "average_sales": mean_sales,
                                                            "mode_sales": mode_sales, "median_sales": median_sales, "average_age": mean_age,
                                                            "median_age": median_age, "popular_genre": popular_genre, "profitable_genre": profitable_genre,
                                                            "chart": chart})

