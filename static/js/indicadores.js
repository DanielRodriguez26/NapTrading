$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    cargarIndicadoresUrl()
}

function cargarIndicadoresUrl() {
    $.ajax({
        url: '/indicadoresUrl',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarIndicadoresUrlSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}

function cargarIndicadoresUrlSuccess(data) {
    var data =data.data
    
    $('#usernameIndicadores').text(`@${data.username}`);
    $('#nombreIndicadores').text(`${data.nombre}`);
}