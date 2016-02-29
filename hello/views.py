from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Item, List


# Create your views here.
def index(request):
    return render(request,
                  'index.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


def new_list(request):
    list_ = List()
    list_.save()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-only-list-in-the-world/')
hello = None
