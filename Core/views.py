from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .forms import HazardReportForm,HospitalForm,PatientForm,MissingComplaintForm
from.models import HazardReport,Hospital,Patient,MissingComplaint

# Permission check helper
def is_admin(user):
    return user.is_authenticated and user.category == 'admin'

# Create your views here.
def home(request):
    return render(request,'home.html')

def admin_dashboard(request):
    hazards_count = HazardReport.objects.count()
    active_count = HazardReport.objects.filter(status='active').count()
    resolved_count = HazardReport.objects.filter(status='resolved').count()
    patients_count = Patient.objects.count()
    hospitals_count = Hospital.objects.count()
    missing_count = MissingComplaint.objects.count()

    recent_hazards = HazardReport.objects.order_by('-created_at')[:6]
    recent_complaints = MissingComplaint.objects.order_by('-created_at')[:6]

    return render(request, 'admin_dashboard.html', {
        'hazards_count': hazards_count,
        'active_count': active_count,
        'resolved_count': resolved_count,
        'patients_count': patients_count,
        'hospitals_count': hospitals_count,
        'missing_count': missing_count,
        'recent_hazards': recent_hazards,
        'recent_complaints': recent_complaints,
    })

def Active_hazard(request):
    return render(request,'active_hazard.html')

def Hazard_details(request):
    return render(request,'hazard_details.html')

def Hospital_details(request):
    return render(request,'hospital.html')
def Hazard_report(request):

     
    if request.method == 'POST':
         form = HazardReportForm(request.POST)
         if form.is_valid():
             hazard = form.save(commit=False)
             hazard.user = request.user
             hazard.save()
             return redirect('home')
         
    else:
        form= HazardReportForm()
        
    return render(request,'hazard_report.html',{'form':form})

def active_hazards(request):
    hazards = HazardReport.objects.filter(status='active')
    print("COUNT:", hazards.count())  

    return render(request, 'active_hazard.html', {
        'hazards': hazards
    })
    
    
def hazard_detail(request,id):
    hazard = get_object_or_404(HazardReport,id=id)
    patients = hazard.patients.all()
    missing_form = MissingComplaintForm()
    return render(
        request,
        'hazard_details.html',{
            'hazard':hazard,
            'patients':patients
            ,'missing_form': missing_form
        }
    )
    

def add_hospital(request):
    if request.method=='POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form=HospitalForm()
    
    return render(request,'add_hospital.html',{'form':form})

def hospital_list(request):
    hospitals=Hospital.objects.all()
    
    return render(request,'show_hospital.html',{'hospitals':hospitals})


def patient_list(request):
    patients = Patient.objects.select_related('hospital', 'hazard').all()
    return render(request, 'patient_list.html', {'patients': patients})


def add_patient(request):
    if request.method =='POST':
        form = PatientForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by=request.user
            patient.save()
            
            return redirect('home')
    else:
        form = PatientForm()
    return render(
        request,
        'add_patient.html',
        {'form':form}
    )
    
def add_missing_complaint(request,hazard_id):
    hazard = get_object_or_404(
        HazardReport,
        id=hazard_id
    )
    if request.method=='POST':
        form = MissingComplaintForm(
            request.POST,
            request.FILES
        )
        if form.is_valid():
            complaint=form.save(commit=False)
            complaint.hazard=hazard
            complaint.created_by = request.user
            complaint.save()
            
            return redirect(
                'hazard_detail',
                id=hazard.id
            )
    else:
        form =MissingComplaintForm()
        
    return render(
        request,
        'add_missing_complaint.html',
        {
             'form': form,
        'hazard': hazard
        })

# Edit Hazard
def edit_hazard(request, id):
    hazard = get_object_or_404(HazardReport, id=id)
    if request.method == 'POST':
        form = HazardReportForm(request.POST, instance=hazard)
        if form.is_valid():
            form.save()
            return redirect('hazard_detail', id=hazard.id)
    else:
        form = HazardReportForm(instance=hazard)
    return render(request, 'edit_hazard.html', {'form': form, 'hazard': hazard})

# Delete Hazard
def delete_hazard(request, id):
    hazard = get_object_or_404(HazardReport, id=id)
    if request.method == 'POST':
        hazard.delete()
        return redirect('admin_dashboard')
    return render(request, 'delete_confirm.html', {'object': hazard, 'type': 'Hazard'})

# Edit Hospital
def edit_hospital(request, id):
    hospital = get_object_or_404(Hospital, id=id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('hospital_list')
    else:
        form = HospitalForm(instance=hospital)
    return render(request, 'edit_hospital.html', {'form': form, 'hospital': hospital})

# Delete Hospital
def delete_hospital(request, id):
    hospital = get_object_or_404(Hospital, id=id)
    if request.method == 'POST':
        hospital.delete()
        return redirect('hospital_list')
    return render(request, 'delete_confirm.html', {'object': hospital, 'type': 'Hospital'})

# Edit Patient (Admin only)
def edit_patient(request, id):
    if not is_admin(request.user):
        return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Only admins can edit patients.</p>")
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('hazard_detail', id=patient.hazard.id)
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

# Delete Patient (Admin only)
def delete_patient(request, id):
    if not is_admin(request.user):
        return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Only admins can delete patients.</p>")
    patient = get_object_or_404(Patient, id=id)
    hazard_id = patient.hazard.id
    if request.method == 'POST':
        patient.delete()
        return redirect('hazard_detail', id=hazard_id)
    return render(request, 'delete_confirm.html', {'object': patient, 'type': 'Patient'})

# Edit Missing Complaint (Admin only)
def edit_missing_complaint(request, id):
    if not is_admin(request.user):
        return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Only admins can edit missing complaint reports.</p>")
    complaint = get_object_or_404(MissingComplaint, id=id)
    if request.method == 'POST':
        form = MissingComplaintForm(request.POST, request.FILES, instance=complaint)
        if form.is_valid():
            form.save()
            return redirect('hazard_detail', id=complaint.hazard.id)
    else:
        form = MissingComplaintForm(instance=complaint)
    return render(request, 'edit_missing_complaint.html', {'form': form, 'complaint': complaint})

# Delete Missing Complaint (Admin only)
def delete_missing_complaint(request, id):
    if not is_admin(request.user):
        return HttpResponseForbidden("<h1>403 Forbidden</h1><p>Only admins can delete missing complaint reports.</p>")
    complaint = get_object_or_404(MissingComplaint, id=id)
    hazard_id = complaint.hazard.id
    if request.method == 'POST':
        complaint.delete()
        return redirect('hazard_detail', id=hazard_id)
    return render(request, 'delete_confirm.html', {'object': complaint, 'type': 'Missing Report'})

