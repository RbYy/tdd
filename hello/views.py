from django.shortcuts import render, redirect

from django.http import HttpResponse

from .models import Greeting, Item


# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    items = Item.objects.all()
    return render(request,
        'index.html', {'items': items})


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

hello = None