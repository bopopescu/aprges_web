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
from datetime import date,datetime

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
                      'Server=DESKTOP-VRSDL3N;'
                      'Database=APRGESMALLARA;'
                      'Trusted_Connection=yes;')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass

def days_between(d1, d2):
    return abs(d2 - d1).days

def buscarporNombre():

    try:
        cursor.execute('select * from A_FUNCIONARIOS')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[3]+" "+ row[4]})        
        return lista

    except Exception as e:
        pass
        print(e)


def buscarporNombreProveedores():

    try:
        cursor.execute('select * from A_PROVEEDORES')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[2]})        
        return lista

    except Exception as e:
        pass
        print(e)

def datosComite():

    lista=[]
    sql="SELECT * FROM DATOS_COMITE"

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'comite':i[2]})
            
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

def existeTipo(nombre):

    sqlexiste="SELECT NOMBRE FROM A_TIPO_AGUA WHERE NOMBRE='"+nombre+"';"

    try:
        cursor.execute(sqlexiste)
        for i in cursor.fetchall():
            return 1
    except:
        pass

    return 0

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

def viewTipo(request):
    
    
    data={
        'asociacion':viewName(),
        'lista':buscarTipos
    }

    if request.method=='POST' and 'imprimir' in request.POST:

        sql="SELECT * FROM A_TIPO_AGUA"
        lista2=[]

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                rut=i[1]
                lista2.append({'id':i[0],'nombre':i[1],'tipo':i[2],'fecha':i[3]})
                
        except Exception as a:
            print(a)

        data={
            'asociacion':viewName(),
            'lista':lista2
        }
        
        pdf = render_to_pdf('reportes/rpt_tipo_agua.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    if request.method=='POST' and 'borrar' in request.POST:
        tipo=request.POST['tipo2']
        
        sql1="DELETE FROM A_TIPO_AGUA WHERE ID="+tipo
            
        try:
                
            cursor.execute(sql1)
            conn.commit()

            sql="DELETE FROM A_TARIFA_HORA WHERE TIPO_AGUA="+tipo
            try:
                cursor.execute(sql)
                cursor.commit()
            except Exception as a:
                print(a)

            print('Guardado correctamente.')
                            
        except Exception as e:
            pass
            print(e)
    
    if request.method=='POST' and 'guardar' in request.POST:

        correlativo=""
        tipo=request.POST['tipo']
        nombre=request.POST['nombre']
        fecha=request.POST['turno']

        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_tipo_agua"
    
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as e:
            pass
            print(e)
        
        existe=existeTipo(nombre)
        
        if(existe==0):
        
            sql1="INSERT INTO A_TIPO_AGUA(ID,NOMBRE,TIPO,TURNOS_MES) VALUES ("+str(correlativo)+",'"+str(nombre)+"',"+str(tipo)+","+str(fecha)+")"
            
            try:
                
                cursor.execute(sql1)
                conn.commit()
                print('Guardado correctamente.')
                            
            except Exception as e:
                pass
                print(e)
            
            data={
                'asociacion':viewName(),
                'lista':buscarTipos
            }
            
            return render(request,'mantenedor/aguatipo.html', data)
        
        else:
            print("No se guardo, ya existe.")
                     

    return render(request,'mantenedor/aguatipo.html', data)

def existeTipoValor(id):

    sqlexiste="SELECT * FROM A_TARIFA_HORA WHERE TIPO_AGUA="+id+";"
    print(sqlexiste)
    try:
        cursor.execute(sqlexiste)
        for i in cursor.fetchall():
            return 1
    except:
        pass

    return 0

def buscarTiposValor():

    try:
        cursor.execute('SELECT A_TARIFA_HORA.ID, A_TIPO_AGUA.NOMBRE, A_TARIFA_HORA.VALOR_HORA FROM A_TARIFA_HORA INNER JOIN A_TIPO_AGUA ON A_TARIFA_HORA.TIPO_AGUA = A_TIPO_AGUA.ID')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1],'valor':row[2]})
        
        return lista

    except Exception as e:
        pass
        print(e)

# CARGAR TARIFA POR VALOR HORA

def viewTarifa(request):

    if request.method=='POST' and 'limpiar' in request.POST:
        data={
            'asociacion':viewName(),
            'tipos':buscarTipos(),
            'lista':buscarTiposValor,
            'nombrebomba':'',
            'fecha':'',
            'valor':'',
            'kilo':'',
            'iva':'',
            'transporte':'',
            'id':''
        }
                
        return render(request,'mantenedor/VALORHORA.html', data)

    if request.method=='POST' and 'buscar' in request.POST:

        tipobomba=request.POST['tipobomba']
        nombrebomba=request.POST['nombrebomba']
        fechaingreso=""
        valor=""
        kilo=""
        iva=""
        transporte=""
        id_=""

        sql="SELECT * FROM A_TARIFA_HORA WHERE ID="+tipobomba+""

        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                id_=i[0]
                tipobomba=i[1]
                valor=i[2]
                kilo=i[3]
                iva=i[4]
                transporte=i[5]
                fechaingreso=i[6]

            data={
                'asociacion':viewName(),
                'tipos':buscarTipos(),
                'lista':buscarTiposValor,
                'tipobomba':tipobomba,
                'nombrebomba':nombrebomba,
                'fecha':fechaingreso,
                'valor':valor,
                'kilo':kilo,
                'iva':iva,
                'transporte':transporte,
                'id':id_
            }
                
            return render(request,'mantenedor/VALORHORA.html', data)
        
        except Exception as e:
            print("Consulta Error" +str(e) )
            pass
    
    if request.method=='POST' and 'borrar' in request.POST:

        id_=request.POST['tipobomba']

        sql="DELETE FROM A_TARIFA_HORA WHERE ID="+id_

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
            print(sql)

    if request.method=='POST' and 'guardar' in request.POST:

        id_=request.POST['id_']
        print("idddd " + id_)
        correlativo=""
        tipo=request.POST['tipo']
        valor=request.POST['valor']
        fecha=request.POST['fecha']
        kilo=request.POST['kilo']
        iva=request.POST['iva']
        transporte=request.POST['transporte']

        mensaje=""

        if id_=='0' or id_==None or id_==' ' or id_=='':

            print("Entro aca")

            sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM A_TARIFA_HORA"
    
            try:
                cursor.execute(sql)

                for i in cursor.fetchall():
                    correlativo=i[0]+1
                
            except Exception as e:
                pass
                print(e)

            existe=existeTipoValor(tipo)

            #Inertar
            if(existe==0):
            
                sql1="INSERT INTO A_TARIFA_HORA(ID,TIPO_AGUA,VALOR_HORA,KILO_WANTT,IVA,TRANSPORTE,FECHA_INGRESO) VALUES ("+str(correlativo)+","+tipo+","+valor+","+kilo+","+iva+","+transporte+",'"+fecha+"')"
                
                try:
                    
                    cursor.execute(sql1)
                    conn.commit()
                    print('Guardado correctamente.')
                                
                except Exception as e:
                    pass
                    print(e)
            
            else:
                mensaje="No se guardo, existe valor hora en bomba"
            
            data={
                'asociacion':viewName(),
                'tipos':buscarTipos(),
                'lista':buscarTiposValor,
                'mensaje':mensaje,
                'id':'0'
            }
                
            return render(request,'mantenedor/VALORHORA.html', data)

        else:
            sql="UPDATE A_TARIFA_HORA SET VALOR_HORA="+valor+", KILO_WANTT=0, IVA=0,TRANSPORTE=0 WHERE ID="+id_

            try:
                cursor.execute(sql)
                conn.commit()
                mensaje="Se modifico correctamente."
                print("Se debe modificar")

            except Exception as e:
                pass
                print(e)

            data={
                'asociacion':viewName(),
                'tipos':buscarTipos(),
                'lista':buscarTiposValor,
                'mensaje':mensaje,
                'id':'0'
            }
                
            return render(request,'mantenedor/VALORHORA.html', data)

    data={
        'asociacion':viewName(),
        'tipos':buscarTipos(),
        'lista':buscarTiposValor
    }

    return render(request,'mantenedor/VALORHORA.html', data)

# FIN DE CARGAR TARIFA POR VALOR HORA

def viewReportes(request):
    data={
        'asociacion':viewName(),
    }
    return render(request,'reporte.html', data)

def buscarTarifas():

    try:
        cursor.execute('SELECT distinct(isnull(TIPO,-1)) FROM GLO_TARIFA')

        lista=[]
        
        for row in cursor.fetchall():
            if row[0]!=-1:
                lista.append({'TIPO':row[0]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def buscarTiposSector():

    try:
        cursor.execute('SELECT * FROM GLO_SECTOR')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1],'tipotar':row[5],'tratamiento':row[7],'multatrat':row[8],'porcentaje':row[9],'alcantarillado':row[10]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def existeSector(id_):

    sqlexiste="SELECT * FROM GLO_SECTOR WHERE GLOSA='"+id_+"';"
    print(sqlexiste)
    try:
        cursor.execute(sqlexiste)
        for i in cursor.fetchall():
            return 1
    except:
        pass
        print("Error " + str(sqlexiste))

    return 0

def viewSectores(request):

    id_=None
    tratamiento=0
    multa=0
    consumo=0
    alcantarillado=0
    sin_consumo=0
    nombre=""
    tipotar=''
    mensaje=""

    if request.method=='POST' and 'borrar' in request.POST:

        nombre=request.POST['nombreid']

        sql="DELETE FROM GLO_SECTOR WHERE SECTOR="+nombre+""

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print("Error : " + sql)

    if request.method=='POST' and 'editar' in request.POST:

        nombre=request.POST['nombreid']

        sql="SELECT * FROM GLO_SECTOR WHERE SECTOR="+nombre+""
        print(sql)
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                id_=i[0]
                nombre=i[1]
                tipotar=i[5]
                tratamiento=i[7]
                multa=i[8]
                consumo=i[9]
                alcantarillado=i[10]
        
        except Exception as e:
            print("Consulta Error" +str(e) )
            pass

    if request.method=='POST' and 'guardar' in request.POST:

        id_=request.POST['id_']
        correlativo=""
        nombre=request.POST['nombre']
        mensaje=""
        tipotar=request.POST['tipotar']
        tratamiento=request.POST['tratamiento']
        multa=request.POST['multa']
        consumo=request.POST['consumo']
        alcantarillado=request.POST['alcantarillado']

        #sql="SELECT COUNT(ID) FROM A_SECTOR"
        sql="SELECT IsNull(MAX(SECTOR),0) FROM GLO_SECTOR"
    
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as e:
            pass
            print(e)
        
        if id_=='0' or id_==None or id_=='' or id_==' ' or id_=='None':
            print("NUMERO IDENTIFIADOR " + str(id_))
            existe=existeSector(nombre)

            #Inertar
            if(existe==0):
            
                sql1="INSERT INTO GLO_SECTOR(SECTOR, GLOSA,VENCIMIENTO,FLAG,ARRANQUE,COMITE,TIPOTAR,TRATAMIENTO,MULTATRAT,PORCENTAJE,ALCANTARILLADO) VALUES ("+str(correlativo)+",'"+nombre+"',26,0,1000,58,"+tipotar+","+tratamiento+","+multa+","+consumo+","+alcantarillado+")"
                
                try:
                    
                    cursor.execute(sql1)
                    conn.commit()
                    id_='0'
                    print('Guardado correctamente.')
                                
                except Exception as e:
                    pass
                    print("Error " + str(sql1))
            
            else:
                mensaje="No se guardo, existe valor hora en bomba"

        else:
            sql="UPDATE GLO_SECTOR SET GLOSA='"+nombre+"',TIPOTAR="+tipotar+" WHERE SECTOR="+id_

            try:
                cursor.execute(sql)
                conn.commit()
                mensaje="Se modifico correctamente."
                id_='0'
                print("Se debe modificar")

            except Exception as e:
                pass
                print("Error " + str(sql))

    data={
        'lista':buscarTiposSector,
        'asociacion':viewName(),
        'tratamiento':tratamiento,
        'multa':multa,
        'consumo':consumo,
        'alcantarillado':alcantarillado,
        'sin_consumo':sin_consumo,
        'nombre':nombre,
        'id':id_,
        'tipoTARIFA':buscarTarifas,
        'tipotar':tipotar,
        'mensaje':mensaje
    }
    return render(request,'mantenedor/SECTOR.html', data)

def viewCallesArea(request):

    if request.method=='POST' and 'guardar' in request.POST:
        sector=request.POST['sector']
        calle=request.POST['calle']
        area=request.POST['area']
        estanque=request.POST['estanque']

    return render(request, 'mantenedor/calle_area.html', {})

def listarOcupacion():
    sql="SELECT * FROM GLO_CARGO"
    lista=[]

    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            lista.append({'id':i[0],'nombre':i[1]})
    except Exception as a:
        print(a)
        print(sql)
    
    return lista

def buscarCorrelativoCargo():

    sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) AS ValorMaximo FROM GLO_CARGO"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
        
    except Exception as a:
        print(a)
        print(sql)
    
    return correlativo

def viewCargo(request):
    
    if request.method=='POST' and 'guardar' in request.POST:

        correlativo=request.POST['correlativo']
        desc=request.POST['desc']

        sql="INSERT INTO GLO_CARGO(CORRELATIVO,CARGO) VALUES("+correlativo+",'"+desc+"')"

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
            print(sql)
    
    if request.method=='POST' and 'borrar' in request.POST:

        correlativo=request.POST['tipo2']

        sql="DELETE FROM GLO_CARGO WHERE CORRELATIVO="+correlativo

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
            print(sql)

    data={
        # 'correlativo':buscarCorrelativoCargo(),
        'lista':listarOcupacion()
    }

    return render(request, 'mantenedor/cargo.html', data)

def corrProvedores():
    sql="SELECT IIf(IsNull(MAX(RUT)), 0, Max(RUT)) AS ValorMaximo FROM GLO_PROVEEDOR"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
        
    except Exception as a:
        print(a)
        print(sql)
    
    return correlativo

def corrFuncionarios():
    sql="SELECT IIf(IsNull(MAX(RUT)), 0, Max(RUT)) AS ValorMaximo FROM FUNCIONARIO"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
        
    except Exception as a:
        print(a)
        print(sql)
    
    return correlativo

def viewFuncionarios(request):
    now = datetime.datetime.now()
    rut=""
    fecha=""
    nombres=""
    apellidos=""
    direccion=""
    telefono=""
    idcargo=""
    cargo=""
    mensaje=""
    numero=0

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
    
    sql="SELECT CORRELATIVO,CARGO FROM GLO_CARGO"
    lista=[]
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'id':i[0],'cargo':i[1]})
    except Exception as a:
        print("Error : " +sql)

    if request.method=='POST' and 'buscar' in request.POST:

        numero=request.POST['numero'].replace(' ','')
        sql="SELECT GLO_CARGO.CARGO, * FROM A_FUNCIONARIOS INNER JOIN GLO_CARGO ON A_FUNCIONARIOS.ID_OCUPACION = GLO_CARGO.CORRELATIVO WHERE (((A_FUNCIONARIOS.[ID])="+numero+"));"
        print(sql)

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                rut=i[2]
                fecha=i[3]
                nombres=i[4]
                apellidos=i[5]
                direccion=i[8]
                telefono=i[9]
                idcargo=i[6]
                cargo=i[0]
        except Exception as a:
            print(a)
            print(sql)

    if request.method=='POST' and 'guardar' in request.POST:
        id_=request.POST['identi']
        
        rut=request.POST['rut']
        nombres=request.POST['nombres']
        apellidos=request.POST['apellidos']
        cargo=request.POST['ocupacion']
        direccion=request.POST['direccion']
        telefono=request.POST['telefono']
        fecha=request.POST['fecha']
        id_ocupacion=request.POST['ocupacion']

        if id_=='0' or id_==0 or id_==None or id_==' ' or id_=='':

            sql="INSERT INTO A_FUNCIONARIOS(ID,RUT,FECHA_INGRESO,NOMBRES,APELLIDOS,ID_OCUPACION,DIRECCION,TELEFONO) VALUES("+str(corrFuncionarios())+",'"+str(rut)+"','"+str(fecha)+"','"+str(nombres)+"','"+str(apellidos)+"',"+str(id_ocupacion)+",'"+str(direccion)+"',"+str(telefono)+")"
            
            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Se guardo correctamente"
            except Exception as a:
                print("Error sql: " + sql)

        else:

            sql="UPDATE A_FUNCIONARIOS SET RUT='"+rut+"' ,FECHA_INGRESO='"+fecha+"' ,NOMBRES='"+nombres+"', APELLIDOS='"+apellidos+"' ,ID_OCUPACION="+id_ocupacion+", DIRECCION='"+direccion+"' ,TELEFONO="+telefono+" WHERE ID="+str(id_) 
            print(sql)
            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Se modifico correctamente"
            except Exception as a:
                print("Error sql: " + sql)

    if request.method=='POST' and 'borrar' in request.POST:
        rut=request.POST['rut']

    data={
        'dia': (now.day), 
        'mes': (now.month), 
        'año': (now.year),
        'fecha_actual': str(now.day)+"/"+str(now.month)+"/"+str(now.year),
        'all_socios':buscarporNombre,
        'lista':lista,
        'rut':rut,
        'fecha':fecha,
        'nombres':nombres,
        'apellidos':apellidos,
        'direccion':direccion,
        'telefono':telefono,
        'idcargo':idcargo,
        'cargo':cargo,
        'mensaje':mensaje,
        'numero':numero
    }
    return render(request, 'mantenedor/funcionarios.html', data)

def existeProveedor(rut):

    sql="SELECT * FROM GLO_PROVEEDOR WHERE RUT='"+rut+"';"
    existe=0

    try:
        cursor.execute(sql)
        
        for i in cursor.fetchall():
            existe=1
    except Exception as a:
        print(a)

    return existe

def viewProveedor(request):

    mensaje=""
    rut=""
    giro=""
    razon=""
    direccion=""
    telefono=""
    contacto=""
    numero=""

    if request.method=='POST' and 'buscar' in request.POST:
        numero=request.POST['id_']

        sql="SELECT * FROM GLO_PROVEEDOR WHERE RUT="+numero
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                rut=i[1]
                giro=i[2]
                razon=i[3]
                direccion=i[4]
                telefono=i[5]
                contacto=i[6]
        except Exception as a:
            print(a)

    if request.method=='POST' and 'eliminar' in request.POST:

        id_=request.POST['numero']

        sql="DELETE FROM GLO_PROVEEDOR WHERE RUT="+id_
        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Se elimino correctamente"

        except Exception as a:
            print(a)

    if request.method=='POST' and 'guardar' in request.POST:

        id_=request.POST['numero']
        
        rut=request.POST['rut']
        giro=request.POST['giro']
        razon=request.POST['razon']
        direccion=request.POST['direccion']
        telefono=request.POST['telefono']
        contacto=request.POST['contacto']

        existe=existeProveedor(rut)

        if id_=='0' or id_==0 or id_==None or id_==' ' or id_=='':      
            if existe==0:

                #sql="INSERT INTO A_PROVEEDORES(ID,RUT,GIRO,RAZON_SOCIAL,DIRECCION,TELEFONO,CONTACTO_VENDEDOR) VALUES("+str(corrProvedores())+",'"+str(rut)+"','"+str(giro)+"','"+str(razon)+"','"+str(direccion)+"',"+telefono+",'"+str(contacto)+"')"
                sql="INSERT INTO A_PROVEEDORES(ID,RUT,GIRO,RAZON_SOCIAL,DIRECCION,TELEFONO,CONTACTO_VENDEDOR) VALUES("+str(corrProvedores())+",'"+str(rut)+"','"+str(giro)+"','"+str(razon)+"','"+str(direccion)+"',"+str(telefono)+",'"+str(contacto)+"')"
                
                try:
                    cursor.execute(sql)
                    cursor.commit()
                    mensaje="Quedo guardado correctamente"

                except Exception as a:
                    print(a)
            else:
                mensaje="No se pudo guardar, proveedor ya existe"
        else:
            sql="UPDATE GLO_PROVEEDOR SET RUT='"+rut+"', GIRO='"+giro+"', RAZON='"+razon+"', DIRECCION='"+direccion+"', TELEFONO="+telefono+", CONTACTO='"+contacto+"' WHERE ID="+id_
            try:
                cursor.execute(sql)
                cursor.commit()
                mensaje="Se modifico correctamente"
            except Exception as a:
                print(a)

    data={
        'rut':rut,
        'giro':giro,
        'razon':razon,
        'direccion':direccion,
        'telefono':telefono,
        'contacto':contacto,
        'numero':numero,
        'mensaje':mensaje,
        'all_socios':buscarporNombreProveedores()
    }

    return render(request, 'mantenedor/proveedor.html', data)

def viewDatos(request):

    sql="SELECT * FROM DATOS_COMITE"
    rut=""
    giro=""
    nombre=""
    direccion=""
    fono=""
    region=""
    comuna=""
    provincia=""
    email=""
    
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            rut=i[1]
            giro=i[2]
            nombre=i[3]
            direccion=i[4]
            fono=i[5]
            region=i[6]
            comuna=i[7]
            provincia=i[8]
            email=i[9]

    except Exception as a:
        print(a)

    if request.method=='POST' and 'guardar' in request.POST:

        rut=request.POST['rut']
        nombre=request.POST['nombre']
        giro=request.POST['giro']
        direccion=request.POST['direccion']
        fono=request.POST['fono']
        region=request.POST['region']
        comuna=request.POST['comuna']
        provincia=request.POST['provincia']
        email=request.POST['email']

        sql="UPDATE DATOS_COMITE SET RUT='"+rut+"',GIRO='"+giro+"',NOMBRE='"+nombre+"',DIRECCION='"+direccion+"',FONO='"+fono+"',REGION='"+region+"',COMUNA='"+comuna+"',PROVINCIA='"+provincia+"',EMAIL='"+email+"' WHERE CORRELATIVO=1"
        
        try:
            cursor.execute(sql)
            cursor.commit()
            print("&%&%&%&%     Se actualizo correctamente &%&%&")
        except Exception as a:
            print(a)

    data={
        'rut':rut,
        'giro':giro,
        'nombre':nombre,
        'direccion':direccion,
        'fono':fono,
        'region':region,
        'comuna':comuna,
        'provincia':provincia,
        'email':email,
        'lista':buscarTiposSector,
        'asociacion':viewName(),
    }
    return render(request,'mantenedor/asociacion.html', data)

def buscarConvenio():

    sql="SELECT * FROM GLO_COBRO"
    lista=[]
    try:
        cursor.execute(sql)
        
        for i in cursor.fetchall():
            lista.append({'id':i[0],'nombre':i[1]})
        
    except Exception as a:
        print(a)
    
    return lista

def viewConvenioMan(request):
    
    if request.method=='POST' and 'borrar' in request.POST:
        tipo2=request.POST['tipo2']

        sql="DELETE FROM GLO_COBRO WHERE CORRELATIVO="+tipo2

        try:
            cursor.execute(sql)
            cursor.commit()
        
        except Exception as a:
            print(a)

    if request.method=='POST' and 'guardar' in request.POST:

        correlativo=0
        desc=request.POST['desc']

        sql="SELECT IIf(IsNull(MAX(CORRELATIVO)), 0, Max(CORRELATIVO)) FROM GLO_COBRO"
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as a:
            print(a)
        
        if correlativo==5 or correlativo==3 or correlativo==2:
            correlativo=correlativo+1

        sql="INSERT INTO GLO_COBRO(CORRELATIVO,DESCRIPCION) VALUES("+str(correlativo)+",'"+desc+"')"

        try:
            cursor.execute(sql)
            cursor.commit()
            mensaje="Quedo guardado correctamente"

        except Exception as a:
            print(a)

    data={
        'lista':buscarConvenio(),
        'asociacion':viewName(),
    }
    return render(request,'mantenedor/convenio.html', data)

def correlativotarifa():
    
    correlativo=0
    sql="SELECT IsNull(MAX(CORRELATIVO),0) FROM GLO_TARIFA"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
    except Exception as a:
        print(a)
    
    return correlativo

def buscardatosTarifa(id_):

    sql="SELECT * FROM GLO_TARIFA where tipo="+str(id_)+" ORDER BY 3"
    lista=[]

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'tramo':i[1],'desde':i[2],'hasta':i[3],'fecha':i[7],'mt3':i[4],'valormt3':i[5],'valor':i[4],'fijo':i[11],'solidario':i[12]})
    except Exception as a:
        print(a)

    return lista

def buscarcargofijo(id_):
    sql="SELECT DISTINCT(FIJO) FROM GLO_TARIFA where tipo="+str(id_)
    fijo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            fijo=i[0]
    except Exception as a:
        print(a)

    return fijo

def buscartramo(id_):
    sql="SELECT MAX(TRAMO) FROM GLO_TARIFA where tipo="+str(id_)
    fijo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            fijo=i[0]+1
    except Exception as a:
        print(a)

    return fijo

def buscarSolidario(id_):
    sql="SELECT DISTINCT(FONDO) FROM GLO_TARIFA where tipo="+str(id_)
    fijo=0

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            fijo=i[0]
    except Exception as a:
        print(a)

    return fijo


def viewTramo(request,id_):

    print("tarifa seleccionada  " + str(id_))
    
    now =time.strftime("%d-%m-%Y")
    cargofijo=0
    fondosolidario=0
    lista=[]
    inicio=0
    hasta=0
    valor_inicial=0
    intervalo=0
    fechaexcel = date(1900,1,1)
    fechatextD=0
    existe=1
    tramo=0
    desde=0
    valor=0
    mensaje=""
    resultado=""

    if request.method=='POST' and 'guardartarifa' in request.POST:

        existe=buscardatosTarifa(id_)
        if len(existe)>0:
            mensaje="ERROR"
        else:

            inicial=0
            mensaje=""
            tramotabla=request.POST.getlist('tramotabla')
            desdetabla=request.POST.getlist('desdetabla')
            hastatabla=request.POST.getlist('hastatabla')
            valortabla=request.POST.getlist('valortabla')
            fechatabla=request.POST.getlist('fechatabla')
            fijo=request.POST['fijo']
            solidario=request.POST['solidario']

            listatramo=[]
            listafecha=[]
            listadesde=[]
            listahasta=[]
            listavalor=[]

            for i in tramotabla:
                listatramo.append(i)

            for i in desdetabla:
                listadesde.append(i)
            
            for i in hastatabla:
                listahasta.append(i)
            
            for i in valortabla:
                listavalor.append(i)
            
            for i in fechatabla:
                listafecha.append(i)
            
            while inicial<len(listatramo):

                fechaac=listafecha[inicial]
                bjDate1 = datetime.strptime(fechaac, '%d-%m-%Y')
                d22=date(bjDate1.year,bjDate1.month,bjDate1.day)
                fechatextD=days_between(d22, fechaexcel)

                sql="INSERT INTO GLO_TARIFA(correlativo,tramo,desde,hasta,valor,valormt3,fecha,fechastr,vigente,tipo,comite,fijo,fondo) values("+str(correlativotarifa())+","+str(listatramo[inicial])+","+str(listadesde[inicial])+","+str(listahasta[inicial])+","+str(listavalor[inicial])+","+str(listavalor[inicial])+","+str(fechatextD)+","+str(listafecha[inicial])+",0,"+str(id_)+",64,"+str(fijo)+","+solidario+")"

                try:
                    cursor.execute(sql)
                    cursor.commit()
                    mensaje="quedo guardado correctamente"
                    resultado="OK"
                except Exception as a:
                    print(a)    
                    resultado="ERROR"

                inicial=inicial+1

    if request.method=='POST' and 'eliminartarifa' in request.POST:

        tipo=request.POST['tipo']

        sql="DELETE FROM GLO_TARIFA WHERE TIPO="+tipo+" AND VIGENTE=0"

        try:
            cursor.execute(sql)
            cursor.commit()
            desde=0
            hasta=0
            ultimo=0
        except Exception as a:
            print(a)

    if request.method=='POST' and 'imprimirtarifa' in request.POST:
        
        data={
            'lista':buscardatosTarifa(id_),
            'comite':viewName(),
            'fijo':buscarcargofijo(id_),
            'solidario':buscarSolidario(id_)
        }

        pdf = render_to_pdf('reportes/tarifa.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

    if request.method=='POST' and 'generart' in request.POST:

        inicio=request.POST['inicio']
        hasta=request.POST['hasta']
        valor_inicial=request.POST['valor_inicial']
        intervalo=request.POST['intervalo']
        existe=request.POST['existe']

        fechaac=str(now.day)+"-"+str(now.month)+"-"+str(now.year)
        bjDate1 = datetime.strptime(fechaac, '%d-%m-%Y')
        d22=date(bjDate1.year,bjDate1.month,bjDate1.day)
        fechatextD=days_between(d22, fechaexcel)

        if existe=='0':
            while inicio<=hasta:
                valor=str(int(valor_inicial)+int(intervalo))
                sql="INSERT INTO GLO_TARIFA(correlativo,tramo,desde,hasta,valor,valormt3,fecha,fechastr,vigente,tipo,comite,fijo,fondo) values("+str(correlativotarifa())+","+inicio+","+inicio+","+inicio+","+valor+","+valor+","+fechatextD+","+fechaac+",0,3,64,"+valor_inicial+",0)"

                try:
                    cursor.execute(sql)
                    cursor.commit()
                except Exception as a:
                    print(a)

                inicio=inicio+1
            mensaje="Se genero correctamente"
        else:
            mensaje="Se debe eliminar tabla tarifaria antes de ingresar una nueva."

    if request.method=='POST' and 'guardar' in request.POST:        
        fijo=request.POST['fijo']      
        solidario=request.POST['solidario']      
        tramo=request.POST['tramo']      
        hoy=request.POST['hoy']
        desde=request.POST['desde']      
        hasta=request.POST['hasta']      
        valor=request.POST['valor']   

    print(mensaje)
    data={
        'comite':viewName(),
        'tramo':buscartramo(id_),
        'desde':desde,
        'valor':valor,
        'existe':existe,
        'inicio':inicio,
        'hasta':hasta,
        'valor_inicial':valor_inicial,
        'intervalo':intervalo,
        'fijo':buscarcargofijo(id_),
        'lista':buscardatosTarifa(id_),
        'solidario':buscarSolidario(id_),
        'hoy': time.strftime("%d-%m-%Y"),
        'id_':id_,
        'desdeultimo':desde,
        'hastaultimo':hasta,
        'valorultimo':valor,
        'resultado':resultado,
        'mensaje':mensaje
    }

    if id_=='3':
        return render(request, 'mantenedor/tramoespecial.html', data)
    else:
        return render(request, 'mantenedor/tramo.html', data)

def viewMedidor(request):

    
    if request.method=='POST' and 'guardar' in request.POST:                
        codigo=request.POST['codigo']              
        descripcion=request.POST['descripcion']     

    return render(request, 'mantenedor/estado_medidor.html', {})