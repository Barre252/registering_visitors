from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import CustomUser, VisitorRegistration
from .forms import LoginForm, VisitorsForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from django.contrib import messages
from django.contrib.auth import logout

from datetime import date, datetime, time
from django.utils.timezone import localdate, now, make_aware
from django.utils import timezone

from django.http import JsonResponse

# Create your views here.

@login_required(login_url=reverse_lazy('login_page'))
def dashboard(request):
    today = timezone.localdate()

    start_datetime = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_datetime = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    records = VisitorRegistration.objects.all()
    # todays_records = VisitorRegistration.objects.filter(
    #     check_in_date__range=(start_datetime, end_datetime)
    # )

    context = {
        'records': records,
        # 'todays_records': todays_records,
        'today': today,
    }
    return render(request, 'visitor_app/dashboard.html', context)

def get_today_visits(request):
    today = timezone.localdate()
    start_dt = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    end_dt = timezone.make_aware(datetime.combine(today, datetime.max.time()))

    visits = VisitorRegistration.objects.filter(
        check_in_date__range=(start_dt, end_dt)
    ).order_by('-check_in_date')

    data = []
    for v in visits:
        if v.hours_to_stay:
            total_seconds = v.hours_to_stay.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)

            if hours and minutes:
                duration_str = f"{hours} hour{'s' if hours != 1 else ''} {minutes} minute{'s' if minutes != 1 else ''}"
            elif hours:
                duration_str = f"{hours} hour{'s' if hours != 1 else ''}"
            elif minutes:
                duration_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
            else:
                duration_str = "0 minutes"
        else:
            duration_str = "N/A"

        data.append({
            'id': v.id,
            'full_name': v.full_name,
            'phone_number': v.phone_number,
            'person_to_visit': v.person_to_visit,
            'civil_servant': "Yes" if v.civil_servant else "No",
            'visit_reason': v.visit_reason,
            'hours_to_stay': duration_str,
            'check_in_date': timezone.localtime(v.check_in_date).strftime('%Y-%m-%d %H:%M:%S'),
        })

    return JsonResponse({'records': data})

def register_visitor(request):
    
    form = VisitorsForm()

    if request.method == "POST":
         form = VisitorsForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('after_registration')
         
    context = {'form':form}
    return render(request, 'visitor_app/register_visitor.html', context)


@login_required(login_url=reverse_lazy('login_page'))
def after_registration(request):
    return render(request, 'visitor_app/after_registration.html')



# Login function
def login_page(request):
    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')


            user = authenticate(request, username=username, password=password)


            if user is not None:
                auth.login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url) if next_url else redirect('dashboard')


    context = {'form':form}

    return render(request, 'visitor_app/login_page.html', context)


# Logout Function
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login_page')