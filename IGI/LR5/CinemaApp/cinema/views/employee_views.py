from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from cinema.models import *

logger = logging.getLogger('db_logger')
def info_sales(request):
    sales = TicketSelling.objects.all()
    logger.info("Get all sales successfully")
    return render(request, "cinema/employee/sales_information.html", {"sales": sales})