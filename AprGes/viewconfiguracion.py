import pyodbc
import zipfile

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

try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\RiegoWeb\\Riego\\RIEGO.mdb')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass

def viewAsociacion():

    nombre=""
    lista=[]
    sql="SELECT * FROM DATOS_COMITE"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'rut':i[1],'giro':i[2],'nombre':i[3],'direccion':i[4],'telefono':i[5],'comuna':i[7]})
            
    except Exception as e:
        print(e)

    return lista

def buscarpor():

    lista=[]

    try:
        cursor.execute('select A_SOCIOS.TIPO , A_SOCIOS.* from A_SOCIOS')
        
        for row in cursor.fetchall():
            lista.append({'tipo':row[0],'id':row[1],'nombre':row[3]})        

    except Exception as e:
        pass
        print(e)

    return lista

def buscarSector():

    sql="SELECT SECTOR,GLOSA FROM GLO_SECTOR"
    lista=[]

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'id':i[0], 'nombre':i[1]})

    except Exception as a:
        print(a)

    return lista

def buscarUsuario(user):

    sql="SELECT * FROM USUARIO WHERE USUARIO='"+user+"';"
    usuario=""

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            usuario=str(i[0])

    except Exception as a:
        print(a)

    return usuario

def historialCondonacion(request):
    lista=[]

    if request.method=='POST' and 'buscar' in request.POST:

        id_=request.POST['id_'].replace(' ','')
        sql="SELECT OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS, OPER_CONDONACION.FECHA, OPER_CONDONACION.MONTO, OPER_CONDONACION.CORRELATIVO FROM OPER_CONDONACION INNER JOIN OPER_CLIENTE ON OPER_CONDONACION.RUT = OPER_CLIENTE.RUT WHERE (((OPER_CLIENTE.RUT)="+id_+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista.append({'rut':i[0],'nombres':i[1]+" "+i[2],'fecha':i[3],'total':i[4],'id':int(i[5])})
        except Exception as a:
            print(a)
            mensaje="No se encontraron datos"
    
    if request.method=='POST' and 'ver' in request.POST:

        id_=request.POST['nro']
        lista=[]

        sql="SELECT OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS, OPER_CONDONACION.FECHA, OPER_CONDONACION.MONTO, OPER_CONDONACION.CORRELATIVO,OPER_CONDONACION.MOTIVO,OPER_CLIENTE.SITIO FROM OPER_CONDONACION INNER JOIN OPER_CLIENTE ON OPER_CONDONACION.RUT = OPER_CLIENTE.RUT WHERE (((OPER_CONDONACION.CORRELATIVO)="+id_+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista.append({'rut':str(round(int(i[0]))),'nombres':i[1]+" "+i[2],'fecha':i[3],'total':i[4],'id':i[5],'motivo':i[6],'direccion':i[7]})
        except Exception as a:
            print(a)

        data={
            'datos':viewAsociacion(),
            'listadetalle':lista
        }

        pdf = render_to_pdf('configuracion/condonacionrpt.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    data={
        'all_socios':buscarpor(),
        'lista':lista
    }
    return render(request, 'configuracion/historialcondonacion.html', data)

def correlativocondonacion():
    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_CONDONACION"
    print(sql)
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def correlativocondonaciondet():
    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_DET_CONDONACION"
    print(sql)
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def viewCodonacion(request):
    lista=[]
    rut=""
    nombre=""
    id_=""
    mensaje=""

    if request.method=='POST' and 'buscar' in request.POST:

        valores=0
        id_=request.POST['id_'].replace(' ','')

        sql="SELECT OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS FROM OPER_CLIENTE WHERE (((OPER_CLIENTE.RUT)="+id_+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                rut=i[0]
                nombre=i[1]+" "+i[2]
        except Exception as a:
            print(a)

        sql="SELECT A_DET_BOLETA.ID, A_DET_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_BOLETA.PERIODO, A_BOLETA.ANO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+id_+") AND ((A_DET_BOLETA.CODIGO)<>5));"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                if int(i[4])>=int(i[5]):
                    if int(i[4])-int(i[5])!=0:
                        valores=int(i[4])-int(i[5])
                        lista.append({'id':i[0],'codigo':i[2],'des':i[3],'valor':str(valores),'mes':i[6],'ano':i[7]})
        except Exception as a:
            print(a)
    
    if request.method=='POST' and 'guardar' in request.POST:
        now = datetime.datetime.now()
        inicial=0
        id_=request.POST['numero']
        motivo=request.POST['motivo']
        total=request.POST['total']
        fecha=now.date().strftime('%d-%m-%Y')
        rut=request.POST['rut']

        valorpagos=request.POST.getlist('abono')
        nroaviso=request.POST.getlist('idaviso')
        codigo=request.POST.getlist('codigo')
        desc=request.POST.getlist('des')

        listaabono=[]
        listaaviso=[]
        listacodigo=[]
        listadesc=[]

        for i in desc:
            listadesc.append(i)
        for i in codigo:
            listacodigo.append(i)
        for i in valorpagos:
            listaabono.append(i)
        for i in nroaviso:
            listaaviso.append(i)

        sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM OPER_CONDONACION"
        correlativo=0

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                correlativo=round(i[0]+1)
        except Exception as a:
            print(a)
        
        sql="INSERT INTO A_CONDONACION(ID,IDBOLETA,ID_PARCELERO,MONTO,FECHA,RUT,MOTIVO) VALUES("+str(correlativo)+",0,"+id_+","+total+",'"+fecha+"','"+rut+"','"+motivo+"')"
        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)

        while inicial<len(listaabono):

            valorpagado=0
            
            if str(listaabono[inicial])!=" " and str(listaabono[inicial])!="":

                sql="INSERT INTO A_DET_CONDONACION(CORRELATIVO,ID_CONDONACION,IDBOLETA,CODIGO,DESCRIPCION,VALOR) VALUES("+str(correlativocondonaciondet())+","+str(correlativo)+","+str(listaaviso[inicial])+","+str(listacodigo[inicial])+",'"+str(listadesc[inicial])+"',"+str(listaabono[inicial])+")"
                print(sql)
                try:
                    cursor.execute(sql)
                    cursor.commit() 
                except Exception as a:
                    print(a)
                
                sql="SELECT PAGADO FROM A_DET_BOLETA WHERE ID="+listaaviso[inicial]
                print(sql)
                try:
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        valorpagado=i[0]
                except Exception as a:
                    print(a)

                sql="UPDATE A_DET_BOLETA SET PAGADO="+str(int(valorpagado)+int(listaabono[inicial]))+" where ID="+listaaviso[inicial]
                print(sql)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                    rut=""
                    mensaje="Quedo guardado correctamente"
                except Exception as a:
                    print(a)

            inicial=inicial+1


    data={
        'all_socios':buscarpor(),
        'lista':lista,
        'rut':rut,
        'nombre':nombre,
        'numero':id_,
        'mensaje':mensaje
    }
    return render(request, 'configuracion/condonacion.html', data)

def claveActual(user,actual):

    sql="SELECT * FROM USUARIO WHERE CLAVE='"+actual+"' AND USUARIO='"+user+"';"
    estado=1
    
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            estado=0
    except Exception as a:
        print(a)
    
    return estado

def viewContraseña(request):
    mensaje=""

    if request.method=='POST' and 'guardar' in request.POST:

        usuario=request.POST['usuario']
        nueva=request.POST['nueva']
        repetir=request.POST['repetir']
        actual=request.POST['actual']

        goodactual=claveActual(usuario,actual)

        if goodactual==0:

            if nueva==repetir:

                sql="UPDATE USUARIO SET CLAVE='"+nueva+"' WHERE USUARIO="";"

                try:
                    cursor.execute(sql)
                    cursor.commit()
                except Exception as a:
                    print(a)

                mensaje="Se guardo correctamente la contraseña."
            
            else:
                mensaje="Favor vuelva a repetir contraseñas."
        else:
            mensaje="No coincide la contraseña actual."

    data={
        'mensaje':mensaje
    }

    return render(request, 'configuracion/contraseña.html', data)

def viewEliminar_abono(request):
    data={}
    if request.method=='POST' and 'eliminar' in request.POST:
        
        numero=request.POST['numero']

        existe=0

        sql="SELECT * FROM OPER_ABONO WHERE CORRELATIVO="+numero
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                existe=1
        except Exception as a:
            print(a)

        if existe==1:

            sql="SELECT BOLETA_CORRELATIVO, CODIGO FROM OPER_DET_ABONO WHERE CORRELATIVO="+numero

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():

                    sql="UPDATE A_DET_BOLETA SET PAGADO=0 WHERE CODIGO="+str(i[1])+" AND IDBOLETA="+str(i[0])
                    try:
                        cursor.execute(sql)
                        cursor.commit()
                    except Exception as a:
                        print(a)
                
                sql="DELETE FROM OPER_ABONO WHERE CORRELATIVO="+numero

                try:
                    cursor.execute(sql)
                    cursor.commit()
                    mensaje="Se elimino correctamente"
                except Exception as a:
                    print(a)

                sql="DELETE FROM OPER_DET_ABONO WHERE CORRELATIVO="+numero

                try:
                    cursor.execute(sql)
                    cursor.commit()
                except Exception as a:
                    print(a)
                
                mensaje="Se elimino correctamente"

            except Exception as a:
                print(a)

        else:
            mensaje="No se pudo eliminar, abono no existe"
        
        data={
            'mensaje':mensaje
        }

    return render(request, 'configuracion/eliminar_abono.html', data)

def viewMensaje(request):

    mensajeaviso=""

    sql="SELECT DESCRIPCION FROM GLO_MENSAJE"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            mensajeaviso=i[0]
    except Exception as a:
        print(a)

    if request.method=='POST' and 'guardar' in request.POST:

        mensaje=request.POST['mensaje']

        sql="UPDATE GLO_MENSAJE SET DESCRIPCION='"+mensaje+"' WHERE CORRELATIVO=1;"

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)

    data={
        'mensaje':mensajeaviso
    }  

    return render(request, 'configuracion/mensaje.html', data)

def viewRespaldo_info(request):

    mensaje=""

    if request.method=='POST' and 'respaldar' in request.POST:

        fecha=request.POST['fecha']
        
        jungle_zip = zipfile.ZipFile('C:\\RiegoWeb\\Riego\\RIEGO.mdb', 'w')
        jungle_zip.write('C:\\RiegoWeb\\Riego\\RIEGO'+fecha+'.rar', compress_type=zipfile.ZIP_DEFLATED)
        jungle_zip.close()
        mensaje="Se respaldo correctamente"

    data={
        'mensaje':mensaje
    }

    return render(request, 'configuracion/respaldar_info.html', data)

def viewBoletas_vigentes(request):
    
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

    if request.method=='POST' and 'guardarpor' in request.POST:

        numero=request.POST['numero']

        opcion=request.POST.getlist('vigencia1')

        for i in opcion:
            modoopcion=i[0]
            
        existe=0

        sql="SELECT * FROM OPER_BOLETA WHERE IDBOLETA="+numero

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                existe=1
        except Exception as a:
            print(a)

        if existe==0:
            mensaje="Numero de boleta no existe en los registros"
        else:
            if modoopcion=='1':

                sql="UPDATE OPER_BOLETA SET VIGENTE=1 WHERE IDBOLETA="+numero
            
            else:
                sql="UPDATE OPER_BOLETA SET VIGENTE=0 WHERE IDBOLETA="+numero
            
            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Quedo guardado correctamente"
            except Exception as a:
                print(a)
                print(sql)

    if request.method=='POST' and 'guardar' in request.POST:

        mes=request.POST['mes']
        ano=request.POST['ano']
        opcion=request.POST.getlist('vigencia')
        modoopcion=0
        sql=""

        for i in opcion:
            modoopcion=i[0]
            print(str(modoopcion))
            # 0 es por secotr
            # 1 es por parcelero
        
        if modoopcion=='1':

            sql="UPDATE OPER_BOLETA SET VIGENTE=1 WHERE PERIODO='"+mes+"' AND ANO ="+ano
        
        else:
            sql="UPDATE OPER_BOLETA SET VIGENTE=0 WHERE PERIODO='"+mes+"' AND ANO ="+ano
        
        print(sql)
        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Quedo guardado correctamente"
        except Exception as a:
            print(a)
            print(sql)

    data={
        'lista_sector':buscarSector(),
        'mes':mes,
        'ano':str(now.year),
        'mensaje':mensaje
    }

    return render(request, 'configuracion/boletas_vigentes.html', data)

def viewArreglaDatos(request):

    if request.method=='POST' and 'guardar' in request.POST:
        medidor=request.POST['medidor']
        cancelados_consumo=request.POST['cancelados_consumo']
        cancelados_credito=request.POST['cancelados_credito']
        cancelados_total=request.POST['cancelados_total']
        sin.cancelar_consumo=request.POST['sin-cancelar_consumo']
        sin.cancelar_credito=request.POST['sin-cancelar_credito']
        sin.cancelar_total=request.POST['sin-cancelar_total']

    return render(request, 'configuracion/arregla_datos.html', {})
    
def viewAvisosVigentes(request):
    return render(request, 'configuracion/avisos_vigentes.html', {})
    
def viewCrearUsuario(request):
    return render(request, 'configuracion/crear_usuario.html', {})
    
def viewMensajeCobro(request):
    return render(request, 'configuracion/mensaje_cobro.html', {})
