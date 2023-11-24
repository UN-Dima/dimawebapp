import os
import subprocess
import random

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tinymce.models import HTMLField
from datetime import date

from utils.update_db import update_table

upload_to_newsletter = os.path.join('uploads', 'newsletter')
upload_to_broadcast = os.path.join('uploads', 'broadcast')
upload_to_content = os.path.join('uploads', 'content')
upload_to_updates = os.path.join('uploads', 'updates')


# ----------------------------------------------------------------------
def run_command(command):
    """This post save function creates a thumbnail for the commentary PDF"""
    proc = subprocess.Popen(command,
                            shell=True,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )
    return proc.communicate()[0]


########################################################################
class Content(models.Model):
    """"""
    label = models.CharField('Destino', primary_key=True, max_length=2**7, editable=True)
    content = HTMLField('Contenido', max_length=2**15)

    # ----------------------------------------------------------------------
    class Meta:
        verbose_name = "Contenido estático"
        verbose_name_plural = "Contenidos estáticos"

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'Editar el contenido que se mostrará en la sección de "{self.label.capitalize()}"'


########################################################################
class Attachment_Content(models.Model):
    content = models.ForeignKey('dima.Content', related_name='attachment', on_delete=models.CASCADE)
    name = models.CharField('Nombre del archivo', max_length=2 ** 10)
    attachment = models.FileField('Adjunto', upload_to=upload_to_content, blank=True, null=True)
    type= models.CharField('Tipo', max_length=2 ** 10,blank=True, null=True)
    size=models.FloatField('Tamaño',blank=True, null=True)
    area=models.CharField('Área', max_length=2 ** 10,blank=True, null=True)
    label=models.CharField('Etiqueta', max_length=2 ** 10,blank=True, null=True)
    class Meta:
        verbose_name = "Adjunto"


########################################################################
class Team(models.Model):
    """"""
    area = models.CharField('Area', max_length=2**8)
    names = models.CharField('Nombres', help_text='Separados por coma (,)', max_length=2**8)
    email = models.CharField('Correos electrónicos', help_text='Separados por coma (,)', max_length=2**8)
    ext = models.CharField('Extensiones', max_length=2**3, help_text='Separados por coma (,)')

    # ----------------------------------------------------------------------
    class Meta:
        verbose_name = "Equipo de trabajo"
        verbose_name_plural = "Equipo de trabajo"

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""
        if attr.endswith('_split'):
            field = attr.replace('_split', '')
            return getattr(self, field).split(',')

        return super().__getattr__(attr)

    # ----------------------------------------------------------------------

    def __str__(self):
        return f'Editar equipo de trabajo'


########################################################################
class Newsletter(models.Model):
    """"""
    file = models.FileField('Boletín', upload_to=upload_to_newsletter)
    upload = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(upload_to=upload_to_newsletter, blank=True, null=True)

    # ----------------------------------------------------------------------
    class Meta:
        verbose_name = "Boletín"
        verbose_name_plural = "Boletines"

    # ----------------------------------------------------------------------
    def save(self):
        """"""
        thumbnail = f"{self.file.name.removesuffix('.pdf')}.png"
        self.thumbnail = os.path.join(upload_to_newsletter, thumbnail)
        super(Newsletter, self).save()

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'Editar boletín (ID:#{self.pk})'


class UpdateFiles(models.Model):
    """"""
    table_to_update = models.CharField('Tabla', max_length=2**8, help_text='Base de Datos a Actualizar')
    file = models.FileField('Archivo', upload_to=upload_to_updates)
    upload_date = models.DateTimeField(auto_now_add=True)

    def save(self):
        """"""
        if self.file.name.lower().endswith('.xls') or self.file.name.lower().endswith('.xml'):
            super(UpdateFiles, self).save()
            print(self.file.name)
            update_table(self.table_to_update, self.file.name)
            print('Hello, World!')
        else:
            raise 'Archivo No Soportado'

    class Meta:
        verbose_name = "Actualizar XLS"
        verbose_name_plural = "Actualizaciónes de XLS"

    def __str__(self):
        return f'Editar xls de referencia'
        

########################################################################
class Broadcast(models.Model):
    """"""
    image = models.FileField('Imagen para difusión', upload_to=upload_to_broadcast)
    expiration = models.DateField('Finalización', help_text='Hasta cuando será visible en el carusel')
    link = models.URLField('Link de referencia', help_text='Opcional', blank=True, null=True)
    title = models.CharField('Titulo', help_text='Opcional', max_length=2 ** 10, blank=True, null=True)
    description = models.TextField('Descripción', help_text='Opcional', max_length=2**10, blank=True, null=True)
    upload = models.DateTimeField(auto_now_add=True)
    dominant = models.CharField(max_length=7, blank=True, null=True, editable=False)
    active = models.BooleanField('Difusión activa', help_text='La oculta del carusel ', default=True)

    # ----------------------------------------------------------------------
    class Meta:
        verbose_name = "Difusión (imagen en carusel)"
        verbose_name_plural = "Difusiónes"

    # ----------------------------------------------------------------------
    def save(self):
        """"""
        super().save()
        command = f"{settings.SCRIPTS_ROOT}/dominantcolor {self.image.path}"
        dominant = run_command(command).strip()
        self.dominant = dominant.decode()
        super().save()

    # ----------------------------------------------------------------------
    @property
    def expired(self):
        return date.today() > self.expiration

    # ----------------------------------------------------------------------
    @property
    def show(self):
        return self.active and not self.expired

    # ----------------------------------------------------------------------
    def __str__(self):
        return f'Difución (ID:#{self.pk})'


# ----------------------------------------------------------------------
@receiver(post_save, sender=Newsletter)
def on_post_save(sender, instance=False, **kwargs):
    """"""
    newsletter = sender.objects.get(pk=instance.pk)
    command = f"convert -quality 95 -thumbnail 222 {newsletter.file.path}[0] {newsletter.thumbnail.path}"
    run_command(command)


# ----------------------------------------------------------------------
@receiver(post_delete, sender=Broadcast)
def on_post_delete_broadcast(sender, instance, **kwargs):
    """"""
    for object_ in ['image']:
        if file := getattr(instance, object_, None):
            if os.path.isfile(file.path):
                os.remove(file.path)


# ----------------------------------------------------------------------
@receiver(post_delete, sender=Newsletter)
def on_post_delete_newsletter(sender, instance, **kwargs):
    """"""
    for object_ in ['file', 'thumbnail']:
        if file := getattr(instance, object_, None):
            if os.path.isfile(file.path):
                os.remove(file.path)


# ----------------------------------------------------------------------
@receiver(post_delete, sender=Attachment_Content)
def on_post_delete_Attachment_Content(sender, instance, **kwargs):
    """"""
    for object_ in ['attachment']:
        if file := getattr(instance, object_, None):
            if os.path.isfile(file.path):
                os.remove(file.path)
