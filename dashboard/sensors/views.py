from django.shortcuts import render
from django.utils import timezone
from .models import Log

# Create your views here.
def log_list(request):
	logs = Log.objects.all()
	return render(request, 'sensors/log_list.html', {'logs':logs})
