from django import forms 
from.models import HazardReport,Hospital,Patient,MissingComplaint

class HazardReportForm(forms.ModelForm):
    class Meta:
        model = HazardReport
        fields=['title','description','servity']
        
        widgets ={
            'title':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter hazard title'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Describe the hazard',
                'rows':4
            }),
            'servity':forms.Select(attrs={
                'class':'form-select'
            })
        }
        
class HospitalForm(forms.ModelForm):
    class Meta:
        model= Hospital
        fields = ['name','location','phone','capacity']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter hospital name'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, district, or area'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact number'
            }),
            'capacity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bed capacity'
            }),
        }
        

class PatientForm(forms.ModelForm):
    class Meta:
        model  =Patient
        fields=[
            'name','age','gender','condition','hospital','hazard','image'
        ]     
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Patient full name'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Age'
            }),
            'gender': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Gender'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hospital': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hazard': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }
        
        
class MissingComplaintForm(forms.ModelForm):
    class Meta:
        model  =MissingComplaint
        fields=[
            'person_name','age','gender','image','contact_number','missing_person_name','missing_person_age','missing_person_gender'
        ]     
        widgets = {
            'person_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Your age'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control form-control-sm'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact number'}),
            'missing_person_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Missing person's name"}),
            'missing_person_age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': "Missing person's age"}),
            'missing_person_gender': forms.Select(attrs={'class': 'form-select'}),
        }
     
        
        

        

        