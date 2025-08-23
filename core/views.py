from django.shortcuts import render, redirect

def home(request):
    from board.models import Announcement, Event
    announcements = Announcement.objects.filter(status='published').order_by('-publish_date')[:5]
    events = Event.objects.order_by('start_datetime')[:5]
    return render(request, 'core/home.html', {'announcements': announcements, 'events': events})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # For development: print/log. In production send email.
        print(f'Contact message from {name} <{email}>: {message}')
        return redirect('core:home')
    return render(request, 'core/contact.html')
