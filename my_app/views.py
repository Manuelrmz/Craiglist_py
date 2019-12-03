from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

# Create your views here.
BASE_CRAIGLIST_URL = 'https://monterrey.craigslist.org/search/hhh?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    stuff_for_frontend = {}
    if request.method == 'POST':
        search = request.POST.get('search')
        Search.objects.create(search=search)
        final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
        response = requests.get(final_url)
        data = response.text
        stuff_for_frontend = {'search': search}
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
