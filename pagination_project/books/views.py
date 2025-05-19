from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Book

def book_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__icontains=search_query) | 
            Q(published_year__icontains=search_query)
        ).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
    
    items_per_page = request.GET.get('per_page', 5)
    try:
        items_per_page = int(items_per_page)
        if items_per_page < 1:
            items_per_page = 5
        elif items_per_page > 50:
            items_per_page = 50
    except ValueError:
        items_per_page = 5
    
    paginator = Paginator(books, items_per_page)
    
    page_number = request.GET.get('page', 1)
    
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'current_per_page': items_per_page,
        'per_page_options': [5, 10, 25, 50],
        'search_query': search_query,
    }
    
    return render(request, 'books/book_list.html', context)