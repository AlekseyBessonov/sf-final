from django.urls import path
from .views import *
from rest_framework.schemas import get_schema_view
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', SearchMachines.as_view(), name='search'),
    path('user/', by_user_machine, name='user'),
    path('to/', TOListVew.as_view(), name='to'),
    # path('complaint/', by_user_complaint, name='complaint'),
    path('machineadd', MachineCreateVew.as_view(), name='machine_create'),
    path('addto', TOCreateVew.as_view(), name='to_create'),
    path('complaintadd', ComplaintCreateVew.as_view(), name='complaint_create'),
    path('<int:pk>/medit', MachineUpdateView.as_view(), name='machine_update'),
    path('<int:pk>/tedit', TOUpdateView.as_view(), name='to_update'),
    path('<int:pk>/cedit', ComplaintUpdateView.as_view(), name='complaint_update'),
    path('complaint/', ComplaintListVew.as_view(), name='complaint'),
    path('to/<int:to_id>/', to_detail, name='to_detail'),
    path('complaint/<int:complaint_id>/', complaint_detail, name='complaint_detail'),
    path('machine/<int:machine_id>/', machine_detail, name='machine_detail'),
    path('deletemachine/<int:pk>/', MachineDeleteView.as_view(), name='machine_delete'),
    path('deleteto/<int:pk>/', TODeleteView.as_view(), name='to_delete'),
    path('deleteсo/<int:pk>/', ComplaintDeleteView.as_view(), name='complaint_delete'),
    path('complaintlist/<int:machine_id>/', complaint_list_machine, name='complaint_list'),
    path('tolist/<int:machine_id>/', to_list_machine, name='to_list'),
    #Списки списков )))))
    path('servisecomp/', ServiceCompanyListView.as_view(), name='servisecomp'),
    path('modeltech/', TechniqueModelListView.as_view(), name='modeltech'),
    path('modeleng/', EngineModelListView.as_view(), name='modeleng'),
    path('modeltrans/', TransmitionModelListView.as_view(), name='modeltrans'),
    path('modelaxel/', DriveAxleModelListView.as_view(), name='modelaxel'),
    path('modelsteer/', SteeringBridgeModelListView.as_view(), name='modelsteer'),
    path('servisetype/', ServiceTypeListView.as_view(), name='servisetype'),
    path('fnode/', FailureNodeListView.as_view(), name='fnode'),
    path('reco/', RecoveryMethodListView.as_view(), name='reco'),
    #Добавление списков
    path('create_servisecomp/', ServiceCompanyCreateVew.as_view(), name='create_servisecomp'),
    path('create_modeltech/', TechniqueModelCreateVew.as_view(), name='create_modeltech'),
    path('create_modeleng/', EngineModelCreateVew.as_view(), name='create_modeleng'),
    path('create_modeltrans/', TransmissionModelCreateVew.as_view(), name='create_modeltrans'),
    path('create_modelaxel/', DriveAxleModelCreateVew.as_view(), name='create_modelaxel'),
    path('create_modelsteer/', SteeringBridgeModelCreateVew.as_view(), name='create_modelsteer'),
    path('create_servisetype/', ServiceTypeCreateVew.as_view(), name='create_servisetype'),
    path('create_fnode/', FailureNodeCreateVew.as_view(), name='create_fnode'),
    path('create_reco/', RecoveryMethodCreateVew.as_view(), name='create_reco'),
    #Удаление списков
    path('delete_servisecomp/<int:pk>/', ServiceCompanyDeleteView.as_view(), name='delete_servisecomp'),
    path('delete_techniquemodel/<int:pk>/', TechniqueModelDeleteView.as_view(), name='delete_techniquemodel'),
    path('delete_enginemodel/<int:pk>/', EngineModelDeleteView.as_view(), name='delete_enginemodel'),
    path('delete_modeltrans/<int:pk>/', TransmissionModelDeleteView.as_view(), name='delete_modeltrans'),
    path('delete_modelaxel/<int:pk>/', DriveAxleModelDeleteView.as_view(), name='delete_modelaxel'),
    path('delete_modelsteer/<int:pk>/', SteeringBridgeModelDeleteView.as_view(), name='delete_modelsteer'),
   path('delete_servisetype/<int:pk>/', ServiceTypeDeleteView.as_view(), name='delete_servisetype'),
    path('delete_fnode/<int:pk>/', FailureNodeDeleteView.as_view(), name='delete_fnode'),
    path('delete_reco/<int:pk>/', RecoveryMethodDeleteView.as_view(), name='delete_reco'),
    #Редактирование списков
    path('edit_servisecomp/<int:pk>/', ServiceCompanyUpdateView.as_view(), name='edit_servisecomp'),
    path('edit_modeltech/<int:pk>/', TechniqueModelUpdateView.as_view(), name='edit_modeltech'),
   path('edit_enginemodel/<int:pk>/', EngineModelUpdateView.as_view(), name='edit_enginemodel'),
    path('edit_modeltrans/<int:pk>/', TransmissionModelUpdateView.as_view(), name='edit_modeltrans'),
    path('edit_modelaxel/<int:pk>/', DriveAxleModelUpdateView.as_view(), name='edit_modelaxel'),
    path('edit_modelsteer/<int:pk>/', SteeringBridgeModelUpdateView.as_view(), name='edit_modelsteer'),
    path('edit_servisetype/<int:pk>/', ServiceTypeUpdateView.as_view(), name='edit_servisetype'),
    path('edit_fnode/<int:pk>/', FailureNodeUpdateView.as_view(), name='edit_fnode'),
    path('edit_reco/<int:pk>/', RecoveryMethodUpdateView.as_view(), name='edit_reco'),

# API
    path('api/machine/', MachineAPIVew.as_view()),
    path('api/to/', TOAPIVew.as_view()),
    path('api/complaint/', ComplaintAPIVew.as_view()),
    path('openapi', get_schema_view(
        title="My_Silant",
        description="API for My_Silant",
        version="v 1.0.0"
    ), name='openapi-schema'),
]