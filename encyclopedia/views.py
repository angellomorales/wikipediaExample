from django.shortcuts import render
from django.http import HttpResponseRedirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        content = "Page Not Found"
        title = content
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })


def search(request):
    entries = util.list_entries()
    find_entries = list()

    if request.method == "GET":
        result = request.GET["q"]
        content = util.get_entry(result)
        if content == None:
            content = "Page Not Found"
            for entry in entries:
                if result in entry:
                    find_entries.append(entry)
                elif result.capitalize() in entry:
                    find_entries.append(entry)
                elif result.upper() in entry:
                    find_entries.append(entry)
                elif result.lower() in entry:
                    find_entries.append(entry)
            if find_entries:
                return render(request, "encyclopedia/search.html", {
                    "search_result": find_entries,
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title": content,
                    "content": content
                })
        else:
            return render(request, "encyclopedia/entry.html", {
                "title": result.capitalize(),
                "content": content
            })
