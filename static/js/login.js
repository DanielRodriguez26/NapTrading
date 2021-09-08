window.onload = function() {
    registarEventos()
}

function registarEventos() {
    $('#submit').click(()=>{
        var data = new FormData();
        data.append('usuario' , $("#usuario").val());
        data.append('contrasena' , $("#contrasena").val());
    
        $.ajax({
            url: '/loginVerify',
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            success: function (responseJson, status, statusCode) { cargarLoginVerifySuccess(responseJson, statusCode.status); },
            error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
        });
    })
}


function cargarLoginVerifySuccess(responseJson) {
    debugger
    var data = responseJson.data

    if (data.redirect) {
        Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: 'Bienvenido',
            showConfirmButton: false,
            timer: 1500
        }).then((result) => {
            window.location.href = data.url
        })
    }else{
        Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'Hay un error en la validacion!',
        })
    }

    
}