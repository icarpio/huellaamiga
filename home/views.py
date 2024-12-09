from django.shortcuts import render
from django.shortcuts import render, redirect
from huellapp.models import Animal
from huellapp.forms import AnimalForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    # Get all scores, ordered by score in descending order
    animals_list = Animal.objects.order_by('-created_at')
    
    # Set up pagination (10 items per page)
    paginator = Paginator(animals_list, 10)
    
    # Get the current page number from the request
    page = request.GET.get('page', 1)
    
    try:
        # Try to get the specified page
        animals = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        animals = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        animals = paginator.page(paginator.num_pages)
    
    # Context to pass to the template
    context = {
        'animals': animals,
        'total_animals': animals_list.count()
    }
    
    return render(request, 'home/index.html', context)

