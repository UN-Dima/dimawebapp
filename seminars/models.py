from django.db import models
from utils.models import Choices
import json


########################################################################
class Seminars(models.Model):
    """
    
    """
    code = models.BigIntegerField('Código', primary_key=True)
    name = models.CharField('Nombre del semillero', max_length=2**7)
    state = models.CharField('Estado actual',**Choices('SEMINAR_STATE'))
    #Leader should be a foreign key, however seminar db returns the name rather than the id
    #leading to issues regarding accents when doing queries
    leader = models.CharField('Líder', max_length=2**16, default='') # models.ForeignKey('researchers.Professor', verbose_name='Lider', on_delete=models.CASCADE, null=True, blank=True, related_name='seminars')
    email = models.CharField('E-mail', max_length=2**8)
    faculty = models.CharField('Facultad', **Choices('FACULTY'))
    departament = models.CharField('Departamento', **Choices('DEPARTAMENT'))
    founded = models.DateField('Fecha de creación', default='django.utils.timezone.now')
    intro = models.TextField('Presentación', max_length=2**16, null=True, blank=True)
    general_obj = models.TextField('Objetivo General', max_length=2**16, null=True, blank=True)
    justification = models.TextField('Justificación', max_length=2**16, null=True, blank=True)
    focus = models.TextField('Enfoque', max_length=2**16, null=True, blank=True)
    ocde = models.CharField('OCDE', max_length=2**16)
    ODS = models.TextField('Objetivo de desarrollo sosternible', max_length=2**8)
    knowledge_area = models.CharField('Agenda del conocimiento', **Choices('KNOWLEDGE'))
    discourse = models.TextField('Pertinencia / Articulación con grupos de investigación', max_length=2**16, null=True, blank=True)
    methodology = models.TextField('Metodología', max_length=2**16, null=True, blank=True)
    lines = models.TextField('Líneas de investigación', max_length=2**16, null=True, blank=True)

    class Meta:
        verbose_name = "Semillero"
        verbose_name_plural = "Semillero"

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if attr.endswith('_pretty'):
            field = attr.replace('_pretty', '')
            if field in [field.name for field in self._meta.fields]:
                return dict(self._meta.get_field(field).choices).get(getattr(self, field), '')

        elif attr.endswith('_json'):
            field = attr.replace('_json', '')
            return json.loads(getattr(self, field).replace('\'', '\"'))

        return super().__getattr__(attr)

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'Editar semillero (Código: #{self.code})'
