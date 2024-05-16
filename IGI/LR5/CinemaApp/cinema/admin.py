from django.contrib import admin

from .models import *
from django.contrib.auth.admin import UserAdmin

# class GenreAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Genre, GenreAdmin)




# admin.site.register(CustomUser)


# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser
#     list_display = ['email', 'username',]

# admin.site.register(CustomUser)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'birth_date')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'rating', 'display_genre')
    list_filter = ['rating']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['movie']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'role')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('session', 'price')

# @admin.register(ShowSchedule)
# class ShowScheduleAdmin(admin.ModelAdmin):
#     list_display = ('movie', 'start_date', 'end_date')

@admin.register(DictionaryOfTerms)
class DictionaryOfTermsAdmin(admin.ModelAdmin):
    list_display = ('question', 'date')

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('name', 'salary')

admin.site.register(Review)
admin.site.register(Coupon)
admin.site.register(UsedCoupons)
# admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Hall)
# admin.site.register(Session)
admin.site.register(CompanyInfo)
admin.site.register(News)
# admin.site.register(Employee)
# admin.site.register(Ticket)
# admin.site.register(ShowSchedule)
