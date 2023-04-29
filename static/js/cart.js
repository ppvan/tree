console.log("cart.js loaded");

// Add to cart handler
// $("#add-to-cart").click(function () {
//     let product_id = $(this).attr("data-product-id");
//     let quantity = parseInt($('#quantity').text());

//     if (USER === "AnonymousUser") {
//         console.log("User is not authenticated");
//         window.location.replace("/user/login/?next=" + window.location.pathname);
//     } else {
//         console.log("User is authenticated");
//         let url = "/cart/add/";

//         let body = {
//             productId: product_id,
//             username: USER,
//             quantity: quantity
//         };
//         console.log("POST data:", body);

//         $.ajax({
//             url: url,
//             method: "POST",
//             headers: { 'X-CSRFToken': csrftoken },
//             data: JSON.stringify(body),
//             success: function (data) {
//                 console.log("Response: ", data);
//             }
//         });
//     }

//     // var url = "/cart/add/" + product_id + "/";
//     // $.ajax({
//     //     url: url,
//     //     success: function (data) {
//     //         $("#cart-count").html(data.cart_count);
//     //     }
//     // });

//     console.log("add to cart", product_id, quantity, USER);
// });