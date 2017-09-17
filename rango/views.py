from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from registration.backends.simple.views import RegistrationView
from datetime import datetime


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    # visits = int(request.COOKIES.get('visits', '1'))
    # last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    # last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")
    print(visits)
    print(last_visit_time)
    if (datetime.now() - last_visit_time).seconds > 0:
        print((datetime.now() - last_visit_time).seconds)
        visits = visits + 1
        # response.set_cookie('last_visit', str(datetime.now()))
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # response.set_cookie('last_visit', last_visit_cookie)
        request.session['last_visit'] = last_visit_cookie
    # response.set_cookie('visits', visits)
    request.session['visits'] = visits


def index(request):
    # request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]
    category_dict = {'categories': category_list, 'pages': pages_list}
    visitor_cookie_handler(request)
    # category_dict['visits'] = request.COOKIES.get('visits')
    category_dict['visits'] = request.session['visits']
    category_dict['last_visit'] = datetime.strptime(request.session['last_visit'][:-7], "%Y-%m-%d %H:%M:%S")
    # context = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
    response = render(request, 'rango/index.html', context=category_dict)
    return response


def about(request):
    # if request.session.test_cookie_worked():
    #     print('Test cookie worked')
    #     request.session.delete_test_cookie()
    # return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
    context = {'boldmessage': "This tutorial has been put together by jack."}
    visitor_cookie_handler(request)
    context['visits'] = request.session['visits']
    context['last_visit'] = datetime.strptime(request.session['last_visit'][:-7], "%Y-%m-%d %H:%M:%S")
    # return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
    return render(request, 'rango/about.html', context=context)


# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    if request.user.is_authenticated():
        form = CategoryForm()
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                cat = form.save(commit=True)
                print(cat, cat.slug)
                return index(request)
            else:
                print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})
    else:
        return HttpResponse("You are not logged in.")


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                print(page)
                return show_category(request, category_name_slug)
            else:
                print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         userform = UserForm(data=request.POST)
#         userprofileform = UserProfileForm(data=request.POST)
#         print(userform, userprofileform)
#         if userform.is_valid() and userprofileform.is_valid():
#             user = userform.save()
#             print(user)
#             user.set_password(user.password)
#             print(user.password)
#             user.save()
#             profile = userprofileform.save(commit=False)
#             profile.user = user
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#             profile.save()
#             registered = True
#         else:
#             print(userform.errors, userprofileform.errors)
#     else:
#         userform = UserForm()
#         userprofileform = UserProfileForm()
#     return render(request, 'rango/register.html',
#                   {'userform': userform, 'userprofileform': userprofileform, 'registered': registered})


# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         print(user)
#         print(type(user))
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('rango:index'))
#             else:
#                 return HttpResponse('Your rango account is disable')
#         else:
#             print("Invalid login details: {0}, {1}".format(username, password))
#             return HttpResponse("Invalid login details supplied.")
#     else:
#         return render(request, 'rango/login.html', {})


# @login_required
# def log_out(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('rango:index'))

# class MyRegistrationView(RegistrationView):
#     def get_success_url(self, user):
#         return '/rango/'



@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
