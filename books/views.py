from django.shortcuts import render,redirect
from books.models import Books
from books.enums import *
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    python_new = Books.objects.get_books_by_type(PYTHON,limit=3,sort='new')
    python_hot = Books.objects.get_books_by_type(PYTHON,limit=4,sort='hot')
    
    javascript_new = Books.objects.get_books_by_type(JAVASCRIPT,limit=3,sort='new')
    javascript_hot = Books.objects.get_books_by_type(JAVASCRIPT,limit=4,sort='hot')
    
    
    algorithms_new = Books.objects.get_books_by_type(ALGORITHMS,limit=3,sort='new')
    algorithms_hot = Books.objects.get_books_by_type(ALGORITHMS,limit=4,sort='hot')
    
    machinelearning_new = Books.objects.get_books_by_type(MACHINELEARNING,3,sort='new')
    machinelearning_hot = Books.objects.get_books_by_type(MACHINELEARNING,4,sort='hot')
    
    operatingsystem_new = Books.objects.get_books_by_type(OPERATINGSYSTEM,3,sort='new')
    operatingsystem_hot = Books.objects.get_books_by_type(OPERATINGSYSTEM,4,sort='hot')
    
    database_new = Books.objects.get_books_by_type(DATABASE,3,sort='new')
    database_hot = Books.objects.get_books_by_type(DATABASE,4,sort='hot')

    context = {
        'python_new':python_new,
        'python_hot':python_hot,
        'javascript_new':javascript_new,
        'javascript_hot':javascript_hot,
        'algorithms_new':algorithms_new,
        'algorithms_hot':algorithms_hot,
        'machinelearning_new':machinelearning_new,
        'machinelearning_hot':machinelearning_hot,
        'operatingsystem_new':operatingsystem_new,
        'operatingsystem_hot':operatingsystem_hot, 
        'database_new':database_new,
        'database_hot':database_hot,
}
    return render(request,'books/index.html',context)
def detail(request,books_id):
    books = Books.objects.get_books_by_id(books_id=books_id)
    if books is None:
        return redirect(reverse('books:index'))
    books_li = Books.objects.get_books_by_type(type_id=books.type_id,limit=2,sort='new')
    type_title = BOOKS_TYPE[books.type_id]
    context = {'books':books,'books_li':books_li,'type_title':type_title}
    return render(request,'books/detail.html',context)
