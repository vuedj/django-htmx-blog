from django.shortcuts import render, redirect
from base.models import Post
from django.http import HttpResponse


def index(request):
    post = Post.objects.first()
    context = {"post": post}
    if post is None:
        context["no_posts"] = True
    return render(request, "index.html", context)


def post_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return redirect("/")
    context = {"post": post}
    return render(request, "index.html", context)
