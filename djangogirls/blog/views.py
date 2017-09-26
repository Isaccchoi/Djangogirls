from django.shortcuts import render, get_object_or_404

from blog.models import Post


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False)
    context = {
        # posts key의 value는 Queryset
        'posts': posts
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    context = {'post': post}
    return render(request, 'blog/post_detail.html', context)
