from django.shortcuts import render
from django.views import generic
from django.utils import timezone
# Create your views here.
class IndexView(generic.ListView):
    def index(request):
        return render(request, 'music/index.html')

class AboutView(generic.ListView):
    def about(request):
        return render(request, 'music/about.html')