console.log("cart.js loaded");

$('#quantity-decrease').click(function () {
    let quantity = parseInt($('#id_quantity').val());
    if (quantity > 1) {
        $('#id_quantity').val(quantity - 1);
    }
});

$('#quantity-increase').click(function () {
    let quantity = parseInt($('#id_quantity').val());
    let stock = parseInt($('#stock').text());

    if (quantity < stock) {
        $('#id_quantity').val(quantity + 1);
    } else {
        alert("Lưu trữ trong kho không đủ!");
    }
});

$('#id_quantity').change(function () {
    let quantity = parseInt($('#id_quantity').val());
    let stock = parseInt($('#stock').text());

    if (quantity > stock) {
        alert("Lưu trữ trong kho không đủ!");
        $('#id_quantity').val(stock);
    }
});

$('#cart_add').submit(function (event) {
    let quantity = parseInt($('#id_quantity').val());
    let stock = parseInt($('#stock').text());

    if (quantity > stock) {
        event.preventDefault();
        alert("Lưu trữ trong kho không đủ!");
        $('#id_quantity').val(stock);
    }
});