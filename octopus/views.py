from django.db.models import fields
from django.db.models.base import Model
from django.forms.models import ModelMultipleChoiceField
from django.shortcuts import redirect, render
from django.db import IntegrityError
from .models import *
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.forms import ModelForm, widgets
from django import forms
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import datetime


def dates_of_week():
    dates = []
    a = datetime.datetime.now().isocalendar()
    week = a[1]
    year = datetime.datetime.now().year
    for i in range(1, 8):
        date = datetime.date(year, 1, i) + datetime.timedelta(weeks=+week)
        dates.append(date.strftime("%d-%m-%y"))
    print(dates)
    return dates

# Create your iews here.


def index(request):
    if request.user.is_authenticated:
        return render(request, "octopus/index.html", {

        })
        # return HttpResponseRedirect(reverse('bank_list_view'))
    else:
        return render(request, "octopus/index.html", {

        })


def bank_list_view(request):
    banks = FoodBank.objects.all()
    return render(request, "octopus/bank_list.html", {
        'banks': banks
    })

# User registration


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        birthdate = request.POST['birthdate']
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "octopus/register.html", {
                "message": "Passwords must match."
            })
        check = request.POST['representative']
        if check == 'on':
            rep = True
        else:
            rep = False
        # Attempt to create new user
        try:
            user = User.objects.create_user(
                username, email, password, first_name=first_name, last_name=last_name, Birthday=birthdate, representative=rep)
            user.save()
        except IntegrityError:
            return render(request, "octopus/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "octopus/register.html", {
        })

# 😉️ FOR AUTHENTICATING USERS


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "octopus/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "octopus/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

# create food-bank


class CreateBankForm(ModelForm):
    class Meta:
        model = FoodBank
        fields = ['name','email','phone_number', 'about', 'opening_time', 'closing_time',
                'building_number_name', 'building_street', 'building_city',
                  'building_state', 'building_pincode', 'logo']
        widgets = {
            'opening_time': widgets.TimeInput(attrs={'type': 'time', 'class': "form-control"}),
            'closing_time': widgets.TimeInput(attrs={'type': 'time', 'class': "form-control"}),
            'logo': widgets.FileInput(attrs={'class': "form-control"}),
            'name': widgets.TextInput(attrs={'class': "form-control"}),
            'about': widgets.Textarea(attrs={'class': "form-control"}),
            'building_number_name': widgets.TextInput(attrs={'class': "form-control"}),
            'building_street': widgets.TextInput(attrs={'class': "form-control"}),
            'building_city': widgets.TextInput(attrs={'class': "form-control"}),
            'building_state': widgets.TextInput(attrs={'class': "form-control"}),
            'building_pincode': widgets.TextInput(attrs={'class': "form-control"}),
            'email': widgets.EmailInput(attrs={'class': "form-control"}),
            'phone_number': widgets.TextInput(attrs={'class': "form-control"})
        }


class CreateWorkingDay(forms.Form):
    days = forms.ModelMultipleChoiceField(
        queryset=Day.objects.all(), label="Days")


def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            data = request.POST
            creator = request.user
            name = data['name']
            about = data['about']
            email = data['email']
            phone_number = data['phone_number']
            opening_time = data['opening_time']
            closing_time = data['closing_time']
            building_number_name = data['building_number_name']
            building_street = data['building_street']
            building_city = data['building_city']
            building_state = data['building_state']
            building_pincode = data['building_pincode']
            logo = request.FILES.get('logo')

            f = FoodBank(name=name,email=email,phone_number=phone_number, about=about, opening_time=opening_time, closing_time=closing_time,
                          building_number_name=building_number_name, building_street=building_street, building_city=building_city,
                         building_state=building_state, logo=logo, creator=creator,building_pincode=building_pincode)
            f.save()

            days = data['days']
            for day in days:
                d = WorkingDays(food_bank=FoodBank.objects.get(
                    name=name), day=Day.objects.get(id=day))
                d.save()

            return HttpResponseRedirect(reverse("index"))

        else:
            form = CreateBankForm()
            day_form = CreateWorkingDay()
            return render(request, 'octopus/create.html', {
                "form": form,
                "day_form": day_form
            })
    else:
        return HttpResponseRedirect(reverse('login'))


def bank_view(request, bank_id):
    try:
        bank = FoodBank.objects.get(pk=bank_id)
    except FoodBank.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))
    return render(request, "octopus/bank.html", {
        'bank': bank,
        'days_open': WorkingDays.objects.filter(food_bank=bank)
    })


def get_today_string():
    today = datetime.datetime.now().date()
    today_as_string = f'{today.year}-{today.month}-{today.day}'
    return today_as_string


class CreateTicketForm(ModelForm):
    class Meta:
        model = RequestTicket
        fields = ['pickup_date',
                  'pickup_time', 'requested_packages'
                  ]
        widgets = {
            'requested_to': widgets.Select(attrs={'class': "form-control"}),
            'pickup_time': widgets.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'id': 'pickup_time'}),
            'pickup_date': widgets.DateInput(attrs={
                'id': 'pickup_date',
                'type': 'date',
                'min': get_today_string(),
                'max': f"{datetime.datetime.now().date().year}-12-31"
            }),
            'requested_packages': widgets.NumberInput(attrs={'class': "form-control"}),
            # 'note' : widgets.Textarea(attrs={'class':"form-control",'class':'ticket-note'})
        }


def get_bank_json(request, bank_id):
    try:
        bank = FoodBank.objects.get(pk=bank_id)
    except FoodBank.DoesNotExist:
        return JsonResponse({'error': "no such bank"})
    return JsonResponse({'opening_time': bank.opening_time, 'closing_time': bank.closing_time})


def create_ticket(request, bank_id):
    if request.user.is_authenticated:
        try:
            requested_to = FoodBank.objects.get(pk=bank_id)
        except FoodBank.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if request.user == requested_to.creator:
            return HttpResponseRedirect(reverse('index'))
        if request.method == "POST":
            data = request.POST
            requested_by = request.user
            try:
                requested_to = FoodBank.objects.get(pk=bank_id)
            except FoodBank.DoesNotExist:
                return HttpResponseRedirect(reverse('index'))
            pickup_date = data['pickup_date']
            pickup_time = data['pickup_time']
            num = data['requested_packages']
            c = RequestTicket(requested_by=request.user, requested_to=FoodBank.objects.get(pk=bank_id),
                              pickup_date=pickup_date, pickup_time=pickup_time, requested_packages=num)
            c.save()
            return HttpResponseRedirect(reverse(index))

        else:
            return render(request, 'octopus/ticket.html', {
                'form': CreateTicketForm(),
                'bank': FoodBank.objects.get(pk=bank_id),
                'days': WorkingDays.objects.filter(food_bank=FoodBank.objects.get(pk=bank_id))
            })
    else:
        return HttpResponseRedirect(reverse('index'))


def about(request):
    return render(request, 'octopus/about.html', {

    })


def my_foodbanks_view(request):
    if request.user.is_authenticated:
        creator = request.user
        my_banks = FoodBank.objects.filter(creator=creator)
        return render(request, 'octopus/mybanks.html', {
            'banks': my_banks
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def my_foodbank_view(request, bank_id):
    if request.user.is_authenticated:
        my_bank = FoodBank.objects.get(pk=bank_id)
        if my_bank.creator != request.user:
            print(my_bank.creator, request.user)
            return HttpResponseRedirect(reverse('index'))
        packages = RequestTicket.objects.filter(requested_to=my_bank)
        # packages_week = []
        # for package in packages:
        #     if package.pickup_date.strftime("%d-%m-%y") in dates_of_week():
        #         packages_week.append(package)
        #         print(packages_week)
        #     else:
        #         print(package.pickup_date.strftime("%d-%m-%y"))
        completed = RequestTicket.objects.filter(requested_to = my_bank, completed=True)
        # pending = 0
        # for package in packages_week:
        #     if package.completed:
        #         completed += 1
        #     else:
        #         pending += 1
        
        return render(request, 'octopus/mybank.html', {
            'bank': my_bank,
            'total': len(packages),
            'completed': len(completed),
            'pending': len(packages) - len(completed)
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def tickets_view(request, bank_id):
    if request.user.is_authenticated:
        try:
            bank = FoodBank.objects.get(pk=bank_id)
        except FoodBank.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if request.user == bank.creator:
            tickets = RequestTicket.objects.filter(
                requested_to=bank).order_by('pickup_date')
            return render(request, 'octopus/tickets.html', {
                'bank': bank,
                'tickets': tickets
            })
        else:
            return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponseRedirect(reverse('login'))


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'first_name',
                  'last_name', 'email', 'Birthday']
        widgets = {
            'profile_pic': widgets.FileInput(attrs={'class': "form-control"}),
            'first_name': widgets.TextInput(attrs={'class': "form-control"}),
            'last_name': widgets.TextInput(attrs={'class': "form-control"}),
            'email': widgets.EmailInput(attrs={'class': "form-control"}),
            'Birthday': widgets.DateInput(attrs={'class': "form-control"}),
        }


def edit_user(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            form = UserForm(request.POST, instance=user)
            form.save()
            return HttpResponseRedirect(reverse('view_user'))
        else:
            return render(request, 'octopus/edit_user.html', {
                'form': UserForm(instance=user)
            })
    else:
        return HttpResponseRedirect(reverse('login'))


def view_user(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'octopus/view_user.html', {
        })
    else:
        return HttpResponseRedirect(reverse('login'))


def edit_bank(request, bank_id):
    user = request.user
    if user.is_authenticated:
        try:
            bank = FoodBank.objects.get(pk=bank_id)
        except FoodBank.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if bank.creator == user:
            if request.method == "POST":
                form = CreateBankForm(request.POST, instance=bank)
                form.save()
                return HttpResponseRedirect(reverse('my_foodbank_view', args=(bank_id,)))
            else:
                return render(request, 'octopus/edit_bank.html', {
                    'form': CreateBankForm(instance=bank),
                    'bank': bank
                })
    else:
        return HttpResponseRedirect(reverse('login'))


def view_ticket(request, bank_id, ticket_id):
    user = request.user
    if user.is_authenticated:
        try:
            bank = FoodBank.objects.get(pk=bank_id)
        except FoodBank.DoesNotExist:
            return HttpResponseRedirect(reverse('index'))
        if bank.creator == user:
            try:
                ticket = RequestTicket.objects.get(pk = ticket_id)
            except FoodBank.DoesNotExist:
                return HttpResponseRedirect(reverse('index'))
            if ticket.requested_to == bank:
                return render(request, 'octopus/view_ticket.html', {
                    'ticket' : ticket
                })
            else:
                return HttpResponseRedirect(reverse('tickets_view', args=(bank_id,)))
    else:
        return HttpResponseRedirect(reverse('login'))    