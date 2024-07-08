from lib2to3.fixes.fix_input import context

from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.views.generic import TemplateView, ListView, DetailView, View, FormView

from app.models import Event,User
from app.forms import MemberForm, ContactForm, PeopleForm, RegisterForm, LoginForm,EmailForm
from app.tokens import account_activation_token
from config import settings
from django.core.mail import send_mail, EmailMessage
from datetime import datetime


# Create your views here.


class IndexView(FormView):
    model = Event

    template_name = 'app/index.html'

   
    def get(self,request):
        form = MemberForm()
        return render(request,'app/index.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


        return render(request,'app/index.html',{'form':form})
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()

        # Filter upcoming events (events in the future)
        upcoming_events = Event.objects.filter(created_at__gte=now).order_by('created_at')[:2]

        # Filter past events (events in the past)
        latest_events = Event.objects.filter(created_at__lt=now).order_by('-created_at')

        # Add the events to the context
        context['upcoming_events'] = upcoming_events
        context['latest_events'] = latest_events

        return context



class EventsListView(ListView):
    template_name = 'app/event-listing.html'
    model = Event
    paginate_by = 1
    

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        now = datetime.now()

        # Filter upcoming events (events in the future)
        upcoming_events = Event.objects.filter(created_at__gte=now).order_by('created_at')[:2]

        # Filter past events (events in the past)
        latest_events = Event.objects.filter(created_at__lt=now).order_by('-created_at')

        # Add the events to the context
        context['upcoming_events'] = upcoming_events
        context['latest_events'] = latest_events

        return context


class EventsDetailView(TemplateView):
    template_name = 'app/event-detail.html'
    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs['pk'])
        contex['event'] = event
        return contex





# def sending_email(request):
#     sent = False
#
#     if request.method == 'POST':
#         form = EmailForm(request.POST)
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#         from_email = request.POST.get('from_email')
#         to = request.POST.get('to')
#         send_mail(subject, message, from_email, [to])
#         sent = True
#
#     return render(request, 'app/sending-email.html', {'form': form, 'sent': sent})





class LoginPage(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'app/auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

        return render(request, 'app/auth/login.html', {'form': form})


class LogoutPage(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

    def post(self, request):
        return render(request, 'app/auth/logout.html')



class RegisterView(View):

    def get(self, request):
        form = RegisterForm()
        return render(request, 'app/auth/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = User.objects.create_user(first_name=first_name, email=email, password=password)
            user.is_active = False
            user.is_staff = True
            user.is_superuser = True
            user.save()

            current_site = get_current_site(request)
            subject = 'Verify your email'
            message = render_to_string('app/auth/activation.html', {
                'request': request,
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': account_activation_token.make_token(user),
            })

            email = EmailMessage(subject, message, to=[email])
            email.content_subtype = 'html'
            email.send()

            return redirect('verify_email_done')

        return render(request, 'app/auth/register.html', {'form': form})



def verify_email_done(request):
    return render(request, 'app/auth/email/verify-email-done.html')


def verify_email_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return redirect('verify_email_complete')
    else:
        messages.warning(request, 'The link is invalid.')
    return render(request, 'app/auth/email/verify-email-confirm.html')


def verify_email_complete(request):
    return render(request, 'app/auth/email/verify-email-complete.html')


class ContactSave(View):
    def get(self,request):
        form = ContactForm()
        return render(request,'app/index.html',{'form':form})

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')


        return render(request,'app/index.html',{'form':form})

