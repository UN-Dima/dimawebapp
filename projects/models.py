from django.db import models
from utils.models import Choices

import zlib
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
import json


########################################################################
class Call(models.Model):
    """"""
    name = models.CharField('Name', max_length=2**7)
    date = models.DateField('Date', auto_now_add=True)
    call_type = models.CharField('Type', **Choices('CALL_TYPE'))


########################################################################
class Project(models.Model):
    """"""
    hermes_cod = models.BigIntegerField('Código Hermes', primary_key = True)
    quipu_cod_0 = models.BigIntegerField('Código QUIPU_1', null=True, blank=True)
    quipu_cod_1 = models.BigIntegerField('Código QUIPU_2', null=True, blank=True)
    project_name = models.CharField('Nombre del Proyecto',max_length=2**6)
    project_state = models.CharField('Estado del Proyecto',**Choices('PROJECT_STATE'))
    call_type = models.CharField('Tipo de convocatoria',**Choices('CALL_TYPE'),default='')
    call = models.CharField('Convocatoria',max_length=2**6)
    modality = models.CharField('Modalidad',max_length=2**6)
    #professor = models.ForeignKey('researchers.Professor', verbose_name='Identificación Investigador', on_delete=models.CASCADE, null=True, blank=True, related_name='projects')
    professor_id = models.BigIntegerField('Identificación Investigador')
    first_name = models.CharField('Nombre(s)', max_length=2**6)
    last_name = models.CharField('Apellido(s)', max_length=2**6)
    email=models.EmailField('Correo del Investigador')
    departament = models.CharField('Departamento', **Choices('DEPARTAMENT'))
    faculty = models.CharField('Facultad', **Choices('FACULTY'))
    start_date = models.CharField('Fecha Inicio',null=True,blank=True, max_length=2**6)
    end_date = models.CharField('Fecha Inicio',null=True,blank=True, max_length=2**6) 
    total_project = models.IntegerField('Total Proyecto',null=True,blank=True)
    total_appropriation = models.IntegerField('Total Apropiación',null=True,blank=True)
    executed = models.IntegerField('Ejecutado',null=True,blank=True)
    total_commitment_balance = models.IntegerField('Total Saldo por Comprometer',null=True,blank=True)
    execution_percentage = models.FloatField('Porcentaje Ejecutado',null=True,blank=True)

    def __getattr__(self, attr):
        """"""
        if attr.endswith('_pretty'):
            field = attr.replace('_pretty', '')
            if field in [fields.name for fields in self._meta.fields]:
                return dict(self._meta.get_field(field).choices)[getattr(self, field)]

        elif attr.endswith('_json'):
            field = attr.replace('_json', '')
            return json.loads(getattr(self, field))

        return super().__getattr__(attr)

    @property
    def obscure(self):
        return b64e(zlib.compress(str(self.pk).encode(), 9)).decode()

    # ----------------------------------------------------------------------
    @classmethod
    def unobscure(cls, obscured: bytes) -> bytes:
        return zlib.decompress(b64d(obscured))

    class Meta:
        verbose_name = "Proyecto"
