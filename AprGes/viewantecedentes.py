import pyodbc

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404 , render_to_response, get_list_or_404 
from time import gmtime, strftime

import time
import datetime

import pdfkit
import mysql.connector

from django.http import HttpResponse
from django import template

import xlrd
import xlwt
import os.path as path

import os
import subprocess
from AprGes.utils import render_to_pdf

#Instalar CONTROLADOR ODBC especifico según 64bits o 32bits del computador , en este caso es controlador en 64bits
"""
try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\RiegoWeb\\Riego\\RIEGO.mdb')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass
"""
try:
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=JMC-HP\APRGES;'
                      'Database=APRGESMALLARA;'
                      'Trusted_Connection=yes;')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass

def viewName():

    nombre=""
    sql="SELECT NOMBRE FROM DATOS_COMITE"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            nombre=i[0]
            
    except Exception as e:
        print(e)

    return nombre

def buscarTipos():

    try:
        cursor.execute('select * from A_TIPO_AGUA')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1],'fecha':row[3]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def Id0000(nombre):

    sqlexiste="SELECT RUT FROM OPER_CLIENTE WHERE CORRELATIVO="+nombre+";"

    try:
        cursor.execute(sqlexiste)
        for i in cursor.fetchall():
            return 1
    except:
        pass

    return 0

def buscarTenencia():

    try:
        cursor.execute('select * from A_TENENCIA')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def buscarSector():

    try:
        cursor.execute('select * from GLO_SECTOR')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def buscarpor():

    lista=[]

    try:
        cursor.execute('select OPER_CLIENTE.TIPO , OPER_CLIENTE.* from OPER_CLIENTE')
        
        for row in cursor.fetchall():
            lista.append({'tipo':row[0],'id':row[1],'nombre':row[3]})        

    except Exception as e:
        pass
        print(e)

    return lista

def buscarporNombre():

    lista=[]

    try:
        cursor.execute('select OPER_CLIENTE.TIPO , OPER_CLIENTE.* from OPER_CLIENTE')
        
        for row in cursor.fetchall():
            lista.append({'tipo':row[0],'id':row[1],'nombre':row[3]})        

    except Exception as e:
        pass
        print(e)
    
    try:
        cursor.execute('select A_FUNCIONARIOS.TIPO ,A_FUNCIONARIOS.* from A_FUNCIONARIOS')
        
        for row in cursor.fetchall():
            lista.append({'tipo':row[0],'id':row[1],'nombre':row[4]+ " " + row[5]})        
    except Exception as e:
        pass
        print(e)
    
    try:
        cursor.execute('select A_PROVEEDORES.TIPO ,A_PROVEEDORES.* from A_PROVEEDORES')
        
        for row in cursor.fetchall():
            lista.append({'tipo':row[0],'id':row[1],'nombre':row[3]})        
           
    except Exception as e:
        pass
        print(e)
    
    return lista

def buscarporProveedor():

    try:
        cursor.execute('select * from A_PROVEEDORES')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[2]})      
            print(lista)  
        return lista

    except Exception as e:
        pass
        print(e)

def buscarporFuncionario():

    try:
        cursor.execute('select * from A_FUNCIONARIOS')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[3]+" "+row[4]})        
        return lista

    except Exception as e:
        pass
        print(e)

def correlativoSocio():
    correlativo=0

    #sql="SELECT MAX(ID) FROM A_SOCIOS"
    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_CLIENTE"
    
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    
    return correlativo

def viewSocios(request):

    mensaje=""

    if request.method=='POST' and 'eliminar' in request.POST:

        nombre=request.POST['identi1'].replace(' ','')

        sql="DELETE FROM OPER_CLIENTE WHERE CORRELATIVO="+nombre
        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Se elimino correctamente"
        except Exception as a:
            print(a)

    if request.method=='POST' and 'buscar' in request.POST:

        nombre=request.POST['identi'].replace(' ','')
        id_=""
        rut=""
        nombres=""
        apellidos=""
        direccion=""
        fecha=""
        hec=""
        ruta=""
        correo=""
        rol=""
        tenencia=""
        agricultor=""
        nopago=""
        sector=""
        nombresector=""
        nombretenencia=""
        vigente=""

        try:
            sql="SELECT A_SOCIOS.*, A_SECTOR.NOMBRE, A_TENENCIA.NOMBRE, A_SOCIOS.VIGENTE FROM (A_SOCIOS INNER JOIN A_TENENCIA ON A_SOCIOS.ID_TENENCIA = A_TENENCIA.ID) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE (((A_SOCIOS.ID)="+nombre+"))"
            print(sql)
            cursor.execute(sql)

            for i in cursor.fetchall():
                id_=i[0]
                rut=i[1]
                nombres=i[2]
                apellidos=i[3]
                direccion=i[4]
                fecha=i[5]
                hec=i[6]
                ruta=i[7]
                correo=i[8]
                rol=i[9]
                tenencia=i[10]
                agricultor=i[11]
                nopago=i[15]
                sector=i[12]
                nombresector=i[16]
                nombretenencia=i[17]
                vigente=i[13]

            data={
                'correlativo':id_,
                'rut':rut,
                'nombres':nombres,
                'apellidos':apellidos,
                'direccion':direccion,
                'fecha':fecha,
                'hec':hec,
                'ruta':ruta,
                'correo':correo,
                'rol':rol,
                'tenenciaid':tenencia,
                'agricultor':agricultor,
                'idsector':sector,
                'nombresector':nombresector,
                'nombretenencia':nombretenencia,
                'asociacion':viewName(),
                'tenencia':buscarTenencia(),
                'sector':buscarSector(),
                'vigente':vigente,
                'all_socios':buscarporNombre,
                'nopago':nopago
            }

            return render(request,'antecedentes/socio.html', data)

        except Exception as e:
            pass
            print(e)

    if request.method=='POST' and 'guardar' in request.POST:

        id_=request.POST['identi1']
        cliente=request.POST['rut']
        cliente1=cliente[0:2]
        cliente2=cliente[3:6]
        cliente3=cliente[7:10]
        rut=cliente1+cliente2+cliente3
        nombres=request.POST['nombres']
        apellidos=request.POST['apellidos']
        direccion=request.POST['direccion']
        sitio=request.POST['sitio']
        telefono=request.POST['telefono']
        ruta=request.POST['ruta']
        fecha=request.POST['fecha']
        socio=request.POST['socio']
        correo=request.POST['correo']
        dia_pago=request.POST['dia_pago']
        nro_contable=request.POST['nro_contable']
        sexo=request.POST['sexo']
        glosa=request.POST['glosa']
        # hec=request.POST['hec'].replace(",", ".")
        # n_rol=request.POST['rol']
        # tenencia=request.POST['idtenencia']
        # agricultor=request.POST['agricultor']
        # sector=request.POST['sector']
        # estado=request.POST.getlist('radio')
        # nopago=request.POST.getlist('radio1')

        for i in estado:
            vigente=i[0]
        
        for i in nopago:
            multa=i[0]

        existe=Id0000(id_)

        print("valorrr" + str(existe))

        if existe==0:

            sql1="INSERT INTO A_SOCIOS(ID,RUT,NOMBRES,APELLIDOS,DIRECCION,FECHA_INGRESO,TOTAL_HEC,RUTA,CORREO,N_ROL,ID_TENENCIA,NOMBRE_AGRICULTOR,ID_SECTOR,VIGENTE,MULTAXNOPAGO) VALUES ("+str(id_)+",'"+cliente+"','"+nombres+"','"+apellidos+"','"+direccion+"','"+fecha+"','"+hec+"',"+ruta+",'"+correo+"','"+n_rol+"',"+tenencia+",'"+agricultor+"',"+sector+","+str(vigente)+","+str(multa)+")"
            print(sql1)
            try:
                cursor.execute(sql1)
                conn.commit()
                mensaje="Se guardo correctamente"
                                    
            except Exception as e:
                pass
                print(e)    
                mensaje="No coinciden los campos " 

            data={
                'asociacion':viewName(),
                'correlativo':correlativoSocio(),
                'tenencia':buscarTenencia(),
                'sector':buscarSector(),
                'mensaje':"Quedo guardado correctamente.",
                'all_socios':buscarpor()
            }

            return render(request,'antecedentes/socio.html', data)   

        else:
            sql="UPDATE A_SOCIOS SET RUT='"+cliente+"', NOMBRES='"+nombres+"', APELLIDOS='"+apellidos+"', DIRECCION='"+direccion+"', FECHA_INGRESO='"+fecha+"', TOTAL_HEC="+str(hec)+", RUTA="+ruta+", CORREO='"+correo+"', N_ROL='"+n_rol+"', ID_TENENCIA="+tenencia+", NOMBRE_AGRICULTOR='"+agricultor+"', ID_SECTOR="+sector+" , VIGENTE="+str(vigente)+", MULTAXNOPAGO="+str(multa)+" WHERE ID="+id_
            print(sql)

            try:
                cursor.execute(sql)
                conn.commit()
                mensaje="Se modifico correctamente."
                print("Se debe modificar")

            except Exception as e:
                pass
                print(e)
                mensaje="No coinciden los campos "

            data={
                'mensaje':mensaje,
                'asociacion':viewName(),
                'correlativo':correlativoSocio(),
                'tenencia':buscarTenencia(),
                'sector':buscarSector(),
                'all_socios':buscarpor()
            }

            return render(request,'antecedentes/socio.html', data)

    data={
        'asociacion':viewName(),
        'correlativo':correlativoSocio(),
        'tenencia':buscarTenencia(),
        'sector':buscarSector(),
        'all_socios':buscarpor(),
        'mensaje':mensaje
    }

    return render(request,'antecedentes/socio.html', data)

def numero_orden():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_ORDENTRABAJO"
    correlativo=0

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    
    return correlativo

def orden(request):
    pdf= render_to_pdf('reportes/orden.html', {})
    return HttpResponse(pdf, content_type='application/pdf')
    
def correlativoOrden():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_ORDENTRABAJO"
    correlativo=0

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    
    return correlativo

def buscardatos():

    sql="SELECT A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_ORDENTRABAJO.ID FROM A_ORDENTRABAJO INNER JOIN A_SOCIOS ON A_ORDENTRABAJO.ID_PARCELERO = A_SOCIOS.ID WHERE A_ORDENTRABAJO.TIPO=1;"
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'rut':i[0],'nombres':i[1]+" "+i[2],'id':i[3]})
    except Exception as a:
        print(a)

    sql="SELECT A_FUNCIONARIOS.RUT, A_FUNCIONARIOS.NOMBRES, A_FUNCIONARIOS.APELLIDOS, A_ORDENTRABAJO.ID FROM A_ORDENTRABAJO INNER JOIN A_FUNCIONARIOS ON A_ORDENTRABAJO.ID_PARCELERO = A_FUNCIONARIOS.ID WHERE A_ORDENTRABAJO.TIPO=2;"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'rut':i[0],'nombres':i[1]+" "+i[2],'id':i[3]})
    except Exception as a:
        print(a)
    
    sql="SELECT A_PROVEEDORES.RUT, A_PROVEEDORES.GIRO, A_PROVEEDORES.RAZON_SOCIAL, A_ORDENTRABAJO.ID FROM A_ORDENTRABAJO INNER JOIN A_PROVEEDORES ON A_ORDENTRABAJO.ID_PARCELERO = A_PROVEEDORES.ID WHERE A_ORDENTRABAJO.TIPO=3;"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'rut':i[0],'nombres':i[1]+" "+i[2],'id':i[3]})
    except Exception as a:
        print(a)

    return lista

def historialOrden(request):

    if request.method=='POST' and 'ver' in request.POST:

        nro=request.POST['nro'].replace(' ','')
        nombres=""
        apellido=""
        des=""
        numero=""
        operacion=""
        observacion=""
        otros=""
        emision=""
        fecha_desde=""
        fecha_hasta=""
        hora_inicio=""
        hora_termino=""
        responsable=""
        tipo=""

        sql="SELECT TIPO FROM OPER_ORDENTRABAJO WHERE CORRELATIVO="+nro

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                tipo=i[0]
        except Exception as a:
            print(a)
        
        print(str(tipo))

        if tipo==1:
                
            sql="SELECT A_ORDENTRABAJO.*, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, * FROM A_ORDENTRABAJO INNER JOIN A_SOCIOS ON (A_ORDENTRABAJO.TIPO = A_SOCIOS.TIPO) AND (A_ORDENTRABAJO.ID_PARCELERO = A_SOCIOS.ID) WHERE (((A_ORDENTRABAJO.ID)="+str(nro)+") AND ((A_ORDENTRABAJO.TIPO)="+str(tipo)+"));"
            
        elif tipo==2:
                
            sql="SELECT A_ORDENTRABAJO.*, A_FUNCIONARIOS.RUT, A_FUNCIONARIOS.NOMBRES, * FROM A_ORDENTRABAJO INNER JOIN A_FUNCIONARIOS ON (A_ORDENTRABAJO.ID_PARCELERO = A_FUNCIONARIOS.ID) AND (A_ORDENTRABAJO.TIPO = A_FUNCIONARIOS.TIPO) WHERE (((A_ORDENTRABAJO.TIPO)="+str(tipo)+") AND ((A_ORDENTRABAJO.ID)="+str(nro)+"));"

        elif tipo==3:
            sql="SELECT A_ORDENTRABAJO.*, A_PROVEEDORES.RUT, A_PROVEEDORES.GIRO, A_PROVEEDORES.RAZON_SOCIAL, * FROM A_ORDENTRABAJO INNER JOIN A_PROVEEDORES ON (A_ORDENTRABAJO.TIPO = A_PROVEEDORES.TIPO) AND (A_ORDENTRABAJO.ID_PARCELERO = A_PROVEEDORES.ID) WHERE (((A_ORDENTRABAJO.ID)="+str(nro)+") AND ((A_ORDENTRABAJO.TIPO)="+str(tipo)+"));"

        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                des=i[6]
                numero=i[0]
                operacion=i[7]
                observacion=i[8]
                responsable=i[4]
                otros=i[5]
                emision=i[3]
                fecha_desde=i[9]
                fecha_hasta=i[10]
                hora_inicio=i[11]
                hora_termino=i[12]
                nombres=i[14]
                apellido=i[15]


            data={
                'nombres':nombres,
                'apellido':apellido,
                'des':des,
                'numero':numero,
                'operacion':operacion,
                'observacion':observacion,
                'otros':otros,
                'emision':emision,
                'fecha_desde':fecha_desde,
                'fecha_hasta':fecha_hasta,
                'hora_inicio':hora_inicio,
                'hora_termino':hora_termino,
                'responsable':responsable,
            }

            try:
                pdf = render_to_pdf('reportes/orden.html', data)
                return HttpResponse(pdf, content_type='application/pdf')
            except Exception as a:
                print(a)
        except Exception as a:
            print(a)

    if request.method=='POST' and 'eliminar' in request.POST:

        nro=request.POST['nro']

        sql="DELETE FROM OPER_ORDENTRABAJO WHERE CORRELATIVO="+nro

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
             

    data={
        'lista':buscardatos()
    }

    return render(request, 'antecedentes/orden_trabajo_historial.html', data)

def viewOrden_trabajo(request):
    now = datetime.datetime.now()
    mensaje=""

    if now.month==1:
        mes='Enero'
    if now.month==2:
        mes='Febrero'
    if now.month==3:
        mes='Marzo'
    if now.month==4:
        mes='Abril'
    if now.month==5:
        mes='Mayo'
    if now.month==6:
        mes='Junio'
    if now.month==7:
        mes='Julio'
    if now.month==8:
        mes='Agosto'
    if now.month==9:
        mes='Septiembre'
    if now.month==10:
        mes='Octubre'
    if now.month==11:
        mes='Noviembre'
    if now.month==12:
        mes='Diciembre'


    if request.method=='POST' and 'guardar' in request.POST:

        des=request.POST['desc']
        id_=request.POST['id_1']
        tipo=request.POST['tipo']
        numero=request.POST['nro']
        operacion=request.POST['operacion']
        observacion=request.POST['observacion']
        otros=request.POST['otros']
        emision=request.POST['fecha_actual']
        fecha_desde=request.POST['fecha_desde']
        fecha_hasta=request.POST['fecha_hasta']
        hora_inicio=request.POST['hora_inicio']
        hora_termino=request.POST['hora_termino']
        responsable=request.POST['responsable']
        nombres=""
        
        sql="INSERT INTO A_ORDENTRABAJO(ID,ID_PARCELERO,TIPO,FECHA_EMISION,RESPONSABLE,OTROS,DESCRIPCION,OPERACION,OBSERVACION,FECHA_DESDE,FECHA_HASTA,HORA_INICIO,HORA_TERMINO) VALUES("+str(numero)+","+id_+","+tipo+",'"+emision+"','"+responsable+"','"+otros+"','"+des+"','"+operacion+"','"+observacion+"','"+fecha_desde+"','"+fecha_hasta+"','"+hora_inicio+"','"+hora_termino+"')"
        
        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Se guardo correctamente"
            

            if tipo=='1':
                
                sql="SELECT A_ORDENTRABAJO.*, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, * FROM A_ORDENTRABAJO INNER JOIN A_SOCIOS ON (A_ORDENTRABAJO.TIPO = A_SOCIOS.TIPO) AND (A_ORDENTRABAJO.ID_PARCELERO = A_SOCIOS.ID) WHERE (((A_ORDENTRABAJO.ID)="+numero+") AND ((A_ORDENTRABAJO.ID_PARCELERO)="+id_+") AND ((A_ORDENTRABAJO.TIPO)="+tipo+"));"
            
            elif tipo=='2':
                
                sql="SELECT A_ORDENTRABAJO.*, A_FUNCIONARIOS.RUT, A_FUNCIONARIOS.NOMBRES, * FROM A_ORDENTRABAJO INNER JOIN A_FUNCIONARIOS ON (A_ORDENTRABAJO.ID_PARCELERO = A_FUNCIONARIOS.ID) AND (A_ORDENTRABAJO.TIPO = A_FUNCIONARIOS.TIPO) WHERE (((A_ORDENTRABAJO.ID_PARCELERO)="+id_+") AND ((A_ORDENTRABAJO.TIPO)="+tipo+") AND ((A_ORDENTRABAJO.ID)="+numero+"));"

            else:
                sql="SELECT A_ORDENTRABAJO.*, A_PROVEEDORES.RUT, A_PROVEEDORES.GIRO, A_PROVEEDORES.RAZON_SOCIAL, * FROM A_ORDENTRABAJO INNER JOIN A_PROVEEDORES ON (A_ORDENTRABAJO.TIPO = A_PROVEEDORES.TIPO) AND (A_ORDENTRABAJO.ID_PARCELERO = A_PROVEEDORES.ID) WHERE (((A_ORDENTRABAJO.ID)="+numero+") AND ((A_ORDENTRABAJO.ID_PARCELERO)="+id_+") AND ((A_ORDENTRABAJO.TIPO)="+tipo+"));"

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    des=i[6]
                    numero=i[0]
                    operacion=i[7]
                    observacion=i[8]
                    responsable=i[4]
                    otros=i[5]
                    emision=i[3]
                    fecha_desde=i[9]
                    fecha_hasta=i[10]
                    hora_inicio=i[11]
                    hora_termino=i[12]
                    nombres=i[14]
                    apellido=i[15]


                data={
                    'nombres':nombres,
                    'apellido':apellido,
                    'des':des,
                    'numero':numero,
                    'operacion':operacion,
                    'observacion':observacion,
                    'otros':otros,
                    'emision':emision,
                    'fecha_desde':fecha_desde,
                    'fecha_hasta':fecha_hasta,
                    'hora_inicio':hora_inicio,
                    'hora_termino':hora_termino,
                    'responsable':responsable,
                }

                pdf= render_to_pdf('reportes/orden.html', data)
                return HttpResponse(pdf, content_type='application/pdf')
            
            except Exception as a:
                print(a)

        except Exception as a:
            print(a)

    data={
        'all_proveedor':buscarporProveedor(),
        'all_funcionario':buscarporFuncionario(),
        'all_socios':buscarporNombre(),
        'nroorden':numero_orden(),
        'fecha_actual': now.date().strftime('%d-%m-%Y'),
        'mensaje':mensaje
    }
    return render(request, 'antecedentes/orden_trabajo.html', data)

def viewInstalacion(request):
    now = datetime.datetime.now()
    
    if request.method=='POST' and 'guardar' in request.POST:
        medidor=request.POST['medidor']
        diametro=request.POST['diametro']
        marca=request.POST['marca']
        sector=request.POST['sector']
        calle=request.POST['calle']
        area=request.POST['area']
        sitio=request.POST['sitio']
        ruta=request.POST['ruta']
        hoy=request.POST['hoy']
        referencia=request.POST['referencia']
        nro_serie=request.POST['nro_serie']
        mts_distancia=request.POST['mts_distancia']
        diametro_red=request.POST['diametro_red']
        digitos_medidor=request.POST['digitos_medidor']
        email=request.POST['email']
        rut_usuario=request.POST['rut_usuario']
        nombre_usuario=request.POST['nombre_usuario']
        rut_socio=request.POST['rut_socio']
        nombre_socio=request.POST['nombre_socio']
        cod_beneficiario=request.POST['cod_beneficiario']
        solidario=request.POST['solidario']
        descuento=request.POST['descuento']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }

    return render(request, 'antecedentes/instalacion_medidor.html', data)

def viewEstanque(request):

    now = datetime.datetime.now()
    
    if request.method=='POST' and 'guardar' in request.POST:
        serie=request.POST['serie']
        marca=request.POST['marca']
        diametro=request.POST['diametro']
        nombre=request.POST['nombre']
        informe=request.POST['informe']

    data={
        'fecha': str(now.month)+"/"+str(now.year)
    }
    return render(request, 'antecedentes/consumo_estanque.html', data)
