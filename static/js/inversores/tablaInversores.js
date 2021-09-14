var espanol = {
    sLengthMenu: "Mostrar _MENU_ registros",
    sZeroRecords: "No se encontraron resultados",
    sEmptyTable: "",
    sInfo: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
    sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
    sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
    sInfoPostFix: "",
    sSearch: "Buscar:",
    sUrl: "",
    sInfoThousands: ",",
    sLoadingRecords: "Cargando...",
    oPaginate: {
        sFirst: "Primero",
        sLast: "Último",
        sNext: "Siguiente",
        sPrevious: "Anterior",
    },
    oAria: {
        sSortAscending: ": Activar para ordenar la columna de manera ascendente",
        sSortDescending: ": Activar para ordenar la columna de manera descendente",
    },
    buttons: {
        copy: "Copiar",
        colvis: "Visibilidad",
    }
};
$(document).ready(()=> {
    registarEventos()
})
function registarEventos() {
    $('#modalCapital').modal('hide');
    cargarAdministrativosTablaSuccess()
    
}

function cargarAdministrativosTablaSuccess() {
    $('#tblInversores').empty().append(`
    <table class="table table-striped" id="tableInversores">
`);
    //deleting operators to reset
    
    $tblOperadores = $('#tableInversores').DataTable({
        responsive: true,
        searching: false,
        language: espanol,
        info: false,
        bLengthChange: false,
        processing: false,
        serverSide: true,
        pageLength: 10,
        ajax: {
            type: 'POST',
            url: '/administrarInversoresTabla',
        },
        columns: [{
            title: "Nombre",
            "data-label": "Nombre",
            "data": "nombre",
            "orderable": true,
        },
        {
            title: "Identificación",
            "data-label": "Identificación",
            "data": "identificacion",
            "orderable": true,
        },
        {
            title: "Email",
            "data-label": "Email",
            "data": "email",
            "orderable": true,
        },
        {
            title: "Teléfono",
            "data-label": "Teléfono",
            "data": "telefono",
            "orderable": true,

        },
        {
            title: "Pais",
            "data-label": "Pais",
            "data": "pais",
            "orderable": true,
        },
        {
            title: "Agregar Capital",
            "data": "usuario_id",
            "orderable": false,
            'className': 'table-dibanka__column table-dibanka__column--button',
            "render": (usuario_id, type, administrador) => {
                var respuesta = '';

                if (usuario_id) {
                    
                    respuesta += `
                            <button data-id="${usuario_id}" class="badge bg-success agregar-capital">Agregar Capital</button>
                        `;
                }
                return respuesta;
            }
        },
        {
            title: "Restaurar Contraseña",
            "data": "usuario_id",
            "orderable": false,
            'className': 'table-dibanka__column table-dibanka__column--button',
            "render": (usuario_id, type, administrador) => {
                var respuesta = '';

                if (usuario_id) {
                    
                    respuesta += `
                            <button data-id="${usuario_id}" class="badge bg-warning cambiar-contrasena">Cambiar contraseña</button>
                        `;
                }
                return respuesta;
            }
        }
        ],
        'drawCallback': () => {
            // Create an array of labels containing all table headers
            var labels = [];
            $('#tableInversores thead th').each(function () {
                labels.push($(this).text());
            });

            // Add data-label attribute to each cell
            $('#tableInversores tbody tr').each(function () {
                $(this).find('td').each(function (column) {
                    $(this).attr('data-label', labels[column]);
                });
            });

            $('.cambiar-contrasena').click((e) => {
                
                let usuario_id = e.currentTarget.getAttribute('data-id');
                cambiarContrasena(usuario_id)
            });
            $('.agregar-capital').click((e) => {
                
                let usuario_id = e.currentTarget.getAttribute('data-id');
                agregarCapitalModal(usuario_id)
            });
        }
    });
}

function cambiarContrasena(usuario_id) {

    var data = new FormData();
    data.append('usuario' , usuario_id);

    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/editarAdministrador',
        success: function (responseJson, status, statusCode) {
            cambiarContrasenaSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    })

}

function cambiarContrasenaSuccess(responseJson) {
    
    var data = responseJson.data
    username = data.username
    contra = data.contra
    mensaje = data.mensaje
    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Cambio de Contraseña',
            text: `Para ${username}  la contraseña es: ${contra}`,
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

function agregarCapitalModal(usuario_id) {

    $('#modalCapital').modal('show')

    $('#guardarCapital').click(()=>{
        agregarCapital(usuario_id)
    })
}

function agregarCapital(usuario_id) {
    var data = new FormData();
    data.append('usuario' , usuario_id);
    data.append('capital' , $('#montoCapital').val())

    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/agregarCapital',
        success: function (responseJson, status, statusCode) {
            cambiarContrasenaSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    })
}
