from django.urls import path
from . import views

app_name = "reflections"

urlpatterns = [
    # 노트 목록 (List)
    path("", views.note_list, name="note_list"),
    
    # 노트 작성 (Create)
    path("create/", views.note_create, name="note_create"),
    
    # 노트 상세 (Read)
    path("<int:pk>/", views.note_detail, name="note_detail"),
    
    # 노트 수정 (Update)
    path("<int:pk>/update/", views.note_update, name="note_update"),
    
    # 노트 삭제 (Delete)
    path("<int:pk>/delete/", views.note_delete, name="note_delete"),
]
