from django.shortcuts import render
from django.http import HttpResponse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = "Page Not Found"
        title=content
        return render(request, "encyclopedia/error.html", {
        "title": title,
        "content":content
    })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content":content
        })
