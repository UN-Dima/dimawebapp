
import os
import pandas as pd
import numpy as np
import difflib
def tamano_carpeta(carpeta):
    tamano_total = 0

    for ruta_actual, carpetas, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_actual, archivo)
            tamano_total += os.path.getsize(ruta_completa)
    tamano_mb = tamano_total / (1024 * 1024)
    return round(tamano_mb,2)

root_t='uploads/'
root='media_root'+'/'+'uploads'
folder_path = root +'/'+ 'content'
zip_path =root+'/'+'Zip'
folders = os.listdir(folder_path)
zips=os.listdir(zip_path)
Area={'Comité de ética':'Comité de ética','Certificado estudiantes':'Estudiante auxiliar',
    'Formatos contrapartidas':'Contrapartidas','Gestión propiedad intelectual':'Propiedad intelectual',
    'Marketing tecnológico':'Lorem impsum','Paz y salvos':'Paz y salvo','Solicitudes':'Solicitudes'}
table=pd.DataFrame(columns=['id','name','size','area','content_id','type','attachment','label'])

i=2
for key,value in Area.items():
    table.loc[i,:]=[i,key,tamano_carpeta(folder_path+'/'+key),value,'formatos',None,root_t+'Zip/'+key+'.rar','folder']
    i=i+1
    for j in os.listdir(folder_path+'/'+key):
        table.loc[i,:]=[i,j,None,value,'formatos',j.split('.')[-1],root_t+'content/'+key+'/'+j,'file']
        i=i+1

table.to_csv('dima_attachment_content.csv',index=False)