from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="title", required=True)
    content = forms.CharField(widget=forms.Textarea,
                              label="content", required=True)


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


def new(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if ('qediting' in request.POST):
                # edit page
                title = request.POST["qediting"]
                if util.checkEdit(title, content):
                    return render(request, "encyclopedia/entry.html", {
                        "title": title,
                        "content": content
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "title": "error",
                        "content": "Not possible to edit"
                    })
            else:
                # new page
                if util.checkSave(title, content):
                    return render(request, "encyclopedia/entry.html", {
                        "title": title,
                        "content": content
                    })
                else:
                    return render(request, "encyclopedia/error.html", {
                        "title": "error",
                        "content": "content already exist"
                    })
        else:
            if ('qedit' in request.POST):
                title = request.POST["qedit"]
                content = util.get_entry(title)
                editform = NewPageForm(
                    initial={'title': title, 'content': content})
                return render(request, "encyclopedia/new.html", {
                    "isediting": "True",
                    "title": title,
                    "form": editform
                })
            else:
                return render(request, "encyclopedia/new.html", {
                    "isediting": "False",
                    "form": form
                })

    return render(request, "encyclopedia/new.html", {
        "form": NewPageForm()
    })


def randomPage(request):
    entries = util.list_entries()
    randomIndex = random.choice(entries)
    # url = reverse('encyclopedia:entry', kwargs={'title': randomIndex})
    # return HttpResponseRedirect(url)
    return HttpResponseRedirect(reverse('encyclopedia:entry', args=(randomIndex,)))
