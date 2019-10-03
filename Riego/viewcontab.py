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
import pandas as pd
import math
import os
import subprocess
from Riego.utils import render_to_pdf

from Riego.viewconexion import nombreConexion

#Instalar CONTROLADOR ODBC especifico según 64bits o 32bits del computador , en este caso es controlador en 64bits

try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\RiegoWeb\\Riego\\RIEGO.mdb')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass

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

def viewName():

    nombre=""
    sql="SELECT NOMBRE FROM DATOS_COMITE"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            nombre=i[0]
            
    except Exception as e:
        print(e)

def viewID3(request):

    nombre=request.GET.get('socio')
    id_=""
    cantidad=0

    if nombre != None:
        for x in nombre:
            if x==" ":
                cantidad=cantidad+1
            elif cantidad>1:
                break
            if cantidad==1:
                id_=x
    
    return render(request, 'id_3.html', {'nombre': id_})

def buscarporNombre():

    lista=[]

    try:
        cursor.execute('select A_SOCIOS.TIPO , A_SOCIOS.* from A_SOCIOS')
        
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

def viewpdf(request):

    nivel1=[]
    nivel2=[]
    listai=[]
    now=datetime.datetime.now()
    
    sql="SELECT codigo, detalle from nivel1"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            nivel1.append({'codigo':i[0],'nivel1':i[1]})
    except Exception as a:
        print(a)
    
    sql="SELECT nivel3.detalle, nivel2.detalle, nivel2.codigo, nivel2.sub_codigo FROM nivel3 INNER JOIN (nivel1 INNER JOIN nivel2 ON nivel1.codigo = nivel2.sub_codigo) ON nivel3.sub_codigo2 = nivel2.codigo order by 2"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            nivel2.append({'d1':i[0],'d2':i[1],'codigo':i[2]})
    except Exception as a:
        print(a)
    
    print(nivel2)

    data={
        'datos':viewAsociacion(),
        'fecha':now.date().strftime('%d-%m-%Y'),
        'nivel1':nivel1,
        'nivel2':nivel2
    }

    pdf = render_to_pdf('reportes/plan.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def detalle1(tipo):

    sql="SELECT codigo,detalle FROM nivel2 WHERE sub_codigo='"+tipo+"'"
    lista=[]

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'id':i[0],'nombre':i[1]})
        
        return lista
    
    except Exception as a:
        print(a)

def detalle2(tipo):

    sql="SELECT nivel2.detalle, nivel3.detalle FROM nivel3 INNER JOIN nivel2 ON (nivel3.sub_codigo2 = nivel2.codigo) AND (nivel3.sub_codigo = nivel2.sub_codigo) WHERE (((nivel2.sub_codigo)='"+tipo+"'));"
    lista2=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista2.append({'id':i[0],'nombre':i[1]})

        return lista2

    except Exception as a:
        print(a)

def viewPlanCuentaE(request):
    
    lista=detalle1('02')
    lista2=detalle2('02')
            
    if request.method=='POST' and 'guardar' in request.POST:

        sub2=request.POST['tipo']
        desc=request.POST['desc']

        sql="INSERT INTO nivel3(sub_codigo,sub_codigo2,detalle) VALUES ('02','"+sub2+"','"+desc+"')"

        try:
            cursor.execute(sql)
            cursor.commit()
            print("Guardado correctamente")

            lista=detalle1('02')
            lista2=detalle2('02')

            data={
                'asociacion':viewName(),
                'all_socios':buscarporNombre,
                'lista':lista,
                'lista2':lista2
            }

            return render(request,'contabilidad/plan_cuenta_egreso.html',data)

        except Exception as a:
            print(a)

    data={
        'asociacion':viewName(),
        'all_socios':buscarporNombre,
        'lista':lista,
        'lista2':lista2
    }

    return render(request,'contabilidad/plan_cuenta_egreso.html',data)

def plan(request):
    pdf= render_to_pdf('reportes/plan.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def viewPlanCuentaI(request):

    lista=detalle1('01')
    lista2=detalle2('01')
            
    if request.method=='POST' and 'guardar' in request.POST:

        sub2=request.POST['tipo']
        desc=request.POST['desc']

        sql="INSERT INTO nivel3(sub_codigo,sub_codigo2,detalle) VALUES ('01','"+sub2+"','"+desc+"')"

        try:
            cursor.execute(sql)
            cursor.commit()
            print("Guardado correctamente")

            lista=detalle1('01')
            lista2=detalle2('01')

            data={
                'asociacion':viewName(),
                'all_socios':buscarporNombre,
                'lista':lista,
                'lista2':lista2
            }

            return render(request,'contabilidad/plan_cuenta_ingreso.html',data)

        except Exception as a:
            print(a)

    data={
        'asociacion':viewName(),
        'all_socios':buscarporNombre,
        'lista':lista,
        'lista2':lista2
    }

    return render(request,'contabilidad/plan_cuenta_ingreso.html',data)

def listarConceptoI():

    sql="SELECT sub_codigo,detalle, nivel2.codigo FROM nivel2 WHERE sub_codigo='01'"
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'id':i[2],'nombre':i[1]})
    except Exception as a:
        print(a)
    return lista

def listarDetalleI(request):

    conpecto=request.GET.get('concepto')

    listarcalle=[]

    sql="SELECT nivel3.* FROM nivel3 WHERE (((nivel3.sub_codigo2)='"+conpecto+"'));"
    
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            listarcalle.append({'correlativo':i[0],'nombre':i[1]})
            
    except Exception as a:
        print(a)

    return render(request, 'contabilidad/concepto_list1.html', {'lista': listarcalle})

def listarConceptoE():

    sql="SELECT sub_codigo,detalle, nivel2.codigo FROM nivel2 WHERE sub_codigo='02'"
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'id':i[2],'nombre':i[1]})
    except Exception as a:
        print(a)
    
    return lista

def listarDetalleE(request):

    conpecto=request.GET.get('concepto')

    listarcalle=[]

    sql="SELECT nivel3.* FROM nivel3 WHERE (((nivel3.sub_codigo2)='"+conpecto+"'));"
    
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            listarcalle.append({'correlativo':i[0],'nombre':i[1]})
            
    except Exception as a:
        print(a)

    return render(request, 'contabilidad/concepto_list.html', {'lista': listarcalle})

def correlativoComprobante():

    sql="SELECT IIf(IsNull(MAX(nrocom)), 0, Max(nrocom)) FROM COMPROBANTE WHERE NIVEL='1'"
    print(sql)
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def correlativoComprobanteI():

    sql="SELECT IIf(IsNull(MAX(nrocom)), 0, Max(nrocom)) FROM COMPROBANTE WHERE NIVEL='2'"
    print(sql)
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def correlativoComprobanteDet():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM DET_COMPROBANTE"
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def historialIngresos(request):

    lista=[]

    if request.method=='POST' and 'buscar' in request.POST:

        tipo=request.POST['tipo']
        id_=request.POST['id_'].replace(' ','')

        if tipo=='1':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS FROM COMPROBANTE INNER JOIN OPER_CLIENTE ON COMPROBANTE.RUT = OPER_CLIENTE.RUT WHERE (((COMPROBANTE.TIPO)=1) AND ((OPER_CLIENTE.RUT)="+id_+") AND COMPROBANTE.NIVEL='2');"
        
        elif tipo=='2':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, FUNCIONARIO.RUT, FUNCIONARIO.NOMBRES, FUNCIONARIO.APELLIDOS FROM COMPROBANTE INNER JOIN FUNCIONARIOS ON COMPROBANTE.RUT = FUNCIONARIOS.RUT WHERE (((COMPROBANTE.TIPO)=2) AND ((FUNCIONARIOS.RUT)="+id_+") AND COMPROBANTE.NIVEL='2');"
        
        elif tipo=='3':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, GLO_PROVEEDOR.RUT, GLO_PROVEEDOR.GIRO, GLO_PROVEEDOR.RAZON FROM COMPROBANTE INNER JOIN GLO_PROVEEDOR ON COMPROBANTE.RUT = GLO_PROVEEDOR.RUT WHERE (((COMPROBANTE.TIPO)=3) AND COMPROBANTE.RUT="+id_+" AND COMPROBANTE.NIVEL='2');"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista.append({'id':i[0],'total':i[1],'rut':i[2],'nombres':i[3]+" "+i[4]})
        except Exception as a:
            print(a)

    if request.method=='POST' and 'ver' in request.POST:

        nro=request.POST['nro_']
        id_=request.POST['nro']
        tipo=""
        lista2=[]
        total=0
        numero=0
        rut=""
        nombres=""
        
        sql="SELECT TIPO,RUT FROM COMPROBANTE WHERE CORRELATIVO="+nro
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                tipo=i[0]
                id_1=i[1]
        except Exception as a:
            print(a)
        
        print("tipo: " + str(tipo))

        if tipo==1:

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS FROM COMPROBANTE INNER JOIN OPER_CLIENTE ON COMPROBANTE.RUT = OPER_CLIENTE.RUT WHERE (((COMPROBANTE.TIPO)=1) AND ((OPER_CLIENTE.RUT)="+str(id_1)+"));"
        
        elif str(tipo)=='2':
            print("squi")
            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, FUNCIONARIOS.RUT, FUNCIONARIOS.NOMBRES, FUNCIONARIOS.APELLIDOS FROM COMPROBANTE INNER JOIN FUNCIONARIOS ON COMPROBANTE.RUT = FUNCIONARIOS.RUT WHERE (((COMPROBANTE.TIPO)=2) AND ((FUNCIONARIOS.RUT)="+str(id_1)+"));"

        elif tipo==3:

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, GLO_PROVEEDOR.RUT, GLO_PROVEEDOR.GIRO, GLO_PROVEEDOR.RAZON FROM COMPROBANTE INNER JOIN GLO_PROVEEDOR ON COMPROBANTE.RUT = GLO_PROVEEDOR.RUT WHERE (((COMPROBANTE.TIPO)=3) AND COMPROBANTE.RUT="+str(id_1)+");"

        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                numero=i[0]
                rut=i[2]
                nombres=i[3]+" "+i[4]
                print(str(nombres))
        except Exception as a:  
            print("Error " + sql)
        
        sql="SELECT DET_COMPROBANTE.ID_COMPROBANTE, DET_COMPROBANTE.CONCEPTO, DET_COMPROBANTE.DETALLE, DET_COMPROBANTE.MONTO, DET_COMPROBANTE.FECHA FROM DET_COMPROBANTE WHERE (((A_DET_COMPROBANTE.ID_COMPROBANTE)="+str(nro)+"));"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                total=total+i[3]
                lista2.append({'detalle':i[2],'monto':i[3]})
        except Exception as a:
            print(a)
        
        data={
            'datos':viewAsociacion(),
            'lista2':lista2,
            'nro':str(numero),
            'total':str(total),
            'numero':id_,
            'rut':rut,
            'nombres':nombres
        }
        
        pdf= render_to_pdf('reportes/ingreso.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    if request.method=='POST' and 'eliminar' in request.POST:

        nro=request.POST['nro']

        sql="DELETE FROM COMPROBANTE WHERE CORRELATIVO="+nro

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)

    data={
        'all_socios':buscarporNombre(),
        'lista':lista,
    }


    return render(request,'contabilidad/historial_ingresos.html',data)

def historialEgresos(request):

    lista=[]

    if request.method=='POST' and 'buscar' in request.POST:

        tipo=request.POST['tipo']
        id_=request.POST['id_'].replace(' ','')

        if tipo=='1':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS FROM COMPROBANTE INNER JOIN OPER_CLIENTE ON COMPROBANTE.RUT = OPER_CLIENTE.RUT WHERE (((COMPROBANTE.TIPO)=1) AND ((OPER_CLIENTE.ID)="+id_+") AND COMPROBANTE.NIVEL='1');"
        
        elif tipo=='2':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, FUNCIONARIOS.RUT, FUNCIONARIOS.NOMBRES, FUNCIONARIOS.APELLIDOS FROM COMPROBANTE INNER JOIN FUNCIONARIOS ON COMPROBANTE.RUT = FUNCIONARIOS.RUT WHERE (((COMPROBANTE.TIPO)=2) AND ((FUNCIONARIOS.RUT)="+id_+") AND COMPROBANTE.NIVEL='1');"
        
        elif tipo=='3':

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, GLO_PROVEEDOR.RUT, GLO_PROVEEDOR.GIRO, GLO_PROVEEDOR.RAZON FROM COMPROBANTE INNER JOIN GLO_PROVEEDOR ON COMPROBANTE.RUT = GLO_PROVEEDOR.RUT WHERE (((COMPROBANTE.TIPO)=3) AND COMPROBANTE.RUT="+id_+" AND COMPROBANTE.NIVEL='1');"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista.append({'id':i[0],'total':i[1],'rut':i[2],'nombres':i[3]+" "+i[4]})
        except Exception as a:
            print(a)

    if request.method=='POST' and 'ver' in request.POST:

        nro=request.POST['nro_']
        id_=request.POST['nro']
        tipo=""
        lista2=[]
        total=0
        numero=0
        rut=""
        nombres=""
        
        sql="SELECT TIPO,RUT FROM COMPROBANTE WHERE CORRELATIVO="+nro
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                tipo=i[0]
                id_1=i[1]
        except Exception as a:
            print(a)
        
        sql=""

        if tipo==1:

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS FROM COMPROBANTE INNER JOIN OPER_CLIENTE ON COMPROBANTE.RUT = OPER_CLIENTE.RUT WHERE (((COMPROBANTE.TIPO)=1) AND ((OPER_CLIENTE.RUT)="+str(id_1)+"));"
        
        elif tipo==2:

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, FUNCIONARIO.RUT, FUNCIONARIO.NOMBRES, FUNCIONARIO.APELLIDOS FROM COMPROBANTE INNER JOIN FUNCIONARIO ON COMPROBANTE.RUT = FUNCIONARIO.RUT WHERE (((COMPROBANTE.TIPO)=2) AND ((FUNCIONARIO.RUT)="+str(id_1)+"));"
        
        elif tipo==3:

            sql="SELECT COMPROBANTE.CORRELATIVO, COMPROBANTE.TOTAL, GLO_PROVEEDOR.RUT, GLO_PROVEEDOR.GIRO, GLO_PROVEEDOR.RAZON FROM COMPROBANTE INNER JOIN GLO_PROVEEDOR ON COMPROBANTE.RUT = GLO_PROVEEDOR.RUT WHERE (((COMPROBANTE.TIPO)=3) AND COMPROBANTE.RUT="+str(id_1)+");"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                numero=i[0]
                rut=i[2]
                nombres=i[3]+" "+i[4]
        except Exception as a:  
            print("Error " + sql)
        
        sql="SELECT A_DET_COMPROBANTE.ID_COMPROBANTE, A_DET_COMPROBANTE.CONCEPTO, A_DET_COMPROBANTE.DETALLE, A_DET_COMPROBANTE.MONTO, A_DET_COMPROBANTE.FECHA FROM A_DET_COMPROBANTE WHERE (((A_DET_COMPROBANTE.ID_COMPROBANTE)="+str(nro)+"));"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                total=total+i[3]
                lista2.append({'detalle':i[2],'monto':i[3]})
        except Exception as a:
            print(a)

        data={
            'datos':viewAsociacion(),
            'lista2':lista2,
            'nro':str(numero),
            'total':str(total),
            'numero':nro,
            'rut':rut,
            'nombres':nombres
        }
        
        pdf= render_to_pdf('reportes/egreso.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    if request.method=='POST' and 'eliminar' in request.POST:

        nro=request.POST['nro']

        sql="DELETE FROM COMPROBANTE WHERE CORRELATIVO="+nro

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)

    data={
        'all_socios':buscarporNombre(),
        'lista':lista,
    }


    return render(request,'contabilidad/historial_egreso.html',data)

def correlativoC():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM COMPROBANTE"
    print(sql)
    correlativo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def viewEgresos(request):
    now=datetime.datetime.now()
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

        id_=request.POST['id_1']
        tipo=request.POST['tipo']
        numero=request.POST['numero']
        total=request.POST['total']
        glosa=request.POST['glosa']
        detalle=request.POST.getlist('detalle1')
        valor=request.POST.getlist('valor')
        codigo=request.POST.getlist('ide')
        fecha=request.POST['fecha_actual']

        listadetalle=[]
        listavalor=[]
        listacodigo=[]
        inicial=0

        for i in codigo:
            listacodigo.append(i)
            print(listacodigo)

        for i in detalle:
            listadetalle.append(i)
        
        for i in valor:
            listavalor.append(i)
        
        existe=0

        sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM COMPROBANTE"
        correlativo=0

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                correlativo=i[0]+1
        except Exception as a:
            print(a)

        sql="SELECT * FROM COMPROBANTE WHERE NROCOM="+numero+" WHERE NIVEL='1'"
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                existe=1
        except Exception as a:
            print(a)
        
        if existe==0:
        
            sql="INSERT INTO COMPROBANTE(NROCOM,CORRELATIVO,RUT,NIVEL,TOTAL,FECHA,TIPO,NRODOC,GLOSA) VALUES("+numero+","+str(correlativo)+","+id_+",'1',"+total+",'"+fecha+"',"+tipo+",0,'"+glosa+"')"
            
            try:
                cursor.execute(sql)
                cursor.commit()
            except Exception as a:
                print(a)

            while inicial<len(listadetalle):
                sql="INSERT INTO A_DET_COMPROBANTE(ID,ID_COMPROBANTE,CONCEPTO,DETALLE,MONTO,FECHA) VALUES("+str(correlativoComprobanteDet())+","+str(correlativo)+","+listacodigo[inicial]+",'"+listadetalle[inicial]+"',"+listavalor[inicial]+",'"+fecha+"')"
                print(sql)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                    mensaje="Quedo guardado correctamente"
                except Exception as a:
                    print(a)  
                    mensaje="No se pudo guardar correctamente"

                inicial=inicial+1
        else:
            mensaje="No se pudo guardar, existe numero de comprobante"

    data={
        'numero':correlativoComprobante(),
        'listar_egresos':listarConceptoE(),
        'asociacion':viewName(),
        'all_socios':buscarporNombre, 
        'fecha_actual': now.date().strftime('%d-%m-%Y'),
        'mensaje':mensaje
    }

    return render(request,'contabilidad/egreso.html',data)

def egreso(request):
    pdf= render_to_pdf('reportes/egreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def viewIngresos(request):
    now=datetime.datetime.now()
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

        id_=request.POST['id_1']
        tipo=request.POST['tipo']
        numero=request.POST['numero']
        total=request.POST['total']
        glosa=request.POST['glosa']
        detalle=request.POST.getlist('detalle1')
        valor=request.POST.getlist('valor')
        codigo=request.POST.getlist('ide')
        fecha=request.POST['fecha_actual']

        listadetalle=[]
        listavalor=[]
        listacodigo=[]
        inicial=0

        for i in codigo:
            listacodigo.append(i)

        for i in detalle:
            listadetalle.append(i)
        
        for i in valor:
            listavalor.append(i)
        
        existe=0

        sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM COMPROBANTE"
        correlativo=0

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                correlativo=i[0]+1
        except Exception as a:
            print(a)

        sql="SELECT * FROM COMPROBANTE WHERE NROCOM="+numero+" WHERE NIVEL='1'"
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                existe=1
        except Exception as a:
            print(a)
        
        if existe==0:
        
            sql="INSERT INTO COMPROBANTE(NROCOM,CORRELATIVO,RUT,NIVEL,TOTAL,FECHA,TIPO,NRODOC,GLOSA) VALUES("+numero+","+str(correlativo)+","+id_+",'2',"+total+",'"+fecha+"',"+tipo+",0,'"+glosa+"')"
            
            try:
                cursor.execute(sql)
                cursor.commit()
            except Exception as a:
                print(a)

            while inicial<len(listadetalle):
                sql="INSERT INTO A_DET_COMPROBANTE(ID,ID_COMPROBANTE,CONCEPTO,DETALLE,MONTO,FECHA) VALUES("+str(correlativoComprobanteDet())+","+str(correlativo)+","+listacodigo[inicial]+",'"+listadetalle[inicial]+"',"+listavalor[inicial]+",'"+fecha+"')"
                print(sql)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                    mensaje="Quedo guardado correctamente"
                except Exception as a:
                    print(a)  
                    mensaje="No se pudo guardar correctamente"

                inicial=inicial+1
        else:
            mensaje="No se pudo guardar, existe numero de comprobante"

    data={
        'numero':correlativoComprobanteI(),
        'fecha_actual': now.date().strftime('%d-%m-%Y'),
        'listar_ingresos': listarConceptoI(),
        'all_socios':buscarporNombre,
        'mensaje':mensaje,
        'asociacion':viewName(),
    }

    return render(request, 'contabilidad/ingreso.html', data)

def ingreso(request):
    pdf = render_to_pdf('reportes/ingreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')
    
def correlativoSaldo():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM INGRESO_CUENTA"
    correlativo=1
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    return correlativo

def viewSaldoFavorH(request):

    lista=[]


    if request.method=='POST' and 'buscar' in request.POST:

        id_=request.POST['id_'].replace(' ','')

        sql="SELECT INGRESO_CUENTA.CORRELATIVO, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS, INGRESO_CUENTA.MONTO, INGRESO_CUENTA.SALDO FROM INGRESO_CUENTA INNER JOIN OPER_CLIENTE ON INGRESO_CUENTA.RUT = OPER_CLIENTE.RUT WHERE (((OPER_CLIENTE.RUT)="+str(id_)+"));"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                if i[5]!=0 :
                    lista.append({'id':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'monto':i[4],'saldo':i[5]})
        except Exception as a:
            print(a)

    if request.method=='POST' and 'ver' in request.POST:

        #id_=request.POST['id_'].replace(' ','')
        nro=request.POST['nro']
        lista=[]

        sql="SELECT INGRESO_CUENTA.CORRELATIVO, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS, INGRESO_CUENTA.FECHA, INGRESO_CUENTA.MONTO, INGRESO_CUENTA.SALDO, INGRESO_CUENTA.FECHA, A_SALDOS.MOTIVO, OPER_CLIENTE.SITIO FROM INGRESO_CUENTA INNER JOIN OPER_CLIENTE ON INGRESO_CUENTA.RUT = OPER_CLIENTE.RUT WHERE ((INGRESO_CUENTA.CORRELATIVO)="+nro+");"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                if i[5]!=0 :
                    lista.append({'id':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'fecha':i[4],'monto':i[5],'saldo':i[6],'fecha':i[7],'motivo':i[8],'direccion':i[9]})
        except Exception as a:
            print(a)
        data={
            'datos':viewAsociacion(),
            'listadetalle':lista
        }
        
        pdf = render_to_pdf('contabilidad/saldo.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    
    if request.method=='POST' and 'eliminar' in request.POST:

        id_=request.POST['nro'].replace(' ','')

        sql="DELETE FROM INGRESO_CUENTA WHERE CORRELATIVO="+id_

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
    
    data={
        'all_socios':buscarpor(),
        'lista':lista
    }

    return render(request, 'contabilidad/historialsaldo.html', data)

def viewSaldoFavor(request):
    now=datetime.datetime.now()
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

        identi=request.POST['identi'].replace(' ','')
        fecha=request.POST['fecha_actual']
        monto=request.POST['monto']
        motivo=request.POST['motivo']

        periodo=fecha[3:len(fecha)-5]
        ano=fecha[len(fecha)-4:len(fecha)]

        print(periodo)
        
        if periodo==1:
            mes='Enero'
        if periodo==2:
            mes='Febrero'
        if periodo==3:
            mes='Marzo'
        if periodo==4:
            mes='Abril'
        if periodo==5:
            mes='Mayo'
        if periodo==6:
            mes='Junio'
        if periodo==7:
            mes='Julio'
        if periodo==8:
            mes='Agosto'
        if periodo==9:
            mes='Septiembre'
        if periodo==10:
            mes='Octubre'
        if periodo==11:
            mes='Noviembre'
        if periodo==12:
            mes='Diciembre'
        
        print(periodo)

        sql="INSERT INTO INGRESO_CUENTA(CORRELATIVO,RUT,FECHA,MONTO,MOTIVO,SALDO,MES,PERIODO,ANO) VALUES("+str(correlativoSaldo())+","+identi+",'"+fecha+"',"+monto+",'"+motivo+"',"+monto+",'"+mes+"',"+periodo+","+ano+")" 
        print(sql)

        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Se guardo correctamente"
        except Exception as a:
            print(a)
            mensaje="No se pudo guardar, intente nuevamente"

    data={
        'all_socios':buscarporNombre,
        'numero':correlativoSaldo(),
        'fecha_actual': now.date().strftime('%d-%m-%Y'),
        'mensaje':mensaje
    }

    return render(request, 'contabilidad/saldo_favor.html', data)

def plan_de_cuenta(request):
    pdf= render_to_pdf('reportes/plan.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def viewLibroVenta(request):
    return render(request, 'contabilidad/libro_venta.html', {})

def viewArqueoCaja(request):

    now = datetime.datetime.now()
    
    if request.method=='POST' and 'guardar' in request.POST:
        hoy=request.POST['hoy']
        correlativo=request.POST['correlativo']
        oficina=request.POST['oficina']
        cajero=request.POST['cajero']
        fijo=request.POST['fijo']
        ingreso=request.POST['ingreso']
        total_caja=request.POST['total_caja']
        egresos=request.POST['egresos']
        saldo=request.POST['saldo']
        fijo=request.POST['fijo']
        total_neto=request.POST['total_neto']
        # 500=request.POST['500']
        # 100=request.POST['100']
        # 50=request.POST['50']
        # 10=request.POST['10']
        # 20000=request.POST['20000']
        # 10000=request.POST['10000']
        # 5000=request.POST['5000']
        # 2000=request.POST['2000']
        # 1000=request.POST['1000']
        total_metalico=request.POST['total_metalico']
        total_billetes=request.POST['total_billetes']
        total_dinero=request.POST['total_dinero']
        cons_boletas=request.POST['cons_boletas']
        cons_facturas=request.POST['cons_facturas']
        multas=request.POST['multas']
        cuotas_sociales=request.POST['cuotas_sociales']
        otros_ingresos=request.POST['otros_ingresos']
        total=request.POST['total']
        # =request.POST['']
        dep_cta_cte=request.POST['dep_cta_cte']
        dep_billetes=request.POST['dep_billetes']
        dep_cheques=request.POST['dep_cheques']
        monedas=request.POST['monedas']
        total2=request.POST['total2']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }

    return render(request, 'contabilidad/arqueo_caja.html', data)

def viewCuentaCorriente(request):

    now = datetime.datetime.now()
    
    if request.method=='POST' and 'guardar' in request.POST:
        rut=request.POST['rut']
        nombre=request.POST['nombre']
        monto=request.POST['monto']
        hoy=request.POST['hoy']
        motivo=request.POST['motivo']
        medidor=request.POST['medidor']
        
    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }

    return render(request, 'contabilidad/cuenta_corriente.html', data)

def viewConciliacionBancaria(request):
    return render(request, 'contabilidad/conciliacion_bancaria.html', {})


def BenSubsidio(request):    
    pdf= render_to_pdf('contabilidad/reporte.html', {})
    return HttpResponse(pdf, content_type='application/pdf')