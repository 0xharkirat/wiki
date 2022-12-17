from django.shortcuts import render

from . import util

from django import forms


from markdown2 import Markdown

markdowner = Markdown()

class NewSearchForm(forms.Form):
    q = forms.CharField(min_length=1, max_length=255)

class NewAddForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=255)
    content = forms.CharField(widget=forms.Textarea)



def index(request):

    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            q = form.cleaned_data["q"]
            if (util.get_entry(q) is None):
               
               search = []
               for entry in util.list_entries():
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
            "entry": markdowner.convert(util.get_entry(q))
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })
    

def wiki(request, title):


    if (util.get_entry(title) is None):
        return render(request, "encyclopedia/error.html", {
            "title": "Error | 404",
            "message": "404 | No such entry found"
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(util.get_entry(title))
        })

def add(request):

    if request.method == "POST":
        form = NewAddForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if (util.get_entry(title) is None):
                content = form.cleaned_data["content"]
                util.save_entry(title, content)

                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": markdowner.convert(util.get_entry(title))
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "title":"Error",
                    "message": "Sorry, page already exits."
                })



    return render(request, 'encyclopedia/add.html', {
        'aForm': NewAddForm()
    })


    

    

