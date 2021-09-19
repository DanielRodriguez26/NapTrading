$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    $(`#historicos,
    #homeInversor,
    #auditoria,
    #crearInversores,
    #administrarInversores,
    #crearAdministrativos,
    #solicitudes,
    #administrarAdministrativos,
    #cambiarContrasena,
    #administradores,
    #inversores`).hide();

    cargarLinksPermitidos()
    cargarIndicadores()
    cargarLinks()

}

function cargarLinksPermitidos() {
    $.ajax({
        url: '/permisos',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarLinksPermitidosSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}



function cargarIndicadores() {
    $.ajax({
        url: '/indicadores',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarIndicadoresSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}

function cargarLinksPermitidosSuccess(data){
    
    if (data.data == '2') {
        $(`#historicos,
        #auditoria,
        #crearInversores,
        #administrarInversores,
        #crearAdministrativos,
        #solicitudes,
        #administrarAdministrativos,
        #cambiarContrasena,
        #administradores,
        #inversores`).show()
        $('#contenido').load('solicitudes');
    }else if (data.data == '1') {
        $(`#cambiarContrasena,#homeInversor`).show();
        
        
    }
}
function cargarIndicadoresSuccess(data) {
    
    $('#contenido').html(data.data);
}

// Se cargan links del menú
function cargarLinks() {
    $('#historicos').click( function () {
        $('#contenido').load('historicos');
    });

    $('#homeInversor').click( function () {
        cargarIndicadores()
    });

    $('#auditoria').click( function () {
        $('#contenido').load('auditoria');
    });

    $('#crearInversores').click( function () {
        $('#contenido').load('crearInversores');
    });

    $('#administrarInversores').click( function () {
        $('#contenido').load('administrarInversores');
    });

    $('#crearAdministrativos').click( function () {
        $('#contenido').load('crearAdministrativos');
    });

    $('#administrarAdministrativos').click( function () {
        $('#contenido').load('administrarAdministrativos');
    });

    $('#solicitudes').click( function () {
       $('#contenido').load('solicitudes');
    });

    $('#cambiarContrasena').click( function () {
        $('#contenido').load('cambiarContrasena');
    });
}