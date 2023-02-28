from django.db import models


########################################################################
class QuipuProject(models.Model):
    code = models.CharField('Código Quipu', primary_key=True, max_length=2**5)
    proyecto = models.CharField('Nombre del proyecto', max_length=2**5)
    empresa = models.CharField('Empresa', max_length=2**5)
    inicio_reporte = models.DateField('Desde')
    fin_reporte = models.DateField('Hasta')

    # ----------------------------------------------------------------------

    @property
    def resources_list(self):
        """"""
        return ', '.join([r.resource for r in self.resources.all()])


########################################################################
class Resources_QuipuProject(models.Model):
    proyecto = models.ForeignKey('quipu.QuipuProject', related_name='resources', on_delete=models.CASCADE)
    resource = models.CharField('Recurso', max_length=2**5)


########################################################################
class Row_QuipuProject(models.Model):
    resource = models.ForeignKey('quipu.Resources_QuipuProject', related_name='rows', on_delete=models.CASCADE)
    imputacion = models.BigIntegerField('Imputación')
    apropiacion = models.BigIntegerField('Apropiación definitiva')
    cupo = models.BigIntegerField('Cupo')
    disponibilidad = models.BigIntegerField('Disponibilidad')
    registro = models.BigIntegerField('Registro')
    obligaciones = models.BigIntegerField('Obligaciones')
    pago = models.BigIntegerField('Pago')
    saldo_por_comprometer = models.BigIntegerField('Saldo por comprometer')
    por_ejecutar = models.DecimalField('Porcentaje por ejecutar', decimal_places=2, max_digits=5)






