from django.db import models
from utils.models import Choices


########################################################################
class PersonBase():
    """"""
    # ----------------------------------------------------------------------

    def __str__(self):
        """"""
        return self.full_name

    # ----------------------------------------------------------------------
    @property
    def full_name(self):
        """"""
        return f'{self.first_name} {self.last_name}'

    # ----------------------------------------------------------------------
    def fix_name(name: str) -> dict:
        """"""
        name = name.lower().replace(' del', '_del').replace(' de', '_de').strip().split()
        # match len(name):

        if len(name) == 1:  # only first name
            return {'first_name': ''.join(name).title()}

        elif len(name) == 2:  # one first name and one last name
            return {'first_name': name[1].title(),
                    'last_name': name[0].title()}

        elif len(name) == 3:  # one first name and two last name
            return {'first_name': name[-1],
                    'last_name': ' '.join(name[:-1]).replace('_', ' ').title()}

        elif len(name) == 4:  # first name and last name
            return {'first_name': ' '.join(name[-2:]).replace('_', ' ').title(),
                    'last_name': ' '.join(name[:-2]).replace('_', ' ').title()}

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if attr.endswith('_pretty'):
            field = attr.replace('_pretty', '')
            if field in [field.name for field in self._meta.fields]:
                return dict(self._meta.get_field(field).choices)[getattr(self, field)]

        elif attr.endswith('_json'):
            field = attr.replace('_json', '')
            return json.loads(getattr(self, field))

        return super().__getattr__(attr)


########################################################################
class Professor(PersonBase, models.Model):
    """"""
    first_name = models.CharField('Nombre(s)', max_length=2**6)
    last_name = models.CharField('Apellido(s)', max_length=2**6)
    professor_id = models.BigIntegerField('Documento de identificaci??n', primary_key=True)
    category = models.CharField('Categor??a', **Choices('RESEARCHER_CATEGORY'))
    faculty = models.CharField('Facultad', **Choices('FACULTY'))
    departament = models.CharField('Departamento', **Choices('DEPARTAMENT'))
    cvlac = models.URLField('CvLAC', null=True, blank=True)

    class Meta:
        verbose_name = "Docente"


########################################################################
class Researcher(PersonBase, models.Model):
    """"""
    first_name = models.CharField('Nombre(s)', max_length=2**6)
    last_name = models.CharField('Apellido(s)', max_length=2**6)
    researcher_id = models.BigIntegerField('Documento de identificaci??n', primary_key=True)
    joined = models.DateField('Fecha de integraci??n', default='django.utils.timezone.now')
    departed = models.DateField('Fecha de partida', null=True, blank=True)

    class Meta:
        verbose_name = "Investigador"
