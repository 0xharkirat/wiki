from django.shortcuts import render
from . import util
from django import forms
from markdown2 import Markdown
from random import choice

markdowner = Markdown()

# Define search form class
class NewSearchForm(forms.Form):
    q = forms.CharField(min_length=1, max_length=255)

# Define new page form class
class NewAddForm(forms.Form):
    title = forms.CharField(min_length=1, max_length=255)
    content = forms.CharField(widget=forms.Textarea)

# Define new edit form class
class NewEditForm(forms.Form):
    eContent = forms.CharField(widget=forms.Textarea)


# Define index route
def index(request):

    # if method is post
    if request.method == "POST":

        form = NewSearchForm(request.POST)
        # if form is valid
        if form.is_valid():

            q = form.cleaned_data["q"]

            # if user query is not a page
            if (util.get_entry(q) is None):
               
               search = []

               for entry in util.list_entries():
                    entrylower = entry.lower()

                    # search for substring in user query
                    if q in entrylower:
                        search.append(entry)

                # pass the searched result to search.html
               return render(request, "encyclopedia/search.html", {
                "search": search,
                "q": q
               })

            # if user query is a page
            else:

                # return entry page of requested query 
                return render(request, "encyclopedia/entry.html", {
                "title": q,
                "entry": markdowner.convert(util.get_entry(q))
                })

    # if method is get
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })
    
# define the wiki route
def wiki(request, title):

    # if requested entry is none
    if (util.get_entry(title) is None):
        # render error.html
        return render(request, "encyclopedia/error.html", {
            "title": "Error | 404",
            "message": "404 | No such entry found"
        })
    # if requested entry exists
    else:
        # render entry.html
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdowner.convert(util.get_entry(title))
        })

# define the add route
def add(request):

    # if request method is post
    if request.method == "POST":
        form = NewAddForm(request.POST)

        # validate form
        if form.is_valid():

            # get title from form
            title = form.cleaned_data["title"]

            # if title does not exist
            if (util.get_entry(title) is None):

                # get the content from form
                content = form.cleaned_data["content"]

                # save the entry using util.py
                util.save_entry(title, content)

                # also, render that entry.html
                return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": markdowner.convert(util.get_entry(title))
                })
            
            # if the title already exists
            else:
                # render error.html with message
                return render(request, "encyclopedia/error.html", {
                    "title":"Error",
                    "message": "Sorry, page already exits."
                })


    # if request method is get, render add.html to add new page
    return render(request, 'encyclopedia/add.html', {
        'aForm': NewAddForm()
    })

# define random route
def random(request):
    
    # return random page with entry.html
    return render(request, "encyclopedia/entry.html", {
                    "title": choice(util.list_entries()),
                    "entry": markdowner.convert(util.get_entry(choice(util.list_entries())))
    })

def edit(request, title):


    if request.method == "POST":

        form = NewEditForm(request.POST)
        if form.is_valid():

            newContent = form.cleaned_data["eContent"]

            util.save_entry(title,newContent)
            return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": markdowner.convert(util.get_entry(title))
                })


    initial = util.get_entry(title)
    eform = NewEditForm(initial={"eContent": initial})

    return render(request, "encyclopedia/edit.html", {
        "eform": eform,
        "title": title,
        "initial": initial
    })


    


    

    

