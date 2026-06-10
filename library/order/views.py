from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime
from order.models import Order
from book.models import Book

def order_list_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    is_librarian = (request.user.role == 1)
    
    current_view = request.GET.get('view', 'my')
    if not is_librarian:
        current_view = 'my'

    if current_view == 'all' and is_librarian:
        orders = Order.objects.all().select_related('user', 'book')
    else:
        orders = Order.objects.filter(user=request.user).select_related('book')

    available_books = Book.objects.filter(count__gt=1)

    context = {
        'orders': orders,
        'available_books': available_books,
        'is_librarian': is_librarian,
        'current_view': current_view,
        'user_name': request.user.first_name or request.user.email
    }
    return render(request, 'order/order.html', context)


def order_create_view(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        plated_end_at_raw = request.POST.get('plated_end_at')

        if book_id and plated_end_at_raw:
            try:
                book = Book.objects.get(id=book_id)
                plated_end_at = timezone.make_aware(datetime.strptime(plated_end_at_raw, '%Y-%m-%d'))
                
                Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
            except (Book.DoesNotExist, ValueError):
                pass

    return redirect('/orders/?view=my')


def order_close_view(request, order_id):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.role == 1:
            order = Order.get_by_id(order_id)
            if order and order.end_at is None:
                order.update(end_at=timezone.now())

                book = order.book
                book.count += 1
                book.save()

    return redirect('/orders/?view=all')