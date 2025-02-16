from django.shortcuts import render
from django import forms
from . import util
import markdown2
import random
import re




class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content") 

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea,strip=True)



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def display(request,title):
    content = util.get_entry(title)

    if content:
        html_content = markdown2.markdown(content) 
        
        return render(request, "encyclopedia/display.html",{
            "content":html_content,
            "title":title
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "title":title.capitalize()
        })
    
def search(request):
    if request.method == "POST":
        title = request.POST.get('q')
        entries = util.list_entries()

        if title.lower() in [entry.lower() for entry in entries]:
            content = util.get_entry(title)
            html_content = markdown2.markdown(content)
            return render(request,"encyclopedia/display.html",{
                "title":title.capitalize(),
                "content":html_content
            })
        else:
            matches = [entry for entry in entries if title.lower() in entry.lower()]
            if matches:
                return render(request,"encyclopedia/match_list.html",{
                    "matches":matches
                })
            else:
                return render(request,"encyclopedia/error.html",{
                    "title":title.capitalize()
                })
    
def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_content = form.cleaned_data['content']

            existing_entries = util.list_entries()
            if new_title.lower() in [entry.lower() for entry in existing_entries]:
                return render(request,"encyclopedia/new_entry.html",{
                    "form":form,
                    "message":"An entry with that title already exists!"
                })
            
            util.save_entry(new_title.capitalize(),new_content)
            return render(request,"encyclopedia/new_entry.html",{
                "form": NewEntryForm()
            })
        else:
            return render(request,"encyclopedia/new_entry.html",{
                "form":form
            })
    else:
        return render(request,"encyclopedia/new_entry.html",{
            "form": NewEntryForm()
        })


def random_page(request):
    titles = util.list_entries()
    title = random.choice(titles)
    content = util.get_entry(title)
    html_content = markdown2.markdown(content)
    return render(request,"encyclopedia/display.html",{
        "content":html_content,
        "title":title
    })



def edit_page(request,title):
    existing_content = util.get_entry(title.capitalize())
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            new_content = form.cleaned_data['content'].strip()
            new_content = re.sub(r'(\r?\n){2,}', '\n', new_content)
            util.save_entry(title,new_content)
            content = util.get_entry(title)
            return render(request,"encyclopedia/display.html",{
                "content":markdown2.markdown(content),
                "title":title
            })
        else:
            return render(request,"encyclopedia/edit_page.html",{
                "form":form
            })  
    else:
        form = EditForm(initial={'content': existing_content.strip()})
        return render(request,"encyclopedia/edit_page.html",{
            "form":form,
            "title":title
           
        })
