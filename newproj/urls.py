from django.urls import path
from newproj.views import StudentView, DepartmentView, ListStudentView

urlpatterns = [
    path('', StudentView.as_view(), name='student-list'),
    path('<int:pk>', StudentView.as_view(), name='student-retrieve'),
    path('count', ListStudentView.as_view(), name='list-student'),

    path('department', DepartmentView.as_view(), name='department-list'),
    path('department/<int:pk>', DepartmentView.as_view(), name='department-retrieve'),
]
