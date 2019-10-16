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
    path('mantenedor/tarifas/<id_>/', viewTramo),
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
    






    


    path('repotros/0/', view0_EncuestaMovContable),
    path('repotros/1.1/', view1_1LibroCajaIngreso),
    path('repotros/1.2/', view1_2LibroCajaEgreso),
    path('repotros/2/', view2_NominaUsuarioPagosPendientes),
    path('repotros/3/', view3_NominaUsuariosPagoDia),
    path('repotros/4/', view4_RegistroMedidoresSinLectura),
    path('repotros/5/', view5_ListBoletasIngresados),
    path('repotros/6/', view6_ListAbonosIngresados),
    path('repotros/7/', view7_ListComprobantesIngresados),
    path('repotros/8/', view8_ListComprobantesEgresados),
    path('repotros/9/', view9_ListFacturasEmitidas),
    path('repotros/10/', view10_ListFacturasPendientes),
    path('repotros/12/', view12_ListMedidoresCorte),
    path('repotros/13/', view13_ListMedidoresSuspender),
    path('repotros/14/', view14_ListMedidoresRetiro),
    path('repotros/15/', view15_ListadoFacturacion),
    path('repotros/16/', view16_RangoConsumoAño),
    path('repotros/17/', view17_FormatoPlantillaControl),
    path('repotros/18/', view18_EstadisticasMedidores),
    path('repotros/19/', view19_ListadoLecturaMedidoresMes),
    # path('repotros/20/', ),
    path('repotros/21/', view21_UsuariosAsociadoSocio),
    # path('repotros/20/', ),
    path('repotros/24/', view24_ControlArranquesSector),
    # path('repotros/25/', ),
    # path('repotros/26/', ),
    # path('repotros/27/', ),
    # path('repotros/28/', ),
    # path('repotros/29/', ),
    # path('repotros/30/', ),
    # path('repotros/31/', ),
    # path('repotros/32/', ),
    # path('repotros/33/', ),
    # path('repotros/34/', ),
    # path('repotros/35/', ),
    path('repotros/36/', view36_CartaRenuncia),
    # path('repotros/37/', ),
    path('repotros/38/', view38_ListadoSocioOrdenGeografico),
    # path('repotros/39/', ),
    # path('repotros/40/', ),
    # path('repotros/41/', ),
    # path('repotros/42/', ),
    # path('repotros/43/', ),
    path('repotros/44/', view44_ListadoMedidoresNoDisponibles),
    # path('repotros/45/', ),
    # path('repotros/46/', ),
    # path('repotros/47/', ),
    # path('repotros/48/', ),
    # path('repotros/49/', ),
]
