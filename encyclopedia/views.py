from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from django.urls import reverse
from .forms import CreateForm
from . import util
import markdown
import os
import random
import fnmatch
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(), "index" : 1,
    })

def wiki(request, title):
    content = util.get_entry(title)
    
    if content is None:
        raise Http404(f"Requested page \"{title}\" was not found")
    else:
        html_body = markdown.markdown(content, safe_mode=True)
        html_body = html_body.replace('[HTML_REMOVED]', '')
        context = {
            "title" : title,
            "content" : html_body,
        }
        return render(request, "encyclopedia/view_entry.html", context)

def createnew(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            check_if_exists = util.get_entry(title)
            if check_if_exists is None: 
                content = form.cleaned_data.get('content')
                content = re.sub(r'(\r\n|\n|\r)', r'\n', content)
                # The above step is done because textarea is adding extra ]\r\n
                # for every new-line
                util.save_entry(title, content)
                return redirect(f'/wiki/{title}')
            else: 
                messages.error(request, f"Wiki page titled {title} already exists!", extra_tags='danger')
                context = {
                    "form" : form,
                }
                return render(request, "encyclopedia/createnew.html", context)
    else :
        form = CreateForm()
        context = {
            'form' : form,
        }     
        return render(request, "encyclopedia/createnew.html", context)

def randompage(request):
    path = os.path.join(BASE_DIR, 'entries/')
    filename = random.choice(os.listdir(path))
    title, _ = os.path.splitext(filename)
    
    return redirect(f'/wiki/{title}')

def wikisearch(request):
    if request.method == "POST":
        path = os.path.join(BASE_DIR, 'entries/')
        base_string = request.POST.get('q').lower()
        thelist = []
        string = f"*{base_string}*.md"
        for file in os.listdir(path):
            if fnmatch.fnmatch(file, string):
                thelist.append(os.path.splitext(file)[0])
            
        l = len(thelist)
        if l == 0:
            messages.error(request, f"No entry named {base_string}", extra_tags='danger')
            
        if len(thelist) == 1 and (base_string == thelist[0].lower()):
            return redirect(f'/wiki/{thelist[0]}')
        else:
            context = {
                "entries" : thelist,
                "search" : 1, 
            }
            return render(request, "encyclopedia/index.html", context)
    else:
        raise Http404('Page Not Found')

def wikiedit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        initial = {'title':title, 'content':content}
        form = CreateForm(initial)
        context = {
            "form" : form,
        }
        return render(request, "encyclopedia/edit.html", context)
    elif request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            content = re.sub(r'(\r\n|\n|\r)', r'\n', content)
            util.save_entry(title, content)
            messages.success(request, f"Page \"{title}\" updated successfully!")    
            return redirect(f'/wiki/{title}')
        else:
            messages.error(request, f"Something Went Wrong!", extra_tags='danger')    
            return redirect(reverse('wikiedit', kwargs={"title": title}))
    else:
        raise Http404("Page Not Found")
    