from django.shortcuts import render, redirect
import datetime
from django.utils import dateformat, timezone
import calendar
from datetime import datetime as dt
from CinemaApp.settings import BASE_DIR
import os

def home(request):
    time = timezone.datetime.now()
    date = dateformat.format(time, 'd/m/Y')
    d = datetime.date.today()
    c = calendar.TextCalendar()
    cal = calendar.month(time.year, time.month)
    date_db = get_date_db()
    return render(request, 'cinema/account/home.html', {"time": time, "date": date, "cal": cal, "date_db": date_db})

def get_date_db():
    path = os.path.join(BASE_DIR, 'db.log')

    with open(path, 'r') as file:
        last_date = file.read(19)
        last_date = dt.strptime(last_date, "%Y-%m-%d %H:%M:%S")
    return last_date