from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class User(AbstractUser):
    CATEGORY_CHOICES =(
        ('admin','admin'),
        ('volunteer','volunteer')
        
    )
    GENDER_CHOICES=(
        ('Male','male'),
        ('Female','female')
    )
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    phone= models.CharField(max_length=20),
    date_of_birth = models.DateField(null=True,blank=True)
    gender=models.CharField(max_length=100,choices=GENDER_CHOICES)
    volunteer_id = models.CharField(max_length=50,unique=True,null=True,blank=True)
    profile_image = models.ImageField(upload_to='profiles/',null=True,blank=True)


class HazardReport(models.Model):
    SEVRITY_CHOICES=[
        ('Low','low'),
        ('Medimu','medium'),
        ('High','high')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    servity = models.CharField(max_length=100,choices=SEVRITY_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
           ('resolved', 'Resolved')
            
        ],
        default='active',
    )
    def __str__(self):
        return f"{self.title}-{self.servity}"
    
    
class Hospital(models.Model):
    name=models.CharField(max_length=100)
    location =models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    capacity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class Patient(models.Model):
    name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=20, unique=True, blank=True)

    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    condition = models.CharField(
        max_length=20,
        choices=[
            ('stable', 'Stable'),
            ('critical', 'Critical')
        ]
    )

    hospital = models.ForeignKey(
        'Hospital',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # Better use ForeignKey instead of OneToOneField
    hazard = models.ForeignKey(
        'HazardReport',
        on_delete=models.CASCADE,
        related_name='patients'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):

        if not self.patient_id:

            hazard_name = self.hazard.title.upper()

            # find last patient under same hazard
            last_patient = Patient.objects.filter(
                hazard=self.hazard
            ).order_by('id').last()

            if last_patient and last_patient.patient_id:

                last_num = int(
                    last_patient.patient_id.split('-')[-1]
                )

                new_num = last_num + 1

            else:
                new_num = 1

            self.patient_id = (
                f"PAT-{hazard_name}-{new_num:03d}"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_id} --> {self.name}"
    
    

class MissingComplaint(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    patient = models.ForeignKey(
            'Patient',
            on_delete=models.CASCADE,
            related_name='missing_complaints',
            null=True,
            blank=True
    )
    hazard = models.ForeignKey(
        'HazardReport',
        on_delete=models.CASCADE,
        related_name='missing_complaints'
    )
    
    person_name=models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    description = models.TextField()
    last_seen_location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    missing_person_name=models.CharField(max_length=100)
    missing_person_age=models.IntegerField()
    missing_person_gender=models.CharField(max_length=20,choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ImageField(
        upload_to='missing_people/',
        null=True,
        blank=True
    )
    def __str__(self):
        return self.person_name