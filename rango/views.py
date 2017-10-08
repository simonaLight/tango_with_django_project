from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, User, UserProfile, Comment
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from registration.backends.default.views import RegistrationView
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
    # print(visits)
    # print(last_visit_time)
    if (datetime.now() - last_visit_time).seconds > 0:
        # print((datetime.now() - last_visit_time).seconds)
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
    # category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-pub_time')[:5]
    # category_dict = {'categories': category_list, 'pages': pages_list}
    category_dict = {'pages': pages_list}
    visitor_cookie_handler(request)
    # category_dict['visits'] = request.COOKIES.get('visits')
    category_dict['visits'] = request.session['visits']
    category_dict['last_visit'] = datetime.strptime(request.session['last_visit'][:-7], "%Y-%m-%d %H:%M:%S")
    # context = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # return HttpResponse("Rango says hey there partner! <br/> <a href='/rango/about/'>About</a>")
    response = render(request, 'rango/index.html', context=category_dict)
    print(response)
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
        pages = Page.objects.filter(category=category).order_by('-views')
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
#         return HttpResponseRedirect(reverse('rango:about'))


@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")


def track_url(request):
    page_id = None
    if request.method == 'GET':
        print(request)
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                comments = Comment.objects.filter(page_id=page_id)
                print(comments)
                page.views = page.views + 1
                page.save()
            except Exception:
                pass
        return render(request, 'rango/page.html', {'page': page, 'comments': comments})




@login_required
def profile_registration(request):
    userprofileform = UserProfileForm()
    if request.method == 'POST':
        userprofileform = UserProfileForm(request.POST, request.FILES)
        if userprofileform.is_valid():
            user_profile = userprofileform.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('rango:index')
        else:
            print(userprofileform.errors)
    context_dict = {'form': userprofileform}
    return render(request, 'rango/profile_registration.html', context_dict)


@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('rango:index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    print(userprofile)
    print(type(userprofile))
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
    print(form)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def list_profiles(request):
    userprofile_list = User.objects.all()
    print(userprofile_list)
    profile_list = UserProfile.objects.all()
    print(profile_list)
    return render(request, 'rango/list_profile.html',
                  {'userprofile_list': userprofile_list, 'profile_list': profile_list})


@login_required
def user_delete(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('rango:list_profile')


@login_required
def like_category(request):
    cat_id = None
    print(request)
    if request.method == 'GET':
        cat_id = request.GET['category_id']
    print(cat_id)
    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)


@login_required
def comment(request, page_id):
    try:
        page = Page.objects.get(id=page_id)
        category = Category.objects.filter(id=page.category_id)
        print(category)
    except Page.DoesNotExist:
        page = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if page:
                comment = form.save(commit=False)
                comment.page = page
                comment.save()
                return index(request)
            else:
                print(form.errors)
    else:
        form = CommentForm()
    context_dict = {'form': form, 'page': page}
    return render(request, 'rango/comment.html', context_dict)
