from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from .models import MainMenu, Book, Order, OrderItem, RecommendedBook
from .forms import BookForm, ReviewForm

from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail
from django.conf import settings

from django.utils import timezone
from django.views.decorators.http import require_POST

# Create your views here.


def returnpolicy(request):

    return render(request, 'bookMng/returnpolicy.html', 
    {
        'item_list': MainMenu.objects.all()
    }
    )

@login_required(login_url=reverse_lazy('login'))
def contact(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        fromemail = request.POST['fromemail']
        message = request.POST['message']
        send_mail('Message from ' + firstname + ' ' + lastname,
                  message,
                  fromemail,
                  [settings.EMAIL_HOST_USER],
                  fail_silently=False)
        return render(request, 'bookMng/contact.html', {'firstname': firstname})

    else:
        return render(request, 'bookMng/contact.html', {'item_list': MainMenu.objects.all(),})


@login_required(login_url=reverse_lazy('login'))
def index(request):
    # return HttpResponse("<h1 align='center'>Helloooo World</h1> <h2>This is a try</h2>")
    # return render(request, 'bookMng/displaybooks.html')
    return render(request,
                  'bookMng/home.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def cart(request):
    user = request.user

    # create object or query existing object
    order, created = Order.objects.get_or_create(user=user, complete=False)
    # it will get all the orderitems that have order as the parent 
    items = order.orderitem_set.all()

    for item in items:
        item.book.picture = str(item.book.picture)[6:]

    return render(request, 'bookMng/cart.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'items': items,
                      'order': order
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def addtocart(request):
    user = request.user

    bookid = request.GET.get('id', '')
    book = Book.objects.get(id=bookid)

    # create order / find incompete order for current user
    order, created = Order.objects.get_or_create(user=user, complete=False)

    # create order item / find existing order item, modify item quantity
    OrderItem.objects.get_or_create(book=book, order=order)

    # get all the iterms for that order
    items = order.orderitem_set.all()

    tochange = -1

    for item in items:
        if item.book.id == int(bookid):
            tochange = item

    if tochange != -1:

        if 'fromcart' in request.GET:
            print('im getting called fromcart')
            tochange.quantity += 1
            tochange.save()

        if 'arrowup' in request.GET:
            tochange.quantity += 1
            tochange.save()
            return HttpResponseRedirect('/cart')

        if 'arrowdown' in request.GET:
            tochange.quantity -= 1
            # remove cart item if item quantity is 0
            if tochange.quantity == 0:
                for item in items:
                    if item.quantity == 0:
                        item.delete()

            else:
                tochange.save()
            return HttpResponseRedirect('/cart')

    return HttpResponseRedirect('/displaybooks')


@login_required(login_url=reverse_lazy('login'))
def checkout(request):
    user = request.user

    # create object or query existing object
    order, created = Order.objects.get_or_create(user=user, complete=False)
    # it will get all the orderitems that have order as the parent 
    items = order.orderitem_set.all()

    for item in items:
        item.book.picture = str(item.book.picture)[6:]

    return render(request, 'bookMng/checkout.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'items': items,
                      'order': order

                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def placeorder(request):
    user = request.user;

    order, created = Order.objects.get_or_create(user=user, complete=False)
    items = order.orderitem_set.all()

    if items.count() > 0:
        order.complete = True
        order.save()
    elif items.count() == 0:
        return HttpResponseRedirect('/displaybooks')

    return render(request, 'bookMng/order_placed.html',
                  {
                      'item_list': MainMenu.objects.all(),
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def purchasehistory(request):
    user = request.user
    orders = Order.objects.filter(complete=True, user=user)

    items = []

    for order in orders:
        orderitems = order.orderitem_set.all()
        for item in orderitems:
            item.book.picture = str(item.book.picture)[6:]

        items.append(orderitems)

    print(orders)
    print(items)

    return render(request, 'bookMng/purchase_history.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'items': items,
                      'order': orders,
                      'ordercount': orders.count()
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def displaybooks(request):
    books = Book.objects.filter(taken_down=False)
    for b in books:
        b.picture = str(b.picture)[6:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


@login_required(login_url=reverse_lazy('login'))
def recommendedbooks(request):
    books = Book.objects.filter(taken_down=False,  recommended=True)
    for b in books:
        b.picture = str(b.picture)[6:]
    return render(request,
                  'bookMng/recommendedbooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


@login_required(login_url=reverse_lazy('login'))
def mybooks(request):
    books = Book.objects.filter(username=request.user)
    for b in books:
        b.picture = str(b.picture)[6:]
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  })


@login_required(login_url=reverse_lazy('login'))
def book_takedown(request, book_id):
    book = Book.objects.get(id=book_id)
    if book.taken_down == False:
        book.taken_down = True
    else:
        book.taken_down = False
    book.save()
    return render(request,
                  'bookMng/book_takedown.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'taken_down': book.taken_down
                  })


@login_required(login_url=reverse_lazy('login'))
def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def book_detail(request, book_id):
    book = Book.objects.get(id=book_id)
    picture = str(book.picture)[6:]
    reviews = book.review_set.all()
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'picture': picture,
                      'reviews': reviews
                  }
                  )


@login_required(login_url=reverse_lazy('login'))
def postreview(request, book_id):
    submitted = False
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.review_set.all()
    if request.method == 'POST':
        form = ReviewForm(data=request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            return HttpResponseRedirect('/book_detail/{}'.format(book_id))

    else:
        form = ReviewForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'bookMng/postreview.html',
                  {
                      'book': book,
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'reviews': reviews,
                  })


@login_required(login_url=reverse_lazy('login'))
def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        try:
            book = Book.objects.get(name=search)
        except:
            return HttpResponseRedirect('/displaybooks')

        if book.taken_down == True:
            return HttpResponseRedirect('/displaybooks')
        picture = str(book.picture)[6:]
        reviews = book.review_set.all()
        return render(request,
                      'bookMng/book_detail.html',
                      {
                          'item_list': MainMenu.objects.all(),
                          'book': book,
                          'picture': picture,
                          'reviews': reviews
                      })


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)
 