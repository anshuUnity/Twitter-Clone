const realmediabtn = document.getElementById("id_comment_media");
const customFileBtn = document.getElementById('customfile--choose__button');
const fileName = document.getElementById("file--name_custom");
const replyBtn = document.getElementById("comment_submit-btn");
const replyText = document.getElementById("id_comment_content");

customFileBtn.addEventListener('click', function(){
    realmediabtn.click();
});

replyText.addEventListener("keyup", function(){
    if(replyText.value != ""){
        replyBtn.removeAttribute("disabled");
        replyBtn.classList.remove('disabled');
    }else{
        replyBtn.setAttribute("disabled", null)
        replyBtn.classList.add('disabled');
    }
})

realmediabtn.addEventListener("change", function(){
    if(realmediabtn.value){
        fileName.innerHTML = realmediabtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    }
});

const comment_form = document.getElementById('comment-form')

$('#comment-form').submit(function(e){
    e.preventDefault();
    $form = $(this);
    const url = comment_form.action
    var formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: url,
        data: formData,
        dataType: 'json',

        success: function(response){
            console.log(response.date);
            comment_form.reset();
            replyBtn.setAttribute("disabled", null)
            replyBtn.classList.add('disabled');
            $('#exampleModal').modal('hide');
            $('.comment-container').prepend(
                `<div class="main_comment_div">
                    <div class="profile--username_date-div">
                        <div class="comment-user--profile-pic mt-2">
                                <img src="${response.comment_profile}" alt="DP">
                        </div>
                        <div class="username-date-div mt-2">
                            <div class="username--name-div">
                                <span class="name" style="font-weight: 700;">
                                    ${response.name}
                                </span>
            
                                <span class="username">
                                    @${response.comment_username} .
                                </span>
                            </div>
                            <div class="replying--to-div">
                                <span>
                                    Replying to <a href="#">@${response.tweet_username}</a>
                                </span>
                            </div>
                            <div class="comment-content">
                                <span>
                                    ${response.comment}
                                </span>
                            </div>
                            <div class="interaction--icons-div">
                            <div class="comment-icon">
                                <img src="/static/images/icons/comment.svg" alt="comment">
                            </div>
                            <div class="retweet-icon">
                                <img src="/static/images/icons/retweet.svg" alt="retweet">
                            </div>
                            <div class="like-icon">
                                <img src="/static/images/icons/heart.svg" alt="Like">
                            </div>
                            <div class="share-icon">
                                <img src="/static/images/icons/share.svg" alt="share">
                            </div>
                        </div>
                        </div>
                    </div>
                </div>`
            );
        },
        error: function(error){
            console.log(error);
        },

        cache: false,
        contentType:false,
        processData:false

    });
});