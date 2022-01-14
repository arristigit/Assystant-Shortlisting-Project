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
        try:
            # If one Student and Many Departments (OSMD) inputs
            if request.data["relationship_type"] == "OSMD":
                serializer = StudentSerializer(data=request.data)
                if serializer.is_valid():
                    student = serializer.save()

                    if student: 
                        dept_ids = request.data['dept_ids'].split('-')
                        dept_names = request.data['dept_names'].split('-')
                        dept_heads = request.data['dept_heads'].split('-')

                        for depts in range(0, len(dept_ids)):
                            department_details = {
                                'dept_id' : int(dept_ids[depts]),
                                'dept_name' : dept_names[depts],
                                'dept_head' : dept_heads[depts]
                            }
                            dept_serializer = DepartmentSerializer(data=department_details)
                            if dept_serializer.is_valid():
                                dept_save= dept_serializer.save()
                                student.departments.add(dept_save)

                    return Response({"message": "Success! The Student with his Deparments has been created."}, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if request.data["relationship_type"] == "ODMS":
                serializer = DepartmentSerializer(data=request.data)
                if serializer.is_valid():
                    dept_save = serializer.save()

                    if dept_save:
                        std_ids = request.data['std_ids'].split('-')
                        first_names = request.data['first_names'].split('-')
                        last_names = request.data['last_names'].split('-')

                        for stud in range(0, len(std_ids)):
                            student_details = {
                                'std_id' : int(std_ids[stud]),
                                'first_name' : first_names[stud],
                                'last_name' : last_names[stud]
                            }
                            stud_serializer = StudentSerializer(data=student_details)
                            if stud_serializer.is_valid():
                                stud_save= stud_serializer.save()
                                stud_save.departments.add(dept_save)
                
                    return Response({"message": "Success! The Department with its Students has been created."}, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if request.data["relationship_type"] == "MSMD":
                deptments_save = []

                dept_ids = request.data['dept_ids'].split('-')
                dept_names = request.data['dept_names'].split('-')
                dept_heads = request.data['dept_heads'].split('-')

                for dept in range(0, len(dept_ids)):
                    department_details = {
                        'dept_id' : int(dept_ids[dept]),
                        'dept_name' : dept_names[dept],
                        'dept_head' : dept_heads[dept]
                    }
                    serializer = DepartmentSerializer(data=department_details)
                    if serializer.is_valid():
                        dept_save = serializer.save()
                        deptments_save.append(dept_save)


                std_ids = request.data['std_ids'].split('-')
                first_names = request.data['first_names'].split('-')
                last_names = request.data['last_names'].split('-')

                for stud in range(0, len(std_ids)):
                    student_details = {
                        'std_id' : int(std_ids[stud]),
                        'first_name' : first_names[stud],
                        'last_name' : last_names[stud]
                    }
                    # print(student_details)
                    stud_serializer = StudentSerializer(data=student_details)
                    if stud_serializer.is_valid():
                        # print("serializer is valid..")
                        stud_save = stud_serializer.save()

                        for dep in range(0, len(deptments_save)):
                            # print("iteration in departs to add to the studene: ", dep)
                            print(deptments_save[dep])
                            stud_save.departments.add(deptments_save[dep])

                    return Response({"message": "Success! The Students with its Departments has been created."}, status = status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Error": "Please provide correct 'relationship_type'."}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"Error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None, format=None):
        obj = Student.objects.get(std_id=pk)
        serializer = StudentSerializer(obj, data=request.data)
        if serializer.is_valid():
            student = serializer.save()

            dept_ids = request.data['dept_ids'].split('-')
            dept_names = request.data['dept_names'].split('-')
            dept_heads = request.data['dept_heads'].split('-')

            for dept in range(0, len(dept_ids)):
                department_details = {
                    'dept_id' : int(dept_ids[dept]),
                    'dept_name' : dept_names[dept],
                    'dept_head' : dept_heads[dept]
                }
                new_obj = Department.objects.get(dept_id=department_details['dept_id'])
                serializer = DepartmentSerializer(new_obj, data=department_details)
                if serializer.is_valid():
                    dept_save = serializer.save()
                    student.departments.add(dept_save)


            # Add deparment to the Student instance
            # if request.data['departments']:
            #     dept = Department.objects.get(dept_id=request.data['departments'])
            #     student.departments.add(dept)

            return Response({"message":"Success! The Student has been updated completly."}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None, format=None):
        obj = Student.objects.get(std_id=pk)
        serialzer = StudentSerializer(obj, data=request.data, partial=True)
        if serialzer.is_valid():
            student = serialzer.save()

            dept_ids = request.data['dept_ids'].split('-')

            for dep in dept_ids:
                department = Department.objects.get(dept_id=dep)
                student.departments.remove(department)

            # Add deparment to the Student instance
            # if request.data['departments']:
            #     dept = Department.objects.get(dept_id=request.data['departments'])
            #     student.departments.add(dept)
            

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
            dic["dept"] = d.dept_name
            dic["stu_count"] = d.dept.all().count()
            ls.append(dic)
        context = {"ls": ls}
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