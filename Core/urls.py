from django.contrib import admin
from django.urls import path
from.import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('active_hazard/',views.active_hazards,name="Active_hazard"),
    path('hospital_details/',views.Hospital_details,name="Hospital_details"),
    path('hazard_report/',views.Hazard_report,name="Hazard_report"),
    path('hazard_detail/<int:id>/',views.hazard_detail,name="hazard_detail"),
    path('hazard/<int:id>/edit/',views.edit_hazard,name="edit_hazard"),
    path('hazard/<int:id>/delete/',views.delete_hazard,name="delete_hazard"),
    path('add_hospital/',views.add_hospital,name="add_hospital"),
    path('hospital_list/',views.hospital_list,name="hospital_list"),
    path('patients/', views.patient_list, name='patient_list'),
    path('hospital/<int:id>/edit/',views.edit_hospital,name="edit_hospital"),
    path('hospital/<int:id>/delete/',views.delete_hospital,name="delete_hospital"),
    path('add_patient/',views.add_patient,name='add_patient'),
    path('patient/<int:id>/edit/',views.edit_patient,name="edit_patient"),
    path('patient/<int:id>/delete/',views.delete_patient,name="delete_patient"),
    path('missing_complaint/<int:hazard_id>/missing/',views.add_missing_complaint,name='add_missing_complaint'),
    path('missing_complaint/<int:id>/edit/',views.edit_missing_complaint,name="edit_missing_complaint"),
    path('missing_complaint/<int:id>/delete/',views.delete_missing_complaint,name="delete_missing_complaint"),
]