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
from AprGes.utils import render_to_pdf

from AprGes.viewconexion import nombreConexion

#Instalar CONTROLADOR ODBC especifico según 64bits o 32bits del computador , en este caso es controlador en 64bits

try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\Users\\JMC\\Documents\\APR\\AguilaNorte\\29112015\\AguilaNorte.mdb')
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
        sql="SELECT * FROM OPER_CLIENTE WHERE VIGENTE=0"

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
        sql="SELECT INGRESO_CUENTA.CORRELATIVO, OPER_CLIENTE.RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELLIDOS, INGRESO_CUENTA.MONTO, INGRESO_CUENTA.SALDO,INGRESO_CUENTA.MOTIVO FROM INGRESO_CUENTA INNER JOIN OPER_CLIENTE ON INGRESO_CUENTA.RUT = OPER_CLIENTE.RUT;"
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
        sql="SELECT * FROM OPER_CLIENTE WHERE VIGENTE=0"

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
        except Exception as a:
            print(a)
        
    if tipo=='12':
        nombre="Nomina de parceleros eliminados"
        sql="SELECT * FROM OPER_CLIENTE WHERE VIGENTE=1"

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
        sql="SELECT * FROM OPER_CLIENTE WHERE VIGENTE=1"

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

            sql="SELECT FECHA FROM COMPROBANTE WHERE FECHA BETWEEN '"+desde+"' AND '"+hasta+"' ;"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechas.append({'fechas':i[0]})
            except Exception as a:
                print(a)
            print(fechas)
            
            sql="SELECT COMPROBANTE.NROCOM, COMPROBANTE.FECHA, COMPROBANTE.TOTAL FROM COMPROBANTE WHERE (((COMPROBANTE.NIVEL)='1') AND ((COMPROBANTE.FECHA) Between '"+desde+"' And '"+hasta+"'));"
            
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
            sql="SELECT * FROM OPER_CLIENTE WHERE VIGENTE=1"

            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    rut=i[1]
                    lista2.append({'id':i[0],'rut':i[1],'nombre':i[2]+" "+i[3],'direccion':i[4],'correo':i[8]})
                
            except Exception as a:
                print(a)
        
        if tipo=='16':
            nombre="Listado de parceleros por año de ingreso"
            sql="SELECT * FROM OPEr_CLIENTE WHERE VIGENTE=1"

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

            sql="SELECT FECHA FROM COMPROBANTE WHERE FECHA BETWEEN '"+desde+"' AND '"+hasta+"' ;"
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechas.append({'fechas':i[0]})
            except Exception as a:
                print(a)
            print(fechas)
            
            sql="SELECT COMPROBANTE.NROCOM, COMPROBANTE.FECHA, COMPROBANTE.TOTAL FROM COMPROBANTE WHERE (((COMPROBANTE.NIVEL)='2') AND ((COMPROBANTE.FECHA) Between '"+desde+"' And '"+hasta+"'));"
            
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

def viewConsultasMedidor(request):
    
    if request.method=='POST' and 'guardar' in request.POST:
        nombre=request.POST['nombre']
        medidor=request.POST['medidor']
        direccion=request.POST['direccion']
        año=request.POST['año']

    return render(request, 'informes/consultas_medidor.html', {})

def viewConsultasLectura(request):

    if request.method=='POST' and 'guardar' in request.POST:
        nombre=request.POST['nombre']
        direccion=request.POST['direccion']
        medidor=request.POST['medidor']
        año=request.POST['año']

    return render(request, 'informes/consultas_lectura.html', {})

def viewCuentasInd(request):
    
    if request.method=='POST' and 'guardar' in request.POST:
        nombre=request.POST['nombre']
        direccion=request.POST['direccion']
        medidor=request.POST['medidor']
        año=request.POST['año']
        deuda=request.POST['deuda']

    return render(request, 'informes/cuentas_ind.html', {})

def viewTomaLectura(request):
    
    if request.method=='POST' and 'guardar' in request.POST:
        año=request.POST['año']

    return render(request, 'informes/toma_lectura.html', {})

def viewRegistroFinanciero(request):
    
    if request.method=='POST' and 'guardar' in request.POST:
        nro_sector=request.POST['nro_sector']

    return render(request, 'informes/registro_financiero.html', {})

def viewConsultasCorte(request):
        
    now = datetime.datetime.now()

    if request.method=='POST' and 'guardar' in request.POST:
        mes=request.POST['mes']
        año=request.POST['año']
        tipo=request.POST['tipo']
        sector=request.POST['sector']
    
    data={
        'año': now.year
    }

    return render(request, 'informes/consultas_corte.html', data)














def informe1(request):
    pdf= render_to_pdf('reportes/1.Listado de parceleros sin ingreso de consumo.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe2(request):
    pdf= render_to_pdf('reportes/2.Listado de facturación.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe3(request):
    pdf= render_to_pdf('reportes/3.Listado de recaudación por rango de fecha.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe4(request):
    pdf= render_to_pdf('reportes/4.Nomina de parceleros activos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe5(request):
    pdf= render_to_pdf('reportes/5.Listado de consumo hora por mes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe6(request):
    pdf= render_to_pdf('reportes/6.Libro de caja egresos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe7(request):
    pdf= render_to_pdf('reportes/7.Listado de facturas emitidas.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe8(request):
    pdf= render_to_pdf('reportes/8.Listado de facturas pendientes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe9(request):
    pdf= render_to_pdf('reportes/9.Listado de convenios.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe10(request):
    pdf= render_to_pdf('reportes/10.Listado de saldo a favor.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe11(request):
    pdf= render_to_pdf('reportes/11.Nomina de parceleros para asamblea.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe12(request):
    pdf= render_to_pdf('reportes/12.Nomina de parceleros eliminados.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe13(request):
    pdf= render_to_pdf('reportes/13.cpy.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe14(request):
    pdf= render_to_pdf('reportes/14.cpy.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe15(request):
    pdf= render_to_pdf('reportes/15.Nomina de parceleros con pagos al dia.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe16(request):
    pdf= render_to_pdf('reportes/16.Listado de parceleros por año de ingreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe17(request):
    pdf= render_to_pdf('reportes/17.Listado de parceleros alfabetico.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe18(request):
    pdf= render_to_pdf('reportes/18.Nomina de parceleros inactivos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe19(request):
    pdf= render_to_pdf('reportes/19.abono1.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe20(request):
    pdf= render_to_pdf('reportes/20.Libro de caja ingresos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe21(request):
    pdf= render_to_pdf('reportes/21.Listado de facturas anuladas1.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informe43(request):
    pdf= render_to_pdf('reportes/43.listado_de_ingresos_por_item.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeAviso(request):
    pdf= render_to_pdf('reportes/aviso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeConvenio(request):
    pdf= render_to_pdf('reportes/convenio.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeCuenta_ind(request):
    pdf= render_to_pdf('reportes/cuenta_individual.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeEgreso(request):
    pdf= render_to_pdf('reportes/egreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeFactura(request):
    pdf= render_to_pdf('reportes/factura.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeIngreso(request):
    pdf= render_to_pdf('reportes/ingreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeOrden(request):
    pdf= render_to_pdf('reportes/orden.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informePlan(request):
    pdf= render_to_pdf('reportes/plan.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeCondonacionrpt(request):
    pdf= render_to_pdf('configuracion/condonacionrpt.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeSaldo(request):
    pdf= render_to_pdf('contabilidad/saldo.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def informeReporte(request):
    pdf= render_to_pdf('procesos/reporte.html', {})
    return HttpResponse(pdf, content_type='application/pdf')













def view0_EncuestaMoviemientoContableBimestral(request):
    pdf= render_to_pdf('repotros/0_Encuesta del Moviemiento Contable Bimestral.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view1_1LibroCajaIngreso(request):
    pdf= render_to_pdf('repotros/1_LibroCajaIngreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view1_2LibroCajaEgreso(request):
    pdf= render_to_pdf('repotros/1_LibroCajaEgreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view2_NominaUsuariosPagosPendientes(request):
    pdf= render_to_pdf('repotros/2_Nomina de Usuarios con Pagos Pendientes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view3_NominaUsuariosPagosDia(request):
    pdf= render_to_pdf('repotros/3_Nomina de Usuarios con Pagos al Dia.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view4_ListadoMedidoresNoRegistranLectura(request):
    pdf= render_to_pdf('repotros/4_Listado de Medidores que no Registran Lectura.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view5_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view6_ListadoAbonosIngresados(request):
    pdf= render_to_pdf('repotros/6_Listado de Abonos Ingresados.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view7_ListadoComprobantesIngresados(request):
    pdf= render_to_pdf('repotros/7_Listado de Comprobantes Ingresados.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view8_ListadoComprobantesEgresados(request):
    pdf= render_to_pdf('repotros/8_Listado de Comprobantes Egresados.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view9_ListadoFacturasEmitidas(request):
    pdf= render_to_pdf('repotros/9_Listado de Facturas Emitidas.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view10_ListadoFacturasPendientes(request):
    pdf= render_to_pdf('repotros/10_Listado de Facturas Pendientes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view12_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view13_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view14_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view15_ListadoFacturacion(request):
    pdf= render_to_pdf('repotros/15_Listado de Facturacion.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view16_RangoConsumoAño(request):
    pdf= render_to_pdf('repotros/16_Rango de Consumo por Año.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view17_PlanillaControlConsumoPagos(request):
    pdf= render_to_pdf('repotros/17_Planilla Control de Consumo y Pagos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view18_EstadisticaMedidoresUsuarios(request):
    pdf= render_to_pdf('repotros/18_Estadistica de Medidores y Usuarios.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view19_ListadoLecturaMedidoresMes(request):
    pdf= render_to_pdf('repotros/19_Listado de Lectura de Medidores por Mes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view20_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view21_UsuariosAsociadoSocio(request):
    pdf= render_to_pdf('repotros/21_Usuarios Asociados a Cada Socio.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view22_ListadoDiametroMedidores(request):
    pdf= render_to_pdf('repotros/22_Listado de Diametro de Medidores.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view23_ListadoSocioAlfabetico(request):
    pdf= render_to_pdf('repotros/23_Listado de Socio Alfabetico.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view24_ControlArranquesSector(request):
    pdf= render_to_pdf('repotros/24_Control de Arranques por Sector.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view25_ListadoMedidoresCorteVoluntario(request):
    pdf= render_to_pdf('repotros/25_Listado de Medidores con Corte Voluntario.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view26_RegistroCuentasCorrientesClientes(request):
    pdf= render_to_pdf('repotros/26_Registro de Cuentas Corrientes Clientes.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view27_EstadisticaFacturacionMensual(request):
    pdf= render_to_pdf('repotros/27_Estadistica de Facturacion Mensual.html', {})
    return HttpResponse(pdf, content_type='application/pdf')


def view28_MedidoresMarcadosInasistenciaReuniones(request):
    pdf= render_to_pdf('repotros/28_Medidores Marcados con Inasistencia a Reuniones.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view29_ListadoMedidoresInasistenciaReunionesPagados(request):
    pdf= render_to_pdf('repotros/29_Listado de Medidores Marcados con Inasistencia a Reuniones Pagados.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view30_ListadoMedidoresConveniosImpagos(request):
    pdf= render_to_pdf('repotros/30_Listado de  Medidores con Convenios Impagos.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view31_Notificacion(request):
    pdf= render_to_pdf('repotros/31_Notificacion.html', {})
    return HttpResponse(pdf, content_type='application/pdf')    

def view32_OrdenCorte(request):
    pdf= render_to_pdf('repotros/32_Orden de Corte.html', {})
    return HttpResponse(pdf, content_type='application/pdf')    

def view33_SolicitudCorteSuministroVoluntario(request):
    pdf= render_to_pdf('repotros/33_Solicitud de Corte de Suministro Voluntario.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view34_SolicitudTransferencia(request):
    pdf= render_to_pdf('repotros/34_Solicitud de Transferencia.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view35_SolicitudIncorporacion(request):
    pdf= render_to_pdf('repotros/35_Solicitud de Incorporacion.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view36_CartaRenuncia(request):
    pdf= render_to_pdf('repotros/36_Carta de Renuncia.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view37_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view38_ListadoSocioOrdenGeografico(request):
    pdf= render_to_pdf('repotros/38_Listado de Socio Orden Geografico.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view39_ListadoMedidoresMarcadosFactura(request):
    pdf= render_to_pdf('repotros/39_Listado de Medidores Marcados con Factura.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view40_ImprimirComprobanteAbonoNumero(request):
    pdf= render_to_pdf('repotros/40_Imprimir Comprobante de Abono por Numero.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view41_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view42_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view43_ListadoIngresosItems(request):
    pdf= render_to_pdf('repotros/43_Listado de Ingresos por Items.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view44_ListadoMedidoresNoDisponibles(request):
    pdf= render_to_pdf('repotros/44_Listado de Medidores no Disponibles.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view45_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view46_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view47_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view48_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view49_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view50_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view51_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view52_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view53_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view54_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view55_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view56_RendicionAlcantarillado(request):
    pdf= render_to_pdf('repotros/56_Rendicion Alcantarillado.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view57_ConsumosSemestrales(request):
    pdf= render_to_pdf('repotros/57_Consumos Semestrales.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

# def view58_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view59_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view60_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

# def view61_(request):
#     pdf= render_to_pdf('repotros/.html', {})
#     return HttpResponse(pdf, content_type='application/pdf')

def view62_LibroVentasDiarias(request):
    pdf= render_to_pdf('repotros/62_Libro de Ventas Diarias.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view63_ListadoSociosAnoIngreso(request):
    pdf= render_to_pdf('repotros/63_Listado de Socios por Ano de Ingreso.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view67_RegistroLecturaAnual(request):
    pdf= render_to_pdf('repotros/67_Registro de Lectura Anual.html', {})
    return HttpResponse(pdf, content_type='application/pdf')

def view68_ListadoConvenioAnual(request):
    pdf= render_to_pdf('repotros/68_Listado de Convenio Anual.html', {})
    return HttpResponse(pdf, content_type='application/pdf')