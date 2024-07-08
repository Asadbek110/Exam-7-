
from django.urls import path,include

from app.views import (IndexView,
 EventsListView, 
 EventsDetailView,
#  SendEmailView,
#  sending_email,
 LoginPage,
 RegisterView,
 LogoutPage,
 verify_email_done,
 verify_email_confirm,
 verify_email_complete,
 ContactSave                      )


urlpatterns = [
    path('',IndexView.as_view(),name='index'),
    path('events-lists/',EventsListView.as_view(),name='events-lists'),
    path('event-detail/<int:pk>',EventsDetailView.as_view(),name='event-detail'),
    # path('email-form/',EmailFormView.as_view(),name='email-form'),
    # path('send-email/',sending_email,name='send-email'),

    # login
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginPage.as_view(), name='login'),
    path('logout/', LogoutPage.as_view(), name='logout'),
     #  verify email url
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify_email_confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify_email_complete'),
    path('contact-save/',ContactSave.as_view(),name = 'contact_save'),


]
