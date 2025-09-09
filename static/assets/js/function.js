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


                _html += '</div>'; // close product-rate
                _html += '</div>'; // close mb-10

                _html += '<p class="mb-10">'+ res.context.review +'</p>';
                _html += '</div>'; // close desc
                _html += '</div>'; // close user
                _html += '</div>'; // close single-comment

                $(".comment-list").prepend(_html);
                
            }
        },

        
    });
});
