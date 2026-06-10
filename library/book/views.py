from django.shortcuts import render
from book.models import Book

def book_list(request):
    books = Book.get_all()
    return render(request, 'book/book_list.html', {'books': books})

def book_detail(request, book_id):
    book = Book.get_by_id(book_id)
    return render(request, 'book/book_detail.html', {'book': book})

def book_search(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(name__icontains=query)
    return render(request, 'book/book_search.html', {'books': books, 'query': query})