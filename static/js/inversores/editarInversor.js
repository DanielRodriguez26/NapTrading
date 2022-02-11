$(document).ready(() => {
    registarEventos();
});

function registarEventos() {
    $("#editar_inversor").click((e) => {
        actualizarInversor();
    });
    $("#editar_capital").click((e) => {
        actualizarCapital();
    });
    cargarInversoresSuccess();
}

function cargarInversoresSuccess() {
    const usuario = $("#usuario").val();
    var data = new FormData();
    data.append("usuario", usuario);

    $.ajax({
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        type: "POST",
        url: "/editarInversorConsulta",
        success: function (responseJson) {
            cargarInversores(responseJson);
        },
    });
}

function cargarInversores(responseJson) {
    let {
        nombres,
        apellidos,
        identificacion,
        email,
        telefono,
        fecha_inicio_pool,
        pais,
        ganancia,
        capitales,
        porcentaje_ganancias,
    } = responseJson.data[0];

    $("#nombres").val(nombres);
    $("#apellidos").val(apellidos);
    $("#identificacion").val(identificacion);
    $("#email").val(email);
    $("#telefono").val(telefono);
    $("#fecha_inicio_pool").val(fecha_inicio_pool);
    $("#pais").val(pais);
    $("#ganancias").val(ganancia);
    $("#porcentaje_ganancias").val(porcentaje_ganancias);

    for (let i = 0; i < capitales.length; i++) {
        const { fecha, monto, historico_id } = capitales[i];
        $("#tablaGancia").append(`
        <tr>
            <td class="text-bold-500"><input type="date"  
                value="${fecha}"
                onchange="cargarFechaCapital(${historico_id},this.value)"
                > </td>
            <td><input type="text" 
                value="${monto}" 
                onchange="cargarCapital(${historico_id},this.value)"
            ></td>
        </tr>`);
    }
}

function actualizarInversor() {
    const usuario = $("#usuario").val();
    var data = new FormData();
    data.append("nombres", $("#nombres").val());
    data.append("apellidos", $("#apellidos").val());
    data.append("identificacion", $("#identificacion").val());
    data.append("email", $("#email").val());
    data.append("telefono", $("#telefono").val());
    data.append("pais", $("#pais").val());
    data.append("porcentaje_ganancias", $("#porcentaje_ganancias").val());
    data.append("fecha_inicio_pool", $("#fecha_inicio_pool").val());
    data.append("usuario", usuario);
    if (inputIsValid()) {
        $.ajax({
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: "POST",
            url: "/actualizarInversor",
            success: function (responseJson) {
                actualizarInversorSuccess(responseJson);
            },
        });
    }
}

function actualizarCapital() {
    let oldcapital = sessionStorage.getItem("capital");
    let oldfechas = sessionStorage.getItem("fechas");

    const usuario = $("#usuario").val();
    var data = new FormData();
    data.append("nombres", $("#nombres").val());
    data.append("apellidos", $("#apellidos").val());
    data.append("identificacion", $("#identificacion").val());
    data.append("email", $("#email").val());
    data.append("telefono", $("#telefono").val());
    data.append("pais", $("#pais").val());
    data.append("ganancia", $("#ganancias").val());
    data.append("capital", oldcapital);
    data.append("fechas", oldfechas);
    data.append("usuario", usuario);
    if (inputIsValid()) {
        $.ajax({
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            type: "POST",
            url: "/actualizarCapital",
            success: function (responseJson) {
                actualizarInversorSuccess(responseJson);
            },
        });
    }
}

function actualizarInversorSuccess(responseJson) {
    var data = responseJson.data;

    if (data.redirect) {
        Swal.fire({
            icon: "success",
            title: "Bien Hecho",
            text: `Se a actualizado corretamente los datos del inversor`,
        }).then((result) => {
            sessionStorage.clear();
        });
    } else {
        Swal.fire({
            icon: "error",
            title: mensaje,
        });
    }
}

function cargarCapital(historico_id, monto) {
    var data = sessionStorage.getItem("ganancias");
    var capital = [];
    capital.push({
        historico_id: historico_id,
        monto: monto,
    });
    let oldcapital = sessionStorage.getItem("capital") || "[]";
    sessionStorage.setItem(
        "capital",
        JSON.stringify([capital, ...JSON.parse(oldcapital)])
    );
}

function cargarFechaCapital(historico_id, fecha) {
    var fechas = [];
    fechas.push({
        historico_id: historico_id,
        fecha: fecha,
    });
    let oldfechas = sessionStorage.getItem("fechas") || "[]";
    sessionStorage.setItem(
        "fechas",
        JSON.stringify([fechas, ...JSON.parse(oldfechas)])
    );
}

function inputIsValid() {
    if ($("#nombres").val() == "") {
        alerta();
        $("#nombres").focus();
        return false;
    }

    if ($("#apellidos").val() == "") {
        alerta();
        $("#apellidos").focus();
        return false;
    }

    if ($("#identificacion").val() == "") {
        alerta();
        $("#identificacion").focus();
        return false;
    }

    if ($("#email").val() == "") {
        alerta();
        $("#email").focus();
        return false;
    }

    if ($("#telefono").val() == "") {
        alerta();
        $("#telefono").focus();
        return false;
    }

    if ($("#pais").val() == "") {
        alerta();
        $("#pais").focus();
        return false;
    }

    if ($("#ganancias").val() == "") {
        alerta();
        $("#ganancias").focus();
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
