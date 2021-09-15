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
    cargarAuditoriaTablaSuccess()
    
}

function cargarAuditoriaTablaSuccess() {
    $('#tblAuditoria').empty().append(`
    <table class="table table-striped" id="tableAuditoria"></table>
`);
    //deleting operators to reset
    
    $tblAuditoria = $('#tableAuditoria').DataTable({
        responsive: true,
        language: espanol,
        info: false,
        bLengthChange: false,
        processing: false,
        serverSide: true,
        pageLength: 10,
        ajax: {
            type: 'POST',
            url: '/auditoriaTabla',
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
            title: "Fecha",
            "data-label": "Fecha",
            "data": "fecha",
            "orderable": true,
        },
        {
            title: "Accion",
            "data-label": "Accion",
            "data": "accion",
            "orderable": true,

        },
        {
            title: "Descripcion",
            "data-label": "Descripcion",
            "data": "descripcion",
            "orderable": true,
        },
        ],
        'drawCallback': () => {
            // Create an array of labels containing all table headers
            var labels = [];
            $('#tableAuditoria thead th').each(function () {
                labels.push($(this).text());
            });

            // Add data-label attribute to each cell
            $('#tableAuditoria tbody tr').each(function () {
                $(this).find('td').each(function (column) {
                    $(this).attr('data-label', labels[column]);
                });
            });
            $('#myInput').on( 'keyup', function () {
                table.search( this.value ).draw();
            });
        }
    });

}

