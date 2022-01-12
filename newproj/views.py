from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from newproj.models import Student, Department
from newproj.serializers import StudentSerializer, DepartmentSerializer

from django.views import View
from django.shortcuts import render

class StudentView(APIView):
    serializer_class = StudentSerializer

    def get(self, request, pk=None, format=None):
        if pk is not None:
            obj = Student.objects.get(std_id=pk)
            serializer = StudentSerializer(obj)
            return Response(serializer.data)

        obj = Student.objects.all()
        serializer = StudentSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()

            # Add deparment to the Student instance
            dept = Department.objects.get(dept_id=request.data['departments'])
            student.departments.add(dept)

            return Response({"message": "Success! The Student has been created."}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        obj = Student.objects.get(std_id=pk)
        serializer = StudentSerializer(obj, data=request.data)
        if serializer.is_valid():
            student = serializer.save()

            # Add deparment to the Student instance
            if request.data['departments']:
                dept = Department.objects.get(dept_id=request.data['departments'])
                student.departments.add(dept)

            return Response({"message":"Success! The Student has been updated completly."}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None, format=None):
        obj = Student.objects.get(std_id=pk)
        serialzer = StudentSerializer(obj, data=request.data, partial=True)
        if serialzer.is_valid():
            student = serialzer.save()

            # Add deparment to the Student instance
            if request.data['departments']:
                dept = Department.objects.get(dept_id=request.data['departments'])
                student.departments.add(dept)

            return Response({"message":"Success! The Student has been updated paritially."}, status=status.HTTP_202_ACCEPTED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        obj = Student.objects.get(std_id=pk)
        obj.delete()
        return Response({"message":"Success! The Student has been deleted."})

class ListStudentView(View):

    def get(self, request):
        ls = []
        depts = Department.objects.all()
        for d in depts:
            dic = {}
            stu_count = Student.objects.filter(departments__dept_id=d.dept_id).count()
            dic["dept"] = d.dept_name
            dic["stu_count"] = stu_count
            ls.append(dic)
        context = {"ls": ls, "comma": ","}
        return render(request, "student/studentCount.html", context=context)



class DepartmentView(APIView):
    serializer_class = DepartmentSerializer

    def get(self, request, pk=None, format=None):
        if pk is not None:
            obj = Department.objects.get(id=pk)
            serializer = DepartmentSerializer(obj)
            return Response(serializer.data)

        obj = Department.objects.all()
        serializer = DepartmentSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Success! The Department has been created."}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        obj = Department.objects.get(id=pk)
        serializer = DepartmentSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Success! The Department has been updated completly."}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None, format=None):
        obj = Department.objects.get(id=pk)
        serialzer = DepartmentSerializer(obj, data=request.data, partial=True)
        if serialzer.is_valid():
            serialzer.save()
            return Response({"message":"Success! The Department has been updated paritially."}, status=status.HTTP_202_ACCEPTED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        obj = Department.objects.get(id=pk)
        obj.delete()
        return Response({"message":"Success! The Department has been deleted."})