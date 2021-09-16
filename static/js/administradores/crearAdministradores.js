$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    creaAdministrador()
    limpiar()
}

function creaAdministrador() {
    $('#btnCrear').click( function () {
        var data = new FormData();
        data.append('nombre' , $("#nombre").val());
        data.append('apellidos' , $("#apellidos").val());
        data.append('identificacion' , $("#identificacion").val());
        data.append('telefono' , $("#telefono").val());
        data.append('email' , $("#email").val());
        data.append('pais' , $("#pais").val());

        $.ajax({
            data:data,
            cache: false,
            contentType: false,
            processData: false,
            type: 'POST',
            url: '/crearAdministrador',
            success: function (responseJson, status, statusCode) {
                creaAdministradorSuccess(responseJson, statusCode.status);
            },
            error: function (jqXHR, textStatus, errorThrown) {
                errorConsultandoAPI(jqXHR, textStatus, errorThrown);
            }
        })
    });
}

function creaAdministradorSuccess(responseJson) {
    
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

function limpiar(){
    $('#btnLimpiar').click( function () {
        $("#nombre").val('')
        $("#apellidos").val('')
        $("#identificacion").val('')
        $("#telefono").val('')
        $("#email").val('')
        $("#pais").val('')
    })
    
}