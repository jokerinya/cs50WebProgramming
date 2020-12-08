import re
from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
from markdown2 import markdown
from random import choice
from django.contrib import messages


from . import util


class NewEntry(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 80, 'cols': 20}))


class NewEdit(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 80, 'cols': 20}))


def index(request):
    entries = util.list_entries()
    if request.method == "POST":
        query = request.POST["q"]
        # redirect to query result entry page
        if query in entries:
            return redirect("encyclopedia:entry", title=query)
        results = []
        for entry in entries:
            if query in entry:
                results.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entries": results
        })
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })


def entry(request, title):
    result = util.get_entry(title)
    if result:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "result": markdown(result)
        })
    else:
        return render(request, "encyclopedia/404.html", {})


def create(request):
    if request.method == "POST":
        entry = NewEntry(request.POST)
        if entry.is_valid():
            title = entry.cleaned_data["title"]
            content = entry.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/create.html", {
                    "entry": entry,
                    "name_error": True
                })
            else:
                util.save_entry(title, content)
                messages.success(
                    request, f"You have made {title} entry successfully.", extra_tags="extra-css-tag")
                # new created entry
                # return HttpResponseRedirect(reverse("entry", args=[title]))
                return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/create.html", {
                "entry": entry,
                "name_error": False
            })
    else:
        return render(request, "encyclopedia/create.html", {
            "entry": NewEntry(),
            "name_error": False
        })


def random(request):
    title = choice(util.list_entries())
    return redirect("encyclopedia:entry", title=title)


def edit(request, title):
    if request.method == "POST":
        content = NewEdit(request.POST)
        if content.is_valid():
            content = content.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect("encyclopedia:entry", title=title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "content": content,
                "title": title
            })
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "content": NewEdit({"content": content}),
            "title": title
        })
