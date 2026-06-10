# Create your views here.
from django.shortcuts import render, redirect
from .models import Author
from book.models import Book


def author_list_view(request):
    raw_authors = Author.get_all()
    authors_data = []

    for author in raw_authors:
        books_count = Book.objects.filter(authors=author).count()

        authors_data.append({
            'id': author.id,
            'name': author.name,
            'surname': author.surname,
            'patronymic': author.patronymic,
            'books_count': books_count,
            'can_delete': books_count == 0
        })

    return render(request, 'author/authors.html', {'authors': authors_data})


def author_create_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        surname = request.POST.get('surname', '').strip()
        patronymic = request.POST.get('patronymic', '').strip()

        if name and surname:
            Author.create(name=name, surname=surname, patronymic=patronymic)

    return redirect('author_list')


def author_create_page_view(request):
    return render(request, 'author/author_create.html')


def author_delete_view(request, author_id):
    if request.method == 'POST':
        books_count = Book.objects.filter(id=author_id).count()
        
        if books_count == 0:
            Author.delete_by_id(author_id) 

    return redirect('author_list')