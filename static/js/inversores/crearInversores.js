$(document).ready(() => {
    registarEventos()
})

function registarEventos() {
    creaInversor()
}

function creaInversor() {
    $('#btnCrear').click(function () {

        if (inputIsValid()) {
            var data = new FormData();
            data.append('nombre', $("#nombre").val());
            data.append('apellidos', $("#apellidos").val());
            data.append('identificacion', $("#identificacion").val());
            data.append('telefono', $("#telefono").val());
            data.append('email', $("#email").val());
            data.append('pais', $("#pais").val());
            data.append('capital', $("#capital").val());


            $.ajax({
                url: '/crearInversor',
                data: data,
                type: 'POST',
                cache: false,
                contentType: false,
                processData: false,
                success: function (responseJson, status, statusCode) {

                    creaInversorSuccess(responseJson, statusCode.status);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    errorConsultandoAPI(jqXHR, textStatus, errorThrown);
                }
            })
        }


    });
}


function inputIsValid() {

    if ($("#nombre").val() == '') {
        alerta()
        $('#apellidos').focus();
        return false;
    }

    if ($("#apellidos").val() == '') {
        alerta()
        $('#apellidos').focus();
        return false;
    }

    if ($("#telefono").val() == '') {
        alerta()
        $('#telefono').focus();
        return false;
    }

    if ($("#identificacion").val() == '') {
        alerta()
        $('#identificacion').focus();
        return false;
    }

    if ($("#email").val() == '') {
        alerta()
        $('#email').focus();
        return false;
    }

    if ($("#pais").val() == '') {
        alerta()
        $('#pais').focus();
        return false;
    }

    if ($("#capital").val() == '') {
        alerta()
        $('#capital').focus();
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



function creaInversorSuccess(responseJson) {
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