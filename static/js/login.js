window.onload = function () {
    registarEventos()
}

function registarEventos() {
    $('#submit').click(() => {
        var data = new FormData();
        data.append('usuario', $("#usuario").val());
        data.append('contrasena', $("#contrasena").val());
        $.ajax({
            url: '/loginVerify',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function (responseJson, status, statusCode) {
                cargarLoginVerifySuccess(responseJson, statusCode.status);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                errorConsultandoAPI(jqXHR, textStatus, errorThrown);
            }
        });
    })
}


function cargarLoginVerifySuccess(responseJson) {
    
    var data = responseJson.data

    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Bienvenido',
            text: data.nombre,
            showConfirmButton: false,
            timer: 1500
        }).then((result) => {
            window.location.href = data.url
        })
    } else if(data.bloqueo) {
        Swal.fire({
            icon: 'error',
            title: 'Usuario Bloqueado',
            text: data.text,
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Hay un error en la validacion!',
        })
    }

}