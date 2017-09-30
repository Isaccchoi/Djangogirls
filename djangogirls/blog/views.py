from django.contrib.auth import get_user_model
from django.core import paginator
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

from blog.models import Post

User = get_user_model()


def post_list(request):
    posts = Post.objects.filter(published_date__isnull=False).order_by('-published_date')
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        post_list = paginator.page(paginator.num_pages)
    context = {
        # posts key의 value는 Queryset
        'post_list': post_list,
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
    # request 메소드가 POST이며 title 및 content가 잘 들어 있을 경우
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            author = User.objects.get(username='admin')
            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
            )
            # publish에 체크를 할 경우 자동으로 현재 시간에 맞춰 published_date를 넣고 한번 더 저장
            if request.POST.get('publish'):
                post.publish()
            return redirect('post_detail', pk=post.pk)
        # FIXME
    # request 메소드가 GET일 경우 입력할 수 있는 form 제공
    else:
        context = {

        }
    return render(request, 'blog/post_form.html', context)


def post_delete(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('post_list')
    # POST 접근이 아닐 경우 해당 요청한 pk의 detail page로 이동
    return redirect('post_detail', pk=pk)
