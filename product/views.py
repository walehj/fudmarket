from __future__ import unicode_literals


from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product, Images, City, Category, Profile
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.views.generic.edit import CreateView
from django.forms import modelformset_factory
from .forms import PostCreateForm, UserLoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def classifiedView(request, category_slug=None):
    category = None
    classifiedView = Product.objects.all()
    city_list = City.objects.all()
    ads_cat = Category.objects.annotate(total_products=Count('product'))

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        classifiedView = classifiedView.filter(category=category)

    search_query = request.GET.get('q')
    if search_query:
        classifiedView = classifiedView.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(condition__icontains=search_query) |
            Q(brand__brand_name__icontains=search_query) |
            Q(category__category_name__icontains=search_query)
        )

    paginator = Paginator(classifiedView, 2)  # Show 25 contacts per page
    page = request.GET.get('page')
    classifiedView = paginator.get_page(page)
    template = 'classified.html'
    context = {'classified_list': classifiedView,
               'city_list': city_list, 'ads_cat': ads_cat}
    return render(request, template, context)


def howitworksView(request):
    template = 'howitworks.html'
    return render(request, template)


def singleView(request, product_slug):
    singleView = Product.objects.get(slug=product_slug)
    productimages = Images.objects.filter(post=singleView)
    template = 'single.html'
    context = {'singleView': singleView, 'product_images': productimages}
    if request == singleView:
        view = Product.views_count
        #count = Product.objects.get(views)
        view += 1
    return render(request, template, context)


def categoryView(request):
    categoryView = Product.objects.all()
    template = 'categories.html'
    context = {'category_list': categoryView}
    return render(request, template, context)


def Contact(request):
    template = 'contact.html'
    return render(request, template)


def help(request):
    template = 'help.html'
    return render(request, template)


def privacy(request):
    template = 'privacy.html'
    return render(request, template)


def terms(request):
    template = 'terms.html'
    return render(request, template)


def home(request):
    homeview = Product.objects.all()
    template = 'index.html'
    context = {'home': homeview}
    return render(request, template, context)


@login_required
def post_create(request):
    ImageFormset = modelformset_factory(Images, fields=('image',), extra=4)
    if request.method == 'POST':
        form = PostCreateForm(request.POST or None, request.FILES or None)
        formset = ImageFormset(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()

            for f in formset:
                try:
                    photo = Images(post=post, image=f.cleaned_data['image'])
                    photo.save()
                except Exception as e:
                    break
            return redirect('classified')
    else:
        form = PostCreateForm()
        formset = ImageFormset(queryset=Images.objects.none())
    template = 'post-ad.html'
    context = {'form': form, 'formset': formset}
    return render(request, template, context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('classified'))
                else:
                    return HttpResponse("User is not active")
            else:
                return HttpResponse("user is None")
    else:
        form = UserLoginForm()

    template = 'signin.html'
    context = {'form': form}
    return render(request, template, context)


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return redirect('classified')
    else:
        form = UserRegistrationForm()
    template = 'registration/signup.html'
    context = {'form': form}
    return render(request, template, context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(
            data=request.POST or None, instance=request.user)
        profile_form = ProfileEditForm(
            data=request.POST or None, instance=request.user.profile, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse("classified"))
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
    template = 'edit_profile.html'
    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, template, context)


def base(request):
    caty = Category.objects.all()
    template = 'base.html'
    context = {'caty': caty}
    return render(request, template, context)
