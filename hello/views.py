from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Greeting, Item


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')
    return render(request,
                  'index.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

hello = None