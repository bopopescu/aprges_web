from Riego.utils import render_to_pdf
from django.shortcuts import render
from django.http import HttpResponse
import time
import pyodbc
from datetime import datetime
import xlrd
import xlwt
import os

now = datetime.now()

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

def mesNumero(mes):
    mesnum=0
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
        
    return mesnum

def correlativoSubsidio():
    sql="SELECT MAX(ISNULL(CORRELATIVO, 0)) FROM SUBSIDIO"
    correlativo=0
    try:
        cursor.execute(sql)

        for i in cursor.fetchall():
            correlativo=i[0]+1
            
    except Exception as e:
        pass
        print(e)
    
    return correlativo

def xstr(s):
    if s is None:
        return '0'
    return "'"+str(s)+"'"

def Cargasubsidio(request):

    mes=request.GET.get('concepto')
    ano=request.GET.get('ano')
    mesnum=0

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

    aviso=""
    subsidio=-1

    sql="SELECT DISTINCT(FECHACARGA) FROM SUBSIDIO WHERE MES="+str(mesnum)+" AND ANO="+str(ano)
    print(sql)
    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            if int(i[0])==0:
                subsidio=0
            else:
                subsidio=int(i[0])
    except Exception as a:
        print(a)

    print(str(subsidio))
    if subsidio>0:
        excel_date = subsidio
        dt = datetime.fromordinal(datetime(1900, 1, 1).toordinal() + excel_date - 2)
        mesfelipe = dt.strftime("%m")
        if mesfelipe=='01':
            mesfelipe="Enero"
        if mesfelipe=='02':
            mesfelipe="Febrero"
        if mesfelipe=='03':
            mesfelipe="Marzo"
        if mesfelipe=='04':
            mesfelipe="Abril"
        if mesfelipe=='05':
            mesfelipe="Mayo"
        if mesfelipe=='06':
            mesfelipe="Junio"
        if mesfelipe=='07':
            mesfelipe="Julio"
        if mesfelipe=='08':
            mesfelipe="Agosto"
        if mesfelipe=='09':
            mesfelipe="Septiembre"
        if mesfelipe=='10':
            mesfelipe="Octubre"
        if mesfelipe=='11':
            mesfelipe="Noviembre"
        if mesfelipe=='12':
            mesfelipe="Diciembre"
        ano=dt.strftime("%Y")
        aviso="Fecha de carga mes de " + str(mesfelipe)+" del "+str(ano)
    elif subsidio==0:
        aviso="No tiene fecha de carga"
    else:
        aviso="No se ha generado nomina de subsidio"
    return render(request, 'otros/cargasub.html', {'subsidio': aviso})

def days_between(d1, d2):
    return abs(d2 - d1).days

def revisarSubsidio(mes, ano):

    existe=1

    sql="SELECT * FROM SUBSIDIO WHERE MES="+str(mes)+" AND ANO="+str(ano)

    try:
        cursor.execute(sql)
        for i in cursor.fetchall():
            existe=0
    except Exception as a:
        print(a)

    return existe 

def subsidio(request):

    nombre=""
    mensaje=""
    aviso=""
    ano=str(now.year)
    mes=mesNombre(now.month)

    if request.method=='POST' and 'generar' in request.POST:
        ano=request.POST['ano']
        mes=request.POST['mes']
        numeromes=mesNumero(mes)
        maximo=0
        submt3=0
        subsidio=0
        deuda=0
        maxboleta=0
        comuna=""
        valor=0
        M3=0 
        total=0  
        cod=""
        sql=""
        tiposub=1
    

        #REVISAR SI EXISTE
        existe=revisarSubsidio(mes,ano)

        if existe==1:
            #GENERAR TABLA SUBSIDIO

            sql="SELECT OPER_LECTURA.MEDIDOR_CORRELATIVO, OPER_LECTURA.M3_CONSUMOS, OPER_LECTURA.VALOR_ESTIMADO, OPER_LECTURA.FIJO, GLO_MEDIDOR.SUB100 FROM OPER_LECTURA INNER JOIN GLO_MEDIDOR ON OPER_LECTURA.MEDIDOR_CORRELATIVO = GLO_MEDIDOR.CORRELATIVO WHERE (((GLO_MEDIDOR.ACTIVO)=0) AND ((GLO_MEDIDOR.SUBSIDIO)=1) AND ((OPER_LECTURA.MES)="+str(numeromes)+") AND ((OPER_LECTURA.ANO)="+ano+"))"
            #sql="SELECT OPER_LECTURA.MEDIDOR_CORRELATIVO, OPER_LECTURA.M3_CONSUMOS, OPER_LECTURA.VALOR_ESTIMADO, OPER_LECTURA.FIJO, GLO_MEDIDOR.SUB100 FROM OPER_LECTURA INNER JOIN GLO_MEDIDOR ON OPER_LECTURA.MEDIDOR_CORRELATIVO = GLO_MEDIDOR.CORRELATIVO WHERE (((GLO_MEDIDOR.ACTIVO)=0) AND ((GLO_MEDIDOR.SUBSIDIO)=1) AND GLO_MEDIDOR.CORRELATIVO=1255 AND ((OPER_LECTURA.MES)="+str(numeromes)+") AND ((OPER_LECTURA.ANO)="+ano+"))"

            
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():
                    valor=i[2]
                    M3=i[1]

                    sql="SELECT MAXIMO FROM CONFIGURA WHERE CORRELATIVO=1"
                    try:
                        cursor.execute(sql)
                        for j in cursor.fetchall():
                            maximo=int(j[0])
                    except Exception as a:
                        print(a)

                    if int(i[1])>maximo: 
                        sql="SELECT VALOR FROM GLO_TARIFA WHERE DESDE="+str(maximo)
                        try:
                            cursor.execute(sql)
                            for row in cursor.fetchall():
                                subsidio=int(row[0]/2)
                        except Exception as a:
                            print(a)
                    else:
                        subsidio=int(valor/2)       
                    
                    sub100=i[4]
                    if sub100!=1:
                        maximo=maximo/2
                        tiposub=0
                    
                    if int(i[1])>=maximo:
                        submt3=maximo
                    else:
                        submt3=int(i[1])/2
                    
                    print("tipo subb " + str(tiposub))

                    sql="SELECT Sum(OPER_DET_AVISO.VALOR) AS SumaDeVALOR, Sum(OPER_DET_AVISO.PAGADO) AS SumaDePAGADO, OPER_AVISO.IDBOLETA FROM OPER_AVISO INNER JOIN OPER_DET_AVISO ON OPER_AVISO.CORRELATIVO = OPER_DET_AVISO.AVISO_CORRELATIVO GROUP BY OPER_AVISO.VIGENTE, OPER_DET_AVISO.CODIGO, OPER_AVISO.MEDIDOR_CORRELATIVO,OPER_AVISO.IDBOLETA HAVING (((OPER_AVISO.VIGENTE)=0) AND ((OPER_DET_AVISO.CODIGO)<>5) AND ((OPER_AVISO.MEDIDOR_CORRELATIVO)="+str(i[0])+"));"
                    print("deudas " + str(sql))
                    try:
                        cursor.execute(sql)
                        for deu in cursor.fetchall():
                            deuda=deuda+(deu[0]-deu[1])
                    except Exception as a:
                        print(a)

                    sql="INSERT INTO SUBSIDIO(CORRELATIVO,MEDIDOR_CORRELATIVO,CONSUMO,SUBMTS3,VALOR,FIJO,SUBSIDIO,COMITE,MES,ANO,DEUD,MON,TARIFA_CORRELATIVO,TIPOSUB) VALUES("+str(correlativoSubsidio())+","+str(i[0])+","+str(i[1])+","+str(submt3)+","+str(i[2])+","+str(i[3])+","+str(subsidio)+",65,"+str(numeromes)+","+ano+",0,"+str(deuda)+",0,"+str(tiposub)+")"
                    
                    try:
                        cursor.execute(sql)
                        cursor.commit()
                    except Exception as a:
                        print(a)
                    
                    #COMUNA Y ORGIN
                    sql="SELECT COMUNA,REGION,PROVINCIA,codregion,codcomuna,CODSERVICIO FROM DATOS_COMITE"
                    
                    try:
                        cursor.execute(sql)
                        for datos in cursor.fetchall():
                            cod=str(datos[3])+""+str(datos[4])+str(datos[5])
                            comuna=str(datos[0])
                    except Exception as a:
                        print(a)
                    
                    descuento=valor-subsidio
                    
                    #SELECCIONAR DATOS DEL BENEFICIARIO
                    sql="SELECT OPER_CLIENTE.RUT, OPER_CLIENTE.VER_RUT, OPER_CLIENTE.APELL_PAT, GLO_SECTOR.GLOSA, GLO_MEDIDOR.NUMDEC, GLO_MEDIDOR.FECDEC,GLO_MEDIDOR.PUNTAJE,GLO_MEDIDOR.FECENC,GLO_MEDIDOR.NUMSOCIO,GLO_MEDIDOR.DVNUM,GLO_MEDIDOR.NUMVIV, GLO_MEDIDOR.CORRELATIVO,GLO_MEDIDOR.RUTBEN, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELL_PAT, OPER_CLIENTE.APELL_MAT, GLO_MEDIDOR.SUBSIDIO FROM (GLO_MEDIDOR INNER JOIN OPER_CLIENTE ON GLO_MEDIDOR.SOCIO = OPER_CLIENTE.RUT) INNER JOIN (GLO_SECTOR INNER JOIN GLO_CALLE ON GLO_SECTOR.SECTOR = GLO_CALLE.SECTOR) ON OPER_CLIENTE.CALLE_CORRELATIVO = GLO_CALLE.CORRELATIVO GROUP BY OPER_CLIENTE.RUT, OPER_CLIENTE.VER_RUT, OPER_CLIENTE.APELL_PAT, GLO_SECTOR.GLOSA, GLO_MEDIDOR.NUMDEC, GLO_MEDIDOR.RUTBEN, GLO_MEDIDOR.NOMBEN, GLO_MEDIDOR.PATERNOBEN, GLO_MEDIDOR.MATERNOBEN, GLO_MEDIDOR.SUBSIDIO, GLO_MEDIDOR.CORRELATIVO, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELL_MAT, GLO_MEDIDOR.NUMDEC, GLO_MEDIDOR.FECDEC,GLO_MEDIDOR.PUNTAJE,GLO_MEDIDOR.FECENC,GLO_MEDIDOR.NUMSOCIO,GLO_MEDIDOR.DVNUM,GLO_MEDIDOR.NUMVIV HAVING (((GLO_MEDIDOR.SUBSIDIO)=1) AND GLO_MEDIDOR.CORRELATIVO="+str(i[0])+");"
                    
                    try:
                        cursor.execute(sql)
                        for reg in cursor.fetchall():  
                            numunico=cod+"2"+str(i[0])
                            sql1="INSERT INTO REGBENEFICIARIO(COMUNA,RUT,DVRUT,NOMBRE,DIRECCION,NUMDEC,FECDEC,PUNTAJE,FECENC,NUMSOCIO,DVNUM,NUMVIV,M3,CONS,SUBS,BEN,DEUD,MON,OBS,MEDIDOR,ID,RUTE,RUTBEN,NOMBEN,PATBEN,MATBEN) VALUES ('"+str(comuna)+"',"+str(reg[0])+",'"+str(reg[1])+"','"+str(reg[2])+"','"+str(reg[3])+"',"+ xstr(reg[4])+","+xstr(reg[5])+","+xstr(reg[6])+","+xstr(reg[7])+","+xstr(numunico)+","+xstr(reg[9])+","+xstr(reg[10])+","+str(M3)+","+str(valor)+","+str(subsidio)+","+str(descuento)+","+str(deuda)+",0,'10','"+str(i[0])+"',1,'"+str(reg[0])+"',"+xstr(reg[12])+",'"+str(reg[13])+"','"+str(reg[14])+"','"+str(reg[15])+"')"
                            
                            try:
                                cursor.execute(sql1)
                                cursor.commit()
                            except Exception as a:
                                print(a)
                    except Exception as a:
                        print(a)
                    deuda=0
                    mensaje="Se genero correctamente"

            except Exception as a:
                print(a)
        else:
            mensaje="Nomina de subsidio ya esta generada"

    if request.method=='POST' and 'cargar' in request.POST:    

        #UPDATE VALOR SUBSIDIO A TABLA DE CONSUMO
        mesnomina=request.POST['mesn']
        numeromesnomina=mesNumero(mesnomina)
        anonomina=request.POST['anon']

        ano=request.POST['anocarga']
        mes=request.POST['mescarga']
        numeromes=mesNumero(mes)
        print("mes " + str(numeromes))
        fechaexcel = datetime(1900,1,1)
        bjDate1 = datetime.strptime("28-"+str(numeromes)+"-"+str(ano), '%d-%m-%Y')
        d22=datetime(bjDate1.year,bjDate1.month,bjDate1.day)
        fnumero=days_between(d22, fechaexcel)
        
        if mesnomina!='' and anonomina!='' and mesnomina!=' ' and anonomina!=' ':
            sql="SELECT MEDIDOR_CORRELATIVO,SUBSIDIO FROM SUBSIDIO WHERE MES="+str(numeromesnomina)+ "  AND ANO="+str(anonomina)
            print(sql)
            try:
                cursor.execute(sql)
                for i in cursor.fetchall():

                    sql="UPDATE OPER_LECTURA SET VALOR_SUBSIDIO="+str(i[1])+" WHERE MEDIDOR_CORRELATIVO="+str(i[0])+" AND MES="+str(numeromesnomina)+ "  AND ANO="+str(anonomina)

                    try:
                        cursor.execute(sql)
                        cursor.commit()
                    except Exception as a:
                        print(a)
                
                sql="UPDATE SUBSIDIO SET FECHACARGA="+str(fnumero)+" WHERE MES="+str(numeromesnomina)+ "  AND ANO="+str(anonomina)
                print("fecha carga text " + str(fnumero))
                try:
                    cursor.execute(sql)
                    cursor.commit()
                    aviso="Fecha de carga mes de " + str(mes)+" del "+str(ano)
                    mes=request.POST['mesn']
                    ano=request.POST['anon']
                except Exception as a:
                    print(a)
            except Exception as a:
                print(a)
        else:
            mensaje="Debe seleccionar mes y digitar año"
    if request.method=='POST' and 'imprimir' in request.POST:

        ano=request.POST['ano']
        mes=request.POST['mes']
        numeromes=mesNumero(mes)
        lista=[]
        comuna=""
        titulo=""

        sql="SELECT COMUNA from DATOS_COMITE"

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                comuna=i[0]
        except Exception as a:
            print(a)
        
        #COMUNA Y ORGIN
        sql="SELECT COMUNA,REGION,PROVINCIA,codregion,codcomuna,CODSERVICIO FROM DATOS_COMITE"
                    
        try:
            cursor.execute(sql)
            for datos in cursor.fetchall():
                cod=str(datos[3])+""+str(datos[4])+str(datos[5])
                comuna=str(datos[0])
        except Exception as a:
            print(a)

        sql="SELECT SUBSIDIO.*, OPER_CLIENTE.RUT, OPER_CLIENTE.VER_RUT, OPER_CLIENTE.NOMBRES, OPER_CLIENTE.APELL_PAT, OPER_CLIENTE.APELL_MAT, GLO_SECTOR.GLOSA, GLO_MEDIDOR.NUMDEC, GLO_MEDIDOR.FECDEC, GLO_MEDIDOR.FECENC, GLO_MEDIDOR.PUNTAJE, GLO_MEDIDOR.NUMSOCIO, GLO_MEDIDOR.DVNUM, GLO_MEDIDOR.NUMVIV FROM ((SUBSIDIO INNER JOIN GLO_MEDIDOR ON SUBSIDIO.MEDIDOR_CORRELATIVO = GLO_MEDIDOR.CORRELATIVO) INNER JOIN OPER_CLIENTE ON GLO_MEDIDOR.SOCIO = OPER_CLIENTE.RUT) INNER JOIN (GLO_SECTOR INNER JOIN GLO_CALLE ON GLO_SECTOR.SECTOR = GLO_CALLE.SECTOR) ON OPER_CLIENTE.CALLE_CORRELATIVO = GLO_CALLE.CORRELATIVO WHERE MES="+str(numeromes)+" AND ANO="+str(ano)+";"
        contador=0
        totalcon=0
        totalsub=0
        totalben=0
        totaldeud=0
        totalmon=0

        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                lista.append({'deu':xstr(i[14]),'mon':xstr(i[15]),'sub':xstr(i[8]),'ben':xstr(int(i[6])-int(i[8])),'consumo':xstr(i[3]),'rut':xstr(i[17]),'dv':xstr(i[18]),'nombre':xstr(i[19])+" "+xstr(i[20])+" "+xstr(i[21]),'direccion':xstr(i[22]),'num':xstr(i[23]),'fec':xstr(i[24]),'fecen':xstr(i[25]),'puntaje':xstr(i[26]),'cod':xstr(cod),'dvnum':xstr(i[27]),'numdiv':xstr(i[28])})
                totalcon=totalcon+i[3]
                totalsub=totalsub+i[8]
                totalben=totalben+(int(i[6])-int(i[8]))
                totaldeud=totaldeud+i[14]
                totalmon=totalmon+i[15]
                contador=contador+1
        except Exception as a:
            print(a)
        
        titulo="Listado de Beneficiados mes " + str(mes) +" del ano " + str(ano)

        data={
            'lista':lista,
            'ano':ano,
            'comuna':comuna,
            'Titulo':titulo,
            'total':contador,
            'totalsub':totalsub,
            'totalben':totalben,
            'totaldeud':totaldeud,
            'totalmon':totalmon,
            'totalcon':totalcon
        }

        pdf = render_to_pdf('procesos/reporte.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
    
    if request.method=='POST' and 'eliminar' in request.POST:

        ano=request.POST['ano']
        mes=request.POST['mes']
        numeromes=mesNumero(mes)

        sql="DELETE FROM SUBSIDIO WHERE ANO="+ano+" AND MES="+str(numeromes)
        try:
            cursor.execute(sql)
            cursor.commit()
            
            sql="DELETE FROM REGBENEFICIARIO"
            try:
                cursor.execute(sql)
                cursor.commit()
            except Exception as a:
                print(a)
            mensaje="Se elimino correctamente"
        except Exception as a:
            print(a)
            mensaje="No hay datos para eliminar"

    if request.method=='POST' and 'macro' in request.POST:

        ano=request.POST['ano']
        mes=request.POST['mes']
        numeromes=mesNumero(mes)
        nombrearchivo="A"+ano+"M"+mes+".xls"
        cod=""

        listacod=[]
        listaorigen=[]
        listarut=[]
        listadv=[]
        listapa=[]
        listama=[]
        listanombres=[]
        listadireccion=[]
        listanumdec=[]
        listafecdec=[]
        listatramo=[]
        listafec=[]
        listaunico=[]
        listadvunico=[]
        listanumviv=[]
        listaconsumo=[]
        listamonsub=[]
        listammonco=[]
        listanumdeu=[]
        listamondeud=[]
        listaobs=[]

        listacabezado={
            0:'CODCOM',
            1:'ORIGEN',
            2:'RUT',
            3:'DV-RUT',
            4:'AP. PATERNO',
            5:'AP. MATERNO',
            6:'NOMBRES',
            7:'DIRECCION',
            8:'NUM-DEC',
            9:'FEC-DEC',
            10:'TRAMO RSH',
            11:'FEC-ENC',
            12:'NUMUNICO',
            13:'DV-NUMUNICO',
            14:'NUMVIVTOT',
            15:'CONSUMO',
            16:'MONSUBS',
            17:'MONCOBEN',
            18:'NUMDEUD',
            19:'MONDEUD',
            20:'OBSERVACION',
        }

        j=0
        wb = xlwt.Workbook()
        ws = wb.add_sheet(ano,cell_overwrite_ok=True)

        while j<len(listacabezado):
            ws.write(0,j,listacabezado[j])
            j=j+1
        
        sql="SELECT COMUNA,REGION,PROVINCIA,codregion,codcomuna FROM DATOS_COMITE"
                
        try:
            cursor.execute(sql)
            for datos in cursor.fetchall():
                cod=str(datos[3])+""+str(datos[4])
        except Exception as a:
                    print(a)

        sql="SELECT * FROM REGBENEFICIARIO"
        
        try:
            cursor.execute(sql)
            for i in cursor.fetchall():
                listacod.append(i[0])
                listarut.append(i[22])
                listadv.append(str(i[22])[len(str(i[22])):len(str(i[22]))-1])
                listapa.append(i[24])
                listama.append(i[25])
                listanombres.append(i[23])
                listadireccion.append(i[4])
                listanumdec.append(i[5])
                listafecdec.append(i[6])
                listatramo.append(i[7])
                listafec.append(i[8])
                listaunico.append(i[9])
                listadvunico.append(1)
                listanumviv.append(i[11])
                listaconsumo.append(i[12])
                listamonsub.append(i[14])
                listammonco.append(i[15])
                listanumdeu.append(0)
                listamondeud.append(i[16])
                listaobs.append(i[18])
                
                
                j=1
                n=0  
                while j<=len(listarut):
                    ws.write(j,0,cod)
                    ws.write(j,1,listacod[n])
                    ws.write(j,2,listarut[n])
                    ws.write(j,3,listadv[n])
                    ws.write(j,4,listapa[n])
                    ws.write(j,5,listama[n])
                    ws.write(j,6,listanombres[n])
                    ws.write(j,7,listadireccion[n])
                    ws.write(j,8,listanumdec[n])
                    ws.write(j,9,listafecdec[n])
                    ws.write(j,10,listatramo[n])
                    ws.write(j,11,listafec[n])
                    ws.write(j,12,listaunico[n])
                    ws.write(j,13,listadvunico[n])
                    ws.write(j,14,listanumviv[n])
                    ws.write(j,15,listaconsumo[n])
                    ws.write(j,16,listamonsub[n])
                    ws.write(j,17,listammonco[n])
                    ws.write(j,18,listanumdeu[n])
                    ws.write(j,19,listamondeud[n])
                    ws.write(j,20,listaobs[n])
                    print(listacod)
                    n=n+1
                    j=j+1

        except Exception as a:
            print(a)

        """
        if (os.path.exists('C:\\Macros\\' + nombrearchivo)):
            print("Ya existe.")
        else:
            wb.save('C:\\Macros\\' + nombrearchivo)  
        """

        wb.save('C:\\Macros\\' + nombrearchivo)  

    data={
        'ano':ano,
        'mes':mes,
        'mensaje':mensaje,
        'aviso':aviso
    }
    return render(request, 'procesos/subsidio.html', data)
