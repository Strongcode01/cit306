from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Announcement, Event, TimetableEntry, Result

def announcements_list(request):
    qs = Announcement.objects.filter(status='published')
    q = request.GET.get('q')
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(body__icontains=q)
    return render(request, 'board/announcements_list.html', {'announcements': qs})

def announcement_detail(request, pk):
    a = get_object_or_404(Announcement, pk=pk)
    return render(request, 'board/announcement_detail.html', {'announcement': a})

def events_list(request):
    events = Event.objects.order_by('start_datetime')
    return render(request, 'board/events_list.html', {'events': events})

def event_detail(request, pk):
    e = get_object_or_404(Event, pk=pk)
    return render(request, 'board/event_detail.html', {'event': e})

def timetable(request):
    level = request.GET.get('level')
    semester = request.GET.get('semester')
    qs = TimetableEntry.objects.all()
    if level:
        qs = qs.filter(level=level)
    if semester:
        qs = qs.filter(semester=semester)
    return render(request, 'board/timetable.html', {'timetable': qs})

def results(request):
    qs = Result.objects.order_by('-upload_date')
    return render(request, 'board/results.html', {'results': qs})

def archive(request):
    qs = Announcement.objects.filter(status='archived')
    return render(request, 'board/archive.html', {'items': qs})

def search(request):
    q = request.GET.get('q')
    results = {'announcements': [], 'events': [], 'results': []}
    if q:
        results['announcements'] = Announcement.objects.filter(title__icontains=q)[:20]
        results['events'] = Event.objects.filter(title__icontains=q)[:20]
        results['results'] = Result.objects.filter(title__icontains=q)[:20]
    return render(request, 'board/search_results.html', {'results': results, 'q': q})

@login_required
def admin_dashboard(request):
    announcements = Announcement.objects.count()
    events = Event.objects.count()
    timetables = TimetableEntry.objects.count()
    results_count = Result.objects.count()
    return render(request, 'admin_dashboard.html', {
        'announcements': announcements,
        'events': events,
        'timetables': timetables,
        'results': results_count,
    })
