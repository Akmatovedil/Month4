from django.shortcuts import render, HttpResponse, Http404, redirect
from news.models import News, Comment, Category
from .forms import NewsCreateForm

def main_view(request):
    return HttpResponse("<h1>Welcome to Home Page<h1>")


def index_view(request):
    dict = {
        'color': 'red',
        'number': 'six',
        'list': [1, 2, 3, 4, 5, 6]
    }
    return render(request, 'index.html', context=dict)


def news_list_view(request):
    queryset = News.objects.all()
    context = {
        'title': 'All news',
        'news_list': queryset,
        'categories': Category.objects.all()

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
        'news_list': News.objects.filter(category_id = id),
        'categories': Category.objects.all()
    }
    return render(request, 'news.html', context=context)


def news_create_view(request):
    if request.method == 'GET':
        context = {
            'form': NewsCreateForm(),
            'categories': Category.objects.all()
        }
        return render(request, 'add_news.html', context=context)
    else:
        form = NewsCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/news')
        return render(request, 'add_news.html', context={
            'form': form,
            'categories': Category.objects.all()
        })