$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    cargarIndicadores()
    cargarLinksSolicitudes()
    cargarLinksHistorico()
    cargarLinksHomeInversor()
    cargarLinksAuditoria()
    cargarLinksCrearInversores()
    cargarLinksAdministrarInversores()
    cargarLinksCrearAdministrativos()
    cargarLinksAdministrarAdministrativos()
}

function cargarIndicadores() {
    $.ajax({
        url: '/indicadores',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarIndicadoresSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}

function cargarIndicadoresSuccess(data) {
    
    $('#contenido').html(data.data);
}

// Se cargan links del menú
function cargarLinksHistorico() {
    $('#historicos').click( function () {
        $('#contenido').load('historicos');
    });
}
function cargarLinksHomeInversor() {
    $('#homeInversor').click( function () {
        cargarIndicadores()
    });
}
function cargarLinksAuditoria() {
    $('#auditoria').click( function () {
        $('#contenido').load('auditoria');
    });
}
function cargarLinksCrearInversores() {
    $('#crearInversores').click( function () {
        $('#contenido').load('crearInversores');
    });
}
function cargarLinksAdministrarInversores() {
    $('#administrarInversores').click( function () {
        $('#contenido').load('administrarInversores');
    });
}

function cargarLinksCrearAdministrativos() {
    $('#crearAdministrativos').click( function () {
        $('#contenido').load('crearAdministrativos');
    });
}
function cargarLinksAdministrarAdministrativos() {
    $('#administrarAdministrativos').click( function () {
        $('#contenido').load('administrarAdministrativos');
    });
}

function cargarLinksSolicitudes() {
    $('#solicitudes').click( function () {
       $('#contenido').load('solicitudes');
    });
}/*
function cargarLinksHomeInversor3() {
    $('#homeInversor').click( function () {
        $('#contenido').load('administrarInversores');
    });
} */