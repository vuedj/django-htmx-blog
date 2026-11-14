from django.http import HttpResponse
from django.shortcuts import render
from base.models import Post
from datetime import datetime
from django.http import QueryDict


def posts(request):
    if request.method == "POST":
        current_timestamp = datetime.now()
        post = Post.objects.create(title=current_timestamp)
        context = {"post": post}
        response = render(request, "responses/post_add.html", context)
        response["HX-Trigger"] = "postDeleted"
        return response


def posts_detail(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":
        context = {"post": post}
        return render(request, "components/post.html", context)

    elif request.method == "DELETE":
        post_id = post.id
        post.delete()
        total = Post.objects.count()
        context = {"post_id": post_id, "total": total}
        response = render(request, "responses/post_delete.html", context)
        response["HX-Trigger"] = "postDeleted"
        response["HX-Redirect"] = "/"
        return response


def posts_edit(request, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        return HttpResponse(status=404)
    if request.method == "GET":

        context = {"post": post}
        return render(request, "components/edit.html", context)

    elif request.method == "PUT":
        data = QueryDict(request.body, encoding="utf-8")

        post.title = data.get("title")
        post.body = data.get("body")
        post.save()

        context = {"post": post}
        return render(request, "responses/post_edit.html", context)


def sidebar(request):
    posts = Post.objects.all()
    total = Post.objects.count()
    context = {"posts": posts, "total": total}
    return render(request, "components/sidebar.html", context)


def total(request):
    total = Post.objects.count()
    return render(request, "components/total.html", {"total": total})
