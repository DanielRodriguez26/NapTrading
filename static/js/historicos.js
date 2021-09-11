window.onload = function() {
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

    registarEventos()
}
function registarEventos() {
    cargarHistoricosTablaSuccess()
    cargarIndicadoresHistoricos()
}

function cargarIndicadoresHistoricos(params) {
    $.ajax({
        url: '/indicadoresHistoricos',
        type: 'GET',
        success: function (responseJson, status, statusCode) { cargarIndicadoresHistoricosSuccess(responseJson, statusCode.status); },
        error: function (jqXHR, textStatus, errorThrown) { errorConsultandoAPI(jqXHR, textStatus, errorThrown); }
    });
}
function cargarIndicadoresHistoricosSuccess(responseJson) {
    data = responseJson
}

function cargarHistoricosTablaSuccess() {
    $('#tblHistoricos').empty().append(`
    <table class="table table-striped" id="tableHistopricos">
`);
    //deleting operators to reset
    
    $tblOperadores = $('#tableHistopricos').DataTable({
        lengthMenu: [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        responsive: true,
        searching: false,
        language: espanol,
        info: false,
        bLengthChange: false,
        processing: false,
        serverSide: true,
        pageLength: 5,
        columnDefs: [
            { orderable: true, targets: 0 }
        ],
        order: [[0, 'asc']],
        ajax: {
            type: 'POST',
            url: '/historicosTabla',
        },
        columns: [{
            title: "OPERADOR",
            "data": "nombre",
            'className': 'fullTitle table-dibanka__column table-dibanka__column--normal table-dibanka__column--sm-bold',
            "orderable": true,
            "render": function (valorCuota, type, operador) {
                var respuesta = `
                    <span class='labelnombreOperador'>${operador.nombre}</span>
                    <span class='labelbeneficioOperador'>Beneficios: ${operador.beneficios}</span>
                    `
                return respuesta;
            }
        },
        {
            title: "FACTOR POR MILLON",
            'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
            "data-label": "FACTOR POR MILLON",
            "data": "fxMillon",
            "orderable": true,
        },
        {
            title: "Valor Cuota",
            'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
            "data-label": "VALOR CUOTA",
            "data": "cuota",
            "orderable": true,
            "render": function (valorCuota, type, row) {
                return formatCurrency(valorCuota);
            }
        },
        {
            title: "MONTO MAX. A PRESTAR",
            'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
            "data-label": "MONTO MAX. A PRESTAR",
            "data": "monto",
            "orderable": true,
            "render": function (montoMax, type, row) {
                return formatCurrency(montoMax);
            }
        },
        {
            "data": "operadorID",
            "orderable": false,
            "render": (operadorID, type, operador) => {

            }
        }
        ],
        'drawCallback': () => {
            // Create an array of labels containing all table headers
            var labels = [];
            $('#tblOperadores thead th').each(function () {
                labels.push($(this).text());
            });

            // Add data-label attribute to each cell
            $('#tblOperadores tbody tr').each(function () {
                $(this).find('td').each(function (column) {
                    $(this).attr('data-label', labels[column]);
                });
            });

            $('.solicitar-credito').click((e) => {
                let operadorID = e.currentTarget.getAttribute('data-id');
                cargarConfirmacionSolicitud(operadorID)
            });
        }
    });
}