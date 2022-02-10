$(document).ready(()=> {
    registarEventos()
})

function registarEventos() {
    $('#editar_inversor').click((e)=>{
        actualizarInversor()
    });
    $('#editar_capital').click((e)=>{
        actualizarCapital()
    });
    cargarInversoresSuccess()
}

function cargarInversoresSuccess(){
    const usuario = $('#usuario').val()
    var data = new FormData();
    data.append('usuario' , usuario);

    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/editarInversorConsulta',
        success: function (responseJson) {
            cargarInversores(responseJson)
        },
    })
}

function cargarInversores(responseJson){
    debugger
    let{
        nombres,
        apellidos,
        identificacion,
        email,
        telefono,
        fecha_inicio_pool,
        pais,
        capital,
        ganancia,
        porcentaje_ganancias
    }= responseJson.data[0]
    
    $('#nombres').val(nombres)
    $('#apellidos').val(apellidos)
    $('#identificacion').val(identificacion)
    $('#email').val(email)
    $('#telefono').val(telefono)
    $('#fecha_inicio_pool').val(fecha_inicio_pool)
    $('#pais').val(pais)
    $('#capital').val(capital)
    $('#ganancia').val(ganancia)
    $('#porcentaje_ganancias').val(porcentaje_ganancias)
}

function actualizarInversor(){
    
    const usuario = $('#usuario').val()
    var data = new FormData();
    data.append('nombres',$('#nombres').val())
    data.append('apellidos',$('#apellidos').val())
    data.append('identificacion',$('#identificacion').val())
    data.append('email',$('#email').val())
    data.append('telefono',$('#telefono').val())
    data.append('pais',$('#pais').val())
    data.append('usuario' , usuario);
    
    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/actualizarInversor',
        success: function (responseJson) {
            actualizarInversorSuccess(responseJson)
        },
    })
}

function actualizarCapital(){
    
    const usuario = $('#usuario').val()
    var data = new FormData();
    data.append('nombres',$('#nombres').val())
    data.append('apellidos',$('#apellidos').val())
    data.append('identificacion',$('#identificacion').val())
    data.append('email',$('#email').val())
    data.append('telefono',$('#telefono').val())
    data.append('pais',$('#pais').val())
    data.append('capital',$('#capital').val())
    data.append('ganancia',$('#ganancia').val())
    data.append('porcentaje_ganancias',$('#porcentaje_ganancias').val())
    data.append('fecha_inicio_pool',$('#fecha_inicio_pool').val())
    data.append('usuario' , usuario);
    
    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/actualizarCapital',
        success: function (responseJson) {
            actualizarInversorSuccess(responseJson)
        },
    })
}


function actualizarInversorSuccess(responseJson) {
    var data = responseJson.data

    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Bien Hecho',
            text: `Se a actualizado corretamente los datos del inversor`,
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


