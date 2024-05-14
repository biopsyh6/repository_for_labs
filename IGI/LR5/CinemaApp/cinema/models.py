from typing import Any
from django.db import models
import uuid
import os
from django.core.files import File
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import re
import logging
from django.core.exceptions import ValidationError
from tzlocal import get_localzone_name
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
import datetime
import requests
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


# class CustomUser(AbstractUser):
#     STATUS = [
#         ('EM', 'Employee'),
#         ('CS', 'Customer'),
#     ]
#     status = models.CharField(max_length=2, choices=STATUS, default="CS")
#     phone_number = models.CharField(max_length=13)
#     age = models.PositiveSmallIntegerField(default=18)

#     timezone = get_localzone_name()

#     def __str__(self):
#         return self.username
    
#     def save(self, *args, **kwargs):
#         phone_number_pattern = re.compile(r'\+375(29)\d{7}')
#         if not re.fullmatch(phone_number_pattern, str(self.phone_number)) or self.age < 18 or self.age > 120:
#             logger.exception("ValidationError")
#             raise ValidationError("Error when creating user")
#         super().save(*args, **kwargs)

class Client(models.Model):
    """
    Model representing a client
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=20, help_text="Enter name of client")
    surname = models.CharField(max_length=20, help_text="Enter surname of client")
    email = models.EmailField(max_length=30, default='default@mail.ru')
    birth_date = models.DateField(validators=[MaxValueValidator(datetime.date.today() - datetime.timedelta(days=18 * 365),
                                                                message="You must be at least 18 years old to register")], null=True)
    age = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^\+375(44|29)\d{7}$', 
                                                                              message="Incorrect telephone number")]
                                                                              ,default="+375291111111")
    image = models.ImageField(upload_to='custom/avatars', default='avatars/default_client.png')

    def __str__(self):
        return f"{self.surname} {self.name} {self.email}"

class Genre(models.Model):
    """
    Model representing a movie genre.
    """
    name = models.CharField(max_length=50, help_text="Enter a movie genre")
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name
    
class Movie(models.Model):
    """
    Model representing a movie.
    """
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this movie")
    duration = models.IntegerField(help_text="Select duration in minutes")
    budget = models.DecimalField(max_digits=9, decimal_places=0, help_text="Select film budget")
    poster = models.ImageField(upload_to='images/posters', default='avatars/default_client.png')
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the film")
    rating = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(10.0)], 
                                 help_text="Select rating for this film")

    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    display_genre.short_description = 'Genre'

    def __str__(self):
        """
        String for representing the Movie object.
        """
        return self.title
    
class Hall(models.Model):
    """
    Model representing a hall.
    """
    name = models.CharField(max_length=20, help_text="Enter hall")

    def __str__(self):
        """
        String for representing the Hall object.
        """
        return self.name

class Session(models.Model):
    """
    Model representing a session.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this session")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, help_text="Enter movie for session")
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, help_text="Enter hall for session")
    start_time = models.DateTimeField(help_text="Enter date and time for session")
    end_time = models.DateTimeField(default=timezone.datetime.now, help_text="Enter the date and time for the end of the session")

    def __str__(self):
        """
        String for representing the Session object.
        """
        return self.movie.title


# class TicketPrice(models.Model):
#     """
#     Model representing a ticket price
#     """
#     price = models.FloatField(help_text="Enter price")

#     def __str__(self):
#         """
#         String for representing the TicketPrice object.
#         """
#         return str(self.price)
    

class Employee(models.Model):
    """
    Model representing an employee
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ROLES = [
        ('CA', 'Cashier'),
        ('OP', 'Operator'),
        ('AD', 'Administrator'),
        ('CO', 'Controller'),
        ('CL', 'Cleaner'),
        ('SE', 'Security'),
        ('SA', 'System Administrator'),
    ]
    name = models.CharField(max_length=20, help_text="Enter name of employee")
    surname = models.CharField(max_length=20, help_text="Enter surname of employee", default="")
    email = models.EmailField(max_length=30, default='default@mail.ru')
    birth_date = models.DateField(validators=[MaxValueValidator(datetime.date.today() - datetime.timedelta(days=18 * 365),
                                                                message="You must be at least 18 years old to register")], null=True)
    role = models.CharField(max_length=2, choices=ROLES)
    phone_number = models.CharField(max_length=13,
                                    validators=[RegexValidator(
                                        regex=r'^\+375(44|29)\d{7}$',
                                        message='Incorrect telephone number'
                                    )], default="+375291111111")
    image = models.ImageField(upload_to='custom/avatars', default='avatars/default_client.png')

    def __str__(self):
        """
        String for representing the Employee object.
        """
        return self.name
    

class Ticket(models.Model):
    """
    Model representing a ticket
    """
    session = models.ForeignKey(Session, on_delete=models.CASCADE, help_text="Enter session for ticket")
    price = models.FloatField(help_text="Enter price")
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, help_text="Enter the employee who sold the ticket")

    def __str__(self):
        """
        String for representing the Ticket object.
        """
        return self.session.movie.title
    
class TicketSelling(models.Model):
    """
    Model representing a ticket selling
    """
    client = models.ForeignKey(Client, related_name='purchases', on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    promo_code = models.CharField(max_length=20, null=True)

    def apply_promo(self, promo):
        if UsedCoupons.objects.filter(user_id=self.client, promo_id=promo).exists():
            return
        self.ticket.price *= 1 - promo.discount/100
        self.promo_code = promo.promo
        self.save()

        logging.info(f'Applied promo for {self.ticket.session.movie.title}')

        UsedCoupons.objects.create(coupon=promo, user=self.client)

    
# class ShowSchedule(models.Model):
#     """
#     Model representing a show schedule
#     """
#     session = models.OneToOneField('Session', on_delete=models.CASCADE)
#     # hall = models.ForeignKey(Hall, on_delete=models.CASCADE, help_text="Enter hall for show schedule")
#     start_date = models.DateTimeField(default=timezone.datetime.now, help_text="Enter start date for show schedule")
#     end_date = models.DateTimeField(default=timezone.datetime.now, help_text="Enter end date for show schedule")

#     def __str__(self):
#         """
#         String for representing the ShowSchedule object.
#         """
#         return str(self.start_date)

class CompanyInfo(models.Model):
    """
    Model representing a company info
    """
    text = models.TextField()

    def __str__(self):
        """
        String for representing the CompanyInfo object.
        """
        return self.text

class News(models.Model):
    """
    Model representing an article
    """
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    url = models.URLField(max_length=1000, default='')
    image = models.ImageField(upload_to='news/', default='news/no_image_icon.png')
    image_url = models.URLField(max_length=1000, null=True)
    

    def save_image_from_url(self):
        if self.image_url is None:
            return False
        r = requests.get(self.image_url)
        if r.status_code == 200:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(r.content)
            img_temp.flush() #From buffer to disk
            try:
                self.image.save(os.path.basename(self.image_url), File(img_temp), save=True)
            except:
                logging.info("Error in saving file")
                return False
            else: 
                return True
        else:
            return False

    def __str__(self):
        """
        String for representing the News object.
        """
        return self.title
    
class DictionaryOfTerms(models.Model):
    """
    Model representing a dictionary of terms
    """
    question = models.CharField(max_length=1000)
    answer = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        String for representing the DictionaryOfTerms object.
        """
        return self.question

class Vacancy(models.Model):
    """
    Model representing a vacancy
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=200)
    salary = models.FloatField(validators=[MinValueValidator(0.0)])

    def __str__(self):
        """
        String for representing the Vacancy object.
        """
        return self.name

class Review(models.Model):
    """
    Model representing a review
    """
    sender = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    rate = models.IntegerField(validators=[MaxValueValidator(5, message="Your rate should be no more than 5"),
                                            MinValueValidator(1, message="Your rate should be no less than 1")])
    date = models.DateField(auto_now_add=True)

class Coupon(models.Model):
    """
    Model representing a coupon
    """
    name = models.CharField(max_length=50)
    promo = models.CharField(max_length=20, default='')
    discount = models.PositiveSmallIntegerField(validators=[MaxValueValidator(50, message="Discount shouldn't be more 50 %"),
                                                            MinValueValidator(2, message="Discount shouldn't be less than 2 %")])
    
    def __str__(self):
        return self.name

class UsedCoupons(models.Model):
    """
    Model representing a used coupon
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)