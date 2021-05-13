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

// tabs styling
const tabbtns = document.querySelectorAll('.tab-btn');
const tab_panels = document.querySelectorAll('.tab-panels');

const tweet_tab_spinner = document.getElementById('tab-spinner-1');

function showTabContent(panelIndex){
    tab_panels.forEach(function(node){
        node.style.display="none";
    });
    tab_panels[panelIndex].style.display="block";
}

const tweet_tab = document.getElementById('tweet-tab')

$('#user_tweet').submit(function(e){
    e.preventDefault();
    url = $('#user_tweet').attr('action');
    var username = $('input[name="username"]').val().trim();

    $.ajax({
        type: 'GET',
        url: url,
        data: {
            'username': username
        },
        dataType: 'json',
        success: function(response){
            tweet_tab_spinner.classList.add('tab-spinner-1');
            tweet_tab.innerHTML = ''

            for(const item of response.user_tweet){
                tweet_tab.innerHTML += `<div class="user_tweet_tab-div">
                                            <div class="user-profile-pic">
                                                <img src="${response.profile_pic}" alt="">
                                            </div>
                                            <div class="user-detail--tweet-content">
                                                <div class="username-detail">
                                                    <span>
                                                        ${response.fullname}
                                                        ${response.is_verified ? '<img style="width:4%;" src="http://127.0.0.1:8000/static/images/icons/verif-icon.svg" alt="verify"></img>': ''}
                                                    </span>
                                                    
                                                    <span>@${response.username}</span>
                                                </div>
                                                <div class="tweet-content">
                                                    <span>${item.tweet_content}</span>
                                                </div>
                                            </div>
                                        </div>`;
            }

        },
        error: function(error){
            console.log(error);
        },

    });
});

$('#user_reply').submit(function(e){
    e.preventDefault();
});

const likeTab = document.getElementById('like_tab');
const like_tab_spinner = document.getElementById('tab-spinner-3');

$('#user_likes').submit(function(e){
    e.preventDefault();
    url = $('#user_likes').attr('action');
    var username = $('input[name="username_liked_tab"]').val().trim();

    $.ajax({
        type: 'GET',
        url: url,
        data: {
            'username': username
        },
        dataType: 'json',

        success: function(response){
            like_tab_spinner.classList.add('tab-spinner-1');
            likeTab.innerHTML = "";
            for(const item of response.liked_post){
                likeTab.innerHTML += `<div class="user_tweet_tab-div">
                                            <div class="user-profile-pic">
                                                <img src="${item.profile_pic}" alt="">
                                            </div>
                                            <div class="user-detail--tweet-content">
                                                <div class="username-detail">
                                                    <span>
                                                        ${item.fullname}
                                                    </span>
                                                    
                                                    <span>@${item.username}</span>
                                                </div>
                                                <div class="tweet-content">
                                                    <span>${item.content}</span>
                                                </div>
                                            </div>
                                        </div>`;
            }

        },

        error: function(error){
            console.log(error);
        },

    })

});

$('#user_media').submit(function(e){
    e.preventDefault();
});


// sending otp logic
const send_otp_form = document.getElementById('send-otp');
const collect_otp_form = document.getElementById('check-otp'),
success_alert = document.getElementById('success-alert');
const otp_progress_spinner = document.getElementById('otp-spinner');

$('#send-otp').submit(function(e){
    e.preventDefault();
    url = send_otp_form.action;

    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        beforeSend: function(){
            otp_progress_spinner.classList.remove('invisible');
        },
        success: function(response){
            otp_progress_spinner.classList.add('invisible');
            success_alert.classList.remove('invisible')
            success_alert.innerHTML = `<div class="alert alert-success" role="alert">
                                            ${response.data}
                                        </div>`;
        },
        error: function(error){ 
            console.log(error);
        }
    });
});

const email_verify_div = document.getElementById('email-verify-div');

$('#check-otp').submit(function(e){
    e.preventDefault();
    var u_otp_input = document.getElementById('user-otp').value;
    url = collect_otp_form.action;
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            'u_otp': u_otp_input,
        },
        dataType: 'json',
        success: function(response){
            if(response.data){
                email_verify_div.innerHTML = `  <div class="alert alert-success" role="alert">
                                                    Cool!! Your email is verified!!
                                                </div>
                                            `
            }
            else{
                email_verify_div.innerHTML += `
                                                <div class="alert alert-danger" role="alert">
                                                    Please enter a valid otp
                                                </div>`
            }
        },
        error: function(error){
            console.log(error);
        },
    });
});