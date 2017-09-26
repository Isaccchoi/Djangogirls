from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

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
        post = Post(
            title=title,
            content=content,
            author=author,
            )
        post.publish()
        return redirect('post_detail', pk=post.pk)
    else:
        context = {

        }
        return render(request, 'blog/post_form.html', context)
