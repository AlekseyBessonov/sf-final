from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class CarModel (models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    discription = models.CharField(max_length=128, verbose_name='Описание')

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/modeltech'

    class Meta:
        verbose_name = 'Модель погрузчика'
        verbose_name_plural = 'Модели погрузчиков'

class Engine (models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/modeleng'

    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателя'

class Transmition (models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/modeltrans'

    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссии'

class LeadBridge (models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/modelaxel'

    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'

class ControlBridge(models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16,verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/modelsteer'

    class Meta:
        verbose_name = 'Модель управляющего моста'
        verbose_name_plural = 'Модели управляющего моста'

class ServiceCompany(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    discription = models.CharField(max_length=120, verbose_name='Описание')
    logo = models.ImageField(upload_to='logo/', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/servisecomp'

    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'


class Car(models.Model):
    name = models.ForeignKey(CarModel, related_name='Car', verbose_name='Модель техники', on_delete=models.CASCADE)
    car_number = models.CharField(max_length=18, verbose_name='Зав № техники', null=False, blank=False)
    engine = models.ForeignKey(Engine, verbose_name='Модель двигателя', on_delete=models.CASCADE)
    engine_number = models.CharField(max_length=10, verbose_name='Зав № двигателя')
    trans = models.ForeignKey(Transmition, verbose_name='Модель трансмиссии', on_delete=models.CASCADE)
    trans_number = models.CharField(max_length=10, verbose_name='Зав. № трансмиссии')
    leadBR= models.ForeignKey(LeadBridge, verbose_name='Модель ведущего моста', on_delete=models.CASCADE)
    leadBR_number = models.CharField(max_length=10, verbose_name='Зав № ведущего моста')
    controlBR= models.ForeignKey(ControlBridge, verbose_name='Модель управляемого моста', on_delete=models.CASCADE)
    controlBR_number = models.CharField(max_length=10, verbose_name='Зав № управляемого моста')
    contract_Date = models.CharField(max_length=20, verbose_name='Дата и номер договора')
    shipment_date = models.DateField(verbose_name='Дата отгрузки', null=False, blank=False)
    adress = models.CharField(max_length=120, verbose_name='Адрес доставки')
    complectation = models.CharField(max_length=120 ,verbose_name='Комплектация')
    client = models.CharField(max_length=64, verbose_name='Покупатель')
    user = models.CharField(max_length=64, verbose_name='Грузополучатель', default=client)
    user_adress = models.CharField(max_length=120, verbose_name='Адрес поставки', default=adress)
    service = models.ForeignKey(ServiceCompany, verbose_name='Сервисная кампания', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.car_number)

    def get_absolute_url(self):
        return f'/user'

    class Meta:
        verbose_name = 'Погрузчик'
        ordering = ['-shipment_date'] # Сортировка по дате отгрузки
        verbose_name_plural = 'Погрузчики'

#class RepairType (models.Model):
#    name = models.CharField(max_length=20, verbose_name='Название')
#    discription = models.CharField(max_length=80, verbose_name='Описание', null=True, blank=True)
#
#    def __str__(self):
#        return str(self.name)
#
#    class Meta:
#        verbose_name = 'Тип восстановления'
#      verbose_name_plural='Типы восстановления'



class MaintainceType (models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/maintaincetype'

    class Meta:
        verbose_name = 'Вид ТО'
        verbose_name_plural = 'Виды ТО'



class BrokeCharacter (models.Model):
    name = models.CharField(max_length=20, verbose_name='Название')
    discription = models.CharField(max_length=16, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/brchar'

    class Meta:
        verbose_name = 'Характер отказа'
        verbose_name_plural = 'Характер отказа'



class RecoveryMethod(models.Model):
    name = models.CharField(max_length=32, verbose_name='Название')
    description = models.CharField(max_length=32, verbose_name='Описание', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/recmethod'

    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'

class Maintains(models.Model):
    maintains_type = models.ForeignKey(MaintainceType, default='', verbose_name='Вид ТО', on_delete=models.CASCADE)
    company = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.SET_NULL, null=True)
    repaired_car = models.ForeignKey(Car, verbose_name='Зав. № машины', on_delete=models.CASCADE)
    date = models.DateField(verbose_name='Дата начала ТО')  #Дата начала ТО
    order_number = models.CharField(max_length=10, verbose_name='Номер наряд-заказа')
    order_date = models.DateTimeField(verbose_name='Дата окончания ТО')
    car_work_time = models.FloatField(default=0, verbose_name='Время наработки (м\час)')


    def __str__(self):
        return self.order_number

    def get_absolute_url(self):
        return f'/to'

    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Техническое обслуживание'
        ordering = ['-order_date']  # Фильтрация по дате проведения ТО

class Complaint(models.Model):
    date_rejection = models.DateField(verbose_name='Дата отказа')
    operating_time = models.FloatField(verbose_name='Наработка, м\час')
    failure_node = models.ForeignKey(BrokeCharacter, verbose_name='Узел отказа', on_delete=models.CASCADE)
    failure_description = models.TextField(verbose_name='Описание отказа')
    recovery_method = models.ForeignKey(RecoveryMethod, verbose_name='Способ восстановления', on_delete=models.CASCADE)
    spare_parts = models.TextField(verbose_name='Используемые запасные части', null=True, blank=True)
    recovery_date = models.DateField(verbose_name='Дата восстановления')
    machine_complaint = models.ForeignKey(Car, verbose_name='Зав. № машины', on_delete=models.CASCADE)
    service_company_complaint = models.ForeignKey(ServiceCompany, verbose_name='Сервисная компания', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f'/complaint'

    def downtime(self):
        return (self.recovery_date - self.date_rejection).days

    def __str__(self):
        return self.failure_description

    class Meta:
        verbose_name = 'Рекламации'
        verbose_name_plural = 'Рекламации'
        ordering = ['-date_rejection']




