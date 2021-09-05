window.onload = function() {

    registarEventos()

}
function registarEventos() {
        
    cargarLinks()

}


function cargarLinks() {
    $('#usuarios').click( function () {
        alert('Hola')
        $('#contenido').load('usuarios');
    });
}

function cargarIndicadores(params) {
    $.ajax({
        url: '/indicadores',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarIndicadoresSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}


