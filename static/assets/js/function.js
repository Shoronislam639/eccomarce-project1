$("#commentForm").submit(function(e){
    e.preventDefault();

    $.ajax({
        data: $(this).serialize(),
        method: $(this).attr("method"),
        url: $(this).attr("action"),
        dataType: "json",

        success: function(res){
            console.log("Comment added to DB");

            if (res.bool === true){
                $('#review_res').html("Review added successfully.");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                // Build review HTML
                let _html = '';
                _html += '<div class="single-comment justify-content-between d-flex mb-30">';
                _html += '<div class="user justify-content-between d-flex">';
                _html += '<div class="thumb text-center">';
                _html += '<img src="https://www.shutterstock.com/image-vector/user-profile-icon-vector-avatar-600nw-2558760599.jpg" alt="User">';
                _html += '<a href="#" class="font-heading text-brand">'+ res.context.user +'</a>';
                _html += '</div>';

                _html += '<div class="desc">';
                _html += '<div class="d-flex justify-content-between mb-10">';
                _html += '<div class="d-flex align-items-center">';
                _html += '<span class="font-xs text-muted">Just now</span>';
                _html += '</div>';

                // Stars based on rating
                _html += '<div class="product-rate d-inline-block">';
                for(let i = 1; i <= +res.context.rating; i++){
                    _html += '<i class="fas fa-star text-warning"></i>';
                }


                _html += '</div>'; 
                _html += '</div>'; 

                _html += '<p class="mb-10">'+ res.context.review +'</p>';
                _html += '</div>'; 
                _html += '</div>'; 
                _html += '</div>'; 

                $(".comment-list").prepend(_html);
                
            }
        },

        
    });
});







$(document).ready(function(){

    $(".filter-checkbox, #filter-price-btn").on("click",function(){
        


        let min_price = $("#max_price").attr("min");
        let max_price = $("#max_price").val();

        let filter_object = {
        min_price: min_price,
        max_price: max_price,
    }
        $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter")
            console.log(filter_value,filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter="' + filter_key + '"]:checked')).map(function(element){
                return element.value
            })
        })
        console.log("filter object is",filter_object);
        $.ajax({
            url:'/filter-product',
            data:filter_object,
            dataType:'json',
            beforeSend: function(){
                console.log("sending data ...");
            },
            success:function(response){
                console.log(response);
                console.log("Data filter successfully...");
                $("#filtered-product").html(response.data)
            }
        })
    })
    $("#max_price").on("blur", function(){
        let min_price = $(this).attr("min")
        let max_price = $(this).attr("max")
        let current_price = $(this).val()

        if (current_price < parseInt (min_price) || current_price > parseInt (max_price) ){
            min_price = Math.round(min_price * 100) / 100;
            max_price = Math.round(max_price * 100) / 100;

            alert("Price must be between $" + min_price + " and $" + max_price)
            $(this).val(min_price)
            $('#range').val(min_price)
            $(this).focus()
            return false
        }
    })
})



// add to cart functionality

$(".add-to-cart-btn").on("click", function(){
    let this_val =$(this)
    let index = this_val.attr("data-index")
    

    let quantity = $(".product-quantity-"+index).val()
    let product_title = $(".product-title-"+index).val()
    let product_id = $(".product-id-"+index).val()
    let product_price = $(".current-product-price-"+index).text()
    let product_pid = $(".product-pid-"+index).val()
    let product_image = $(".product-image-"+index).val()
    

    console.log("product quantity :",quantity);
    console.log("product title :",product_title);
    console.log("product Id :",product_id);
    console.log("product PID :",product_pid);

    console.log("product price :",product_price);
    console.log("product Image :",product_image);

    console.log("Current element  :",this_val);
    console.log("index  :",index);


    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'pid':product_pid,
            'image':product_image,
            'qty':quantity,
            'title':product_title,
            'price':product_price,
        },
        dataType:'json',
        beforeSend:function(){
            console.log("Adding product to cart");
        },
        success: function (response) {
            this_val.html("✅")
            console.log("Added product to cart");
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})



/*
$(".add-to-cart-btn").on("click", function(){
    let quantity = $("#product-quantity").val()
    let product_title = $(".product-title").val()
    let product_id = $(".product-id").val()
    let product_price = $("#current-product-price").text()
    let this_val =$(this)
    

    console.log("product quantity :",quantity);
    console.log("product title :",product_title);
    console.log("product Id :",product_id);
    console.log("product price :",product_price);
    console.log("Current element  :",this_val);


    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'qty':quantity,
            'title':product_title,
            'price':product_price,
        },
        dataType:'json',
        beforeSend:function(){
            console.log("Adding product to cart");
        },
        success: function (response) {
            this_val.html("Item added to cart")
            console.log("Added product to cart");
            $(".cart-items-count").text(response.totalcartitems)
        }
    })
})

*/

