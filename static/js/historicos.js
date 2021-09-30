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
$(document).ready(() => {
    registarEventos()
})

function registarEventos() {
    cargarHistoricosTablaSuccess()
    cargarIndicadoresHistoricos()
    $('#descargarExcelHistorico').click(() => {
        descargarExcelHistorico()
    })
}

function cargarIndicadoresHistoricos(params) {
    $.ajax({
        url: '/indicadoresHistoricos',
        type: 'GET',
        success: function (responseJson, status, statusCode) {
            cargarIndicadoresHistoricosSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    });
}

function cargarIndicadoresHistoricosSuccess(responseJson) {

    data = responseJson.data
    debugger
    var inversores = data.inversores
    var inversion = formatCurrency(data.inversion)
    var promedioInversion = formatCurrency(data.promedioInversion)
    var gananciasRetiradas = formatCurrency(data.gananciasRetiradas)

    $('#inversoresT').text(inversores);
    $('#inversion').text(inversion);
    $('#promedioInversion').text(promedioInversion);
    $('#gananciasRetiradas').text(gananciasRetiradas);
}

function cargarHistoricosTablaSuccess() {

    $('#tblHistoricos').empty().append(`
    <table class="table table-striped" id="tableHistopricos">
`);
    //deleting operators to reset

    $tblOperadores = $('#tableHistopricos').DataTable({
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
            url: '/historicosTabla',
        },
        columns: [{
                title: "NOMBRE",
                "data": "nombre",
                "data-label": "NOMBRE",
                "orderable": true,
            },
            {
                title: "IDENTIFICACION",
                'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
                "data-label": "IDENTIFICACION",
                "data": "identificacion",
                "orderable": true,
            },
            {
                title: "TELEFONO",
                "data": "telefono",
                "data-label": "TELEFONO",

                "orderable": true,

            },
            {
                title: "CAPITAL",
                'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
                "data-label": "CAPITAL",
                "data": "capital",
                "orderable": true,
                "render": function (capital, type, row) {
                    return formatCurrency(capital);
                }
            },
            {
                title: "GANANCIAS",
                'className': 'table-dibanka__column table-dibanka__column--bold table-dibanka__column--gray-bg',
                "data-label": "MONTO MAX. A PRESTAR",
                "data": "ganancias",
                "orderable": true,
                "render": function (ganancias, type, row) {
                    return formatCurrency(ganancias);
                }
            },

            {
                title: "TOTAL RETIRO",
                "data-label": "TOTAL RETIRO",
                "data": "totalRetiro",
                "orderable": true,
                "render": function (totalRetiro, type, row) {
                    return formatCurrency(totalRetiro);
                }
            },
            {
                title: "TOTAL REINVERTIDO",
                "data-label": "TOTAL REINVERTIDO",
                "data": "totalReinvertido",
                "orderable": true,
                "render": function (totalReinvertido, type, row) {
                    return formatCurrency(totalReinvertido);
                }
            },
        ]
    });
}

function descargarExcelHistorico() {
    $.ajax({
        url: '/descargarExcelHistorico',
        type: 'GET',
        success: function (responseJson, status, statusCode) {
            descargarExcelHistoricoSuccess(responseJson, statusCode.status);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            errorConsultandoAPI(jqXHR, textStatus, errorThrown);
        }
    });
}


function formatCurrency(value) {

    if (value === '' || value == null || isNaN(value)) {
        return "";
    }

    if (typeof value == "string") {
        value = parseInt(value);
    }

    // El formato aplicado es USD - en-ES porque para Local "es-XX" no es posible aplicar formatos a números de 4 cifras
    var myObjCurrency = {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0,
        minimumFractionDigits: 0,
        currencyDisplay: "symbol"
    };

    return value.toLocaleString("en-ES", myObjCurrency);
}

function descargarExcelHistoricoSuccess(responseJson) {
    debugger
    var url = window.location.origin + responseJson.data;
    var link = document.createElement('a');
    link.href = url;
    hoy = new Date();
    fecha = hoy.getFullYear() + '_' + ( hoy.getMonth() + 1 ) + '_' + hoy.getDate()+ '_' +hoy.getHours() + '_' + hoy.getMinutes() + '_' + hoy.getSeconds();;
    link.download = `Historico_${fecha}.xls`;
    link.click();
}