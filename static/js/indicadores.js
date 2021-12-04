$(document).ready(() => {
    registarEventos()
})

function registarEventos() {
    cargarIndicadoresUrl()

}

function cargarIndicadoresUrl() {
    $.ajax({
        url: '/indicadoresUrl',
        type: 'GET',
        success: function (responseJson, status, statusCode) {
            cargarIndicadoresUrlSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    });
}

function cargarIndicadoresUrlSuccess(data) {
    var data = data.data
    capital, totalInvertido, ganancias, gananciasAcumuladas, TotalRetiros, fechaPull
    var capital = formatCurrency(data.capital)
    var ganancias = formatCurrency(data.ganancias)
    var TotalRetiros = formatCurrency(data.TotalRetiros)
    var totalCapital = formatCurrency(data.totalCapital)
    var gananciasAcumuladas = formatCurrency(data.gananciasAcumuladas)
    var totalInvertido = formatCurrency(data.totalInvertido)
    var totalInvertidoAcumulado = formatCurrency(data.totalInvertidoAcumulado)
    var fechaPull = data.fechaPull



    $('#capitalInvertido').text(capital);
    $('#ganancias').text(ganancias);
    $('#totalInvertido').text(totalInvertido);
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
    if (data.check == 1) {
        $('#reinvertir_ganancias').attr('checked', 'checked');
    }



    $('#aceptarganancias').click(() => {
        const gananciaRetiro = $('#gananciaRetiro').val()
        const emailRetiro = $('#emailRetiro').val()
        const metodoRetiro = $('#metodoRetiro').val()
        retiroganacias('/retirarGanancias', gananciaRetiro, metodoRetiro, emailRetiro)
    })
    $('#aceptarCapital').click(() => {
        const gananciaRetiro = $('#capitalRetiro').val()
        const emailRetiro = $('#capitalEmailRetiro').val()
        const metodoRetiro = $('#capitalMetodoRetiro').val()
        retiroganacias('/retirarCapital', gananciaRetiro, metodoRetiro, emailRetiro)
    })

    $('#reinvertir_ganancias').on("click", () => {
        debugger
        var condiciones = $("#reinvertir_ganancias").is(":checked");
        if (condiciones) {
            reuinvertirGanancias(1)
        } else {
            reuinvertirGanancias(0)
        }
    });

}

function formatCurrency(value) {

    if (value === '' || value == null || isNaN(value)) {
        return "";
    }

    if (typeof value == "string") {
        value = parseInt(value);
    }

    // El formato aplicado es USD - en-ES porque para Local "es-XX" no es posible aplicar formatos a números de 4 cifras
    var myObjCurrency = {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 2,
        minimumFractionDigits: 2,
        currencyDisplay: "symbol"
    };


    return value.toLocaleString("en-ES", myObjCurrency);
}



function retiroganacias(url, gananciaRetiro, metodoRetiro, emailRetiro) {

    if (inputIsValid(gananciaRetiro, emailRetiro)) {
        var data = new FormData();
        data.append('emailRetiro', emailRetiro);
        data.append('metodoRetiro', metodoRetiro);
        data.append('gananciaRetiro', gananciaRetiro);

        $.ajax({
            data: data,
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

}

function retiroganaciasSuccess(responseJson) {
    data = responseJson.data
    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Bien Hecho',
            text: data.mensaje,
            showConfirmButton: false,
            timer: 1500
        }).then((result) => {
            window.location.href = data.url
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: data.mensaje,
            text: data.text,
        })
    }
}

function reuinvertirGanancias(estado) {
    $.ajax({
        data: {
            estado: estado
        },
        cache: false,
        type: 'POST',
        url: '/reuinvertirGanancias',
        success: function (responseJson, status, statusCode) {
            Swal.fire({
                icon: 'success',
                title: 'Bien Hecho',
                text: 'Has seleccionado el campo de reinvertir',
                showConfirmButton: false,
                timer: 1500
            })
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    })
}


function inputIsValid(gananciaRetiro,  emailRetiro) {

    if (emailRetiro == '') {
        alerta()
        return false;
    }

    if (gananciaRetiro == '') {
        alerta()
        return false;
    }
    return true;
}

function alerta(params) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })

    Toast.fire({
        icon: 'error',
        title: 'Debe ingresar el camapo solicitado'
    })
}