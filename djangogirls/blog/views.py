from django.http import HttpResponse
from django.shortcuts import render

from blog.models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False)
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
