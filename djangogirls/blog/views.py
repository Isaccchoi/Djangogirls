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
    # request 메소드가 POST이며 title 및 content가 잘 들어 있을 경우
    if request.method == 'POST' and request.POST.get('title') and request.POST.get('content'):
        title = request.POST['title']
        content = request.POST['content']
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
    # request 메소드가 GET일 경우 입력할 수 있는 form 제공
    elif request.method == 'GET':
        context = {

        }
        return render(request, 'blog/post_form.html', context)
    # request 메소드가 POST이면서 title 및 content가 '안'들어 있을 경우 alert값에 True를 넣어 알람이 나오도록 설정
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
    # POST 접근이 아닐 경우 해당 요청한 pk의 detail page로 이동
    return redirect('post_detail', pk=pk)
