from django.shortcuts import render
from .models import TeamMember

def credentials(request):
    members = TeamMember.objects.all()
    return render(request, 'team/credentials.html', {'members': members})
