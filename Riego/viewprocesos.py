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


import calendar

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

def totalHEC(_id):

    total=0.0

    try:
        cursor.execute('select TOTAL_HEC from A_SOCIOS WHERE ID='+_id)

        for i in cursor.fetchall():
            total=i[0]
            print("Hectareas total de socio es : " + str(total).replace(".", ","))

    except Exception as e:
        pass
        print(e)

    return total

def buscarId(nombre):

    print(nombre)

    sql="SELECT ID FROM A_SOCIOS WHERE NOMBRES='"+nombre+"'"

    lista=[]

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({"rut":i[0],"nombre":i[1]+" "+i[2]+" "+i[3]})

        return lista
    except:
        return ''

def buscarporNombre():

    try:
        cursor.execute('select * from A_SOCIOS')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[2]})        
        return lista

    except Exception as e:
        pass
        print(e)

def viewID(request):

    nombre=request.GET.get('socio')
    id_=""

    if nombre != None:
        for x in nombre:
            id_=id_+x
            if x==" ":
                break
    
    return render(request, 'procesos/id_socio.html', {'nombre': id_})

def buscarlista(mes,ano):

    lista=[]
    sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_CONSUMO_DIARIO.CONSUMO, A_CONSUMO_DIARIO.VALOR_CONSUMO, A_CONSUMO_DIARIO.ID FROM A_SOCIOS INNER JOIN A_CONSUMO_DIARIO ON A_SOCIOS.ID = A_CONSUMO_DIARIO.ID_PARCELERO WHERE (((A_CONSUMO_DIARIO.MES)='"+mes+"') AND ((A_CONSUMO_DIARIO.ANO)="+ano+"));"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'nombre':i[0]+" "+i[1],'consumo':i[2],'valor':i[3],'id':i[4]})
        
    except Exception as a:
        print(a)
    
    return lista

def buscarTurno(id_):
    sql="SELECT TURNOS_MES FROM A_TIPO_AGUA WHERE ID="+id_ 
    turno=0

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            turno=i[0]
    
    except Exception as a:
        print(a)
    print("turno numero: " + str(turno))
    return turno

def buscarSector():

    sql="SELECT ID,NOMBRE FROM A_SECTOR"
    lista=[]

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'id':i[0], 'nombre':i[1]})

    except Exception as a:
        print(a)

    return lista

def buscarInfoRiego():

    # BUSCAR TURNO ACTUAL

    #total de dias al mes
    now = datetime.datetime.now()
    start_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = start_month + datetime.timedelta(35)
    start_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    lastday= (start_next_month - datetime.timedelta(1)).strftime("%d")

    sql="SELECT * FROM A_TIPO_AGUA"
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            
            day_now=now.strftime("%d")
            numero_day=float(lastday)/int(i[3])

            lista.append({'nombre':i[1],'actual':round(int(day_now)/float(numero_day)),'turnos':i[3]})

    except Exception as a:
        print(a)

    return lista

def buscarInfoRiegoPor(tipo):

    now = datetime.datetime.now()
    start_month = datetime.datetime(now.year, now.month, 1)
    date_on_next_month = start_month + datetime.timedelta(35)
    start_next_month = datetime.datetime(date_on_next_month.year, date_on_next_month.month, 1)
    lastday= (start_next_month - datetime.timedelta(1)).strftime("%d")
    sql="SELECT * FROM A_TIPO_AGUA WHERE ID="+tipo
    turno=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            
            day_now=int(now.strftime("%d"))
            numero_day=float(lastday)/int(i[3])

            if 1 <= day_now <=numero_day:
                turno=1
            elif numero_day<day_now<=(numero_day*2):
                turno=2
            elif numero_day*2<day_now<=(numero_day*3):
                turno=3
            elif numero_day*3<day_now<=(numero_day*4):
                turno=4
            #turno=round(int(day_now)/float(numero_day))
    
    except Exception as a:
        print(a)
    return turno

def correaltivoConvenioDet():
    sql="SELECT IIf(IsNull(MAX(nrocom)), 0, Max(nrocom)) FROM a_det_convenio"
            
    try:
        cursor.execute(sql)
        for j in cursor.fetchall():
            correlativo=j[0]+1        
    except Exception as e:
        pass
        print(e)

    return correlativo

def viewConsumo(request):
    
    now = datetime.datetime.now()
    mes=''
    mensaje=""
    sugerencia=[]
    nombre=""
    consumo=""
    id_=""

    prueba=buscarInfoRiegoPor('1')

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

    if request.method=='POST' and 'buscar' in request.POST:

        id_=request.POST['identi']

        mes=request.POST['mes_']
        ano=request.POST['ano_']
        suma=0
        total=0

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12

        id_=request.POST['id_']

        if id_!=None and id_!="" and id_!=" ":
            #Revisar la suma de su consumo mensual
            #sql="SELECT SUM(CONSUMO) FROM A_CONSUMO_DIARIO WHERE ID_PARCELERO="+id_+" AND MES='"+mes+"' AND ANO="+ano
            sql="SELECT Sum(A_CONSUMO_DIARIO.CONSUMO), A_CONSUMO_DIARIO.ID_TIPO_AGUA, A_CONSUMO_DIARIO.TURNO, A_TIPO_AGUA.NOMBRE FROM A_TIPO_AGUA INNER JOIN A_CONSUMO_DIARIO ON A_TIPO_AGUA.ID = A_CONSUMO_DIARIO.ID_TIPO_AGUA GROUP BY A_CONSUMO_DIARIO.TURNO, A_CONSUMO_DIARIO.ID_TIPO_AGUA, A_CONSUMO_DIARIO.ID_PARCELERO, A_CONSUMO_DIARIO.MES, A_CONSUMO_DIARIO.ANO, A_TIPO_AGUA.NOMBRE HAVING (((A_CONSUMO_DIARIO.ID_PARCELERO)="+id_+") AND ((A_CONSUMO_DIARIO.MES)='"+mes+"') AND ((A_CONSUMO_DIARIO.ANO)="+ano+"));"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    sugerencia.append({'nombre':i[3],'consumo':i[0],'turno':i[2]})
                    suma=i[0]
                
                if suma==None:
                    suma=0

            except Exception as a:
                    print(a)
            
            sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.TOTAL_HEC FROM A_SOCIOS WHERE (((A_SOCIOS.ID)="+id_+"));"

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    nombre=i[0]+" "+i[1]
                    consumo=i[2]
            except Exception as a:
                print(a)
                id_=""
                mensaje="No se encontro socio"
        else:
            mensaje="No se encontro socio"

    if request.method=='POST' and 'imprimir' in request.POST:

        mes=request.POST['mes_1']
        ano=request.POST['ano_1']

        data={
            'lista':buscarlista(mes,ano),
            'mes':mes,
            'ano':ano,
        }

        return render(request,'procesos/historialconsumo.html', data)
    
    if request.method=='POST' and 'borrar' in request.POST:

        id_=request.POST['tipo2']
        mes=request.POST['mes_1']
        ano=request.POST['ano_1']

        sql="DELETE FROM A_CONSUMO_DIARIO WHERE ID="+id_

        try:
            cursor.execute(sql)
            cursor.commit()
        
        except Exception as a:
            print(a)
        
        data={
            'lista':buscarlista(mes,ano),
            'mes':mes,
            'ano':ano,
        }

        return render(request,'procesos/historialconsumo.html', data)


    if request.method=='POST' and 'guardar' in request.POST:

        mes=request.POST['mes']
        ano=request.POST['ano']
        tipo=request.POST['tipo']
        hora=request.POST['hora']
        fecha=request.POST['fecha']
        consumo=request.POST['consumo'].replace(",", ".")
        suma=0
        total=0

        turno=buscarInfoRiegoPor(tipo)
        print("TURNO ACTUAL " + str(turno))

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12

        id_=request.POST['identi1']
        print("ID ES: "+id_)
        if id_!=None and id_!="" and id_!=" ":
            #Revisar la suma de su consumo mensual
            #sql="SELECT SUM(CONSUMO) FROM A_CONSUMO_DIARIO WHERE ID_PARCELERO="+id_+" AND MES='"+mes+"' AND ANO="+ano
            sql="SELECT Sum(A_CONSUMO_DIARIO.CONSUMO) AS SumaDeCONSUMO FROM A_CONSUMO_DIARIO HAVING (((A_CONSUMO_DIARIO.ID_PARCELERO)="+id_+") AND ((A_CONSUMO_DIARIO.MES)='"+mes+"') AND ((A_CONSUMO_DIARIO.ANO)="+ano+"));"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    suma=i[0]
                
                if suma==None:
                    suma=0

            except Exception as a:
                    print(a)

            print("Total del socio por ahora: ..... "+ str(float(suma)))

            turnos=buscarTurno(tipo)

            print("ano y mes " + str(now.year )+ str(now.month))

            monthRange = calendar.monthrange(now.year,now.month)
            print(str(monthRange))
            print("numero de turnos: " + str(turnos))

            if now.month>=4 and now.month<=8:
                print("estamos en la fecha")

                sql="SELECT A_TARIFA_HORA.VALOR_HORA FROM A_TARIFA_HORA WHERE (((A_TARIFA_HORA.TIPO_AGUA)="+str(tipo)+"));"
                
                try:
                    cursor.execute(sql)

                    for i in cursor.fetchall():
                        valor_hora=i[0]
                        totalconsumo=valor_hora*float(consumo)

                        #LEY DEL REDONDEO
                        consumoRound=int(math.trunc(totalconsumo))

                        #if consumo[len(consumo)-1]: 
                        print(str(consumoRound)[len(str(consumoRound))-1])

                        if str(consumoRound)[len(str(consumoRound))-1]==6:
                            consumoRound=consumoRound+1


                        sql="INSERT INTO A_CONSUMO_DIARIO(ID_PARCELERO,MES,PERIODO,ANO,ID_TIPO_AGUA,HORA,FECHA_INGRESO,CONSUMO,VALOR_CONSUMO,TURNO) VALUES("+id_+",'"+mes+"',"+str(mesnum)+","+ano+","+tipo+",'"+hora+"','"+fecha+"','"+consumo.replace(".", ",")+"',"+str(consumoRound)+","+str(turno)+")"
                        print(sql)
                        try:
                            print("Se esta insertando....")
                            cursor.execute(sql)
                            cursor.commit()
                            mensaje="Se ingreso correctamente horas de riego."
                            consumo=""
                        except Exception as a:
                            print(a)

                except Exception as a:
                        print(a)
                        mensaje="No se guardo correctamente"
                        consumo=""
                        id_=""

            else:
                print("total hectares: "+str(totalHEC(id_)) +" total suma "+str(suma))
                total=float(consumo)+float(suma)
                print(str(int(total)))
                if total<=float(totalHEC(id_)):

                    print("Esta en el rango para poder guardar...")

                    #Buscar tipo de riego y valor hora
                    sql="SELECT VALOR_HORA FROM A_TARIFA_HORA WHERE TIPO_AGUA="+tipo

                    try:
                        cursor.execute(sql)

                        for i in cursor.fetchall():
                            valor_hora=i[0]
                            totalconsumo=valor_hora*float(consumo)
                            print("Valor hora es: "+str(valor_hora))
                            print("Valor consumo es: " + consumo)
                            print("Valor total a pagar: "+str(totalconsumo))

                            #LEY DEL REDONDEO
                            consumoRound=int(math.trunc(totalconsumo))

                            #if consumo[len(consumo)-1]: 
                            print(str(consumoRound)[len(str(consumoRound))-1])

                            if str(consumoRound)[len(str(consumoRound))-1]==6:
                                consumoRound=consumoRound+1


                            sql="INSERT INTO A_CONSUMO_DIARIO(ID_PARCELERO,MES,ANO,ID_TIPO_AGUA,HORA,FECHA_INGRESO,CONSUMO,VALOR_CONSUMO,TURNO,PERIODO) VALUES("+id_+",'"+mes+"',"+ano+","+tipo+",'"+hora+"','"+fecha+"','"+consumo.replace(".", ",")+"',"+str(consumoRound)+","+str(turno)+","+str(mesnum)+")"

                            try:
                                print("Se esta insertando....")
                                cursor.execute(sql)
                                conn.commit()
                                mensaje="Se ingreso correctamente horas de riego."
                                consumo=""
                            
                            except Exception as a:
                                print(a)
                                id_=""

                    except Exception as a:
                            print(a)
                            id_=""
                            consumo=""

                else:
                    print("No le quedan horas para ingresar su consumo")
                    print("Se supero: " + str(float(suma)+float(consumo)))
                    mensaje="No se pudo ingresar. Parcelero acaba de ocupar total de horas."
                    consumo=""
                    id_=""
        else:
            mensaje="Favor debe seleccionar parcelero"
            id_=""
            consumo=""

    data={
        'info_riego':buscarInfoRiego(),
        'tipos':buscarTipos(),
        'asociacion':viewName(),
        'ano':str(now.year),
        'mes':mes,
        'hora':str(now.hour)+":"+str(now.minute),
        'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
        'all_socios':buscarporNombre,
        'mensaje':mensaje,
        'sugerencia':sugerencia,
        'nombre':nombre,
        'consumo':consumo,
        'numeroid':id_
    }

    return render(request,'procesos/consumo.html', data)

def buscarConvenios():

    try:
        cursor.execute('select * from A_COBROS')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1]})
        
        return lista

    except Exception as e:
        pass
        print(e)
    
def viewConvenioMasivos(request):

    listaup=[]
    data={}

    try:
        cursor.execute("SELECT ID,RUT,NOMBRES FROM A_SOCIOS WHERE VIGENTE=0 AND ID=78")

        for i in cursor.fetchall():
            listaup.append({'id':i[0],'rut':i[1],'nombre':i[2]})

        data={
            'lista_s':buscarSocios(),

            'all_socios':buscarporNombre
        }
                
        return render(request, 'procesos/masivo.html', data)
    
    except Exception as a:
        print(a)
    
    return render(request, 'procesos/masivo.html', data)
        
def buscarSocios():

    listaup=[]

    cursor.execute("SELECT ID,RUT,NOMBRES FROM A_SOCIOS WHERE VIGENTE=0")

    for i in cursor.fetchall():
        listaup.append({'id':i[0],'rut':i[1],'nombre':i[2]})
    
    return listaup

def viewConvenio(request):

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
    
    if request.method=='POST' and 'buscarrep' in request.POST:

        id_=request.POST['identificador']
        lista=[]
        nombres=""
        mensaje=""

        sql="SELECT A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_SOCIOS.ID, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_DET_BOLETA.ID FROM A_SOCIOS INNER JOIN (A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA) ON A_SOCIOS.ID = A_BOLETA.ID_PARCELERO WHERE (((A_BOLETA.VIGENTE)=0) AND ((A_BOLETA.ID_PARCELERO)="+str(id_)+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                identificador=i[4]
                nombres=i[5]+" "+i[6]

                if int(i[2])-int(i[3])!=0:
                    if i[0]==5:
                        sql="SELECT A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.CODIGO)<>5) AND ((A_BOLETA.ID_PARCELERO)="+str(id_)+") AND ((A_BOLETA.VIGENTE)<>0));"
                        try:
                            cursor.execute(sql)
                            for row in cursor.fetchall():
                                if str(row[0])==str(row[1]):
                                    print("sin saldo anterior.")
                                else:  
                                    lista.append({'codigo':i[0],'desc':i[1],'valor':int(row[0])-int(row[1]),'id':i[4],'nombres':i[5]+" "+i[6],'boleta':i[7]})
                        except Exception as a:
                            print(a)
                    else:
                        lista.append({'codigo':i[0],'desc':i[1],'valor':int(i[2])-int(i[3]),'id':i[4],'nombres':i[5]+" "+i[6],'boleta':i[7]})
                
            data={
                'lista':lista,
                'tipos':buscarConvenios(),
                'asociacion':viewName(),
                'ano':str(now.year),
                'mes':mes,
                'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
                'all_socios':buscarporNombre,
                'identificador':id_,
                'nombres':nombres
            }
        except Exception as a:
            print(a)
            mensaje="No se encontraron datos"
        
            data={
                'lista':lista,
                'tipos':buscarConvenios(),
                'asociacion':viewName(),
                'ano':str(now.year),
                'mes':mes,
                'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
                'all_socios':buscarporNombre,
                'mensaje':mensaje
            }
                
        return render(request, 'procesos/repactacion.html', data)

    if request.method=='POST' and 'guardarrep' in request.POST:

        identi=request.POST['identi']
        ch=request.POST.getlist('options[]')
        lista=[]

        correlativo=""
        ano=0
        tipo='3'
        mes=request.POST['mes']
        ano=request.POST['ano']
        total=request.POST['total']
        cuotas=request.POST['cuota']
        interes=request.POST['interes']
        valorcuota=request.POST['valor']
    
        mesaumento=now.month

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12
        
        fecha=str(now.day)+"/"+str(mesnum)+"/"+str(ano)

        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_convenio"
    
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as e:
            pass
            print(e)
        
        if identi!=None and identi!=0:

            if len(ch)==0:
                    mensaje="Error: Debe seleccionar valores"            
            else:

                for i in ch: 
                    print(i)
                    sql="SELECT A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_DET_BOLETA.CODIGO FROM A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+identi+") AND ((A_DET_BOLETA.ID)="+i+") AND ((A_BOLETA.VIGENTE)=0));"
                    
                    try:
                        cursor.execute(sql)
                        for row in cursor.fetchall():
                            valor=row[1]
                            if row[3]==5:
                                #actualizar valores anteriores
                                sql="UPDATE A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA SET A_DET_BOLETA.PAGADO = A_DET_BOLETA.VALOR WHERE (((A_DET_BOLETA.CODIGO)<>5) AND ((A_BOLETA.VIGENTE)<>0) AND ((A_BOLETA.ID_PARCELERO)="+identi+"));"
                                print(sql)
                                try:
                                    cursor.execute(sql)
                                    cursor.commit()
                                except Exception as a:
                                    print(a)
                            else:
                                sql="UPDATE A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA SET A_DET_BOLETA.PAGADO="+valor+" WHERE (((A_DET_BOLETA.CODIGO)<>5) AND ((A_BOLETA.VIGENTE)=0) AND ((A_DET_BOLETA.ID)="+i+"));"
                                print(sql)
                                try:
                                    cursor.execute(sql)
                                    cursor.commit()
                                except Exception as a:
                                    print(a)
                        mensaje="Quedo guardado correctamente"
                    except Exception as a:
                        print(a)
                        mensaje="No se encontraron detalles"
                
            sql="INSERT INTO A_CONVENIO(ID,TIPO_CONVENIO,ID_PARCELERO,TOTAL_CUOTAS,MONTO_PACTADO,INTERES,VALOR_CUOTA,FECHA,MES,ANO) VALUES("+str(correlativo)+","+tipo+","+str(identi)+","+cuotas+","+total+","+interes+","+valorcuota+",'"+fecha+"','"+mes+"',"+ano+")"

            try:
                cursor.execute(sql)
                conn.commit()

                i=1

                while i<=int(cuotas):
                    cuot=str(i)+"/"+str(cuotas)
                    
                    sql="INSERT INTO A_DET_CONVENIO(ID_CONVENIO,FECHA_PROPUESTA,NRO_CUOTA,VALOR_CUOTA,MES,ANO) VALUES("+str(correlativo)+",'"+fecha+"','"+cuot+"',"+valorcuota+","+str(mesnum)+","+str(ano)+")"
                    i=i+1

                    mesnum=mesnum+1

                    if mesnum==13:
                        mesnum=1
                        ano=int(ano)+1

                    fecha=str(now.day)+"/"+str(mesnum)+"/"+str(ano)
                    ano=ano

                    try:
                        cursor.execute(sql)
                        conn.commit()            
                        mensaje="Quedo guardado correctamente"
                    except Exception as a:
                        print(a)
            
            except Exception as a:
                print(a)
                        
        else:
            mensaje="Falta seleccionar parcelero"
        
        data={
            'tipos':buscarConvenios(),
            'asociacion':viewName(),
            'ano':str(now.year),
            'mes':mes,
            'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
            'all_socios':buscarporNombre,
            'mensaje':mensaje
        }
                
        return render(request, 'procesos/repactacion.html', data)



    if request.method=='POST' and 'ver' in request.POST:
        print("Imprimiendo...")
        nro=request.POST['nro']
        convenio=request.POST['idconvenio']
        rut=""
        nombres=""
        direccion=""
        motivo=""
        total=""
        interes=""
        fecha=""

        lista=[]
        lista2=[]

        sql="SELECT A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_COBROS.DESCRIPCION, A_CONVENIO.TOTAL_CUOTAS, A_CONVENIO.MONTO_PACTADO, A_CONVENIO.INTERES, A_CONVENIO.FECHA,A_CONVENIO.ID FROM (A_CONVENIO INNER JOIN A_SOCIOS ON A_CONVENIO.ID_PARCELERO = A_SOCIOS.ID) INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID WHERE (((A_CONVENIO.ID)="+convenio+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                rut=i[0]
                nombres=i[1]+" "+i[2]
                direccion=i[3]
                motivo=i[4]
                total=i[6]
                interes=i[7]
                fecha=i[8]
        except Exception as a:
            print(a)

        sql="SELECT A_DET_CONVENIO.ID_CONVENIO, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA, A_DET_CONVENIO.MES, A_DET_CONVENIO.ANO FROM A_DET_CONVENIO WHERE (((A_DET_CONVENIO.ID_CONVENIO)="+convenio+"));"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                mes=i[3]
                
                if mes==1:
                    mes='Enero'
                if mes==2:
                    mes='Febrero'
                if mes==3:
                    mes='Marzo'
                if mes==4:
                    mes='Abril'
                if mes==5:
                    mes='Mayo'
                if mes==6:
                    mes='Junio'
                if mes==7:
                    mes='Julio'
                if mes==8:
                    mes='Agosto'
                if mes==9:
                    mes='Septiembre'
                if mes==10:
                    mes='Octubre'
                if mes==11:
                    mes='Noviembre'
                if mes==12:
                    mes='Diciembre'

                lista2.append({'nro':i[1],'valor':i[2],'mes':mes,'ano':i[4]})
        except Exception as a:
            print(a)

        data={
            'lista2':lista2,
            'rut':rut,
            'nombres':nombres,
            'direccion':direccion,
            'motivo':motivo,
            'total':total,
            'interes':interes,
            'fecha':fecha,
            'numero':convenio
        }

        pdf = render_to_pdf('reportes/convenio.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    
    if request.method=='POST' and 'eliminar' in request.POST:

        nro=request.POST['nro']
        boleta=request.POST['boleta']

        if boleta=='0':

            sql="DELETE FROM A_DET_CONVENIO WHERE ID="+nro

            try:
                cursor.execute(sql)
                cursor.commit()
            except Exception as a:
                print(a)
        else:
            mensaje="No se puede eliminar, convenio esta enlazado con un aviso"

        data={
            'mensaje':mensaje,
            'all_socios':buscarporNombre
        }

        return render(request, 'procesos/historial.html', data)

    if request.method=='POST' and 'buscar' in request.POST:

        id_=request.POST['identi'].replace(' ','')

        sql="SELECT A_DET_CONVENIO.ID_BOLETA, A_COBROS.DESCRIPCION, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA, A_DET_CONVENIO.TOTAL_PAGADO,A_DET_CONVENIO.ID,A_DET_CONVENIO.ID_CONVENIO FROM (A_CONVENIO INNER JOIN A_DET_CONVENIO ON A_CONVENIO.ID = A_DET_CONVENIO.ID_CONVENIO) INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID WHERE (((A_CONVENIO.ID_PARCELERO)="+str(id_)+"))"
        print(sql)
        lista=[]

        try:

            cursor.execute(sql)

            for i in  cursor.fetchall():
                if i[4]==0:
                    estado="PENDIENTE"
                else:
                    estado="$"+str(i[4])
                lista.append({'boleta':i[0],'cuota':i[2],'valor':i[3],'des':i[1],'total':estado,'id':i[5],'idconvenio':i[6]})
            
            data={
                'all_convenio':lista,
                'all_socios':buscarporNombre
            }

            return render(request, 'procesos/historial.html', data)

        except Exception as e:
            pass
            print(e)
        
        data={
            'all_socios':buscarporNombre
        }

        return render(request, 'procesos/historial.html', data)

    if request.method=='POST' and 'repactacion' in request.POST:

        data={
            'tipos':buscarConvenios(),
            'asociacion':viewName(),
            'ano':str(now.year),
            'mes':mes,
            'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
            'all_socios':buscarporNombre
        }
                
        return render(request, 'procesos/repactacion.html', data)

    if request.method=='POST' and 'individual' in request.POST:

        data={
            'lista_s':buscarSocios(),
            'tipos':buscarConvenios(),
            'asociacion':viewName(),
            'ano':str(now.year),
            'mes':mes,
            'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
            'all_socios':buscarporNombre
        }
                
        return render(request, 'procesos/convenio.html', data)
      


    if request.method=='POST' and 'historial' in request.POST:

        data={
            'all_socios':buscarporNombre
        }

        return render(request, 'procesos/historial.html', data)

    if request.method=='POST' and 'guardarmasivo' in request.POST:
        print("Insertando convenios masivos....")
        correlativo=""

        tipo=request.POST['tipo']
        mes=request.POST['mes']
        ano=request.POST['ano']
        total=request.POST['total']
        cuotas=request.POST['cuota']
        interes=request.POST['interes']
        valorcuota=request.POST['valor']
        mesaumento=now.month

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12
        
        fechaahora=str(now.day)+"/"+str(mesnum)+"/"+str(ano)
        fechamasiva=str(now.day)+"/"+str(mesnum)+"/"+str(ano)
        anomasivo=ano
        mesmasivo=mesnum

        #sql="SELECT COUNT(ID) FROM A_CONVENIO"
        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_convenio"
        ch=request.POST.getlist('options[]')
        j=0

        if len(ch)==0:
                mensaje="Error: Debe seleccionar socios"            
        else:
            for i in ch:
                #sql="SELECT COUNT(ID) FROM A_CONVENIO"
                sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_convenio"
            
                try:
                    cursor.execute(sql)

                    for j in cursor.fetchall():
                        correlativo=j[0]+1
                    
                except Exception as e:
                    pass
                    print(e)

                sql="INSERT INTO A_CONVENIO(ID,TIPO_CONVENIO,ID_PARCELERO,TOTAL_CUOTAS,MONTO_PACTADO,INTERES,VALOR_CUOTA,FECHA,MES,ANO) VALUES("+str(correlativo)+","+tipo+","+str(i)+","+cuotas+","+total+","+interes+","+valorcuota+",'"+fechaahora+"','"+str(mes)+"',"+str(ano)+")"

                try:
                        cursor.execute(sql)
                        conn.commit()

                        i=1

                        while i<=int(cuotas):
                            cuot=str(i)+"/"+str(cuotas)
                            
                            sql="INSERT INTO A_DET_CONVENIO(ID_CONVENIO,FECHA_PROPUESTA,NRO_CUOTA,VALOR_CUOTA,MES,ANO) VALUES("+str(correlativo)+",'"+fechamasiva+"','"+cuot+"',"+valorcuota+",'"+str(mesmasivo)+"',"+str(anomasivo)+")"
                            print(sql)

                            i=i+1

                            mesmasivo=mesmasivo+1

                            if mesmasivo==13:
                                mesmasivo=1
                                anomasivo=int(anomasivo)+1

                            fechamasiva=str(now.day)+"/"+str(mesmasivo)+"/"+str(anomasivo)

                            try:
                                cursor.execute(sql)
                                conn.commit()            

                            except Exception as a:
                                print(a)
                                print(sql)
                    
                except Exception as a:
                    print(a)
                    print(sql)

                mesmasivo=mesnum
                fechamasiva=fechaahora
                anomasivo=ano
                

            mensaje="Quedo guardado correctamente"
                        
                    

    if request.method=='POST' and 'guardar' in request.POST:

        correlativo=""
        ano=0
        tipo=request.POST['tipo']
        mes=request.POST['mes']
        ano=request.POST['ano']
        identificador=request.POST['identi']
        total=request.POST['total']
        cuotas=request.POST['cuota']
        interes=request.POST['interes']
        valorcuota=request.POST['valor']
    
        mesaumento=now.month

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12
        
        fecha=str(now.day)+"/"+str(mesnum)+"/"+str(ano)

        #sql="SELECT COUNT(ID) FROM A_CONVENIO"
        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_convenio"
    
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as e:
            pass
            print(e)

        if identificador!=None and identificador!=0:
                
            sql="INSERT INTO A_CONVENIO(ID,TIPO_CONVENIO,ID_PARCELERO,TOTAL_CUOTAS,MONTO_PACTADO,INTERES,VALOR_CUOTA,FECHA,MES,ANO) VALUES("+str(correlativo)+","+tipo+","+str(identificador)+","+cuotas+","+total+","+interes+","+valorcuota+",'"+fecha+"','"+mes+"',"+ano+")"

            try:
                cursor.execute(sql)
                conn.commit()

                i=1

                while i<=int(cuotas):
                    cuot=str(i)+"/"+str(cuotas)
                    
                    sql="INSERT INTO A_DET_CONVENIO(ID_CONVENIO,FECHA_PROPUESTA,NRO_CUOTA,VALOR_CUOTA,MES,ANO) VALUES("+str(correlativo)+",'"+fecha+"','"+cuot+"',"+valorcuota+","+str(mesnum)+","+str(ano)+")"
                    i=i+1

                    mesnum=mesnum+1

                    if mesnum==13:
                        mesnum=1
                        ano=int(ano)+1

                    fecha=str(now.day)+"/"+str(mesnum)+"/"+str(ano)
                    ano=ano

                    try:
                        cursor.execute(sql)
                        conn.commit()            
                        mensaje="Quedo guardado correctamente"
                    except Exception as a:
                        print(a)
            
            except Exception as a:
                print(a)

            data={
                'tipos':buscarConvenios(),
                'asociacion':viewName(),
                'ano':str(now.year),
                'mes':mes,
                'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
                'all_socios':buscarporNombre,
                'lista_s':buscarSocios(),
                'mensaje':mensaje
            }
                
            return render(request, 'procesos/convenio.html', data)

    data={
        'tipos':buscarConvenios(),
        'asociacion':viewName(),
        'ano':str(now.year),
        'mes':mes,
        'fecha':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
        'all_socios':buscarporNombre,
        'lista_s':buscarSocios(),
        'mensaje':mensaje
    }
        
    return render(request, 'procesos/masivo.html', data)

def convenio(request):
    pdf= render_to_pdf('reportes/convenio.html', {})
    return HttpResponse(pdf, content_type='application/pdf')
    
def buscarCorrelativoBoleta():

    correlativo2=0
    #sql="SELECT COUNT(ID) FROM A_DET_BOLETA"
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_det_boleta"
    
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo2=i[0]+1

    except Exception as a:
        print(a)
    
    return correlativo2

def buscarBoleta(id_,year,month):

    sql="SELECT * FROM A_BOLETA WHERE ANO="+str(year)+" AND MES='"+str(month)+"' AND ID_PARCELERO="+str(id_)
    print(sql)
    existe=0

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            existe=1
    except Exception as a:
        print(a)

    return existe

def mesNombre(mes):
    if mes==1:
        mes='Enero'
    if mes==2:
        mes='Febrero'
    if mes==3:
        mes='Marzo'
    if mes==4:
        mes='Abril'
    if mes==5:
        mes='Mayo'
    if mes==6:
        mes='Junio'
    if mes==7:
        mes='Julio'
    if mes==8:
        mes='Agosto'
    if mes==9:
        mes='Septiembre'
    if mes==10:
        mes='Octubre'
    if mes==11:
        mes='Noviembre'
    if mes==12:
        mes='Diciembre'
    
    return mes

def buscarCierre(mes,ano):

    sql="SELECT VIGENTE FROM A_BOLETA WHERE MES='"+str(mes)+"' AND ANO="+str(ano)
    print(sql)
    estado=0

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            if i[0]==0:
                estado=1
        
    except Exception as a:
        print(a)
    
    return estado

def buscarNumeroAbono():
    #sql="SELECT COUNT(ID) FROM A_ABONO"
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_abono"
    abono=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            abono=i[0]+1
    except Exception as a:
        print(a)
    
    return abono

def buscarPagos(id_):
    sql="SELECT A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO FROM A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(id_)+") AND ((A_BOLETA.VIGENTE)=0));"
    estado=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            if i[1]>0:
                estado=1
    except Exception as a:
        print(a)
        print("Error : "  + sql)

    return estado

def numeroBoleta():
    #sql="SELECT COUNT(IDBOLETA) FROM A_BOLETA"
    sql="SELECT IIf(IsNull(MAX(idboleta)), 0, Max(idboleta)) FROM a_boleta"
    correlativo=1
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    return correlativo

def viewGeneracion(request):

    now = datetime.datetime.now()
    correlativo=1
    mensaje=""
    botoncierre=0

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

    #sql="SELECT COUNT(IDBOLETA) FROM A_BOLETA"
    sql="SELECT IIf(IsNull(MAX(idboleta)), 0, Max(idboleta)) FROM a_boleta"
    
    correlativo=numeroBoleta()

    sql="SELECT A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA FROM (A_CONVENIO INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID) INNER JOIN A_DET_CONVENIO ON A_CONVENIO.ID = A_DET_CONVENIO.ID_CONVENIO WHERE (((A_CONVENIO.ID_PARCELERO)=1)) GROUP BY A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.FECHA_PROPUESTA, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA HAVING (((A_DET_CONVENIO.FECHA_PROPUESTA) Like '*/7/*'))"
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            print("AGIUII")
    except Exception as a:
        print(a)

    if request.method=='POST' and 'cerrar' in request.POST:

        sql="UPDATE A_BOLETA SET VIGENTE=1"

        try:
            cursor.execute(sql)
            cursor.commit()
            botoncierre=1
            mensaje="Se cerro correctamente periodo anterior" 
            print(str(botoncierre))
        except Exception as a:
            print(a)
    
    if request.method=='POST' and 'aceptar' in request.POST:

        id_=0
        sector=0
        mes=request.POST['mes']
        ano=request.POST['ano']
        mensaje=""
        fecha_emision=request.POST['emision']
        fecha_vencimiento=request.POST['vencimiento']
        totalboleta=0
        total_a_pagar=0
        ruta=0
        direccion=""
        valor_consumo=0
        afavor=0

        opcion=request.POST.getlist('toggle-switch')
        opcion2=request.POST.getlist('demo-radio-la1')
        opcion3=request.POST.getlist('toggle-switch1')

        for i in opcion:
            deseahacer=i[0]
        
        for i in opcion2:
            modoopcion=i[0]
            # 0 es por secotr
            # 1 es por parcelero
        
        for i in opcion3:
            tipodocto=i[0]

        if mes=='Enero':
            mesnum=1
        if mes=='Febrero':
            mesnum=2
        if mes=='Marzo':
            mesnum=3
        if mes=='Abril':
            mesnum=4
        if mes=='Mayo':
            mesnum=5
        if mes=='Junio':
            mesnum=6
        if mes=='Julio':
            mesnum=7
        if mes=='Agosto':
            mesnum=8
        if mes=='Septiembre':
            mesnum=9
        if mes=='Octubre':
            mesnum=10
        if mes=='Noviembre':
            mesnum=11
        if mes=='Diciembre':
            mesnum=12

        # MES ANTERIOR VIGENTE O NO VIGENTE
        if mesnum==12:
            mesAnterior=mesNombre(1)
            #ano=int(ano)-1
        else:
            mesAnterior=mesNombre(mesnum-1)

        if deseahacer=='0':

            if buscarCierre(mesAnterior,ano)==0:
                print("Ciere fue de " + str(buscarCierre(mesAnterior,ano)))

                if modoopcion=='0':
                    #Seleccionar sector
                    
                    #CALCULAR TOTAL DE CONSUMO A_BOLETA
                    sql="SELECT A_CONSUMO_DIARIO.ID_PARCELERO, A_SECTOR.ID, A_SOCIOS.RUTA, A_SOCIOS.DIRECCION, Sum(A_CONSUMO_DIARIO.CONSUMO) AS SumaDeCONSUMO, Sum(A_CONSUMO_DIARIO.VALOR_CONSUMO), A_SOCIOS.RUT FROM (A_CONSUMO_DIARIO INNER JOIN A_SOCIOS ON A_CONSUMO_DIARIO.ID_PARCELERO = A_SOCIOS.ID) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE A_SOCIOS.VIGENTE=0 GROUP BY A_CONSUMO_DIARIO.ID_PARCELERO, A_SOCIOS.RUT, A_SECTOR.ID, A_SOCIOS.RUTA, A_SOCIOS.DIRECCION , A_CONSUMO_DIARIO.PERIODO, A_CONSUMO_DIARIO.ANO HAVING (((A_CONSUMO_DIARIO.PERIODO)="+str(mesnum)+") AND ((A_CONSUMO_DIARIO.ANO)="+str(ano)+"));"
                    print("SQL PRINCIPAL: "+ sql)
                    try:
                        cursor.execute(sql)

                        for i in cursor.fetchall():
                            id_=i[0]
                            sector=i[1]
                            ruta=i[2]
                            direccion=i[3]
                            valor_consumo=i[4]
                            valor_mes=i[5]
                            rut=i[6]
                            total_a_pagar=total_a_pagar+valor_mes

                            #Consultar boletas ya generadas en el mes y ano

                            existe=buscarBoleta(id_,str(now.year),mes)

                            print(str(existe))

                            if existe==0:

                                #sql="SELECT COUNT(IDBOLETA) FROM A_BOLETA"
                                sql="SELECT IIf(IsNull(MAX(idboleta)), 0, Max(idboleta)) FROM a_boleta"
                    
                                try:
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        correlativo=i[0]+1
                                        
                                except Exception as e:
                                    pass
                                    print(e)

                                #INSERTAR CONSUMO DE HORA EN DETALLE
                                sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",2,'CONSUMO DE AGUA POR HORA',"+str(valor_mes)+",'"+str(valor_consumo)+"')"

                                try:    
                                    cursor.execute(sql)
                                    cursor.commit()
                                    print("Se ingreso en detalle...")

                                except Exception as a:
                                    print(a)          

                                #INSERTAR CONVENIO A BOLETA           
                                sql="SELECT A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA,A_DET_CONVENIO.ID FROM (A_CONVENIO INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID) INNER JOIN A_DET_CONVENIO ON A_CONVENIO.ID = A_DET_CONVENIO.ID_CONVENIO WHERE (((A_CONVENIO.ID_PARCELERO)="+str(id_)+") and A_DET_CONVENIO.ANO="+str(ano)+" AND A_DET_CONVENIO.MES="+str(mesnum)+") GROUP BY A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.FECHA_PROPUESTA, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA,A_DET_CONVENIO.ID"
                                print("sql convenio : " + sql)
                                try:
                                    cursor.execute(sql) 

                                    for i in cursor.fetchall():
                                        codigo=i[0]
                                        descripcion=i[1]
                                        descripcion2=i[2]
                                        valor=i[3]
                                        total_a_pagar=total_a_pagar+valor
                                        idconvenio=i[4]

                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+","+str(codigo)+",'"+str(descripcion)+"',"+str(valor)+",'"+str(descripcion2)+"')"
                                        
                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                            print("Insertar detalle de convenio...")

                                            #ACTUALIZAR BOLETA EN CONVENIO
                                            sql="UPDATE A_DET_CONVENIO SET ID_BOLETA="+str(correlativo)+" WHERE ID="+str(idconvenio)
                                            print(sql)
                                            try:
                                                cursor.execute(sql)
                                                cursor.commit()
                                            except Exception as a:
                                                print("Error "+str(a)+" en el sql: " + sql)
                                                
                                        except Exception as a:
                                            print("Error "+str(a)+" en el sql: " + sql)
                                        
                                except Exception as a:
                                    print("Error "+str(a)+" en el sql: " + sql)

                                # Buscar saldo anterior
                                
                                sql="SELECT A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO FROM A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA GROUP BY A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_BOLETA.PERIODO, A_BOLETA.ANO, A_BOLETA.ID_PARCELERO, A_DET_BOLETA.CODIGO HAVING (((A_BOLETA.PERIODO)<"+str(mesnum)+") AND ((A_BOLETA.ANO)="+str(ano)+") AND ((A_BOLETA.ID_PARCELERO)="+str(id_)+") AND ((A_DET_BOLETA.CODIGO)<>5));"
                                print("sql saldo anterior: " + sql)
                                totalsaldo=0
                                

                                try:    
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        totalsaldo=totalsaldo+int(i[1])-int(i[2])
                                    
                                    if totalsaldo>0:
                                        #Insertar saldo anterior

                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",5,'SALDO ANTERIOR',"+str(totalsaldo)+",'')"
                                            
                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                            print("Insertar saldo anterior....")
                                                    
                                        except Exception as a:
                                            print(a)
                                            
                                except Exception as a:
                                    print(a)

                                #BUSCAR MENSAJE PARA LOS AVISOS
                                sql="SELECT DESCRIPCION FROM A_MENSAJE"
                                
                                try:
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        mensaje=i[0]
                                except Exception as a:
                                    print(a)
                                
                                total2=total_a_pagar+totalsaldo
                                saldototal=0
                                existesaldos=0

                                # BUSCAR SALDO A FAVOR
                                sql="SELECT A_SALDOS.MONTO, A_SALDOS.SALDO, A_SALDOS.ID FROM A_SALDOS WHERE (((A_SALDOS.ID_PARCELERO)="+str(id_)+"))" 
                                
                                try:
                                    cursor.execute(sql)
                                    for i in cursor.fetchall():
                                        saldo=i[1]
                                        idsaldo=i[2]

                                        if saldo!=0:
                                            existesaldos=1
    
                                            if total2>=saldo:
                                                sql="UPDATE A_SALDOS SET SALDO=0 WHERE ID="+str(idsaldo)

                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                    saldototal=saldototal+saldo

                                                except Exception as a:
                                                    print(a)

                                            elif total2>=0:

                                                sql="UPDATE A_SALDOS SET SALDO="+str(int(saldo)-int(total2))+" WHERE ID="+str(idsaldo)
                                                
                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                    saldototal=saldototal+saldo-(int(saldo)-int(total2))

                                                except Exception as a:
                                                    print(a)
                                            
                                            total2=total2-saldo
                                                                        
                                    if existesaldos==1:
                                        #Insertar saldo a favor
                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",6,'SALDO A FAVOR',-"+str(saldototal)+",'')"
                                            
                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                        except Exception as a:
                                            print(a)
                                            print(sql)
                                    

                                except Exception as a:
                                    print(a)
                                
                                intereses=0

                                #BUSCAR INTERESES POR NO PAGO
                                if totalsaldo>0:

                                    sql="SELECT MULTAXNOPAGO FROM A_SOCIOS WHERE ID="+str(id_)
                                    try:
                                        cursor.execute(sql)
                                        for i in cursor.fetchall():
                                            nopago=i[0]
                                            
                                            if nopago==1:
                                                intereses=round(total_a_pagar*0.02)

                                                #INTERESES
                                                sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",3,'INTERESES',"+str(intereses)+",'')"
                                                print(sql)
                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                except Exception as a:
                                                    print(a)
                                                    print(sql)

                                    except Exception as a:
                                        print(a)
    
                                
                                totalapagarB=total_a_pagar+totalsaldo-saldototal+intereses
                                valor_mes=total_a_pagar+intereses

                                #Insertar en A_Boleta DEBE SER PRIMERO QUE ALL. NO EXISTE RELACION ANTES!!!
                                sql="INSERT INTO A_BOLETA(RUT,IDBOLETA,ID_PARCELERO,SECTOR_CORRELATIVO,MES,PERIODO,ANO,MENSAJE,FECHA_EMISION,FECHA_VENCIMIENTO,TOTALBOLETA,TOTAL_A_PAGAR,RUTA,DIRECCION,VALOR_CONSUMO,AFAVOR,TIPODOCTO) VALUES('"+str(rut)+"',"+str(correlativo)+","+str(id_)+","+str(sector)+",'"+mes+"',"+str(mesnum)+","+ano+",'"+mensaje+"','"+fecha_emision+"','"+fecha_vencimiento+"',"+str(valor_mes)+","+str(totalapagarB)+","+str(ruta)+",'"+str(direccion)+"','"+str(valor_consumo)+"',"+str(afavor)+","+str(tipodocto)+")"
                                print(sql)
                                try:
                                    cursor.execute(sql)
                                    cursor.commit()
                                    print("Guardadoo correctamete.")  
                                    mensaje="Se genero satisfactoriamente."
                                    total_a_pagar=0

                                except Exception as a:
                                    print(a)
                            else:
                                print("Boleta ya esta generada en el mes y año de facturación. Medidor: "+ str(id_))
                                mensaje="Boleta ya esta generada en el mes y año de facturación."
                                
                    except Exception as a:
                        print(a)
                        mensaje="Faltan consumos por ingresar."
                
                else:
                    # SE SELECCIONO PARCELERO
                    id_=request.POST['id_1'].strip()
                    print("id parcelero: "+ id_)

                    #CALCULAR TOTAL DE CONSUMO A_BOLETA
                    sql="SELECT A_CONSUMO_DIARIO.ID_PARCELERO, A_SECTOR.ID, A_SOCIOS.RUTA, A_SOCIOS.DIRECCION, Sum(A_CONSUMO_DIARIO.CONSUMO) AS SumaDeCONSUMO, Sum(A_CONSUMO_DIARIO.VALOR_CONSUMO) , A_SOCIOS.RUT FROM (A_CONSUMO_DIARIO INNER JOIN A_SOCIOS ON A_CONSUMO_DIARIO.ID_PARCELERO = A_SOCIOS.ID) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE A_SOCIOS.VIGENTE=0 GROUP BY A_CONSUMO_DIARIO.ID_PARCELERO, A_SECTOR.ID, A_SOCIOS.RUTA, A_SOCIOS.RUT, A_SOCIOS.DIRECCION , A_CONSUMO_DIARIO.PERIODO, A_CONSUMO_DIARIO.ANO HAVING (((A_CONSUMO_DIARIO.PERIODO)="+str(mesnum)+") AND ((A_CONSUMO_DIARIO.ANO)="+str(ano)+") AND ((A_CONSUMO_DIARIO.ID_PARCELERO)="+str(id_)+"));"
                    print("SQL PRINCIPAL: "+ sql)
                    try:
                        cursor.execute(sql)

                        for i in cursor.fetchall():
                            id_=i[0]
                            sector=i[1]
                            ruta=i[2]
                            direccion=i[3]
                            valor_consumo=i[4]
                            valor_mes=i[5]
                            rut=i[6]
                            total_a_pagar=total_a_pagar+valor_mes

                            #Consultar boletas ya generadas en el mes y ano

                            existe=buscarBoleta(id_,str(now.year),mes)

                            print(str(existe))

                            if existe==0:

                                #sql="SELECT COUNT(IDBOLETA) FROM A_BOLETA"
                                sql="SELECT IIf(IsNull(MAX(idboleta)), 0, Max(idboleta)) FROM a_boleta"
                    
                                try:
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        correlativo=i[0]+1
                                        
                                except Exception as e:
                                    pass
                                    print(e)
                                    print("Error: "+sql)

                                #INSERTAR CONSUMO DE HORA EN DETALLE
                                sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",2,'CONSUMO DE AGUA POR HORA',"+str(valor_mes)+",'"+str(valor_consumo)+"')"
                                print(sql)
                                try:    
                                    cursor.execute(sql)
                                    cursor.commit()
                                    print("Se ingreso en detalle...")

                                except Exception as a:
                                    print(a)      
                                    print("Error: "+sql)    

                                #INSERTAR CONVENIO A BOLETA           
                                sqlCONVENIO="SELECT A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA,A_DET_CONVENIO.ID FROM (A_CONVENIO INNER JOIN A_COBROS ON A_CONVENIO.TIPO_CONVENIO = A_COBROS.ID) INNER JOIN A_DET_CONVENIO ON A_CONVENIO.ID = A_DET_CONVENIO.ID_CONVENIO WHERE (((A_CONVENIO.ID_PARCELERO)="+str(id_)+") and A_DET_CONVENIO.ANO="+str(ano)+" AND A_DET_CONVENIO.MES="+str(mesnum)+") GROUP BY A_COBROS.ID, A_COBROS.DESCRIPCION, A_DET_CONVENIO.FECHA_PROPUESTA, A_DET_CONVENIO.NRO_CUOTA, A_DET_CONVENIO.VALOR_CUOTA ,A_DET_CONVENIO.ID"
                                print("sql convenio : " + sqlCONVENIO)
                                try:
                                    cursor.execute(sqlCONVENIO) 

                                    for i in cursor.fetchall():
                                        codigo=i[0]
                                        descripcion=i[1]
                                        descripcion2=i[2]
                                        valor=i[3]
                                        total_a_pagar=total_a_pagar+valor
                                        idconvenio=i[4]
                                        valor_mes=valor_mes+valor

                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+","+str(codigo)+",'"+str(descripcion)+"',"+str(valor)+",'"+str(descripcion2)+"')"
                                        
                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                            print("Insertar detalle de convenio...")

                                            #ACTUALIZAR BOLETA EN CONVENIO
                                            sql="UPDATE A_DET_CONVENIO SET ID_BOLETA="+str(correlativo)+" WHERE ID="+str(idconvenio)
                                            print(sql)
                                            try:
                                                cursor.execute(sql)
                                                cursor.commit()
                                            except Exception as a:
                                                print("Error "+str(a)+" en el sql: " + sql)
                                                
                                        except Exception as a:
                                            print(a)
                                            print("Error: "+sql)
                                        
                                except Exception as a:
                                    print(a)
                                    print("Error: "+sql)

                                # Buscar saldo anterior
                                
                                sql="SELECT A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO FROM A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA GROUP BY A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_BOLETA.PERIODO, A_BOLETA.ANO, A_BOLETA.ID_PARCELERO, A_DET_BOLETA.CODIGO HAVING (((A_BOLETA.PERIODO)<"+str(mesnum)+") AND ((A_BOLETA.ANO)="+str(ano)+") AND ((A_BOLETA.ID_PARCELERO)="+str(id_)+") AND ((A_DET_BOLETA.CODIGO)<>5));"
                                print("sql saldo anterior: " + sql)
                                totalsaldo=0

                                try:    
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        totalsaldo=totalsaldo+int(i[1])-int(i[2])
                                    
                                    if totalsaldo>0:
                                        #Insertar saldo anterior
                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",5,'SALDO ANTERIOR',"+str(totalsaldo)+",'')"
                                        
                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                        except Exception as a:
                                            print(a)
                                            print(sql)

                                except Exception as a:
                                    print(a)
                                    print("Error: "+sql)
                                
                                #BUSCAR MENSAJE PARA LOS AVISOS
                                sql="SELECT DESCRIPCION FROM A_MENSAJE"
                                
                                try:
                                    cursor.execute(sql)

                                    for i in cursor.fetchall():
                                        mensaje=i[0]
                                except Exception as a:
                                    print(a)

                                
                                total2=total_a_pagar+totalsaldo
                                saldototal=0
                                existesaldos=0

                                # BUSCAR SALDO A FAVOR
                                sql="SELECT A_SALDOS.MONTO, A_SALDOS.SALDO, A_SALDOS.ID FROM A_SALDOS WHERE (((A_SALDOS.ID_PARCELERO)="+str(id_)+"))" 
                                print(sql)
                                try:
                                    cursor.execute(sql)
                                    for i in cursor.fetchall():
                                        saldo=i[1]
                                        idsaldo=i[2]

                                        if saldo!=0:
                                            print(" total : " + str(total2) + " saldo : " + str(saldo))
                                            existesaldos=1

                                            print("Total menos saldo : " + str(total2))
    
                                            if total2>=saldo:
                                                sql="UPDATE A_SALDOS SET SALDO=0 WHERE ID="+str(idsaldo)

                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                    saldototal=saldototal+saldo
                                                except Exception as a:
                                                    print(a)

                                            elif total2>=0:

                                                sql="UPDATE A_SALDOS SET SALDO="+str(int(saldo)-int(total2))+" WHERE ID="+str(idsaldo)
                                                
                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                    saldototal=saldototal+saldo-(int(saldo)-int(total2))
                                                except Exception as a:
                                                    print(a)
                                            
                                            total2=total2-saldo
                                    
                                    if existesaldos==1:
                                        #Insertar saldo a favor
                                        sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",6,'SALDO A FAVOR',-"+str(saldototal)+",'')"
                                        print("sql saldo a favor detalle: " + sql)

                                        try:
                                            cursor.execute(sql)
                                            cursor.commit()
                                        except Exception as a:
                                            print(a)
                                            print(sql)

                                except Exception as a:
                                    print(a)
                                
                                intereses=0

                                #BUSCAR INTERESES POR NO PAGO
                                if totalsaldo>0:

                                    sql="SELECT MULTAXNOPAGO FROM A_SOCIOS WHERE ID="+str(id_)
                                    try:
                                        cursor.execute(sql)
                                        for i in cursor.fetchall():
                                            nopago=i[0]

                                            if nopago==1:
                                                intereses=round(total_a_pagar*0.02)
                                                #INTERESES
                                                sql="INSERT INTO A_DET_BOLETA(ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR,DESCRIPCION2) VALUES("+str(buscarCorrelativoBoleta())+","+str(correlativo)+",3,'INTERESES',"+str(intereses)+",'')"
                                                        
                                                try:
                                                    cursor.execute(sql)
                                                    cursor.commit()
                                                except Exception as a:
                                                    print(a)
                                                    print(sql)
                                    except Exception as a:
                                        print(a)
                                
                                
                                totalapagarB=total_a_pagar+totalsaldo-saldototal+intereses
                                valor_mes=total_a_pagar+intereses
                                                                
                                #Insertar en A_Boleta
                                sql="INSERT INTO A_BOLETA(RUT,IDBOLETA,ID_PARCELERO,SECTOR_CORRELATIVO,MES,PERIODO,ANO,MENSAJE,FECHA_EMISION,FECHA_VENCIMIENTO,TOTALBOLETA,TOTAL_A_PAGAR,RUTA,DIRECCION,VALOR_CONSUMO,AFAVOR,TIPODOCTO) VALUES('"+str(rut)+"',"+str(correlativo)+","+str(id_)+","+str(sector)+",'"+mes+"',"+str(mesnum)+","+ano+",'"+mensaje+"','"+fecha_emision+"','"+fecha_vencimiento+"',"+str(valor_mes)+","+str(totalapagarB)+","+str(ruta)+",'"+str(direccion)+"','"+str(valor_consumo)+"',"+str(afavor)+","+str(tipodocto)+")"
                                print(sql)
                                try:
                                    cursor.execute(sql)
                                    cursor.commit()
                                    print("Guardadoo correctamete.")  
                                    mensaje="Se genero satisfactoriamente."
                                    total_a_pagar=0

                                except Exception as a:
                                    print(a)
                                    print("Error: "+sql)
                            else:
                                print("Boleta ya esta generada en el mes y año de facturación. Medidor: "+ str(id_))
                                mensaje="Boleta ya esta generada en el mes y año de facturación."
                                
                    except Exception as a:
                        print(a)
                        print("Error: "+sql)
                        mensaje="Faltan consumos por ingresar."

                
            else:
                mensaje="Favor debe cerrar periodo anterior antes de continuar."
                print("El cierre no esta realizado")

        elif deseahacer=='1':

            print("Imprimiendo...")

            MES=request.POST['mes']
            ANO=request.POST['ano']
            lista=[]
            listadetalle=[]
            saldo=0
            boleta=""
            
            
            sql="SELECT A_BOLETA.IDBOLETA, A_BOLETA.FECHA_VENCIMIENTO, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SECTOR.NOMBRE, A_BOLETA.VALOR_CONSUMO, A_BOLETA.MES, A_BOLETA.ANO, A_BOLETA.FECHA_EMISION, A_BOLETA.TOTALBOLETA, A_BOLETA.TOTAL_A_PAGAR FROM (A_BOLETA INNER JOIN A_SOCIOS ON A_BOLETA.ID_PARCELERO = A_SOCIOS.ID) INNER JOIN A_SECTOR ON A_SOCIOS.ID_SECTOR = A_SECTOR.ID WHERE (((A_BOLETA.MES)='"+MES+"') AND ((A_BOLETA.ANO)="+ANO+"));"
            print(sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    boleta=i[0]

                    sqldetalle="SELECT A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.DESCRIPCION2, A_DET_BOLETA.PAGADO, A_DET_BOLETA.FECHA_PAGO , A_DET_BOLETA.IDBOLETA FROM A_DET_BOLETA WHERE (((A_DET_BOLETA.IDBOLETA)="+str(boleta)+"));"
                    print(sqldetalle)

                    try:
                        cursor.execute(sqldetalle)
                        for j in cursor.fetchall():
                            if j[1]!='SALDO ANTERIOR':
                                listadetalle.append({'boleta':j[6],'codigo':j[0],'des':j[1],'valor':j[2],'desdetalle':j[3]})
                            else:
                                saldo=saldo+int(j[2])
                    except Exception as a:
                        print(a)
                    
                    lista.append({
                        'boleta':i[0],
                        'vencimiento':i[1],
                        'nombre':i[2]+" "+i[3],
                        'direccion':i[4],
                        'sector':i[5],
                        'valor':i[6],
                        'mes':i[7],
                        'ano':i[8],
                        'emision':i[9],
                        'totalboleta':i[10],
                        'totalpagar':i[11],
                        'saldo':saldo
                    })

                    saldo=0

                data={
                    'asociacion':viewName(),
                    'boleta':boleta,
                    'lista':lista,
                    'listadetalle':listadetalle,
                    'mensaje':mensaje
                }

                pdf = render_to_pdf('reportes/aviso.html', data)

                return HttpResponse(pdf, content_type='application/pdf')
                        
            except Exception as a:
                print(a)
                mensaje="No se encontraron datos para imprimir"

        else:

            if modoopcion=='1':
                print("Selecciono parcelero (eliminar)")

                existePagos=buscarPagos(id_)

                if existePagos==0:
                    
                    id_=request.POST['id_'].strip()
                    MES=request.POST['mes']
                    ANO=request.POST['ano']

                    sql="SELECT IDBOLETA FROM A_BOLETA WHERE VIGENTE=0 AND ID_PARCELERO="+str(id_)+" AND (A_BOLETA.MES)='"+mes+"' AND (A_BOLETA.ANO)="+ano
                    print(sql) 

                    try:
                        cursor.execute(sql)
                        for i in cursor.fetchall():
                            nroboleta=i[0]

                            sql="DELETE FROM A_DET_BOLETA WHERE IDBOLETA="+str(nroboleta)
                            print(sql)

                            try:
                                cursor.execute(sql)
                                cursor.commit()
                            except Exception as a:
                                print(a)
                                print("Error _ " + sql)
                    except Exception as a:
                            print(a)
                        
                    sql="DELETE FROM A_BOLETA WHERE VIGENTE=0 AND ID_PARCELERO="+str(id_)+" AND (A_BOLETA.MES)='"+mes+"' AND (A_BOLETA.ANO)="+ano+""
                    print(sql)

                    try:
                        cursor.execute(sql)
                        cursor.commit()
                        mensaje="Se elimino correctamente."
                    except Exception as a:
                        print(a)
                    
                else:
                    mensaje="No puede eliminar boleta, tiene pagos ingresados. Debe eliminar pago antes de eliminar boleta."

            else:
                print("eliminar por sector")
                MES=request.POST['mes']
                ANO=request.POST['ano']
                existe=0

                #BUSCAR SOCIOS CON BOLETAS VIGENTES
                sql="SELECT A_BOLETA.ID_PARCELERO, A_BOLETA.VIGENTE, A_BOLETA.MES, A_BOLETA.ANO FROM A_BOLETA WHERE (((A_BOLETA.VIGENTE)=0) AND ((A_BOLETA.MES)='"+mes+"') AND ((A_BOLETA.ANO)="+ano+"));"
                print(sql)
                
                try:
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        id_=i[0]
                        existePagos=buscarPagos(id_)

                        if existePagos==0:
                            existe=existe+1
                        else:
                            mensaje="No puede eliminar boleta, hay pagos ingresados. Debe eliminar pago antes de eliminar boletas."
                            break

                except Exception as a:
                    print(a)

                if existe>0:
                    sql="SELECT IDBOLETA FROM A_BOLETA WHERE VIGENTE=0"
                    try:
                        cursor.execute(sql)
                        for i in cursor.fetchall():
                            nroboleta=i[0]

                            sql="DELETE FROM A_DET_BOLETA WHERE IDBOLETA="+str(nroboleta)
                            print(sql)
                            try:
                                cursor.execute(sql)
                                cursor.commit()
                            except Exception as a:
                                print(a)
                                print("Error _ " + sql)
                    except Exception as a:
                        print(a)
                                
                    sql="DELETE FROM A_BOLETA WHERE VIGENTE=0"

                    try:
                        cursor.execute(sql)
                        cursor.commit()
                        mensaje="Se elimino correctamente"
                    except Exception as a:
                        print(a)

    data={
        'asociacion':viewName(),
        'ano':str(now.year),
        'mes':mes,
        'boleta':numeroBoleta(),
        'emision':str(now.day)+"/"+str(now.month)+"/"+str(now.year),
        'vencimiento':str(now.day+20)+"/"+str(now.month)+"/"+str(now.year),
        'all_socios':buscarporNombre,
        'lista_sector':buscarSector(),
        'mensaje':mensaje,
        'cierre':botoncierre
    }
    return render(request, 'procesos/boletas.html', data)

def correlativoFactura():

    #sql="SELECT COUNT(ID) FROM A_ABONO"
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_factura"
    correlativo=1

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)

    return correlativo

def buscardatos():

    #FACTURA LIBRE PARA TODOS ???

    sql="SELECT A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_FACTURA.ID, A_FACTURA.FECHA_CANCELACION, A_FACTURA.ANULAR FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID;"
    print(sql)
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            if i[5]==1:
                estado='ANULADA'
            else:
                estado='VIGENTE'
            lista.append({'rut':i[0],'nombres':i[1]+" "+i[2],'id':i[3],'fecha':i[4],'estado':estado})
    except Exception as a:
        print(a)

    return lista

def historialFactura(request):

    if request.method=='POST' and 'ver' in request.POST:

        nro=request.POST['nro']
        nombres=""
        tipo=""
        numero=""
        nombres=""
        direccion=""
        rut=""
        detalle=""
        monto=""
        telefono=""
        giro=""

        sql="SELECT A_FACTURA.ID, A_SOCIOS.ID, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SOCIOS.RUT, A_FACTURA.DETALLE, A_FACTURA.MONTO, A_FACTURA.TELEFONO, A_FACTURA.GIRO FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID WHERE A_FACTURA.ID="+nro+";"
        print(sql)
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                numero=i[0]
                nombres=i[2]+" "+i[3]
                direccion=i[4]
                rut=i[5]
                detalle=i[6]
                monto=i[7]
                telefono=i[8]
                giro=i[9]

            data={
                'numero':numero,
                'nombres':nombres,
                'direccion':direccion,
                'rut':rut,
                'detalle':detalle,
                'monto':monto,
                'telefono':telefono,
                'giro':giro
            }

            #falta crear reporte de factura
            try:
                pdf = render_to_pdf('reportes/factura.html', data)
                return HttpResponse(pdf, content_type='application/pdf')
            except Exception as a:
                print(a)
        except Exception as a:
            print(a)

    if request.method=='POST' and 'eliminar' in request.POST:

        nro=request.POST['nro']

        sql="DELETE FROM A_ORDENTRABAJO WHERE ID="+nro

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
             

    data={
        'lista':buscardatos()
    }

    return render(request, 'procesos/factura_historial.html', data)

def viewFactura(request):

    now = datetime.datetime.now()
    mensaje=""
    mes=""
    datos=[]
    fecha_actual=""
    id_=""
    direccion=""
    telefono=""
    giro=""
    detalle=""
    monto=""
    anular=""
    detalle=""
    monto=""
    nrofactura=correlativoFactura()
    fechapago=0
    mensajeanular=""
    nombres=""

    if request.method=='POST' and 'pagar' in request.POST:

        nrofactura=request.POST['nro2']

        if nrofactura != None :

            sql="UPDATE A_FACTURA SET FECHA_CANCELACION='"+now.date().strftime('%d-%m-%Y')+"' WHERE ID="+nrofactura
            print(sql)

            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Factura fue cancelada con exito"
                nrofactura=correlativoFactura()
            except Exception as a:
                print(a)

    if request.method=='POST' and 'eliminar' in request.POST:

        nrofactura=request.POST['nro2']

        if nrofactura != None :

            sql="DELETE FROM A_FACTURA WHERE ID="+nrofactura+";"
            print(sql)

            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Factura fue eliminada"
                nrofactura=correlativoFactura()
            except Exception as a:
                print(a)

    if request.method=='POST' and 'buscar' in request.POST:
        
        nrofactura=request.POST['nrofactura']

        sql="SELECT ANULAR FROM A_FACTURA WHERE ID="+nrofactura
        
        try:
            cursor.execute(sql)
            
            for i in cursor.fetchall():
                print(i[0])
                if str(i[0]).strip()=='1':
                    mensajeanular="Factura esta anulada"
        except Exception as a:
            print(a)

        sql="SELECT A_FACTURA.*,A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS FROM A_FACTURA INNER JOIN A_SOCIOS ON A_FACTURA.ID_SOCIO = A_SOCIOS.ID WHERE (((A_FACTURA.[ID])="+nrofactura+"));"
        print(sql)
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                nrofactura=i[0]
                fecha_actual=i[1]
                id_=i[2]
                direccion=i[3]
                telefono=i[4]
                giro=i[5]
                detalle=i[7]
                monto=i[8]
                anular=i[9]
                fechapago=i[6]
                nombres=str(i[13])+" "+str(i[14])

        except Exception as a:
            print(a)

    if request.method=='POST' and 'anular' in request.POST:

        nrofactura=request.POST['nro']
        print("Numero pocos parametros "+str(nrofactura))

        if nrofactura != None :

            sql="UPDATE A_FACTURA SET ANULAR=1 WHERE ID="+nrofactura

            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Factura fue anulada con exito"
                nrofactura=correlativoFactura()
            except Exception as a:
                print(a)
        
        else:
            mensaje="No se pudo anular factura."

    if request.method=='POST' and 'guardar' in request.POST:

        nrofactura=request.POST['nro2']
        emision=request.POST['fecha_actual']
        id_=request.POST['id_'].strip()
        direccion=request.POST['direccion']
        telefono=request.POST['telefono']
        giro=request.POST['giro']
        detalle=request.POST['detalle']
        total=request.POST['total']
        ano=emision[len(emision)-4:len(emision)]
        periodo=emision[3:len(emision)-5]

        if periodo=='01':
            mes='Enero'
        if periodo=='02':
            mes='Febrero'
        if periodo=='03':
            mes='Marzo'
        if periodo=='04':
            mes='Abril'
        if periodo=='05':
            mes='Mayo'
        if periodo=='06':
            mes='Junio'
        if periodo=='07':
            mes='Julio'
        if periodo=='08':
            mes='Agosto'
        if periodo=='09':
            mes='Septiembre'
        if periodo=='10':
            mes='Octubre'
        if periodo=='11':
            mes='Noviembre'
        if periodo=='12':
            mes='Diciembre'

        sql="SELECT * FROM A_FACTURA WHERE ID="+nrofactura

        existe=0
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                existe=1
        except Exception as a:
            print(a)

        if existe==0:

            sql="INSERT INTO A_FACTURA(ID,FECHA_EMISION,ID_SOCIO,DIRECCION,TELEFONO,MONTO,MES,ANO,PERIODO,GIRO,ANULAR,DETALLE) VALUES("+str(nrofactura)+",'"+str(emision)+"',"+str(id_)+",'"+str(direccion)+"',"+str(telefono)+","+str(total)+",'"+str(mes)+"',"+str(ano)+","+str(periodo)+",'"+str(giro)+"',0,'"+str(detalle)+"')"
            print(sql)

            try:
                cursor.execute(sql)
                cursor.commit()
                nrofactura=correlativoFactura()
                mensaje="Se guardo correctamente"
                fecha_actual=""
                id_=""
                direccion=""
                telefono=""
                giro=""
                detalle=""
                monto=""
                anular=""
                fechapago=""

            except Exception as a:
                print(a)
        else:
            mensaje="Numero factura ya esta ingresada."

    data={
        'mensajeanular':mensajeanular,
        'fechapago':fechapago,
        'fecha_actual':fecha_actual,
        'id_':id_,
        'direccion':direccion,
        'telefono':telefono,
        'giro':giro,
        'detalle':detalle,
        'monto':monto,
        'anular':anular,
        'nrofactura':nrofactura,
        'all_socios':buscarporNombre,
        'fecha_actual': now.date().strftime('%d-%m-%Y'), 
        'mensaje':mensaje,
        'nombres':nombres
    }

    return render(request, 'procesos/factura.html', data)

def buscarAbono():

    #sql="SELECT COUNT(ID) FROM A_ABONO"
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_abono"
    correlativo=1

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)

    return correlativo

def buscarDetAbono():

    #sql="SELECT COUNT(ID) FROM A_DET_ABONO"
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_det_abono"
    correlativodet=1

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativodet=i[0]+1
    except Exception as a:
        print(a)

    return correlativodet

def imprimiendoAbono(request,id_):
    
    abono=id_
    nombre="abono1"
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
    
    data={
            'lista':lista,
            'datos':viewAsociacion(),
            'nombre':nombres,
            'direccion':direccion,
            'numeroabono':numeroabono,
            'numeroboleta':numeroboleta,
            'numerosocio':numerosocio,
            'montopagado':montopagado,
            'fechapago':fechapago,
            'deuda':deuda,
        }

    print("exportandooo")
    pdf = render_to_pdf('reportes/19.abono1.html', data)
    return HttpResponse(pdf, content_type='application/pdf')
  
def viewPagos(request):
    now = datetime.datetime.now()
    lista=[]
    rut=0
    nombres=" "
    direccion=0
    totalboleta=0
    totalpagar=0
    vencimiento=0
    boleta=0
    mesfac=""
    anofac=""

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

    if request.method=='POST' and 'abonar' in request.POST:

        print("Abonando....")
        
        inicial=0
        id_=request.POST['id_']

        if id_=='':
            data={
                'dia': (now.day), 
                'mes': (now.month), 
                'año': (now.year),
                'all_socios':buscarporNombre,
                'fecha_actual': str(now.day)+"/"+str(now.month)+"/"+str(now.year),
                'mensaje':'Debe buscar por parcelero antes de abonar'
            }
            
            return render(request, 'procesos/pagos.html', data)

        total=request.POST['total']
        fechaabono=request.POST['fechaabono']
        ano=fechaabono[len(fechaabono)-4:len(fechaabono)]
        periodo=fechaabono[3:len(fechaabono)-5]
        dia=fechaabono[0:len(fechaabono)-8]
        boleta=request.POST['nroboleta']

        codigo=request.POST.getlist('codigo')
        desc=request.POST.getlist('desc')
        valorpagos=request.POST.getlist('abono')
        nroaviso=request.POST.getlist('idaviso')
        nrodet=request.POST.getlist('idboleta')
        fecha=request.POST.getlist('fecha')
        opcion3=request.POST.getlist('toggle-switch')

        totalboleta=request.POST['totalboleta']

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

        for i in opcion3:
            formapago=i[0]

        listacodigo=[]
        listadesc=[]
        listaabono=[]
        listaaviso=[]
        listafecha=[]
        listadet=[]

        for i in nrodet:
            listadet.append(i)

        for i in codigo:
            listacodigo.append(i)
        
        for i in desc:
            listadesc.append(i)

        for i in valorpagos:
            listaabono.append(i)

        for i in nroaviso:
            listaaviso.append(i)
        
        for i in fecha:
            listafecha.append(i)

        numeroabono=buscarAbono()

        sql="INSERT INTO A_ABONO(DEUDA,ID,IDBOLETA,ID_PARCELERO,MONTO,TIPOPAGO,OBSERVACION,FECHA,MES,PERIODO,ANO) VALUES("+str(int(totalboleta)-int(total))+","+str(numeroabono)+","+str(boleta)+","+str(id_)+","+str(total)+","+str(formapago)+",'','"+fechaabono+"','"+str(mes)+"',"+str(periodo)+","+str(ano)+")"
        print(sql)
        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Ingresado Correctamente"
        except Exception as a:
            print(a)
            print("Error : " + sql)

        while inicial<len(listaaviso):

            if str(listaabono[inicial])!=" " and str(listaabono[inicial])!="":
                sql="INSERT INTO A_DET_ABONO(ID,ABONO_ID,IDBOLETA,CODIGO,DESCRIPCION,VALOR) VALUES("+str(buscarDetAbono())+","+str(numeroabono)+","+str(listaaviso[inicial])+","+str(listacodigo[inicial])+",'"+str(listadesc[inicial])+"',"+str(listaabono[inicial])+")"
                try:
                    cursor.execute(sql)
                    cursor.commit()
                except Exception as a:
                    print(a)
                    print("Error : " + sql)

                sql="SELECT A_DET_BOLETA.PAGADO FROM A_DET_BOLETA WHERE ID="+str(listaaviso[inicial])
                try:
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        pagado=i[0]
                except Exception as a:
                    print(a)
                    print("Error : " + sql)
                    
                sql="UPDATE A_DET_BOLETA SET PAGADO="+str(int(listaabono[inicial])+int(pagado))+", FECHA_PAGO='"+fechaabono+"' WHERE ID="+str(listadet[inicial])
                print(sql)
                try:
                    cursor.execute(sql)
                    cursor.commit()
                except Exception as a:
                    print(a)
                    print("Error : " + sql)
                
                if listacodigo[inicial]!=3 and listacodigo[inicial]!=5 and listacodigo[inicial]!=2:
                    print("Se debe actualizar convenio...")
                    sql="UPDATE A_CONVENIO INNER JOIN A_DET_CONVENIO ON A_CONVENIO.ID = A_DET_CONVENIO.ID_CONVENIO SET TOTAL_PAGADO="+str(listaabono[inicial])+",FECHA_PAGO="+fechaabono+" WHERE (((A_CONVENIO.TIPO_CONVENIO)="+str(listacodigo[inicial])+") AND ((A_DET_CONVENIO.ID_BOLETA)="+str(listaaviso[inicial])+"));"
                    try:
                        cursor.execute(sql)
                        cursor.commit()
                    except Exception as a:
                        print(a)
            inicial=inicial+1
        
        data={
            'numero':numeroabono
        }

        return render(request, 'procesos/confirmarpago.html', data)
        

    if request.method=='POST' and 'buscar' in request.POST:

        numero=request.POST['numero'].strip()
        listadetalle=[]
        totalpagar=0
        emision=""
        totalpagado=0

        abono=buscarNumeroAbono()
        print("numero abono " + str(abono))

        sql="SELECT A_BOLETA.ID_PARCELERO, A_SOCIOS.RUT, A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_BOLETA.TOTALBOLETA, A_BOLETA.TOTAL_A_PAGAR,A_BOLETA.FECHA_VENCIMIENTO, A_BOLETA.IDBOLETA,A_BOLETA.FECHA_EMISION, A_BOLETA.ANO, A_BOLETA.MES FROM A_SOCIOS INNER JOIN A_BOLETA ON A_SOCIOS.ID = A_BOLETA.ID_PARCELERO WHERE (((A_BOLETA.ID_PARCELERO)="+str(numero)+")  AND ((A_BOLETA.VIGENTE)=0));"
        print("Buscar: " + sql)
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                numero=i[0]
                rut=i[1]
                nombres=i[2]+" "+i[3]
                direccion=i[4]
                totalboleta=i[5]
                totalpagar=i[6]
                vencimiento=i[7]
                boleta=i[8]
                emision=i[9]
                anofac=i[10]
                mesfac=i[11]
            
            #sql="SELECT Sum(A_DET_BOLETA.PAGADO) AS SumaDePAGADO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA GROUP BY A_BOLETA.ID_PARCELERO HAVING (((A_BOLETA.ID_PARCELERO)="+str(numero)+"));"
            #SELECT A_BOLETA.TOTAL_A_PAGAR, Sum(A_DET_BOLETA.PAGADO) AS SumaDePAGADO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA GROUP BY A_BOLETA.ID_PARCELERO, A_BOLETA.VIGENTE, A_BOLETA.TOTAL_A_PAGAR HAVING (((A_BOLETA.ID_PARCELERO)="+str(numero)+"));"
            sql="SELECT Sum(A_DET_BOLETA.VALOR) AS SumaDeVALOR, Sum(A_DET_BOLETA.PAGADO) AS SumaDePAGADO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.CODIGO)<>5)) GROUP BY A_BOLETA.ID_PARCELERO HAVING (((A_BOLETA.ID_PARCELERO)="+str(numero)+"));"
            print("sql pagado: " + sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    valor=round(i[0])
                    pagado=round(i[1])
                    totalpagado=valor-pagado
            except Exception as a:
                print(a)
                print(sql)

            sql="SELECT A_DET_BOLETA.ID, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.DESCRIPCION2, A_DET_BOLETA.PAGADO, A_DET_BOLETA.FECHA_PAGO, A_BOLETA.PERIODO, A_BOLETA.ANO FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE ((A_DET_BOLETA.IDBOLETA)="+str(boleta)+");"
            print("sql principal :"+sql)
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    lista.append({'id':i[0],'codigo':i[1],'desc':i[2],'can':str(i[4]),'valor':i[3],'fecha':str(i[7])+"/"+str(i[8])})
                    """
                    if int(i[3])==int(i[5]):
                        print("Esta pagado.")
                    else:
                        if i[2]!='SALDO ANTERIOR':
                            listadetalle.append({'id':i[0],'codigo':i[1],'desc':i[2],'can':str(i[4]),'valor':int(i[3])-int(i[5]),'fecha':str(i[7])+"/"+str(i[8])})
                    """
            except Exception as a:
                print(a)
                print("Error :" + sql)
            
            
            sql="SELECT A_DET_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.DESCRIPCION2, A_DET_BOLETA.PAGADO, A_DET_BOLETA.FECHA_PAGO, A_BOLETA.PERIODO, A_BOLETA.ANO,A_DET_BOLETA.ID FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(numero)+") AND ((A_DET_BOLETA.CODIGO)<>5));"
            print("sql de detalle sin saldo anterior... : "+ sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    if int(i[3])==int(i[5]):
                        print("Esta ok.")
                    else:
                        listadetalle.append({'id':i[0],'codigo':i[1],'desc':i[2],'can':str(i[4]),'valor':int(i[3])-int(i[5]),'fecha':str(i[7])+"/"+str(i[8]),'idboleta':i[9]})
            except Exception as a:
                print(a)
                print(sql)


            
            sql="SELECT A_DET_BOLETA.ID, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.DESCRIPCION2, A_DET_BOLETA.PAGADO, A_DET_BOLETA.FECHA_PAGO , A_BOLETA.PERIODO, A_BOLETA.ANO FROM A_BOLETA INNER JOIN A_DET_BOLETA ON A_BOLETA.IDBOLETA = A_DET_BOLETA.IDBOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(numero)+") AND ((A_BOLETA.VIGENTE)<>0) AND ((A_DET_BOLETA.CODIGO)<>1) AND ((A_DET_BOLETA.CODIGO)<>5));"
            totalsaldo=0
            print("sql saldo anterior : " + sql)

            try:    
                cursor.execute(sql)

                for i in cursor.fetchall():
                    if int(i[3])==int(i[5]):
                        print("Esta pagado.")
                    else:
                        print("Parece q a ca se vuelve a repetir")
                        #totalsaldo=totalsaldo+int(i[3])-int(i[5])
                        #listadetalle.append({'id':i[0],'codigo':i[1],'desc':str(i[2]),'can':str(i[4]),'valor':i[3],'fecha':str(i[7])+"/"+str(i[8])})
                
            except Exception as a:
                print(a)
                print("Error :" + sql)

            data={
                'dia': (now.day), 
                'mes': (now.month), 
                'ano': (now.year),
                'fechafactu': 'Fecha de facturación mes de '+str(mesfac)+' del '+str(anofac),
                'all_socios':buscarporNombre,
                'fecha_actual': now.date().strftime('%d-%m-%Y'), 
                'rut':rut,
                'nombres':nombres,
                'direccion':direccion,
                'totalboleta':totalboleta,
                'totalpagar':totalpagar,
                'emision':emision,
                'vencimiento':vencimiento,
                'boleta':boleta,
                'lista':lista,
                'numero':numero,
                'listadetalle':listadetalle,
                'abono':abono,
                'pagado':totalpagado,
                'numero':numero
            }
                
            return render(request, 'procesos/pagos.html', data)
        except Exception as a:
            print(a)
            print("Error :" + sql)

    data={
        'dia': (now.day), 
        'mes': (now.month), 
        'año': (now.year),
        'all_socios':buscarporNombre,
        'fecha_actual': str(now.day)+"/"+str(now.month)+"/"+str(now.year),
    }
    
    return render(request, 'procesos/pagos.html', data)

def pdfhistorialcliente(request,id_,ano_):

    listames=[]
    lista=[]
    nombres=""
    direccion=""
    rut=""

    listames.append({'mes':'Enero'})
    listames.append({'mes':'Febrero'})
    listames.append({'mes':'Marzo'})
    listames.append({'mes':'Abril'})
    listames.append({'mes':'Mayo'})
    listames.append({'mes':'Junio'})
    listames.append({'mes':'Julio'})
    listames.append({'mes':'Agosto'})
    listames.append({'mes':'Septiembre'})
    listames.append({'mes':'Octubre'})
    listames.append({'mes':'Noviembre'})
    listames.append({'mes':'Diciembre'})

    print("buscando...")

    socio=id_
    ano=ano_
    boleta=0
    pagado=0
    estado=""
    otros=0
    horas=0
    consumo=0
    afavor=0
    intereses=0
    saldo=0
    fechapago=""
    multa=""

    sql="SELECT A_BOLETA.IDBOLETA, A_BOLETA.PERIODO, A_BOLETA.MES, A_BOLETA.ANO, A_BOLETA.TOTAL_A_PAGAR, A_BOLETA.ID_PARCELERO, A_BOLETA.VIGENTE FROM A_BOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(socio)+") AND ((A_BOLETA.ANO)="+ano+"));"
        
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            mesboleta=str(i[2])
            total=i[4]
            mesb=i[2]

            if i[6]==0:
                estado="VIGENTE"
            else:
                estado="NO VIGENTE"
                    
            boleta=i[0]

            sql="SELECT A_DET_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_DET_BOLETA.DESCRIPCION2, A_BOLETA.MES FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.IDBOLETA)="+str(boleta)+"));"
                
            try:
                cursor.execute(sql)
                for j in cursor.fetchall():

                    if j[2]=='CONSUMO DE AGUA POR HORA':
                        consumo=j[3]
                        horas=j[5]
                    elif j[2]=='MULTA POR INASISTENCIA':
                        multa=j[3]
                    elif j[2]=='SALDO ANTERIOR':
                        saldo=j[3]
                    elif j[2]=='SALDO A FAVOR':
                        afavor=j[3]
                    elif j[2]=='INTERESES':
                        intereses=j[3]
                    else:
                        otros=j[3]  
                        
            except Exception as a:
                print(a)
                
            sql="SELECT Sum(A_DET_BOLETA.PAGADO) AS SumaDePAGADO,Sum(A_DET_BOLETA.VALOR) FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.CODIGO)<>5)) HAVING (((A_BOLETA.IDBOLETA)<="+str(boleta)+"));"
            print(sql)
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    if row[1]-row[0]==0:
                        pagado=total
                    else:
                        pagado=int(row[1]-row[0])
            except Exception as a:
                print(a)
            
            sql="SELECT A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA FROM A_ABONO GROUP BY A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA HAVING (((A_ABONO.IDBOLETA)="+str(boleta)+"));"

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechapago=fechapago+" A: "+str(i[0])+" F: "+str(i[1])+" $"+str(i[2])
            except Exception as a:
                print(a)

            lista.append({'mes':mesb,'horas':horas,'fechapago':fechapago,'vconsumo':consumo,'deuda':0,'otras':otros,'afavor':afavor,'saldo':saldo,'multas':multa,'total':total,'cancelado':pagado,'abono':'0','boleta':boleta,'estado':estado,'intereses':intereses})

    except Exception as a:
        print(a)

    sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SOCIOS.RUT FROM A_SOCIOS WHERE (((A_SOCIOS.ID)="+socio+"));"
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            nombres=i[0]+" "+i[1]
            direccion=i[2]
            rut=i[3]
    except Exception as a:
        print(a)

    data={
        'mes':listames,
        'lista':lista,
        'all_socios':buscarporNombre(),
        'nombres':nombres,
        'direccion':direccion,
        'rut':rut,
        'ano':ano
    }

    pdf = render_to_pdf('reportes/cuenta_individual.html', data)
    return HttpResponse(pdf, content_type='application/pdf')

def errorhistorial(request):
    return HttpResponse("Error: vuelva antrás, debe seleccionar parcelero, antes de dar clic en consultar.")

def historialcliente(request):

    listames=[]
    lista=[]
    nombres=""
    direccion=""
    rut=""
    ano=""
    socio=""

    listames.append({'mes':'Enero'})
    listames.append({'mes':'Febrero'})
    listames.append({'mes':'Marzo'})
    listames.append({'mes':'Abril'})
    listames.append({'mes':'Mayo'})
    listames.append({'mes':'Junio'})
    listames.append({'mes':'Julio'})
    listames.append({'mes':'Agosto'})
    listames.append({'mes':'Septiembre'})
    listames.append({'mes':'Octubre'})
    listames.append({'mes':'Noviembre'})
    listames.append({'mes':'Diciembre'})


    if request.method=='POST' and 'buscar' in request.POST:
        print("buscando...")

        socio=request.POST['identi']
        ano=request.POST['ano']
        boleta=0
        pagado=0
        estado=""
        otros=""
        horas=""
        consumo=""
        afavor=""
        intereses=""
        saldo=""
        fechapago=""
        multa=""

        sql="SELECT A_BOLETA.IDBOLETA, A_BOLETA.PERIODO, A_BOLETA.MES, A_BOLETA.ANO, A_BOLETA.TOTAL_A_PAGAR, A_BOLETA.ID_PARCELERO, A_BOLETA.VIGENTE FROM A_BOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(socio)+") AND ((A_BOLETA.ANO)="+ano+"));"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                mesboleta=str(i[2])
                total=i[4]
                mesb=i[2]

                if i[6]==0:
                    estado="VIGENTE"
                else:
                    estado="NO VIGENTE"
                    
                boleta=i[0]

                sql="SELECT A_DET_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_DET_BOLETA.DESCRIPCION2, A_BOLETA.MES FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.IDBOLETA)="+str(boleta)+"));"
                
                try:
                    cursor.execute(sql)
                    for j in cursor.fetchall():

                        if j[2]=='CONSUMO DE AGUA POR HORA':
                            consumo=j[3]
                            horas=j[5]
                        elif j[2]=='MULTA POR INASISTENCIA':
                            multa=j[3]
                        elif j[2]=='SALDO ANTERIOR':
                            saldo=j[3]
                        elif j[2]=='SALDO A FAVOR':
                            afavor=j[3]
                        elif j[2]=='INTERESES':
                            intereses=j[3]
                        else:
                            otros=j[3]  
                        
                except Exception as a:
                    print(a)
                
                sql="SELECT Sum(A_ABONO.MONTO) AS SumaDeMONTO, A_ABONO.IDBOLETA FROM A_ABONO GROUP BY A_ABONO.IDBOLETA HAVING (((A_ABONO.IDBOLETA)="+str(boleta)+"));"
                try:
                    cursor.execute(sql)
                    for row in cursor.fetchall():
                        if row[0]>0:
                            pagado=round(row[0])
                        else:
                            pagado=0
                except Exception as a:
                    print(a)
                
                sql="SELECT A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA FROM A_ABONO GROUP BY A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA HAVING (((A_ABONO.IDBOLETA)="+str(boleta)+"));"

                try:
                    cursor.execute(sql)
                    for i in cursor.fetchall():
                        fechapago=fechapago+" A: "+str(i[0])+" F: "+str(i[1])+" $"+str(i[2])
                except Exception as a:
                    print(a)

                lista.append({'mes':mesb,'horas':horas,'fechapago':fechapago,'boletas':boleta,'vconsumo':consumo,'deuda':0,'otras':otros,'afavor':afavor,'saldo':saldo,'multas':multa,'total':total,'cancelado':pagado,'abono':'0','boleta':boleta,'estado':estado,'intereses':intereses})
                pagado=0
                fechapago=""
        except Exception as a:
            print(a)

        sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SOCIOS.RUT FROM A_SOCIOS WHERE (((A_SOCIOS.ID)="+socio+"));"
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                nombres=i[0]+" "+i[1]
                direccion=i[2]
                rut=i[3]
        except Exception as a:
            print(a)

    data={
        'mes':listames,
        'lista':lista,
        'all_socios':buscarporNombre(),
        'nombres':nombres,
        'direccion':direccion,
        'rut':rut,
        'ano':ano,
        'numero':socio.replace(' ','')
    }

    return render(request, 'procesos/historial_cliente.html', data)

def historial_cliente(request,id_,ano_):

    listames=[]
    lista=[]
    nombres=""
    direccion=""
    rut=""
    ano=""

    listames.append({'mes':'Enero'})
    listames.append({'mes':'Febrero'})
    listames.append({'mes':'Marzo'})
    listames.append({'mes':'Abril'})
    listames.append({'mes':'Mayo'})
    listames.append({'mes':'Junio'})
    listames.append({'mes':'Julio'})
    listames.append({'mes':'Agosto'})
    listames.append({'mes':'Septiembre'})
    listames.append({'mes':'Octubre'})
    listames.append({'mes':'Noviembre'})
    listames.append({'mes':'Diciembre'})

    print("buscando...")

    socio=id_
    ano=ano_
    boleta=0
    pagado=0
    estado=""
    otros=""
    horas=""
    consumo=""
    afavor=""
    intereses=""
    saldo=""
    fechapago=""
    multa=""

    sql="SELECT A_BOLETA.IDBOLETA, A_BOLETA.PERIODO, A_BOLETA.MES, A_BOLETA.ANO, A_BOLETA.TOTAL_A_PAGAR, A_BOLETA.ID_PARCELERO, A_BOLETA.VIGENTE FROM A_BOLETA WHERE (((A_BOLETA.ID_PARCELERO)="+str(socio)+") AND ((A_BOLETA.ANO)="+ano+"));"
        
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            mesboleta=str(i[2])
            total=i[4]
            mesb=i[2]

            if i[6]==0:
                estado="VIGENTE"
            else:
                estado="NO VIGENTE"
                    
            boleta=i[0]

            sql="SELECT A_DET_BOLETA.IDBOLETA, A_DET_BOLETA.CODIGO, A_DET_BOLETA.DESCRIPCION, A_DET_BOLETA.VALOR, A_DET_BOLETA.PAGADO, A_DET_BOLETA.DESCRIPCION2, A_BOLETA.MES FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.IDBOLETA)="+str(boleta)+"));"
                
            try:
                cursor.execute(sql)
                for j in cursor.fetchall():

                    if j[2]=='CONSUMO DE AGUA POR HORA':
                        consumo=j[3]
                        horas=j[5]
                    elif j[2]=='MULTA POR INASISTENCIA':
                        multa=j[3]
                    elif j[2]=='SALDO ANTERIOR':
                        saldo=j[3]
                    elif j[2]=='SALDO A FAVOR':
                        afavor=j[3]
                    elif j[2]=='INTERESES':
                        intereses=j[3]
                    else:
                        otros=j[3]  
                        
            except Exception as a:
                print(a)
                
            #sql="SELECT Sum(A_DET_BOLETA.PAGADO) AS SumaDePAGADO,Sum(A_DET_BOLETA.VALOR) FROM A_DET_BOLETA INNER JOIN A_BOLETA ON A_DET_BOLETA.IDBOLETA = A_BOLETA.IDBOLETA WHERE (((A_DET_BOLETA.CODIGO)<>5)) HAVING (((A_BOLETA.IDBOLETA)="+str(boleta)+"));"
            sql="SELECT Sum(A_ABONO.MONTO) AS SumaDeMONTO, A_ABONO.IDBOLETA FROM A_ABONO GROUP BY A_ABONO.IDBOLETA HAVING (((A_ABONO.IDBOLETA)="+str(boleta)+"));"
            try:
                cursor.execute(sql)
                for row in cursor.fetchall():
                    if row[0]>0:
                        pagado=round(row[0])
                    else:
                        pagado=0
            except Exception as a:
                print(a)
            
                
            sql="SELECT A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA FROM A_ABONO GROUP BY A_ABONO.ID, A_ABONO.FECHA, A_ABONO.MONTO, A_ABONO.IDBOLETA HAVING (((A_ABONO.IDBOLETA)="+str(boleta)+"));"

            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    fechapago=fechapago+" A: "+str(i[0])+" F: "+str(i[1])+" $"+str(i[2])
            except Exception as a:
                print(a)

            lista.append({'mes':mesb,'horas':horas,'fechapago':fechapago,'boletas':boleta,'vconsumo':consumo,'deuda':0,'otras':otros,'afavor':afavor,'saldo':saldo,'multas':multa,'total':total,'cancelado':pagado,'abono':'0','boleta':boleta,'estado':estado,'intereses':intereses})
            pagado=0
            fechapago=""
    except Exception as a:
        print(a)

    sql="SELECT A_SOCIOS.NOMBRES, A_SOCIOS.APELLIDOS, A_SOCIOS.DIRECCION, A_SOCIOS.RUT FROM A_SOCIOS WHERE (((A_SOCIOS.ID)="+socio+"));"
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            nombres=i[0]+" "+i[1]
            direccion=i[2]
            rut=i[3]
    except Exception as a:
        print(a)

    data={
        'mes':listames,
        'lista':lista,
        'all_socios':buscarporNombre(),
        'nombres':nombres,
        'direccion':direccion,
        'rut':rut,
        'ano':ano,
        'numero':socio.replace(' ',''),
    }

    return render(request, 'procesos/historial_cliente.html', data)

def viewBoletaLibre(request):
    now = datetime.datetime.now()

    if request.method=='POST' and 'guardar' in request.POST:
        nro_boleta=request.POST['nro_boleta']
        rut_cliente=request.POST['rut_cliente']
        nombre_cliente=request.POST['nombre_cliente']
        direccion=request.POST['direccion']
        serie_medidor=request.POST['serie_medidor']
        hoy=request.POST['hoy']
        detalle=request.POST['detalle']
        total_pagar=request.POST['total_pagar']
        nivel2=request.POST['nivel2']
        nivel3=request.POST['nivel3']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }

    return render(request, 'procesos/boleta_libre.html', data)

def viewCancelarBoleta(request):

    now = datetime.datetime.now()

    if request.method=='POST' and 'guardar' in request.POST:
        nombre=request.POST['nombre']
        direccion=request.POST['direccion']
        sector=request.POST['sector']
        rut=request.POST['rut']
        nro_medidor=request.POST['nro_medidor']
        nro_socio=request.POST['nro_socio']
        hoy=request.POST['hoy']
        nro_boleta=request.POST['nro_boleta']
        consumo=request.POST['consumo']
        multa=request.POST['multa']
        nro_comprobante=request.POST['nro_comprobante']
        otros_cobros=request.POST['otros_cobros']
        total_pagar=request.POST['total_pagar']
        efectivo=request.POST['efectivo']
        vuelto=request.POST['vuelto']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }

    return render(request, 'procesos/cancelar_boleta.html', data)

def viewCierrePeriodo(request):

    return render(request, 'procesos/cierre_periodo.html', {})

def viewFacturaLibre(request):

    now = datetime.datetime.now()

    if request.method=='POST' and 'guardar' in request.POST:
        nro_factura=request.POST['nro_factura']
        hoy=request.POST['hoy']
        mes=request.POST['mes']
        año=request.POST['año']
        rut_cliente=request.POST['rut_cliente']
        direccion=request.POST['direccion']
        comuna=request.POST['comuna']
        telefono=request.POST['telefono']
        giro=request.POST['giro']
        cond_venta=request.POST['cond_venta']
        cant_mt3=request.POST['cant_mt3']
        detalle=request.POST['detalle']
        total=request.POST['total']
        cancelacion=request.POST['cancelacion']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }
    return render(request, 'procesos/factura_libre.html', data)

def viewIngresoLectura(request):
    return render(request, 'procesos/ingreso_lectura.html', {})
    
def viewLectura_rapida(request):

    now = datetime.datetime.now()

    if request.method=='POST' and 'guardar' in request.POST:
        mes=request.POST['mes']
        año=request.POST['año']
        hoy=request.POST['hoy']
        medidor=request.POST['medidor']
        lect_actual=request.POST['lect_actual']

    data={
        'hoy': str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    }
    return render(request, 'procesos/lectura_rapida.html', data)

def viewSubsidio(request):
    return render(request, 'procesos/subsidio.html', {})
