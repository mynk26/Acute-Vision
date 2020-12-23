from django import forms
from django.forms import ModelForm,Form
from section.models import Section,Class
from time_table.models import Subject
from .models import Attendance


class SectionModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Section_Name

class ClassModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.Class_Number

class SubjectModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s - (%s)" % (obj.Subject_Code,obj.Subject_Name)


class StudentAttendanceForm(Form):
    Semester = forms.IntegerField()
    Section_List = (('',''),('A','A'),('B','B'),('C','C'))
    Section = forms.ChoiceField(choices=Section_List)

class CheckAttendanceForm(Form):
    Section = SectionModelChoiceField(queryset=Section.objects.all())
    From = forms.DateField(label='From', widget=forms.SelectDateWidget)
    To = forms.DateField(label='To', widget=forms.SelectDateWidget)


class TakeAttendanceForm(Form):
    Section = SectionModelChoiceField(queryset=Section.objects.all())
    Class = ClassModelChoiceField(queryset=Class.objects.all())
    Subject = SubjectModelChoiceField(queryset=Subject.objects.all())

class ModifyAttendanceForm(Form):
    Section = SectionModelChoiceField(queryset=Section.objects.all())
    Subject = SubjectModelChoiceField(queryset=Subject.objects.all())
    Date = forms.DateField(label='Date', widget=forms.SelectDateWidget)

class ModifyAttendanceSelectedForm(ModelForm):
    Enrollment = forms.CharField(max_length=254)
    Subject_Code=forms.CharField(max_length=30)
    Section = forms.CharField(max_length=30)
    class Meta:
        model=Attendance
        fields = ('Date','Status')
    field_order=['Enrollment','Subject_Code','Section','Date','Status']
