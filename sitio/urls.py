from django.contrib import admin
from django.urls import path

from Riego.viewhome import *
from Riego.viewmantenedor import *
from Riego.viewprocesos  import *
from Riego.viewantecedentes  import *
from Riego.viewcontab import * 
from Riego.viewinformes import * 
from Riego.viewconfiguracion import *

from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('admin/', admin.site.urls),

    #home
    path('home/',viewHome),

    #Mantenedor
    path('mantenedor/tipoagua/',viewTipo),
    path('mantenedor/valor/',viewTarifa),
    path('mantenedor/sector/',viewSectores),
    path('mantenedor/calle_area/', viewCallesArea),
    path('mantenedor/cargo/', viewCargo),
    path('mantenedor/funcionarios/', viewFuncionarios),
    path('mantenedor/proveedor/', viewProveedor),
    path('mantenedor/convenio/',viewConvenioMan),

    path('mantenedor/asociacion/',viewDatos),


    path('mantenedor/tramo1/', viewTramo1),
    path('mantenedor/tramo2/', viewTramo2),
    path('mantenedor/tramo3/', viewTramo3),
    path('mantenedor/tramo4/', viewTramo4),

    #Antecedentes
    path('antecedentes/socios/',viewSocios),
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

    # Informes
    path('informes/',viewInformes),
    path('informes/<id_>/',viewInformesSinModel),

    #Contabilidad
    path('contabilidad/plancuenta/egreso/',viewPlanCuentaE),
    path('contabilidad/plancuenta/ingreso/',viewPlanCuentaI),
    path('contabilidad/plancuenta/pdf/',viewpdf),

    path('egresos/lista/',listarDetalleE),

    path('contabilidad/comprobante/egresos/',viewEgresos),
    path('contabilidad/ingreso/', viewIngresos), 
    path('contabilidad/saldofavor/', viewSaldoFavor),
    path('contabilidad/saldofavor/historial/', viewSaldoFavorH),

    #Configuración
    path('configuracion/eliminar_abono/', viewEliminar_abono),
    path('configuracion/condonacion/', viewCodonacion),
    path('configuracion/mensaje/', viewMensaje), 
    path('configuracion/contraseña/', viewContraseña), 
    path('configuracion/respaldar_info/', viewRespaldo_info),
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

]
