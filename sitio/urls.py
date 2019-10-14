from django.contrib import admin
from django.urls import path

from AprGes.viewsubsidio import *
from AprGes.viewhome import *
from AprGes.viewmantenedor import *
from AprGes.viewprocesos  import *
from AprGes.viewantecedentes  import *
from AprGes.viewcontab import * 
from AprGes.viewinformes import * 
from AprGes.viewconfiguracion import *

from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #home
    path('home/',viewHome),

    #Mantenedor
    path('mantenedor/tipoagua/',viewTipo),
    path('mantenedor/valor/',viewTarifa),
    path('mantenedor/tramo1/', viewTramo1),
    path('mantenedor/tramo2/', viewTramo2),
    path('mantenedor/tramo3/', viewTramo3),
    path('mantenedor/tramo4/', viewTramo4),
    path('mantenedor/sector/',viewSectores),
    path('mantenedor/calle_area/', viewCallesArea),
    path('mantenedor/cargo/', viewCargo),
    path('mantenedor/funcionarios/', viewFuncionarios),
    path('mantenedor/medidor/', viewMedidor),
    path('mantenedor/proveedor/', viewProveedor),
    path('mantenedor/convenio/',viewConvenioMan),
    path('mantenedor/asociacion/',viewDatos),

    #Antecedentes
    path('antecedentes/socios/',viewSocios),
    path('antecedentes/instalacion_medidor/', viewInstalacion),
    path('antecedentes/consumo_estanque/', viewEstanque), 
    path('antecedentes/orden_trabajo/', viewOrden_trabajo),
    path('reportes/orden/', orden),

    #Procesos
    path('procesos/consumo/id/',viewID),
    path('procesos/consumo/id3/',viewID3),

    path('procesos/consumo/',viewConsumo),
    path('procesos/convenios/',viewConvenio),
    path('procesos/convenios/masivos/',viewConvenioMasivos),

    path('procesos/generacion/',viewGeneracion),
    path('procesos/pagos/', viewPagos),    
    path('procesos/historial_cliente/<id_>/<ano_>/', historial_cliente),
    path('procesos/historial_cliente/', historialcliente),
    #path('reportes/cuenta_ind/', cuenta_ind),
    path('procesos/factura/',viewFactura),
    path('historialcliente/<id_>/<ano_>/',pdfhistorialcliente),

    path('procesos/historial_cliente///', errorhistorial),

    path('procesos/boleta_libre/', viewBoletaLibre),
    path('procesos/cancelar_boleta/', viewCancelarBoleta),
    path('procesos/cierre_periodo/', viewCierrePeriodo),
    path('procesos/factura_libre/', viewFacturaLibre),
    path('procesos/ingreso_lectura/', viewIngresoLectura),
    path('procesos/lectura_rapida/', viewLectura_rapida),
    path('procesos/subsidio/', subsidio),
    path('subsidio/carga/', Cargasubsidio),

    # Informes
    path('informes/informes/',viewInformes),
    path('informes/<id_>/',viewInformesSinModel),
    path('informes/consultas/medidor/',viewConsultasMedidor),
    path('informes/consultas/lectura/',viewConsultasLectura),
    path('informes/cuentas/ind/',viewCuentasInd),
    path('informes/toma/lectura/',viewTomaLectura),
    path('informes/registro/financiero/',viewRegistroFinanciero),
    path('informes/consultas/corte/',viewConsultasCorte), 
 

    #Contabilidad
    path('contabilidad/plancuenta/egreso/',viewPlanCuentaE),
    path('contabilidad/plancuenta/ingreso/',viewPlanCuentaI),
    path('contabilidad/plancuenta/pdf/',viewpdf),

    path('egresos/lista/',listarDetalleE),

    path('contabilidad/comprobante/egresos/',viewEgresos),
    path('contabilidad/comprobante/ingreso/', viewIngresos), 
    path('contabilidad/saldofavor/', viewSaldoFavor),
    path('contabilidad/saldofavor/historial/', viewSaldoFavorH),
    path('contabilidad/libro_venta/', viewLibroVenta),
    path('contabilidad/arqueo_caja/', viewArqueoCaja),
    path('contabilidad/cuenta_corriente/', viewCuentaCorriente),
    path('contabilidad/conciliacion_bancaria/', viewConciliacionBancaria),
    path('contabilidad/reporte/', BenSubsidio),


    #Configuración
    path('configuracion/eliminar_abono/', viewEliminar_abono),
    path('configuracion/condonacion/', viewCodonacion),
    path('configuracion/mensaje/', viewMensaje), 
    path('configuracion/contraseña/', viewContraseña), 
    path('configuracion/respaldar_info/', viewRespaldo_info),
    path('configuracion/arregla_datos/', viewArreglaDatos),
    path('configuracion/mensaje_cobro/', viewMensajeCobro),
    path('configuracion/crear_usuario/', viewCrearUsuario),
    path('configuracion/avisos_vigentes/', viewAvisosVigentes),
    path('configuracion/boletas_vigentes/', viewBoletas_vigentes),

    #Reportes
    path('reportes/',viewReportes),
    path('imprimiendo/abono/<id_>/',imprimiendoAbono),

    #Historiales
    path('antecedentes/orden_trabajo/historial/',historialOrden),
    path('procesos/factura/historial/',historialFactura),
    path('contabilidad/plancuenta/egreso/historial/',historialEgresos),
    path('contabilidad/plancuenta/ingresos/historial/',historialIngresos),
    path('configuracion/condonacion/historial/', historialCondonacion),



    path('reportes/1/', informe1),
    path('reportes/2/', informe2),
    path('reportes/3/', informe3),
    path('reportes/4/', informe4),
    path('reportes/5/', informe5),
    path('reportes/5/', informe5),
    path('reportes/6/', informe6),
    path('reportes/7/', informe7),
    path('reportes/8/', informe8),
    path('reportes/9/', informe9),
    path('reportes/10/', informe10),
    path('reportes/11/', informe11),
    path('reportes/12/', informe12),
    path('reportes/13/', informe13),
    path('reportes/14/', informe14),
    path('reportes/15/', informe15),
    path('reportes/16/', informe16),
    path('reportes/17/', informe17),
    path('reportes/18/', informe18),
    path('reportes/19/', informe19),
    path('reportes/20/', informe20),
    path('reportes/21/', informe21),
    path('reportes/43/', informe43),
    path('reportes/aviso/', informeAviso),
    path('reportes/convenio/', informeConvenio),
    path('reportes/cuenta_individual/', informeCuenta_ind),
    path('reportes/egreso/', informeEgreso),
    path('reportes/factura/', informeFactura),
    path('reportes/ingreso/', informeIngreso),
    path('reportes/orden/', informeOrden),
    path('reportes/plan/', informePlan),
    path('configuracion/condonacionrpt/', informeCondonacionrpt),
    path('contabilidad/saldo/', informeSaldo),
    path('procesos/reporte/', informeReporte),
]
