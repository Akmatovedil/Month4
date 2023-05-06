from django.shortcuts import render, HttpResponse, Http404, redirect
from news.models import News, Comment, Category
from .forms import NewsCreateForm, UserCreateForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.db.models import Q
from django.views.generic import TemplateView, ListView, FormView


class NewsCreateView(FormView):
    form_class = NewsCreateForm
    template_name = 'add_news.html'
    success_url = '/news/'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            return redirect('/add_news/')


class CategoryNewsListView(ListView):
    model = News

    def get_queryset(self):
        return News.objects.filter(
            category_id=self.request.resolver_match.kwargs['id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryNewsListView, self).get_context_data()
        category_id = self.request.resolver_match.kwargs['id']
        try:
            category = Category.objects.get(id=category_id)
        except:
            raise Http404
        context['title'] = category.title
        context['categories'] = Category.objects.all()
        return context


class IndexView(TemplateView):
    template_name = 'index.html'

    def gef(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['color'] = 'GREEN'
        context['number'] = 10
        context['list'] = [1, 2, 3]
        context['categories'] = Category.objects.all()
        return self.render_to_response(context)


class RegisterView(TemplateView):
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': UserCreateForm(),
            'categories': Category.objects.all()
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username,
                                     password=password,
                                     email=email,
                                     is_active=True)
            return redirect('/login/')
        else:
            context = {
                'form': form,
                'categories': Category.objects.all()
            }
            return self.render_to_response(context)


def main_view(request):
    return HttpResponse("<h1>Welcome to Home Page<h1>")


PAGE_SIZE = 3


def news_list_view(request):
    page = int(request.GET.get('page', 1))
    all_news = News.objects.all()
    queryset = News.objects.all()[PAGE_SIZE * (page - 1): PAGE_SIZE * page]
    if all_news.count() % PAGE_SIZE == 0:
        count_buttons = all_news.count() // PAGE_SIZE
    else:
        count_buttons = all_news.count() // PAGE_SIZE + 1
    context = {
        'title': 'All news',
        'news_list': queryset,
        'next': page + 1,
        'next_disabled': 'disabled' if page >= count_buttons else '',
        'prev': page - 1,
        'prev_disabled': 'disabled' if page == 1 else '',
        'page': page,
        'categories': Category.objects.all(),
        'buttons': [i for i in range(1, count_buttons + 1)]

    }
    return render(request, 'news.html', context=context)


def news_item_view(request, id):
    try:
        detail = News.objects.get(id=id)
    except News.DoesNotExist:
        raise Http404('News not found')
    if request.method == 'GET':
        context = {
            'news_detail': detail,
            'comments': Comment.objects.filter(news_id=id),
            'categories': Category.objects.all()
        }
        return render(request, 'detail.html', context=context)
    else:
        author = request.POST.get('author')
        text = request.POST.get('text')
        Comment.objects.create(
            author=author,
            text=text,
            news_id=id
        )
        return redirect(f'/news/{id}/')


def category_news_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except:
        raise Http404()
    context = {
        'title': category.title,
        'news_list': News.objects.filter(category_id=id),
        'categories': Category.objects.all()
    }
    return render(request, 'news/news_list.html', context=context)


def login_view(request):
    context = {
        'form': LoginForm(),
        'categories': Category.objects.all()
    }
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/news/')
            return redirect('/login/')
    return render(request, 'login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/news/')


def search_view(request):
    search = request.GET.get('search_word', '')
    queryset = News.objects.filter(Q(title__icontains=search)
                                   | Q(text__icontains=search))
    context = {
        'title': 'Results of search....' if queryset else 'News not found by yout search word!!!',
        'news_list': queryset,
        'categories': Category.objects.all()

    }
    return render(request, 'search.html', context=context)
