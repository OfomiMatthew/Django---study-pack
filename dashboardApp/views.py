from django.shortcuts import render,redirect
from .models import Notes, Homework
from .forms import *
from django.contrib import messages
from django.views import generic

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
    homeworks = Homework.objects.filter(user = request.user)
    if len(homeworks) == 0:
        homework_done == True
    else:
        homework_done = False
    context = {'homeworks':homeworks,'homework_done':homework_done}
    return render(request,'dashboardApp/homework.html',context)


    
