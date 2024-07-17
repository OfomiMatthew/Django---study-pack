from django.urls import path 
from . import views 

urlpatterns = [
    path('',views.home,name='home'),
    # notes path
    path('notes',views.notes,name='notes'),
    path('delete-notes/<int:pk>/',views.delete_note, name='delete-note'),
    path('notes-details/<int:pk>/',views.NotesDetailView.as_view(),name='notes-details'),
    path('update-note/<int:pk>/',views.update_note,name='update-note'),

    # homework paths
    path('homework',views.homework,name='homework')
]
