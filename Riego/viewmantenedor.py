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
from Riego.utils import render_to_pdf

#Instalar CONTROLADOR ODBC especifico según 64bits o 32bits del computador , en este caso es controlador en 64bits

try:
    conn = pyodbc.connect('DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\\RiegoWeb\\Riego\\RIEGO.mdb')
    cursor = conn.cursor()
except pyodbc.Error as ex:
    sqlstate = ex.args[0]
    print(sqlstate)
    if sqlstate == '08001':
        pass

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

def buscarTiposSector():

    try:
        cursor.execute('SELECT * FROM A_SECTOR')

        lista=[]
        
        for row in cursor.fetchall():
            lista.append({'id':row[0],'nombre':row[1]})
        
        return lista

    except Exception as e:
        pass
        print(e)

def existeSector(id):

    sqlexiste="SELECT * FROM A_SECTOR WHERE NOMBRE='"+id+"';"
    print(sqlexiste)
    try:
        cursor.execute(sqlexiste)
        for i in cursor.fetchall():
            return 1
    except:
        pass

    return 0


def viewSectores(request):

    id_=None

    if request.method=='POST' and 'borrar' in request.POST:

        nombre=request.POST['nombreid']

        sql="DELETE FROM A_SECTOR WHERE ID="+nombre+""

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print("Error : " + sql)

    if request.method=='POST' and 'editar' in request.POST:

        nombre=request.POST['nombreid']
        id_=""

        sql="SELECT * FROM A_SECTOR WHERE ID="+nombre+""
        print(sql)
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                id_=i[0]
                nombre=i[1]

            data={
                'asociacion':viewName(),
                'lista':buscarTiposSector,
                'nombre':nombre,
                'id':id_
            }
                
            return render(request,'mantenedor/SECTOR.html', data)
        
        except Exception as e:
            print("Consulta Error" +str(e) )
            pass

    if request.method=='POST' and 'guardar' in request.POST:

        id_=request.POST['id_']
        correlativo=""
        nombre=request.POST['nombre']
        mensaje=""

        #sql="SELECT COUNT(ID) FROM A_SECTOR"
        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) AS ValorMaximo FROM a_sector"
    
        try:
            cursor.execute(sql)

            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as e:
            pass
            print(e)

        if id_=='0' or id_==None or id_=='' or id_==' ':

            existe=existeSector(nombre)

            #Inertar
            if(existe==0):
            
                sql1="INSERT INTO A_SECTOR(ID,NOMBRE) VALUES ("+str(correlativo)+",'"+nombre+"')"
                
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
                #'tipos':buscarTipos(),
                'lista':buscarTiposSector,
                'mensaje':mensaje,
                'id':'0'
            }  
            return render(request,'mantenedor/SECTOR.html', data)

        else:
            sql="UPDATE A_SECTOR SET NOMBRE='"+nombre+"' WHERE ID="+id_

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
                #'tipos':buscarTipos(),
                'lista':buscarTiposSector,
                'mensaje':mensaje,
                'id':'0'
            }
                
            return render(request,'mantenedor/SECTOR.html', data)
    data={
        'lista':buscarTiposSector,
        'asociacion':viewName(),
    }
    return render(request,'mantenedor/SECTOR.html', data)

def viewCallesArea(request):
    return render(request, 'mantenedor/calle_area.html', {})

def listarOcupacion():
    sql="SELECT * FROM A_OCUPACION"
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

    sql="SELECT IIf(IsNull(MAX(codigo)), 0, Max(codigo)) AS ValorMaximo FROM a_ocupacion"

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

        sql="INSERT INTO A_OCUPACION(CODIGO,CARGO) VALUES("+correlativo+",'"+desc+"')"

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
            print(sql)
    
    if request.method=='POST' and 'borrar' in request.POST:

        correlativo=request.POST['tipo2']

        sql="DELETE FROM A_OCUPACION WHERE CODIGO="+correlativo

        try:
            cursor.execute(sql)
            cursor.commit()
        except Exception as a:
            print(a)
            print(sql)

    data={
        'correlativo':buscarCorrelativoCargo(),
        'lista':listarOcupacion()
    }

    return render(request, 'mantenedor/cargo.html', data)

def corrProvedores():
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) AS ValorMaximo FROM a_proveedores"

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            correlativo=i[0]+1
        
    except Exception as a:
        print(a)
        print(sql)
    
    return correlativo

def corrFuncionarios():
    sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) AS ValorMaximo FROM a_FUNCIONARIOS"

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
    
    sql="SELECT CODIGO,CARGO FROM A_OCUPACION"
    lista=[]
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            lista.append({'id':i[0],'cargo':i[1]})
    except Exception as a:
        print("Error : " +sql)

    if request.method=='POST' and 'buscar' in request.POST:

        numero=request.POST['numero'].replace(' ','')
        sql="SELECT A_OCUPACION.CARGO, * FROM A_FUNCIONARIOS INNER JOIN A_OCUPACION ON A_FUNCIONARIOS.ID_OCUPACION = A_OCUPACION.CODIGO WHERE (((A_FUNCIONARIOS.[ID])="+numero+"));"
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

    sql="SELECT * FROM A_PROVEEDORES WHERE RUT='"+rut+"';"
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

        sql="SELECT * FROM A_PROVEEDORES WHERE ID="+numero
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

        sql="DELETE FROM A_PROVEEDORES WHERE ID="+id_
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
            sql="UPDATE A_PROVEEDORES SET RUT='"+rut+"', GIRO='"+giro+"', RAZON_SOCIAL='"+razon+"', DIRECCION='"+direccion+"', TELEFONO="+telefono+", CONTACTO_VENDEDOR='"+contacto+"' WHERE ID="+id_
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

    sql="SELECT * FROM A_DATOS"
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

        sql="UPDATE A_DATOS SET RUT='"+rut+"',GIRO='"+giro+"',NOMBRE='"+nombre+"',DIRECCION='"+direccion+"',FONO='"+fono+"',REGION='"+region+"',COMUNA='"+comuna+"',PROVINCIA='"+provincia+"',EMAIL='"+email+"' WHERE CORRELATIVO=1"
        
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

    sql="SELECT * FROM A_COBROS"
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

        sql="DELETE FROM A_COBROS WHERE ID="+tipo2

        try:
            cursor.execute(sql)
            cursor.commit()
        
        except Exception as a:
            print(a)

    if request.method=='POST' and 'guardar' in request.POST:

        correlativo=0
        desc=request.POST['desc']

        sql="SELECT IIf(IsNull(MAX(id)), 0, Max(id)) FROM a_cobros"
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                correlativo=i[0]+1
            
        except Exception as a:
            print(a)
        
        if correlativo==5 or correlativo==3 or correlativo==2:
            correlativo=correlativo+1

        sql="INSERT INTO A_COBROS(ID,DESCRIPCION) VALUES("+str(correlativo)+",'"+desc+"')"

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
