$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    cargarIndicadoresUrl()
    retiroganacias()
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
    capital ,totalInvertido, ganancias, gananciasAcumuladas,TotalRetiros,fechaPull
    var capital = formatCurrency(data.capital)
    var ganancias = formatCurrency(data.ganancias)
    var TotalRetiros = formatCurrency(data.TotalRetiros)
    var totalCapital = formatCurrency(data.totalCapital)
    var gananciasAcumuladas = formatCurrency(data.gananciasAcumuladas)
    var totalCapital = formatCurrency(data.totalCapital)
    var totalInvertidoAcumulado = formatCurrency(data.totalInvertidoAcumulado)
    var fechaPull = data.fechaPull

    
    
    $('#capitalInvertido').text(capital);
    $('#ganancias').text(ganancias);
    $('#totalInvertido').text(totalCapital);
    $('#totalInvertidoAcumulado').text(totalInvertidoAcumulado);
    $('#fechaPull').text(fechaPull);
    $('#totalCapital').text(totalCapital);
    $('#TotalRetiros').text(TotalRetiros);
    $('#gananciasAcumuladas').text(gananciasAcumuladas);
    $('#usernameIndicadores').text(`@${data.username}`);
    $('#nombreIndicadores').text(`${data.nombre}`);

    $('#fechaPullinicio').text(`${data.fechaPullinicio}`);
    $('#fechaPullGanancia').text(`Se puede retirar el ${data.fechaPullGanancia}`);
    $('#fechaIvertida').text(`Se puede retirar el ${data.fechaIvertida}`);


    $('#aceptarganancias').click(()=>{retiroganacias('/retirarGanancias')})
    $('#aceptarCapital').click(()=>{retiroganacias('/retirarCapital')})

}

function formatCurrency(value) {

    if(value === '' || value == null || isNaN(value) ){
        return "";
    }
    
    if(typeof value == "string"){
        value = parseInt(value);
    }

    // El formato aplicado es USD - en-ES porque para Local "es-XX" no es posible aplicar formatos a números de 4 cifras
    var myObjCurrency = {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0,
        minimumFractionDigits: 0,
        currencyDisplay: "symbol"
    };
    

    return value.toLocaleString("en-ES", myObjCurrency);
}	



function retiroganacias(url){
    debugger
    var data = new FormData();
    data.append('emailRetiro' , $("#emailRetiro").val());
    data.append('metodoRetiro' ,  $('#metodoRetiro').val());
    data.append('gananciaRetiro' , $("#gananciaRetiro").val());

    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: url,
        success: function (responseJson, status, statusCode) {
            retiroganaciasSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    })
}

function retiroganaciasSuccess(responseJson){
    data = responseJson.data
    if(data.redirect){
        Swal.fire({
            icon: 'success',
            title: 'Bien Hecho',
            text: data.mensaje,
            showConfirmButton: false,
            timer: 1500
        }).then((result) => {
            window.location.href = data.url
        })
    }
    else{
        Swal.fire({
            icon: 'error',
            title: data.mensaje,
            text: data.text,
        })
    }
}