from django.shortcuts import render,redirect,reverse
from utils.decorators import login_required
import re
from django.http import JsonResponse
from users.models import Passport,Address
from django.core.paginator import Paginator
from order.models import OrderInfo,OrderBooks
from books.models import Books
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from users.tasks import send_active_email
# Create your views here.
def register(request):
    return render(request,'users/register.html')
def register_handle(request):
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    if not all ([username,password,email]):
        return render(request,'users/register.html',{'errmsg':'參數不能爲空!'})
    if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request,'users/register.html',{'errmsg':'郵箱不合法'})
    p = Pssport.objects.check_passport(username=username)
    if p:
        return render(request,'users/register.html',{'errmsg':'用戶名已經存在'})
    passport = Passport.objects.add_one_passport(username=username,password=password,email=email)
    serializer = Serializer(settings.SECRET_KEY,3600)
    token = serializer.dumps({'confirm':passport.id})
    token = token.decode()
    send_mail('书城用户激活','',settings.EMAIL_FROM,[email],html_message='<a href="http://127.0.0.1:8000/user/active/%s/">http://127.0.0.1:8000/user/active/</a>' % token)
    send_active_email.delay(token,username,email)
    return redirect(reverse('books:index'))
def login(request):
    if request.COOKIES.get('username'):
        username = request.COOKIES.get('username')
        checked = 'checked'
    else:
        username = ''
        checked = ''
        context = {
            'username':username,
            'checked':checked,
}
        return render(request,'users/login.html',context)
def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember = request.POST.get('remember')
    #email = request.POST.get('email')
    
    if not all([username,password,remember]):
        return JsonResponse({'res':2})
    passport = Passport.objects.get_one_passport(username=username,password=password)
    if passport:
        next_url = reverse('books:index')
        jres = JsonResponse({'res':1,'next_url':next_url})
        if remember == 'true':
            jres,delete_cooie('username')
        request.session['islogin']= True
        request.session['username'] = username
        request.session['passport_id'] = passport.id
        return jres
    else:
        return JsonResponse({'res':0})

def logout(request):
    request.session.flush()
    return redirect(reverse('books:index'))
@login_required
def user(request):
    passport_id = request.session.get('passport_id')
    addr = Address.objects.get_default_address(passport_id=passport_id)
    books_li = []
    context = {
        'addr':addr,
        'page':'user',
        'books_li':books_li
}
    return render(request,'users/user_center_info.html',context)

@login_required
def address(request):
    '''用户中心-地址页'''
    # 获取登录用户的id
    passport_id = request.session.get('passport_id')

    if request.method == 'GET':
        # 显示地址页面
        # 查询用户的默认地址
        addr = Address.objects.get_default_address(passport_id=passport_id)
        return render(request, 'users/user_center_site.html', {'addr': addr, 'page': 'address'})
    else:
        # 添加收货地址
        # 1.接收数据
        recipient_name = request.POST.get('username')
        recipient_addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        recipient_phone = request.POST.get('phone')

        # 2.进行校验
        if not all([recipient_name, recipient_addr, zip_code, recipient_phone]):
            return render(request, 'users/user_center_site.html', {'errmsg': '参数不必为空!'})

        # 3.添加收货地址
        Address.objects.add_one_address(passport_id=passport_id,
                                        recipient_name=recipient_name,
                                        recipient_addr=recipient_addr,
                                        zip_code=zip_code,
                                        recipient_phone=recipient_phone)

        # 4.返回应答
        return redirect(reverse('user:address'))

@login_required
def order(request,page):
    passport_id = request.session.get('passport_id')
    order_li = OrderInfo.objects.filter(passport_id=passport_id)
    for order in order_li:
        order_id = order.order_id
        order_books_li = OrderBooks.objects.filter(order_id=order_id)
        for order_books in order_books_li:
            count = order_boojs.count
            price = order_books.price
            amount = count * price
            order_books.amount = amount
        order.order_books_li = order_books_li
    paginator = Paginator(order_li,3)
    num_pages = paginator.num_pages
    if not page:
        page = 1
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)
    order_li = paginator.page(page)
    if num_pages < 5:
        pages = range(1,6)
    elif num_pages - page <= 2:
        pages = range(bun_pages - 4,num_pages +1)
    else:
        pages = range(page -2 ,page +3)
    context = {
        'order_li':order_li,
        'pages':pages,
}
    return render(request,'users/user_center_order.html',context)

