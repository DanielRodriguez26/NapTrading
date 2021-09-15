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
    cargarSolicitudesTablaSuccess()
    
}

function cargarSolicitudesTablaSuccess() {
    $('#tbltableSolicitudes').empty().append(`
    <table class="table table-striped" id="tableSolicitud">`);
    //deleting operators to reset
    
    $tblSolicitudes = $('#tableSolicitud').DataTable({
        responsive: true,
        searching: false,
        language: espanol,
        info: false,
        bLengthChange: false,
        processing: false,
        serverSide: true,
        pageLength: 10,
        columnDefs: [
            { orderable: true, targets: 0 }
        ],
        order: [[0, 'asc']],
        ajax: {
            type: 'POST',
            url: '/solicitudesTabla',
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
            title: "Email Solicitud",
            "data-label": "Email Solicitud",
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
            title: "Fecha",
            "data-label": "Fecha",
            "data": "fecha",
            "orderable": true,
        },
        {
            title: "Acción",
            "data-label": "Acción",
            "data": "tipoMovimiento",
            "orderable": true,
        },
        {
            title: "Monto",
            "data-label": "Monto",
            "data": "monto",
            "orderable": true,
        },
        {
            title: "Fecha Limite",
            "data-label": "Fecha Limite",
            "data": "fechaLimite",
            "orderable": true,
        },
        {
            title: "Metodo Desembolso",
            "data-label": "Metodo Desembols",
            "data": "metodo_desembolso",
            "orderable": true,
        },
        {
            title: "Marcar Concluido",
            "data": "movimiento_id",
            "orderable": false,
            "render": (movimiento_id, type, administrador) => {
                var respuesta = '';

                if (movimiento_id) {
                    
                    respuesta += `<button data-id="${movimiento_id}" class="badge bg-warning finalizar-ticket">Finalizar Ticket</button>`;
                }
                return respuesta;
            }
        }
        ],
        'drawCallback': () => {
            // Create an array of labels containing all table headers
            var labels = [];
            $('#tableSolicitud thead th').each(function () {
                labels.push($(this).text());
            });

            // Add data-label attribute to each cell
            $('#tableSolicitud tbody tr').each(function () {
                $(this).find('td').each(function (column) {
                    $(this).attr('data-label', labels[column]);
                });
            });
            $('.finalizar-ticket').click((e) => {  
                debugger              
                let movimiento_id = e.currentTarget.getAttribute('data-id');
                finalizarTicket(movimiento_id)
            });
            
        }
    });
}

function finalizarTicket(movimiento_id) {

    var data = new FormData();
    data.append('movimientoID' , movimiento_id);
    $.ajax({
        data:data,
        cache: false,
        contentType: false,
        processData: false,
        type: 'POST',
        url: '/finalizarTicket',
        success: function (responseJson, status, statusCode) {
            finalizarTicketSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    })

}

function  finalizarTicketSuccess(responseJson) {
    
    var data = responseJson.data
    username = data.username
    contra = data.contra
    mensaje = data.mensaje
    if (data.redirect) {
        Swal.fire({
            icon: 'success',
            title: 'Ticket Finalizado',
            text: `Se ha finalizado el ticket de manera exitosa`,
        }).then((result) => {
            $('#contenido').load('solicitudes');
        })
    } else {
        Swal.fire({
            icon: 'error',
            title: mensaje,
            
        })
    }

}
