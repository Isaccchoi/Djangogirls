from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.models import Post

User = get_user_model()


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    context = {
        # posts key의 value는 Queryset
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return HttpResponse("페이지가 존재하지 않습니다.", status=404)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)


def post_add(request):
    if request.method == 'POST' and request.POST.get('title') and request.POST.get('content'):
        title = request.POST['title']
        content = request.POST['content']
        author = User.objects.get(username='admin')
        post = Post.objects.create(
            title=title,
            content=content,
            author=author,
        )
        if request.POST.get('publish'):
            post.publish()
        return redirect('post_detail', pk=post.pk)
    elif request.method == 'GET':
        context = {

        }
        return render(request, 'blog/post_form.html', context)
    elif request.method == 'POST' and not request.POST.get('title') or not request.POST.get('content'):
        context = {
            'alert': True
        }
        return render(request, 'blog/post_form.html', context)
    else:
        context = {

        }
        return render(request, 'blog/post_form.html', context)


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    return redirect('post_detail', pk=pk)
