window.onload = function() {
    registarEventos()
}
function registarEventos() {
    cargarLinks()
    cargarIndicadores()

}


function cargarLinks() {
    $('#usuarios').click( function () {
        alert('Hola')
        $('#contenido').load('usuarios');
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

function cargarIndicadoresSuccess(data) {
    $('#contenido').html(data.data);
}


