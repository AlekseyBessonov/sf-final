from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Car, Maintains, Complaint, ServiceCompany, CarModel, Engine, Transmition, \
    LeadBridge, ControlBridge, MaintainceType, BrokeCharacter, RecoveryMethod
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import *
from .filters import *
from rest_framework import generics
from .serializers import MachineSerializer, TOSerializer, ComplaintSerializer
# Create your views here.


class TOListVew(LoginRequiredMixin, ListView):
    model = Maintains
    template_name = 'to.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        filter = TOFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        manager = self.request.user.groups.filter(name='Менеджер') # Фильтруем по менеджеру и проверяем
        if not manager.exists():
            is_manager = 'НЕ Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context


class ComplaintListVew(LoginRequiredMixin, ListView):
    model = Complaint
    context_object_name = 'complaint'
    template_name = 'complaint.html'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        filter = ComplaintFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        manager = self.request.user.groups.filter(name='Менеджер')
        if not manager.exists():
            is_manager = 'НЕ Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context



class TOCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_to',
    )
    template_name = 'to_create.html'
    form_class = TOForm


class ComplaintCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_Maintains',
    )
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

class MachineCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_car',
    )
    template_name = 'machine_create.html'
    form_class = MachineForm

#Представления для редактирования TO, Complaint, Machine
class TOUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_to',)
    template_name = 'to_create.html'
    form_class = TOForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return MaintainceType.objects.get(pk=id)


class ComplaintUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_complaint',)
    template_name = 'complaint_create.html'
    form_class = ComplaintForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Complaint.objects.get(pk=id)

class MachineUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_machine',)
    template_name = 'machine_create.html'
    form_class = MachineForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Car.objects.get(pk=id)


# Представления для удаления данных
class MachineDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_machine',)
    template_name = 'delete_machine.html'
    queryset = Car.objects.all()
    success_url = '/user/'

class TODeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_to',)
    template_name = 'delete_to.html'
    queryset = Maintains.objects.all()
    success_url = '/to/'

class ComplaintDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_complaint',)
    template_name = 'delete_complaint.html'
    queryset = Complaint.objects.all()
    success_url = '/complaint/'


class SearchMachines(ListView):
    model = Car
    template_name = 'search.html'
    context_object_name = 'machine'

    # Функция поиска
    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get('search', '') # Получаем данные из запроса (search)
        if search_query:   # Если данные есть (search==True)
            machine = Car.objects.filter(car_number__icontains=search_query) # Фильтруем по данным из search
            if not machine.exists():  # Если в таблице базы таких данных нет, то присваиваем строке значение о том что их нет )))
                machine = 'К сожалению ничего не найдено :('
        else:   # Если данных для поиска нет (search==False)
            machine = 'К сожалению ничего не найдено :('
        context = machine
        return context

    # Функция проверки является ли пользователь авторизованным
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_aut'] = self.request.user.groups.exists()
        return context


# функция фильтрации по авторизованному пользователю
def by_user_machine(request):
    is_aut = request.user.groups.exists()   # Проверка зарегистрировани ли пользователь
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'

    filter = MachineFilter(request.GET) # Фильтрация перебила всю красоту (((((
    if is_aut:   # Если пользователь зарегистрирован
        if is_manager == 'Менеджер':
            machine = 0
        else:
            machine = Car.objects.filter(client=request.user.first_name) # Фильтруем все строки по полю клиент, если он является пользователем совершающим запрос
            if not machine.exists(): # Если пользователь не является клиентом проверяем является ли он сервисной компанией
                servicelist = ServiceCompany.objects.filter(name=request.user.first_name) # Проверяем есть ли в списке сервисных компаний запись с именм пользователя (сервисная компания)
                if servicelist.exists(): # Если сервисная компания есть в базе идём далее
                    service = ServiceCompany.objects.get(name=request.user.first_name) # Т.к. поле сервисной компании в модели Machine является связанным для начала получаем его id
                    machine = Car.objects.filter(service=service.id) # По id фильтруем все строки по полю сервисной компании
                else:
                    machine = 'К сожалению Ваша техника отсутствует в базе :('
        context = {'machine': machine,
                   'is_aut': is_aut,
                   'filter': filter,
                   'is_manager': is_manager
                   }
    else:
        machine = 'Авторизуйся'
        context = {'machine': machine}
    return render (request, 'user.html', context)


def to_detail(request, to_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        to_d = Maintains.objects.get(pk=to_id)
        machine = Car.objects.get(car_number=to_d.repaired_car)
        service = MaintainceType.objects.get(name=to_d.maintains_type)
        service_company = ServiceCompany.objects.get(name=to_d.company)
        context = {'to_d': to_d,
                   'machine': machine,
                   'is_aut': is_aut,
                   'service': service,
                   'service_company': service_company,
                   'is_manager': is_manager
                   }
    else:
        to_d = 'Авторизуйтесь'
        context = {'to_d': to_d}
    return render(request, 'to_detail.html', context)

def complaint_detail(request, complaint_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_d = Complaint.objects.get(pk=complaint_id)
        machine = Car.objects.get(car_number=complaint_d.machine_complaint)
        node = BrokeCharacter.objects.get(name=complaint_d.failure_node)
        recovery = RecoveryMethod.objects.get(name=complaint_d.recovery_method)
        service = ServiceCompany.objects.get(name=complaint_d.service_company_complaint)
        context = {'complaint_d': complaint_d,
                   'machine': machine,
                   'is_aut': is_aut,
                   'node': node,
                   'recovery': recovery,
                   'service': service,
                   'is_manager': is_manager
                   }
    else:
        complaint_d = 'Авторизуйтесь'
        context = {'complaint_d': complaint_d}
    return render(request, 'complaint_detail.html', context)

def complaint_list_machine(request, machine_id): # Вывод всех рекламаций связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_list = Complaint.objects.filter(machine_complaint=machine_id)
        machine = Car.objects.get(pk=machine_id)
        context = {'complaint_list': complaint_list,
                   'machine': machine,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        complaint_list = 'Авторизуйтесь'
        context = {'complaint_list': complaint_list}
    return render(request, 'complaint_list_machine.html', context)


def to_list_machine(request, machine_id): # Вывод всех ТО связанных с выбранной машиной
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        to_list = ServiceCompany.objects.filter(car=machine_id)
        machine = Car.objects.get(pk=machine_id)
        context = {'to_list': to_list,
                   'machine': machine,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        to_list = 'Авторизуйтесь'
        context = {'to_list': to_list}
    return render(request, 'to_list_machine.html', context)


def machine_detail(request, machine_id):
    is_aut = request.user.groups.exists()
    manager = request.user.groups.filter(name='Менеджер')  # Фильтруем по названию группы аутентифицированного пользователя
    if not manager.exists():
        is_manager = 'НЕ Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        machine = Car.objects.get(pk=machine_id)
        technique = CarModel.objects.get(name=machine.name)
        engine = Engine.objects.get(name=machine.engine)
        trans = Transmition.objects.get(name=machine.trans)
        axle = LeadBridge.objects.get(name=machine.leadBR)
        steering = ControlBridge.objects.get(name=machine.controlBR)
        service = ServiceCompany.objects.get(name=machine.service)
        context = {'machine': machine,
                   'technique': technique,
                   'is_aut': is_aut,
                   'engine': engine,
                   'trans': trans,
                   'axle': axle,
                   'steering': steering,
                   'service': service,
                   'is_manager': is_manager
                   }
    else:
        machine = 'Авторизуйтесь'
        context = {'machine': machine}
    return render(request, 'machine_detail.html', context)

# Списки
# Получение списков
class ServiceCompanyListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_servicecompany')
    model = ServiceCompany
    context_object_name = 'servicecompany'
    template_name = 'lists/servicecompany_list.html'
    queryset = ServiceCompany.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceCompanyFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TechniqueModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_carmodel')
    model = CarModel
    context_object_name = 'techniquemodel'
    template_name = 'lists/techniquemodel_list.html'
    queryset = CarModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = CarModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class EngineModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_engine')
    model = Engine
    context_object_name = 'enginemodel'
    template_name = 'lists/enginemodel_list.html'
    queryset = Engine.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = EngineModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class TransmitionModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_transmition')
    model = Transmition
    context_object_name = 'transmissionmodel'
    template_name = 'lists/transmissionmodel_list.html'
    queryset = Transmition.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = TransmitionModelFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class DriveAxleModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_leadbridge')
    model = LeadBridge
    context_object_name = 'driveaxlemodel'
    template_name = 'lists/driveaxlemodel_list.html'
    queryset = LeadBridge.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = LeadBridgeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class SteeringBridgeModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_controlbridge')
    model = ControlBridge
    context_object_name = 'steeringbridgemodel'
    template_name = 'lists/steeringbridgemodel_list.html'
    queryset = ControlBridge.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ControlBridgeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class ServiceTypeListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_maintaincetype')
    model = MaintainceType
    context_object_name = 'servicetype'
    template_name = 'lists/servicetype_list.html'
    queryset = MaintainceType.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceTypeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class FailureNodeListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_brokecharacter')
    model = BrokeCharacter
    context_object_name = 'failurenode'
    template_name = 'lists/failurenode_list.html'
    queryset = BrokeCharacter.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = FailureNodeFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class RecoveryMethodListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_recoverymethod')
    model = RecoveryMethod
    context_object_name = 'recoverymethod'
    template_name = 'lists/recoverymethod_list.html'
    queryset = RecoveryMethod.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = RecoveryMethodFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context

# Добавление списков
class ServiceCompanyCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm
    login_url = '/'


class TechniqueModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_carmodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm
    login_url = '/'

class EngineModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = 'service.add_Engine'
    template_name = 'lists/create.html'
    form_class = EngineModelForm
    login_url = '/'

class TransmissionModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_transmition')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm
    login_url = '/'

class DriveAxleModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_leadbridge')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm
    login_url = '/'

class SteeringBridgeModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_controlbridge')
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm
    login_url = '/'

class ServiceTypeCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_maintaincetype')
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm
    login_url = '/'

class FailureNodeCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_brokecharacter')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm
    login_url = '/'

class RecoveryMethodCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm
    login_url = '/'

# Формы для удаления списков
class ServiceCompanyDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_servicecompany')
    template_name = 'lists/delete_servicecompany.html'
    queryset = ServiceCompany.objects.all()
    success_url = '/servisecomp/'
    login_url = '/'

class TechniqueModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_carmodel')
    template_name = 'lists/delete_techniquemodel.html'
    queryset = CarModel.objects.all()
    success_url = '/modeltech/'
    login_url = '/'

class EngineModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_engine')
    template_name = 'lists/delete_enginemodel.html'
    queryset = Engine.objects.all()
    success_url = '/modeleng/'
    login_url = '/'

class TransmissionModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_transmition')
    template_name = 'lists/delete_transmissionmodel.html'
    queryset = Transmition.objects.all()
    success_url = '/modeltrans/'
    login_url = '/'

class DriveAxleModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_leabr')
    template_name = 'lists/delete_driveaxlemodel.html'
    queryset = LeadBridge.objects.all()
    success_url = '/modelaxel/'
    login_url = '/'

class SteeringBridgeModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_controlbr')
    template_name = 'lists/delete_steeringbridgemodel.html'
    queryset = ControlBridge.objects.all()
    success_url = '/modelsteer/'
    login_url = '/'

class ServiceTypeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_servicetype')
    template_name = 'lists/delete_servicetype.html'
    queryset = MaintainceType.objects.all()
    success_url = '/servisetype/'
    login_url = '/'

class FailureNodeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_BrokeCharacter')
    template_name = 'lists/delete_failurenode.html'
    queryset = BrokeCharacter.objects.all()
    success_url = '/fnode/'
    login_url = '/'

class RecoveryMethodDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_recoverymethod')
    template_name = 'lists/delete_recoverymethod.html'
    queryset = RecoveryMethod.objects.all()
    success_url = '/reco/'
    login_url = '/'

# Редактирование списков
class ServiceCompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceCompany.objects.get(pk=id)

class TechniqueModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_carmodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return CarModel.objects.get(pk=id)

class EngineModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_engine')
    template_name = 'lists/create.html'
    form_class = EngineModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Engine.objects.get(pk=id)

class TransmissionModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_transmition')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Transmition.objects.get(pk=id)

class DriveAxleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_leadbr')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return LeadBridge.objects.get(pk=id)

class SteeringBridgeModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_controlbr')
    template_name = 'lists/create.html'
    form_class = SteeringBridgeModelForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ControlBridge.objects.get(pk=id)

class ServiceTypeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_servicetype')
    template_name = 'lists/create.html'
    form_class = ServiceTypeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return MaintainceType.objects.get(pk=id)

class FailureNodeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_brokecharacter')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return BrokeCharacter.objects.get(pk=id)

class RecoveryMethodUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm # Форму берём ту же что и для добавления новых данных

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return RecoveryMethod.objects.get(pk=id)

class MachineAPIVew(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = MachineSerializer


class TOAPIVew(generics.ListAPIView):
    queryset = Maintains.objects.all()
    serializer_class = TOSerializer


class ComplaintAPIVew(generics.ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

