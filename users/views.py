from django.shortcuts import render,redirect,reverse
import re
from users.models import Passport
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
    try:
        Passport.objects.add_one_passport(username=username,password=password,email=email)
    except:
        return render(request,'users/register.html',{'errmsg':'用戶名已經存在'})
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
    email = request.POST.get('email')
    
    if not all([username,password,renenber]):
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

