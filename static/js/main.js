
$(document).ready(function () {
    $('#avatar').click(function () {
        $('#profile-menu').toggleClass('hidden grid');
    });

    $('.message').fadeOut(5000, "swing");

    $('#profile-menu').focusout(function () {
        $('#profile-menu').addClass('hidden');
        console.log("focusout");
    });
});

$(document).on('click', ".add-to-cart", function(){
    var _vm = $(this);
    var _qty = $("#productQty").val();
    var _productId = $(".product-id").val();
    var _productName = $(".product-name").val();
    var _productPrice = parseFloat($(".product-price").text().replace(' d', ''));
    
    console.log(_qty, _productId, _productName, _productPrice);

    $.ajax({
        url: '/add-to-cart',
        data:{
            'id': _productId,
            'qty': _qty,
            'name': _productName,
            'price': _productPrice
        },
        dataType: 'json',
        beforeSend: function(){
            _vm.attr('disabled', true);
        },
        success: function(res){
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
        }
    });
});

$(document).on('click','.delete-cart-item', function(){
    var _pId = $(this).attr('data-item');
    var _vm = $(this);
    $.ajax({
        url: '/delete-from-cart',
        data: {
            'id': _pId,
        },
        dataType: 'json',
        beforeSend: function(){
            _vm.attr('disabled', true);
        },
        success: function(res){
            $(".cart-list").text(res.totalitems);
            _vm.attr('disabled', false);
            $("#cartList").html(res.data);
        }
    });
});

$(document).on('click','.update-cart-item', function(){
    var _pId = $(this).attr('data-item');
    var _pQty = $(".product-qty-" + _pId).val();
    var _vm = $(this);
    $.ajax({
        url : '/update-from-cart',
        data : {
            'id':_pId,
            'qty':_pQty
        },
        dataType: 'json',
        beforeSend: function(){
            _vm.attr('disabled', true);
        },
        success: function(res){
            _vm.attr('disabled', false);
            $("#cartList").html(res.data);
        }
    });
});