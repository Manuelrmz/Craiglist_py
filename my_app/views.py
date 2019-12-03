from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from .models import Search

# Create your views here.
BASE_CRAIGLIST_URL = 'https://monterrey.craigslist.org/search/?query={}'


def home(request):
    return render(request, 'base.html')


def new_search(request):
    stuff_for_frontend = {}
    if request.method == 'POST':
        search = request.POST.get('search')
        Search.objects.create(search=search)
        final_url = BASE_CRAIGLIST_URL.format(quote_plus(search))
        # Getting body of the html from final url
        response = requests.get(final_url)
        # Extracting the source code of the page
        data = response.text
        #Passing the source code to Beautifil Soup to create a BeautifilSoup object for it
        soup = BeautifulSoup(data, features='html.parser')
        #Extracting all the <a> tags whose class name is 'result-title' into a list
        post_listing = soup.find_all('li', {'class': 'result-row'})
        final_postings = []
        for post in post_listing:
            post_title = post.find(class_='result-title').text
            post_url = post.find('a').get('href')
            if post.find(class_='result-price'):
                post_price = post.find(class_='result-price').text
            else:
                post_price = 'N/A'
                
            if post.find(class_='result-image').get('data-ids'):
                post_image_id = post.find(class_='result-image').get('data-ids').split(',')[0].split(':')[1]
                print(post_image_id)
                post_image_url = "https://images.craigslist.org/{}_300x300.jpg".format(post_image_id)
            else:
                post_image_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSnOVJl3wmLObFPGSFoXwCapIPqhQaB9J23eMILwUpt3Iwkvxr0'

            final_postings.append((post_title, post_url, post_price, post_image_url))

        stuff_for_frontend = {'search': search, 'final_postings' : final_postings}
    return render(request, 'my_app/new_search.html', stuff_for_frontend)
