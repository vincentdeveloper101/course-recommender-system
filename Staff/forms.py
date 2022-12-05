from django import forms
from Recommender.models import Course


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'schools', 'tution_fees', 'image', 'academic_year', 'entry_year' ,'school_phone', 'school_email', 'lectures',
                  'intake_in', 'faculty', 'location', 'description']


class UpdateCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['title', 'schools', 'tution_fees', 'image', 'academic_year', 'entry_year' ,'school_phone', 'school_email', 'lectures',
                  'intake_in', 'faculty', 'location', 'description']

    def save(self, commit=True):
        post = self.instance
        post.title = self.cleaned_data['title']
        post.schools = self.cleaned_data['schools']
        post.academic_year = self.cleaned_data['academic_year']
        post.entry_year = self.cleaned_data['entry_year']
        post.school_phone = self.cleaned_data['school_phone']
        post.school_email = self.cleaned_data['school_email']
        post.tution_fees = self.cleaned_data['tution_fees']
        post.lectures = self.cleaned_data['lectures']
        post.intake_in = self.cleaned_data['intake_in']
        post.faculty = self.cleaned_data['faculty']
        post.location = self.cleaned_data['location']
        post.description = self.cleaned_data['description']

        if self.cleaned_data['image']:
            post.image = self.cleaned_data['image']

        if commit:
            post.save()
        return post
