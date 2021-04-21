var followForm = document.getElementById('follow_form');
var profile_pk = $("[name=profile_pk]").val();
var csrftoken = $("[name=csrfmiddlewaretoken]").val();
var follow_btn = document.getElementById("follow_btn");
const following_count = document.getElementById('following-count');
const followers_count = document.getElementById('followers-count');
const progressSpinner = document.getElementById('spinner')

$("#follow_form").submit(function(e){
    e.preventDefault();
    $.ajax({
        type: 'POST', 
        url: followForm.action,
        data: {
            "profile_pk":profile_pk,
            "csrfmiddlewaretoken":csrftoken,
        },
        dataType: 'json',

        beforeSend:function(){
            progressSpinner.innerHTML = `<div class="spinner-border text-primary" role="status">
                                            <span class="sr-only">Loading...</span>
                                        </div>`;
        },

        success: function(response){
            console.log(response.followers_count);
            if(response.follow){
                follow_btn.innerHTML = "Following";
                follow_btn.classList.add("unfollow");

            }else{
                follow_btn.innerHTML = "Follow"
                follow_btn.classList.remove("unfollow");
            }
            following_count.innerHTML = response.following_count;
            followers_count.innerHTML = response.followers_count;
            progressSpinner.innerHTML = "";
        },
        error: function(error){
            console.log(error);
        },
    });
});