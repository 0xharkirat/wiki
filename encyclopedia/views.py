from django.shortcuts import render

from . import util

from django import forms

from django.http import HttpResponseRedirect
from django.urls import reverse

class NewSearchForm(forms.Form):
    q = forms.CharField(min_length=1)

entries = util.list_entries()

def index(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if (util.get_entry(q) is None):
               # return HttpResponseRedirect(reverse("wiki:search"))
               search = []
               for entry in entries:
                    entrylower = entry.lower()
                    if q in entrylower:
                
                        search.append(entry)
               return render(request, "encyclopedia/search.html", {
                "search": search,
                "q": q
               })

            else:
                return render(request, "encyclopedia/entry.html", {
            "title": q,
            "entry": util.get_entry(q)
        })

    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "form": NewSearchForm()
    })
    

def wiki(request, title):


    if (util.get_entry(title) is None):
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": util.get_entry(title)
        })



    

    

