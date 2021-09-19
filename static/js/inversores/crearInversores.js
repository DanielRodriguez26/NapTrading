$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    creaInversor()
}

function creaInversor() {
    $('#btnCrear').click( function () {
        var data = new FormData();
        data.append('nombre' , $("#nombre").val());
        data.append('apellidos' , $("#apellidos").val());
        data.append('identificacion' , $("#identificacion").val());
        data.append('telefono' , $("#telefono").val());
        data.append('email' , $("#email").val());
        data.append('pais' , $("#pais").val());
        data.append('capital' , $("#capital").val());


        $.ajax({
            data:data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            url: '/crearInversor',
            success: function (responseJson, status, statusCode) {
                creaInversorSuccess(responseJson, statusCode.status);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                errorConsultandoAPI(jqXHR, textStatus, errorThrown);
            }
        })
    });
}


function creaInversorSuccess(responseJson) {
    debugger
    var data = responseJson.data
    username = data.username
    contra = data.contra
    mensaje = data.mensaje
    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Bien Hecho',
            text: `Tu nombre de usuario es: ${username} y la contraseña es: ${contra}`,
        }).then((result) => {
            window.location.href = data.url
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: mensaje,
            
        })
    }

}