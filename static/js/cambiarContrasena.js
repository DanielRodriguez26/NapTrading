$(document).ready(()=>{
    registarEventos()
})

function registarEventos() {
    validarContrasenas()
    cambiarContrasena()
    limpiar()
}

function validarContrasenas(){
    const nuevaContrasena = document.getElementById('nuevaContrasena');
    nuevaContrasena.addEventListener('keyup', function (event) {
        validate()
    });
    const confirmarContrasena = document.getElementById('confirmarContrasena');
    confirmarContrasena.addEventListener('keyup', function (event) {
        validate()
    });
    function validate () {
        if ( nuevaContrasena.checkValidity() ) {
            $("#messageValidarContrasena").css("display","none");
        } else {
            $("#messageValidarContrasena").css("display","block");
        }
        if ( confirmarContrasena.value == nuevaContrasena.value ) {
            $("#messageValidarContrasena2").css("display","none");
        } else {
            $("#messageValidarContrasena2").css("display","block");
        }
    }
}

function cambiarContrasena() {
    $('#btnCambiar').click( function () {
        var data = new FormData();
        data.append('contrasena' , $("#contrasena").val());
        data.append('nuevaContrasena' , $("#nuevaContrasena").val());
        data.append('confirmarContrasena' , $("#confirmarContrasena").val());
        
        const nuevaContrasena = document.getElementById('nuevaContrasena');
        const confirmarContrasena = document.getElementById('confirmarContrasena');
          
        if ( nuevaContrasena.checkValidity() ) {
            if(nuevaContrasena.value == confirmarContrasena.value){
                $.ajax({
                    data:data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    type: 'POST',
                    url: '/cambiarContrasenaLogica',
                    success: function (responseJson, status, statusCode) {
                        cambiarContrasenaSuccess(responseJson, statusCode.status);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        errorConsultandoAPI(jqXHR, textStatus, errorThrown);
                    }
                })
            }else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al validar la información',
                    text: `La nueva contraseña debe ser igual a la confirmación`,
                    
                })
            }

        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error al validar la información',
                text: `La contraseña debe tener minimo 8 caracteres, incluyendo al menos una mayúscula, minúscula y un número.`,
            })
        }
        
    });
}

function cambiarContrasenaSuccess(responseJson) {
    
    var data = responseJson.data
    username = data.username
    contra = data.contra
    mensaje = data.mensaje
    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Bien Hecho',
            text: `Tu contraseña ha sido cambiada con exito`,
        }).then((result) => {
            window.location.href = data.url
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: `Ha ocurrido un error al validar la información`,
            
        })
    }

}

function limpiar(){
    $('#btnLimpiar').click( function () {
        $("#contrasena").val('')
        $("#nuevaContrasena").val('')
        $("#confirmarContrasena").val('')
    })
    
}

/*
if ( nuevaContrasena.checkValidity() ) {

            if(nuevaContrasena === confirmarContrasena){
                $.ajax({
                    data:data,
                    cache: false,
                    contentType: false,
                    processData: false,
                    type: 'POST',
                    url: '/cambiarContrasenaLogica',
                    success: function (responseJson, status, statusCode) {
                        creaAdministradorSuccess(responseJson, statusCode.status);
                    },
                    error: function (jqXHR, textStatus, errorThrown) {
                        errorConsultandoAPI(jqXHR, textStatus, errorThrown);
                    }
                })
            }else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error al validar la información',
                    text: `La nueva contraseña debe ser igual a la confirmación`,
                    
                })
            }

        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error al validar la información',
                text: `La contraseña debe tener minimo 8 caracteres, incluyendo al menos una mayúscula, minúscula y un número.`,
            })
        }
        
    });
}
*/