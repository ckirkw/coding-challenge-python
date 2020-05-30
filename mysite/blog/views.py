from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Article, Comment

''' Renders the article list: GET /posts/ '''
def list(request):
    article_list = Article.objects.order_by('created_at')
    context = {'article_list': article_list, 'is_logged_in': request.user.is_authenticated} 
    return render(request, 'articles/list.html', context)

''' Renders the article detail page: GET /posts/1/ '''
def detail(request, article_id):
    article = None
    can_edit = False
    try:
        article = Article.objects.get(pk=article_id)
        can_edit = request.user.id == article.author.id
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    return render(request, 'articles/detail.html', {'article': article, 'can_edit': can_edit, 'is_logged_in': request.user.is_authenticated})

''' Renders the article create/edit page: GET /posts/1/edit/
    Saves an article: POST /posts/1/edit/ '''
@login_required
def edit(request, article_id):
    article = Article(author=request.user)
    if (article_id != 0):
        try:
            article = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            raise Http404('Article does not exist')
    
    if request.method == 'GET':
        if article.author.id != request.user.id:
            return redirect('detail', article_id=article_id)
        if (article_id == 0):
            article.id = 0
        return render(request, 'articles/edit.html', {'article': article})

    elif request.method == 'POST':
        article.title = request.POST['title']
        article.body = request.POST['body']
        article.save()
        return redirect('detail', article_id=article.id)

''' Saves a comment: POST /posts/1/comments/ '''
''' Retrieves all comments for an article: GET /posts/1/comments/ '''
def comments(request, article_id):
    article = None    
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404('Article does not exist')
    
    if request.method == 'GET':
        data = serializers.serialize('json', article.comment_set.all(), use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)
    
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        comment = Comment(user=request.user)
        comment.comment = request.POST['comment']
        comment.article = article
        comment.save()

        data = serializers.serialize('json', [comment, ], use_natural_foreign_keys=True)
        return JsonResponse(data, safe=False)
    
