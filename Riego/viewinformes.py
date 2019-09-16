import pyodbc

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404 , render_to_response, get_list_or_404 
from time import gmtime, strftime
from datetime import datetime
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
def viewAsociacion():

    nombre=""
    lista=[]
    sql="SELECT * FROM A_DATOS"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'rut':i[1],'giro':i[2],'nombre':i[3],'direccion':i[4],'telefono':i[5],'comuna':i[7]})
            
    except Exception as e:
        print(e)

    return lista

def viewName():

    nombre=""
    sql="SELECT NOMBRE FROM A_DATOS"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            nombre=i[0]
            
    except Exception as e:
        print(e)

    return nombre

def viewName():

    nombre=""
    sql="SELECT NOMBRE FROM A_DATOS"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            nombre=i[0]
            
    except Exception as e:
        print(e)
    
    return nombre

def viewInformesSinModel(request,id_):

    lista=[]
    lista2=[]
    tipo=id_
    now = datetime.datetime.now()
    correlativo=0
    ano=now.year
    nombre=""

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

    if tipo=='1':

        nombre="Listado de parceleros sin ingreso de consumo"
        sql="SELECT A_SOCIOS.ID, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SECTOR.NOMBRE FROM (A_SOCIOS LEFT JOIN A_CONSUMO_DIARIO ON A_SOCIOS.ID = A_CONSUMO_DIARIO.ID_PARCELERO) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE (((A_CONSUMO_DIARIO.VALOR_CONSUMO) Is Null));"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista2.append({'id':i[0],'rut':i[1],'nombre':str(i[2])+" "+str(i[3]),'direccion':i[4],'sector':i[5]})

        except Exception as a:
            print(a)
            #PARCELEROS ACTIVOS
    
    if tipo=='4':
        nombre="Nomina de parceleros activos"
        sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=0"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
        except Exception as a:
            print(a)

    if tipo=='9':
        nombre="Listado de convenios"
        sql="SELECT A_SOCIOS.ID, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_CONVENIO.ID, A_CONVENIO.TOTAL_CUOTAS, A_SECTOR.ID, A_SECTOR.NOMBRE, A_COBROS.DESCRIPCION FROM ((A_CONVENIO INNER JOIN A_SOCIOS ON A_CONVENIO.ID_PARCELERO = A_SOCIOS.ID) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID) INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID;"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                idconvenio=i[5]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'idconvenio':i[5],'total':i[6],'idsector':i[7],'sector':i[8],'desc':i[9]})
                
        except Exception as a:
            print(a)
        
        sql="SELECT A_DET_CONVENIO.ID, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA, A_DET_CONVENIO.TOTAL_PAGADO, A_DET_CONVENIO.ID_CONVENIO,a_det_convenio.id_boleta FROM A_DET_CONVENIO;"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                if i[3]==0:
                    estado="PENDIENTE"
                else:
                    estado="$"+str(i[3])
                lista.append({'idc':i[4],'nrocuotas':i[1],'valor':i[2],'estado':estado,'aviso':i[5]})
        except Exception as a:
            print(a)
        
    if tipo=='10':
        nombre="Listado de saldo a favor"
        sql="SELECT A_SALDOS.ID, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SALDOS.MONTO, A_SALDOS.SALDO,A_saldoS.MOTIVO FROM A_SALDOS INNER JOIN A_SOCIOS ON A_SALDOS.ID_PARCELERO = A_SOCIOS.ID;"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                if i[5]!=0 :
                    lista2.append({'id':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'monto':i[4],'saldo':i[5],'motivo':i[6]})
        except Exception as a:
            print(a)
        
    if tipo=='11':
        nombre="Nomina de parceleros para asamblea"
        sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=0"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
        except Exception as a:
            print(a)
        
    if tipo=='12':
        nombre="Nomina de parceleros eliminados"
        sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=1"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
                
        except Exception as a:
            print(a)
            
    if tipo=='15':
        nombre="Nomina de parceleros con pagos al dia"
        sql="SELECT Max(A_BOLETA.IDBOLETA), A_SOCIOS.ID FROM A_SOCIOS INNER JOIN (A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA) ON A_SOCIOS.ID = A_BOLETA.ID_PARCELERO GROUP BY A_DET_BOLETA.CODIGO, A_SOCIOS.ID HAVING (((A_DET_BOLETA.CODIGO)=5));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():

                sql="SELECT A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.VALOR-A_DET_BOLETA.PAGADO FROM A_SOCIOS INNER JOIN (A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA) ON A_SOCIOS.ID = A_BOLETA.ID_PARCELERO WHERE (((A_SOCIOS.ID)="+str(i[1])+") AND ((A_BOLETA.IDBOLETA)="+str(i[0])+") AND ((A_DET_BOLETA.CODIGO)=5));"
                try:
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                      lista2.append({'rut':i[0],'nombre':i[1]+" "+i[2],'direccion':i[3],'deuda':round(i[6])})
                except Exception as a:
                    print(a)
        except Exception as a:
            print(a)

    if tipo=='17':
        nombre="Listado de parceleros alfabetico"
        sql="SELECT A_SOCIOS.APELLIDOS, A_SOCIOS.NOMBRES, A_SOCIOS.RUT, A_SOCIOS.DIRECCION, A_SOCIOS.FECHA_INGRESO, A_SOCIOS.ID FROM A_SOCIOS where vigente=0 order by  A_SOCIOS.NOMBRES;"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[5],'rut':i[3],'nombre':i[1]+" "+i[0],'direccion':i[3],'fecha':i[4]})
                
        except Exception as a:
            print(a)
                
    #PARCELEROS ELIMINADOS
    if tipo=='18':
        nombre="Nomina de parceleros inactivos"
        sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=1"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8],'fecha':i[5]})
                
        except Exception as a:
            print(a)


    data={
        'asociacion':viewName(),
        'lista2':lista2,
        'lista':lista,
        'mes': mes,
        'ano': ano,
        'hoy': now.date,
        'asociacion':viewName()
    }

    try:
        pdf = render_to_pdf('reportes/'+tipo+"."+nombre+".html", data)
        return HttpResponse(pdf, content_type='application/pdf')
    except Exception as a:
        print(a)

def viewInformes(request):

    lista=[]
    lista2=[]

    now = datetime.datetime.now()
    correlativo=0
    ano=now.year
    nombre=""
    total=0
    desde=""
    hasta=""
    direccion=""
    numeroabono=""
    numeroboleta=""
    numerosocio=""
    montopagado=""
    fechapago=""
    nombres=""
    deuda=""
    fecha=""

    #LISTADO DE FACTURACION
    totalfacturacion=0
    totalconsumo=0
    totalvalorconsumo=0
    totalconvenio=0
    totalsaldo=0
    totalinasistencia=0
    totalafavor=0
    totalmulta=0

    #LIBRO DE CAJA EGRESOS
    totaloperacion=0
    totaladmi=0
    totalmantenimiento=0
    totalmejoramiento=0
    totaldeposito=0
    totalotros=0
    totalegreso=0
    fechas=[]
    fulltotalegresos=0

    #LIBRO DE CAJA INGRESOS
    fulltotalingresos=0
    totalingresos=0
    totalgiros=0

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

    lista.append({'id':1,'nombre':'Listado de parceleros sin ingreso de consumo'})
    lista.append({'id':2,'nombre':'Listado de facturación mensual'})
    lista.append({'id':3,'nombre':'Listado de recaudación por rango de fecha'})
    lista.append({'id':4,'nombre':'Nomina de parceleros activos'})
    lista.append({'id':5,'nombre':'Listado de consumo/hora por mes'})
    lista.append({'id':6,'nombre':'Libro de caja egresos'})
    lista.append({'id':7,'nombre':'Listado de facturas emitidas'})
    lista.append({'id':8,'nombre':'Listado de facturas pendientes'})
    lista.append({'id':9,'nombre':'Listado de convenios'})
    lista.append({'id':10,'nombre':'Listado de saldo a favor'})
    lista.append({'id':11,'nombre':'Nomina de parceleros para asambleas'})
    lista.append({'id':12,'nombre':'Listado de parceleros eliminados'})
    lista.append({'id':13,'nombre':'Listado de compobantes de ingresos'})
    lista.append({'id':14,'nombre':'Listado de comprobantes de egresos'})
    lista.append({'id':15,'nombre':'Nomina de parceleros con pagos pendientes'})
    lista.append({'id':16,'nombre':'Listado de parceleros por año de ingreso'})
    lista.append({'id':17,'nombre':'Listado de parceleros alfabetico'})
    lista.append({'id':18,'nombre':'Nomina de parceleros inactivos'})
    lista.append({'id':19,'nombre':'Imprimir Comprobante de Abono por numero de abono'})
    lista.append({'id':20,'nombre':'Libro de caja ingresos'})
    lista.append({'id':21,'nombre':'Listado de facturas anuladas'})

    if request.method=='POST' and 'imprimir' in request.POST:

        tipo=request.POST['nro']
        print("Se eligio numero: "+ tipo)

        if tipo=='1':

            nombre="Listado de parceleros sin ingreso de consumo"
            sql="SELECT A_SOCIOS.ID, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SECTOR.NOMBRE FROM (A_SOCIOS LEFT JOIN A_CONSUMO_DIARIO ON A_SOCIOS.ID = A_CONSUMO_DIARIO.ID_PARCELERO) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE (((A_CONSUMO_DIARIO.VALOR_CONSUMO) Is Null)) ORDER BY 5;"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    lista2.append({'id':i[0],'rut':i[1],'nombre':str(i[2])+" "+str(i[3]),'direccion':i[4],'sector':i[5]})

            except Exception as a:
                print(a)
                #PARCELEROS ACTIVOS

        if tipo=='2':

            nombre="Listado de facturación"
            mes=request.POST['mes']
            ano=request.POST['ano']
            sql="SELECT A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_BOLETA.VALOR_CONSUMO, A_BOLETA.TOTAL_A_PAGAR, A_BOLETA.IDBOLETA FROM A_BOLETA INNER JOIN A_SOCIOS ON A_BOLETA.ID_PARCELERO = A_SOCIOS.ID WHERE a_boleta.mes='"+mes+"' AND A_BOLETA.ANO="+ano+";"
            saldo=0
            favor=0
            multa=0
            valorconsumo=0
            convenio=0
            fecha="Fecha de facturacion mes "+mes+" del ano "+ano

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    rut=i[0]
                    nombres=str(i[1])+" "+str(i[2])
                    consumo=i[3]
                    totalconsumo=totalconsumo+float(consumo)
                    total=i[4]
                    boleta=i[5]
                    totalfacturacion=totalfacturacion+total

                    sql="SELECT  A_DET_BOLETA.CODIGO,A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR FROM A_DET_BOLETA WHERE (((A_DET_BOLETA.IDBOLETA)="+str(boleta)+"));"

                    try:
                        cursor.execute(sql)
                        for i in cursor.fetchall():

                            if i[1]=='MULTA POR INASISTENCIA':
                                inasistencia=int(i[2])
                                totalinasistencia=totalinasistencia+inasistencia
                            elif i[1]=='SALDO ANTERIOR':
                                saldo=int(i[2])
                                totalsaldo=totalsaldo+saldo
                            elif i[1]=='SALDO A FAVOR':
                                favor=int(i[2])
                                totalafavor=totalafavor+favor
                            elif i[1]=='INTERESES':
                                multa=int(i[2])
                                totalmulta=totalmulta+multa
                            elif i[1]=='CONSUMO DE AGUA POR HORA':
                                valorconsumo=i[2]
                                totalvalorconsumo=int(totalvalorconsumo+float(valorconsumo))
                            else:
                                convenio=int(i[2])
                                totalconvenio=totalconvenio+convenio
                    except Exception as a:
                        print(a)
                    
                    lista2.append({'rut':rut,'nombres':nombres,'consumo':consumo,'total':total,'boleta':boleta,'inasistencia':inasistencia,'saldo':saldo,'favor':favor,'multa':multa,'convenio':convenio,'valorconsumo':valorconsumo})
                    favor=0
                    inasistencia=0
                    saldo=0
                    multa=0
                    valorconsumo=0
                    convenio=0
            except Exception as a:
                print(a)


        if tipo=='3':

            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            nombre="Listado de recaudación por rango de fecha"
            sql="SELECT A_ABONO.ID, A_ABONO.IDBOLETA, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_ABONO.MONTO FROM A_ABONO INNER JOIN A_SOCIOS ON A_ABONO.ID_PARCELERO = A_SOCIOS.ID WHERE A_ABONO.FECHA BETWEEN '"+desde+"' AND '"+hasta+"';"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    total=total+i[5]
                    lista2.append({'abono':i[0],'boleta':i[1],'rut':i[2],'nombres':i[3]+" "+i[4],'total':i[5]})
                
            except Exception as a:
                print(a)

        if tipo=='5': 

            nombre="Listado de consumo hora por mes"
            mes=request.POST['mes']
            ano=request.POST['ano']

            sql="SELECT A_CONSUMO_DIARIO.ID_PARCELERO, A_TIPO_AGUA.NOMBRE, A_CONSUMO_DIARIO.CONSUMO, A_CONSUMO_DIARIO.VALOR_CONSUMO, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS FROM A_TIPO_AGUA INNER JOIN (A_SOCIOS INNER JOIN A_CONSUMO_DIARIO ON A_SOCIOS.ID = A_CONSUMO_DIARIO.ID_PARCELERO) ON A_TIPO_AGUA.ID = A_CONSUMO_DIARIO.ID_TIPO_AGUA WHERE (((A_CONSUMO_DIARIO.MES)='"+mes+"') AND ((A_CONSUMO_DIARIO.ANO)="+ano+"));"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    lista2.append({'id':i[0],'tipo':i[1],'consumo':i[2],'valor':i[3],'nombre':i[4]+" "+i[5]})
                    print(lista2)
                
            except Exception as a:
                print(a)
        
        if tipo=='6':

            nombre="Libro de caja egresos"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            sql="SELECT FECHA FROM A_COMPROBANTE WHERE FECHA BETWEEN '"+desde+"' AND '"+hasta+"' ;"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechas.append({'fechas':i[0]})
            except Exception as a:
                print(a)
            print(fechas)
            
            sql="SELECT A_COMPROBANTE.NROCOM, A_COMPROBANTE.FECHA, A_COMPROBANTE.TOTAL FROM A_COMPROBANTE WHERE (((A_COMPROBANTE.NIVEL)='1') AND ((A_COMPROBANTE.FECHA) Between '"+desde+"' And '"+hasta+"'));"
            
            try:
                cursor.execute(sql)

                for row in cursor.fetchall():
                    nrocom=row[0]
                    fechadoc=row[1]
                    totalegreso=row[2]
                    fulltotalegresos=fulltotalegresos+totalegreso
                    
                    sql="SELECT A_DET_COMPROBANTE.CONCEPTO, A_DET_COMPROBANTE.DETALLE, A_DET_COMPROBANTE.ID_COMPROBANTE, nivel2.detalle, A_DET_COMPROBANTE.MONTO, A_COMPROBANTE.TOTAL FROM ((A_DET_COMPROBANTE INNER JOIN nivel3 ON A_DET_COMPROBANTE.CONCEPTO = nivel3.id) INNER JOIN nivel2 ON nivel3.sub_codigo2 = nivel2.codigo) INNER JOIN A_COMPROBANTE ON A_DET_COMPROBANTE.ID_COMPROBANTE = A_COMPROBANTE.CORRELATIVO GROUP BY A_DET_COMPROBANTE.CONCEPTO, A_DET_COMPROBANTE.DETALLE, A_DET_COMPROBANTE.ID_COMPROBANTE, nivel2.detalle, A_DET_COMPROBANTE.MONTO, A_COMPROBANTE.TOTAL, A_COMPROBANTE.NROCOM, A_COMPROBANTE.NIVEL HAVING (((A_COMPROBANTE.NROCOM)="+str(nrocom)+") AND ((A_COMPROBANTE.NIVEL)='1'));"
                    
                    try:
                        cursor.execute(sql)

                        for i in cursor.fetchall():

                            if i[3]=='OPERACIÓN':
                                totaloperacion=totaloperacion+i[4]
                            if i[3]=='ADMINISTRACION':
                                totaladmi=totaladmi+i[4]
                            if i[3]=='MANTENIMIENTO':
                                totalmantenimiento=totalmantenimiento+i[4]
                            if i[3]=='MEJORAMIENTO':
                                totalmejoramiento=totalmejoramiento+i[4]
                            if i[3]=='DEPOSITOS':
                                totaldeposito=totaldeposito+i[4]
                            if i[3]=='OTROS':
                                totalotros=totalotros+i[4]

                    except Exception as a:
                        print(a)
                    

                    lista2.append({'fecha':fechadoc,'doc':nrocom,'operacion':totaloperacion,'administracion':totaladmi,'mantenimiento':totalmantenimiento,'mejoramiento':totalmejoramiento,'deposito':totaldeposito,'otros':totalotros,'total':totalegreso})
                    
                    totaloperacion=0
                    totaladmi=0
                    totalmantenimiento=0
                    totalmejoramiento=0
                    totaldeposito=0
                    totalotros=0
                    totalegreso=0

            except Exception as a:
                print(a)

        if tipo=='7':

            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            nombre="Listado de facturas emitidas"
            sql="SELECT A_FACTURA.FECHA_EMISION, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_FACTURA.MONTO, A_FACTURA.FECHA_CANCELACION, A_FACTURA.ID FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID  WHERE A_factura.FECHA_EMISION BETWEEN '"+desde+"' AND '"+hasta+"';"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]
                    if i[5]=='0':
                        estado="PENDIENTE"
                    else:
                        estado="PAGADA"
                    lista2.append({'emision':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'monto':i[4],'estado':estado,'id':i[6]})
                
            except Exception as a:
                print(a)
       
        if tipo=='8':
            nombre="Listado de facturas pendientes"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            sql="SELECT A_FACTURA.FECHA_EMISION, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_FACTURA.MONTO, A_FACTURA.FECHA_CANCELACION, A_FACTURA.ID FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID  WHERE A_factura.FECHA_EMISION BETWEEN '"+desde+"' AND '"+hasta+"';"
            
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]
                    if i[5]=='0':
                        estado="PENDIENTE"
                        lista2.append({'emision':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'monto':i[4],'estado':estado,'id':i[6]})

                    else:
                        estado="PAGADA"                
            except Exception as a:
                print(a)
        
        if tipo=='21':
            nombre="Listado de facturas anuladas1"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            sql="SELECT A_FACTURA.FECHA_EMISION, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_FACTURA.MONTO, A_FACTURA.FECHA_CANCELACION, A_FACTURA.ID FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID  WHERE A_factura.FECHA_EMISION BETWEEN '"+desde+"' AND '"+hasta+"' AND ANULAR=1;"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]  
                    lista2.append({'emision':i[0],'rut':i[1],'nombres':i[2]+" "+i[3],'monto':i[4],'estado':'ANULADA','id':i[6]})
            except Exception as a:
                print(a)
      
        
        if tipo=='13':
            #nombre="Listado de comprobantes de ingresos"
            nombre="cpy"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            sql="SELECT A_COMPROBANTE.CORRELATIVO, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_COMPROBANTE.TOTAL FROM A_COMPROBANTE INNER JOIN A_SOCIOS ON A_COMPROBANTE.ID_PARCELERO = A_SOCIOS.ID WHERE A_COMPROBANTE.FECHA BETWEEN '"+desde+"' AND '"+hasta+"'  GROUP BY A_COMPROBANTE.CORRELATIVO, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_COMPROBANTE.TOTAL, A_COMPROBANTE.NIVEL HAVING (((A_COMPROBANTE.NIVEL)='2'));"
            print(sql)
            cursor.execute(sql)

            for i in cursor.fetchall():
                total=total+i[4]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'total':i[4]})
            
            print(lista2)

        if tipo=='14':
            #nombre="Listado de comprobantes de egresos"
            nombre="cpy"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            sql="SELECT A_COMPROBANTE.CORRELATIVO, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_COMPROBANTE.TOTAL FROM A_COMPROBANTE INNER JOIN A_SOCIOS ON A_COMPROBANTE.ID_PARCELERO = A_SOCIOS.ID WHERE A_COMPROBANTE.FECHA BETWEEN '"+desde+"' AND '"+hasta+"'  GROUP BY A_COMPROBANTE.CORRELATIVO, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_COMPROBANTE.TOTAL, A_COMPROBANTE.NIVEL HAVING (((A_COMPROBANTE.NIVEL)='1'));"

            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    total=total+i[4]
                    lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'total':i[4]})
                
            except Exception as a:
                print(a)
        
        if tipo=='15':
            nombre="Nomina de parceleros con pagos al dia"
            sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=1"

            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]
                    lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
            except Exception as a:
                print(a)
        
        if tipo=='16':
            nombre="Listado de parceleros por año de ingreso"
            sql="SELECT * FROM A_SOCIOS WHERE VIGENTE=1"

            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]
                    lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
            except Exception as a:
                print(a)
        

        if tipo=='19':
            nombre="abono1"
            abono=request.POST['abono']
            sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SECTOR.NOMBRE, A_ABONO.ID, A_ABONO.IDBOLETA, A_SOCIOS.ID, A_ABONO.MONTO, A_ABONO.FECHA, A_ABONO.ID,A_ABONO.DEUDA FROM (A_SOCIOS INNER JOIN A_ABONO ON A_SOCIOS.ID = A_ABONO.ID_PARCELERO) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE (((A_ABONO.ID)="+abono+"));"
            print("Exportando abono a pdf...." + sql)
            
            lista=[]
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    
                    nombres=i[0]+" "+i[1]
                    direccion="Sector " + i[3]+ " "+i[2]
                    numeroabono=i[4]
                    numeroboleta=i[5]
                    numerosocio=i[6]
                    montopagado=i[7]
                    fechapago=i[8]
                    deuda=i[10]
                    
                    sql="SELECT A_DET_ABONO.DESCRIPCION, A_DET_ABONO.VALOR, A_DET_ABONO.ABONO_ID FROM A_DET_ABONO WHERE (((A_DET_ABONO.ABONO_ID)="+abono+"));"

                    try:
                        cursor.execute(sql)
                        for i in cursor.fetchall():
                            lista.append({'des':str(i[0])+" $"+str(i[1]),'valor':i[1]})
                    except  Exception as a:
                        print(a)
                        print(sql)
                    
                    
            except Exception as a:
                print(a)
                print(sql)

        if tipo=='20':
            nombre="Libro de caja ingresos"
            desde= datetime.datetime.strptime(request.POST['desde'],'%Y-%m-%d').date().strftime('%d-%m-%Y')
            hasta=datetime.datetime.strptime(request.POST['hasta'],'%Y-%m-%d').date().strftime('%d-%m-%Y')

            sql="SELECT FECHA FROM A_COMPROBANTE WHERE FECHA BETWEEN '"+desde+"' AND '"+hasta+"' ;"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechas.append({'fechas':i[0]})
            except Exception as a:
                print(a)
            print(fechas)
            
            sql="SELECT A_COMPROBANTE.NROCOM, A_COMPROBANTE.FECHA, A_COMPROBANTE.TOTAL FROM A_COMPROBANTE WHERE (((A_COMPROBANTE.NIVEL)='2') AND ((A_COMPROBANTE.FECHA) Between '"+desde+"' And '"+hasta+"'));"
            
            try:
                cursor.execute(sql)

                for row in cursor.fetchall():
                    nrocom=row[0]
                    fechadoc=row[1]
                    totalegreso=row[2]
                    fulltotalingresos=fulltotalingresos+totalegreso
                    
                    sql="SELECT A_DET_COMPROBANTE.CONCEPTO, A_DET_COMPROBANTE.DETALLE, A_DET_COMPROBANTE.ID_COMPROBANTE, nivel2.detalle, A_DET_COMPROBANTE.MONTO, A_COMPROBANTE.TOTAL FROM ((A_DET_COMPROBANTE INNER JOIN nivel3 ON A_DET_COMPROBANTE.CONCEPTO = nivel3.id) INNER JOIN nivel2 ON nivel3.sub_codigo2 = nivel2.codigo) INNER JOIN A_COMPROBANTE ON A_DET_COMPROBANTE.ID_COMPROBANTE = A_COMPROBANTE.CORRELATIVO GROUP BY A_DET_COMPROBANTE.CONCEPTO, A_DET_COMPROBANTE.DETALLE, A_DET_COMPROBANTE.ID_COMPROBANTE, nivel2.detalle, A_DET_COMPROBANTE.MONTO, A_COMPROBANTE.TOTAL, A_COMPROBANTE.NROCOM, A_COMPROBANTE.NIVEL HAVING (((A_COMPROBANTE.NROCOM)="+str(nrocom)+") AND ((A_COMPROBANTE.NIVEL)='2'));"
                    
                    try:
                        cursor.execute(sql)

                        for i in cursor.fetchall():

                            if i[3]=='INGRESOS':
                                totalingresos=totalingresos+i[4]
                            if i[3]=='GIROS':
                                totalgiros=totalgiros+i[4]

                    except Exception as a:
                        print(a)
                    

                    lista2.append({'fecha':fechadoc,'doc':nrocom,'ingresos':totalingresos,'giros':totalgiros,'total':totalegreso})
                    
                    totaloperacion=0
                    totaladmi=0
                    totalmantenimiento=0
                    totalmejoramiento=0
                    totaldeposito=0
                    totalotros=0
                    totalegreso=0

            except Exception as a:
                print(a)

        data={
            'asociacion':viewName(),
            'lista':lista,
            'lista2':lista2,
            'mes': mes,
            'ano': ano,
            'hoy': now.date,
            'asociacion':viewName(),
            'total':total,
            'desde':desde,
            'hasta':hasta,
            'datos':viewAsociacion(),
            'nombre':nombres,
            'direccion':direccion,
            'numeroabono':numeroabono,
            'numeroboleta':numeroboleta,
            'numerosocio':numerosocio,
            'montopagado':montopagado,
            'fechapago':fechapago,
            'deuda':deuda,
            'fecha':fecha,
            'totalfacturacion':totalfacturacion,
            'totalconsumo':totalconsumo,'totalinasistencia':totalinasistencia,'totalsaldo':totalsaldo,'totalafavor':totalafavor,'totalmulta':totalmulta,'totalvalorconsumo':totalvalorconsumo,'totalconvenio':totalconvenio,
            'listafechas':fechas,
            'fulltotalegresos':fulltotalegresos,
            'fulltotalingresos':fulltotalingresos
        }
        try:
            pdf = render_to_pdf('reportes/'+tipo+"."+nombre+".html", data)
            return HttpResponse(pdf, content_type='application/pdf')
        except Exception as a:
            print(a)
    data={
        'asociacion':viewName(),
        'lista':lista,
        'lista2':lista2,
        'mes': mes,
        'ano': ano,
        'hoy': now.date,
        'asociacion':viewName()
    }
    return render(request,'informes.html', data)


def ListaConvenios(request):
    pdf= render_to_pdf('reportes/Listado de Convenios.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def ListaSaldo(request):
    pdf= render_to_pdf('reportes/Listado de Saldo a Favor.html', {})
    return HttpResponse(pdf, content_type='application/pdf')