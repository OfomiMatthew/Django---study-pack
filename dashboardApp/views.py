from django.shortcuts import render,redirect
from .models import Notes, Homework
from .forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch

import requests

# Create your views here.
def home(request):
    return render(request,'dashboardApp/home.html')

# ---------- Notes app function starts here -----------
def notes(request):
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            messages.success(request,f'Notes added by {request.user.username} successfully')
            form = NotesForm()  
    else:
        form = NotesForm()

   
    notes = Notes.objects.filter(user=request.user)
    context = {'notes':notes,'form':form}
    return render(request,'dashboardApp/notes.html',context)

def delete_note(request,pk=None):
    note = Notes.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('notes')
    return render(request,'dashboardApp/delete.html',{'obj':note})

def update_note(request,pk):
    notes = Notes.objects.get(id=pk)
    form = NotesForm(instance=notes)
    if request.method == 'POST':
        form = NotesForm(request.POST,instance=notes)
        if form.is_valid():
            form.save()
            return redirect('notes')
    return render(request,'dashboardApp/notes_update.html',{'form':form})


class NotesDetailView(generic.DetailView):
    model = Notes

# --------- Notes app function ends here----------


# -------- homework function starts here-----
def homework(request):
    if request.method == 'POST':
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished = request.POST['is_finished']
                if finished == 'on':
                    finished = True
                else:
                    finished = False 
            except:
                finished = False
            homeworks = Homework(
                user = request.user,
                subject = request.POST['subject'],
                title = request.POST['title'],
                description = request.POST['description'],
                due_date = request.POST['due_date'],
                is_finished = finished
            )
            homeworks.save()
            messages.success(request,f'Homework added from {request.user.username}')
            form = HomeworkForm()
    else:
        form = HomeworkForm()

    
    homeworks = Homework.objects.filter(user = request.user)
    if len(homeworks) == 0:
        homework_done == True
    else:
        homework_done = False
    context = {'homeworks':homeworks,'homework_done':homework_done,'form':form}
    return render(request,'dashboardApp/homework.html',context)

def update_homework(request,pk):
    homework = Homework.objects.get(id=pk)
    form = HomeworkForm(instance=homework)
    if request.method == 'POST':
        form = HomeworkForm(request.POST,instance=homework)
        if form.is_valid():
            form.save()
            messages.success(request,f'Homework: {homework.title} updated successfully')
            return redirect('homework')
    return render(request,'dashboardApp/homework_update.html',{'form':form})

def delete_homework(request,pk=None):
    homework = Homework.objects.get(id=pk)
    if request.method == 'POST':
        homework.delete()
        messages.info(request,f'Homework: {homework.title} deleted successfully')
        return redirect('homework')
    return render(request,'dashboardApp/delete.html',{'obj':homework})

# ------ homework function ends here --------

def youtube_content(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text,limit=10)
        result_list = []
        for i in video.result()['result']:
            result_dict ={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']
            }
            desc =''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
            context ={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboardApp/youtube.html',context)
    else:
        form = DashboardForm() 
    context = {'form':form}
    return render(request,'dashboardApp/youtube.html',context)


def books(request):
    if request.method == 'POST':
        form = DashboardForm(request.POST)
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q="+text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):

            result_dict ={
             'title':answer['items'][i]['volumeInfo']['title'],
            'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
            'description':answer['items'][i]['volumeInfo'].get('description'),
            'count':answer['items'][i]['volumeInfo'].get('pageCount'),
            'categories':answer['items'][i]['volumeInfo'].get('categories'),
            'rating':answer['items'][i]['volumeInfo'].get('rating'),
            'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
            'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
            }
           
            result_list.append(result_dict)
            context ={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboardApp/youtube.html',context)
    else:
        form = DashboardForm() 
    context = {'form':form}
    return render(request,'dashboardApp/youtube.html',context)
