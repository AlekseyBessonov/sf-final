from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Car, Maintains, Complaint, ServiceCompany, CarModel, Engine, Transmition, LeadBridge, ControlBridge, MaintainceType,\
    BrokeCharacter, RecoveryMethod


# создаём фильтр
class MachineFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т. е. подбираться) информация о товарах
    class Meta:
        model = Car
        fields = (
           'name',
           'engine',
           'trans',
           'leadBR',
           'controlBR',
        )  # поля, которые мы будем фильтровать (т. е. отбирать по каким-то критериям, имена берутся из моделей)


class TOFilter(FilterSet):

    class Meta:
        model = Maintains
        fields = (
            'maintains_type',
            'repaired_car',
            'company',
        )


class ComplaintFilter(FilterSet):

    class Meta:
        model = Complaint
        fields =(
            'failure_node',
            'recovery_method',
            'service_company_complaint',
        )

# Фильтры для списков
class ServiceCompanyFilter(FilterSet):

    class Meta:
        model = ServiceCompany
        fields = (
            'name',
            'discription',
        )

class CarModelFilter(FilterSet):

    class Meta:
        model = CarModel
        fields = (
            'name',
            'discription',
        )

class EngineModelFilter(FilterSet):

    class Meta:
        model = Engine
        fields = (
            'name',
            'discription',
        )

class TransmitionModelFilter(FilterSet):

    class Meta:
        model = Transmition
        fields = (
            'name',
            'discription',
        )

class LeadBridgeFilter(FilterSet):

    class Meta:
        model = LeadBridge
        fields = (
            'name',
            'discription',
        )

class ControlBridgeFilter(FilterSet):

    class Meta:
        model = ControlBridge
        fields = (
            'name',
            'discription',
        )

class ServiceTypeFilter(FilterSet):

    class Meta:
        model = MaintainceType
        fields = (
            'name',
            'discription',
        )

class FailureNodeFilter(FilterSet):

    class Meta:
        model = BrokeCharacter
        fields = (
            'name',
            'discription',
        )

class RecoveryMethodFilter(FilterSet):

    class Meta:
        model = RecoveryMethod
        fields = (
            'name',
            'description',
        )