from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from newproj.models import Student, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['dept_id','dept_name','dept_head']

class StudentSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(read_only=True, many=True)
    full_name = SerializerMethodField(read_only=True)

    class Meta:
        model = Student
        fields = ['std_id', 'full_name', 'first_name','last_name', 'departments']

    def get_full_name(self, obj):
        return obj.get_full_name()