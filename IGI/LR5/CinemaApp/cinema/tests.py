from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client as TestClient
from cinema.models import Client, Movie, Employee, Hall, Session, Ticket, Genre, TicketSelling
import datetime
from cinema.forms import *
from .views import account_views, views, admin_views, api_views, client_views, employee_views, pages
from django.urls import reverse

class TestAccountViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.user_admin = cls.user_model.objects.create_superuser(username='admin')
        cls.admin = TestClient()
        cls.admin.force_login(cls.user_admin)

        cls.user_client1 = cls.user_model.objects.create(username='user1', password='fdjkd++*')
        cls.client_profile1 = Client.objects.create(name='Name1', surname='Surname1', email='user1@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=20 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile1.user = cls.user_client1
        cls.client_acc1 = TestClient()
        cls.client_acc1.force_login(cls.user_client1)

        cls.user_client2 = cls.user_model.objects.create(username='user2')
        cls.client_profile2 = Client.objects.create(name='Name2', surname='Surname2', email='user2@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile2.user = cls.user_client2
        cls.client_acc2 = TestClient()
        cls.client_acc2.force_login(cls.user_client2)

        cls.user_client3 = cls.user_model.objects.create(username='user3')
        cls.client_profile3 = Client.objects.create(name='Name3', surname='Surname3', email='user3@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile3.user = cls.user_client3
        cls.client_acc3 = TestClient()
        cls.client_acc3.force_login(cls.user_client3)


        cls.genre1 = Genre.objects.create(name="Horror")
        cls.genre2 = Genre.objects.create(name="Action")
        cls.movie1 = Movie.objects.create(title="Movie1", country="USA", duration=56, budget=25000,
                                         description="description1", rating=5.6)
        cls.movie1.genre.set([cls.genre1])
        cls.movie2 = Movie.objects.create(title="Movie2", country="USA", duration=60, budget=27000,
                                         description="description2", rating=6.8)
        cls.movie2.genre.set([cls.genre2])
        cls.hall1 = Hall.objects.create(name="first")
        cls.hall2 = Hall.objects.create(name="second")
        
        cls.user_employee1 = cls.user_model.objects.create(username='Employee1')
        cls.employee_profile1 = Employee.objects.create(name='Name4', surname='Surname4', email='user4@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CA', phone_number='+375291111111')
        cls.employee_profile1.user = cls.user_employee1
        cls.employee_acc1 = TestClient()
        cls.employee_acc1.force_login(cls.user_employee1)

        cls.user_employee2 = cls.user_model.objects.create(username='Employee2')
        cls.employee_profile2 = Employee.objects.create(name='Name5', surname='Surname5', email='user5@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CL', phone_number='+375291111111')
        cls.employee_profile2.user = cls.user_employee2
        cls.employee_acc2 = TestClient()
        cls.employee_acc2.force_login(cls.user_employee2)

        cls.session1 = Session.objects.create(movie=cls.movie1, hall=cls.hall1, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        cls.session2 = Session.objects.create(movie=cls.movie2, hall=cls.hall2, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        
        cls.ticket1 = Ticket.objects.create(session=cls.session1, price=10.0, employee=cls.employee_profile1, is_sold=False)
        cls.ticket2 = Ticket.objects.create(session=cls.session1, price=15.0, employee=cls.employee_profile2, is_sold=False)
        cls.ticket3 = Ticket.objects.create(session=cls.session2, price=20.0, employee=cls.employee_profile1, is_sold=True)
        cls.ticket4 = Ticket.objects.create(session=cls.session2, price=25.0, employee=cls.employee_profile2, is_sold=True)

    def test_name_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_surname_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')
    
    def test_email_max_length(self):
        client = Client.objects.get(id=1)
        max_length = client._meta.get_field('email').max_length
        self.assertEqual(max_length, 30)

    def test_name_employee_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_surname_employee_label(self):
        employee = Employee.objects.get(id=1)
        field_label = employee._meta.get_field('surname').verbose_name
        self.assertEqual(field_label, 'surname')

    def test_email_max_employee_length(self):
        employee = Employee.objects.get(id=1)
        max_length = employee._meta.get_field('email').max_length
        self.assertEqual(max_length, 30)


class UserRegistrationFormTest(TestCase):

    def test_username_field_help_text(self):
        form = UserRegistrationForm()
        self.assertEqual(form.fields['username'].help_text, 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')

    def test_username_field_too_long(self):
        username = 'a' * 151
        form_data = {'username': username}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_username_field_special_characters(self):
        username = 'user!name'
        form_data = {'username': username}
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())


class ProfileRegistrationFormTest(TestCase):
     
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.user_admin = cls.user_model.objects.create_superuser(username='admin')
        cls.admin = TestClient()
        cls.admin.force_login(cls.user_admin)

        cls.user_client1 = cls.user_model.objects.create(username='user1', password='fdjkd++*')
        cls.client_profile1 = Client.objects.create(name='Name1', surname='Surname1', email='user1@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=20 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile1.user = cls.user_client1
        cls.client_acc1 = TestClient()
        cls.client_acc1.force_login(cls.user_client1)

        cls.user_client2 = cls.user_model.objects.create(username='user2')
        cls.client_profile2 = Client.objects.create(name='Name2', surname='Surname2', email='user2@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile2.user = cls.user_client2
        cls.client_acc2 = TestClient()
        cls.client_acc2.force_login(cls.user_client2)

        cls.user_client3 = cls.user_model.objects.create(username='user3')
        cls.client_profile3 = Client.objects.create(name='Name3', surname='Surname3', email='user3@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile3.user = cls.user_client3
        cls.client_acc3 = TestClient()
        cls.client_acc3.force_login(cls.user_client3)


        cls.genre1 = Genre.objects.create(name="Horror")
        cls.genre2 = Genre.objects.create(name="Action")
        cls.movie1 = Movie.objects.create(title="Movie1", country="USA", duration=56, budget=25000,
                                         description="description1", rating=5.6)
        cls.movie1.genre.set([cls.genre1])
        cls.movie2 = Movie.objects.create(title="Movie2", country="USA", duration=60, budget=27000,
                                         description="description2", rating=6.8)
        cls.movie2.genre.set([cls.genre2])
        cls.hall1 = Hall.objects.create(name="first")
        cls.hall2 = Hall.objects.create(name="second")
        
        cls.user_employee1 = cls.user_model.objects.create(username='Employee1')
        cls.employee_profile1 = Employee.objects.create(name='Name4', surname='Surname4', email='user4@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CA', phone_number='+375291111111')
        cls.employee_profile1.user = cls.user_employee1
        cls.employee_acc1 = TestClient()
        cls.employee_acc1.force_login(cls.user_employee1)

        cls.user_employee2 = cls.user_model.objects.create(username='Employee2')
        cls.employee_profile2 = Employee.objects.create(name='Name5', surname='Surname5', email='user5@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CL', phone_number='+375291111111')
        cls.employee_profile2.user = cls.user_employee2
        cls.employee_acc2 = TestClient()
        cls.employee_acc2.force_login(cls.user_employee2)

        cls.session1 = Session.objects.create(movie=cls.movie1, hall=cls.hall1, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        cls.session2 = Session.objects.create(movie=cls.movie2, hall=cls.hall2, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        
        cls.ticket1 = Ticket.objects.create(session=cls.session1, price=10.0, employee=cls.employee_profile1, is_sold=False)
        cls.ticket2 = Ticket.objects.create(session=cls.session1, price=15.0, employee=cls.employee_profile2, is_sold=False)
        cls.ticket3 = Ticket.objects.create(session=cls.session2, price=20.0, employee=cls.employee_profile1, is_sold=True)
        cls.ticket4 = Ticket.objects.create(session=cls.session2, price=25.0, employee=cls.employee_profile2, is_sold=True)

    def test_name_field_label(self):
        client = Client.objects.get(id=1)
        field_label = client._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')  

    def test_valid_form(self):
        data = {'name': 'Name1', 'surname': 'Surname1', 'email': 'user1@mail.ru',
                'birth_date': datetime.date.today() - datetime.timedelta(days=20 * 365),
                'phone_number': '+375291111111'}
        form = ProfileRegistrationForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_surname_field_label(self):
        form = ProfileRegistrationForm()
        self.assertTrue(form.fields['surname'].label == None or form.fields['surname'].label == 'Surname')

    def test_email_field_label(self):
        form = ProfileRegistrationForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'Email')

    def test_birth_date_field_label(self):
        form = ProfileRegistrationForm()
        self.assertTrue(form.fields['birth_date'].label == None or form.fields['birth_date'].label == 'Birth date')

    def test_phone_number_field_label(self):
        form = ProfileRegistrationForm()
        self.assertTrue(form.fields['phone_number'].label == None or form.fields['phone_number'].label == 'Phone number')

    def test_image_field_label(self):
        form = ProfileRegistrationForm()
        self.assertTrue(form.fields['image'].label == None or form.fields['image'].label == 'Image')
    

class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_model = get_user_model()
        cls.user_admin = cls.user_model.objects.create_superuser(username='admin')
        cls.admin = TestClient()
        cls.admin.force_login(cls.user_admin)

        cls.user_client1 = cls.user_model.objects.create(username='user1', password='fdjkd++*')
        cls.client_profile1 = Client.objects.create(name='Name1', surname='Surname1', email='user1@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=20 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile1.user = cls.user_client1
        cls.client_acc1 = TestClient()
        cls.client_acc1.force_login(cls.user_client1)

        cls.user_client2 = cls.user_model.objects.create(username='user2')
        cls.client_profile2 = Client.objects.create(name='Name2', surname='Surname2', email='user2@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile2.user = cls.user_client2
        cls.client_acc2 = TestClient()
        cls.client_acc2.force_login(cls.user_client2)

        cls.user_client3 = cls.user_model.objects.create(username='user3')
        cls.client_profile3 = Client.objects.create(name='Name3', surname='Surname3', email='user3@mail.ru',
                                                    birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                    phone_number='+375291111111')
        cls.client_profile3.user = cls.user_client3
        cls.client_acc3 = TestClient()
        cls.client_acc3.force_login(cls.user_client3)


        cls.genre1 = Genre.objects.create(name="Horror")
        cls.genre2 = Genre.objects.create(name="Action")
        cls.movie1 = Movie.objects.create(title="Movie1", country="USA", duration=56, budget=25000,
                                         description="description1", rating=5.6)
        cls.movie1.genre.set([cls.genre1])
        cls.movie2 = Movie.objects.create(title="Movie2", country="USA", duration=60, budget=27000,
                                         description="description2", rating=6.8)
        cls.movie2.genre.set([cls.genre2])
        cls.movie3 = Movie.objects.create(title="Movie3", country="USA", duration=56, budget=25000,
                                        description="description1", rating=5.6)
        cls.movie3.genre.set([cls.genre1])
        cls.hall1 = Hall.objects.create(name="first")
        cls.hall2 = Hall.objects.create(name="second")
        
        cls.user_employee1 = cls.user_model.objects.create(username='Employee1')
        cls.employee_profile1 = Employee.objects.create(name='Name4', surname='Surname4', email='user4@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CA', phone_number='+375291111111')
        cls.employee_profile1.user = cls.user_employee1
        cls.employee_acc1 = TestClient()
        cls.employee_acc1.force_login(cls.user_employee1)

        cls.user_employee2 = cls.user_model.objects.create(username='Employee2')
        cls.employee_profile2 = Employee.objects.create(name='Name5', surname='Surname5', email='user5@mail.ru',
                                                       birth_date=datetime.date.today() - datetime.timedelta(days=25 * 365),
                                                       role='CL', phone_number='+375291111111')
        cls.employee_profile2.user = cls.user_employee2
        cls.employee_acc2 = TestClient()
        cls.employee_acc2.force_login(cls.user_employee2)

        cls.session1 = Session.objects.create(movie=cls.movie1, hall=cls.hall1, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        cls.session2 = Session.objects.create(movie=cls.movie2, hall=cls.hall2, start_time=datetime.datetime.now(),
                                              end_time=datetime.datetime.now() + datetime.timedelta(hours=2))
        
        cls.ticket1 = Ticket.objects.create(session=cls.session1, price=10.0, employee=cls.employee_profile1, is_sold=False)
        cls.ticket2 = Ticket.objects.create(session=cls.session1, price=15.0, employee=cls.employee_profile2, is_sold=False)
        cls.ticket3 = Ticket.objects.create(session=cls.session2, price=20.0, employee=cls.employee_profile1, is_sold=True)
        cls.ticket4 = Ticket.objects.create(session=cls.session2, price=25.0, employee=cls.employee_profile2, is_sold=True)

        cls.ticketselling1 = TicketSelling.objects.create(client=cls.client_profile1, ticket=cls.ticket1, promo_code="meow")
        cls.ticketselling2 = TicketSelling.objects.create(client=cls.client_profile2, ticket=cls.ticket2, promo_code="meow")
    
    def test_call_view_login(self):
        response = self.client.get(reverse(account_views.profile), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={reverse(account_views.profile)}')
        response = self.client.get(reverse(account_views.logout), follow=True)
        self.assertRedirects(response, f'/accounts/login/?next={reverse(account_views.logout)}')
    
    
    def test_index_admin_tickets_view(self):
        response = self.client.get(reverse('index_admin_tickets'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/list_tickets_admin.html')

    def test_index_admin_sessions_view(self):
        response = self.client.get(reverse('index_admin_sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/list_sessions_admin.html')

    def test_index_admin_halls_view(self):
        response = self.client.get(reverse('index_admin_halls'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/list_halls_admin.html')

    def test_index_admin_employees_view(self):
        response = self.client.get(reverse('index_admin_employees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/list_employees_admin.html')
    
    def test_info_sales_view(self):
        response = self.client.get(reverse('info_sales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/employee/sales_information.html')

    def test_success_ticket_view(self):
        response = self.client.get(reverse('success_ticket', args=[1])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/client/success_ticket.html')

    def test_success_ticket_view1(self):
        response = self.client.get(reverse('success_ticket', args=[self.ticketselling1.pk])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/client/success_ticket.html')
    
    def test_success_ticket_view2(self):
        response = self.client.get(reverse('success_ticket', args=[self.ticketselling2.pk])) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/client/success_ticket.html')
    
    def test_to_admin_view(self):
        response = self.client.get(reverse('to_admin')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/home_admin.html')
    
    def test_index_admin_movies_view(self):
        response = self.client.get(reverse('index_admin_movies')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/list_movies_admin.html')

    def test_movie_admin_details_view1(self):
        response = self.client.get(reverse('movie_admin_details', args=[self.movie1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/details_movie_admin.html')

    def test_movie_admin_details_view2(self):
        response = self.client.get(reverse('movie_admin_details', args=[self.movie2.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/details_movie_admin.html')

    def test_movie_admin_details_view3(self):
        response = self.client.get(reverse('movie_admin_details', args=[self.movie3.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/details_movie_admin.html')
    
    def test_session_new_view_get(self):
        response = self.client.get(reverse('session_new'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cinema/admin/add_session_admin.html')

    def test_session_new_view_post(self):
        response = self.client.post(reverse('session_new'), data={ 
            'movie': self.movie1.pk,
            'hall': self.hall1.pk,
            'start_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now() + datetime.timedelta(hours=2),
        })
        self.assertEqual(response.status_code, 302)

    def test_session_new_view_post2(self):
        response = self.client.post(reverse('session_new'), data={ 
            'movie': self.movie2.pk,
            'hall': self.hall2.pk,
            'start_time': datetime.datetime.now(),
            'end_time': datetime.datetime.now() + datetime.timedelta(hours=2),
        })
        self.assertEqual(response.status_code, 302)