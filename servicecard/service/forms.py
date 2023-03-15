from django.forms import ModelForm
from .models import *

class TOForm(ModelForm):

    class Meta:
        model = Maintains
        fields = [
            'maintains_type',
            'date',
            'car_work_time',
            'order_number',
            'order_date',
            'company',
            'repaired_car',
        ]


class ComplaintForm(ModelForm):

    class Meta:
        model = Complaint
        fields = [
            'date_rejection',
            'operating_time',
            'failure_node',
            'failure_description',
            'recovery_method',
            'spare_parts',
            'recovery_date',
            'machine_complaint',
            'service_company_complaint',
        ]

class MachineForm(ModelForm):

    class Meta:
        model = Car
        fields = [
            'car_number',
            'name',
            'engine',
            'engine_number',
            'trans',
            'trans_number',
            'leadBR',
            'leadBR_number',
            'controlBR',
            'controlBR_number',
            'contract_Date',
            'shipment_date',
            'adress',
            'complectation',
            'client',
            'service',
        ]

# Формы списков
class ServiceCompanyForm(ModelForm):

    class Meta:
        model = ServiceCompany
        fields = [
            'name',
            'discription',
        ]

class TechniqueModelForm(ModelForm):

    class Meta:
        model = CarModel
        fields = [
            'name',
            'discription',
        ]

class EngineModelForm(ModelForm):

    class Meta:
        model = Engine
        fields = [
            'name',
            'discription',
        ]

class TransmissionModelForm(ModelForm):

    class Meta:
        model = Transmition
        fields = [
            'name',
            'discription',
        ]

class DriveAxleModelForm(ModelForm):

    class Meta:
        model = LeadBridge
        fields = [
            'name',
            'discription',
        ]

class SteeringBridgeModelForm(ModelForm):

    class Meta:
        model = ControlBridge
        fields = [
            'name',
            'discription',
        ]

class ServiceTypeForm(ModelForm):

    class Meta:
        model = ServiceCompany
        fields = [
            'name',
            'discription',
        ]

class FailureNodeForm(ModelForm):

    class Meta:
        model = BrokeCharacter
        fields = [
            'name',
            'discription',
        ]

class RecoveryMethodForm(ModelForm):

    class Meta:
        model = RecoveryMethod
        fields = [
            'name',
            'description',
        ]