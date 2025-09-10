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

    $(".filter-checkbox").on("click",function(){
        let filter_object = {}

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
})




