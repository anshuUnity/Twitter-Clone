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
            console.log(response);
            comment_form.reset();
            replyBtn.setAttribute("disabled", null)
            replyBtn.classList.add('disabled');
        },
        error: function(error){
            console.log(error);
        },

        cache: false,
        contentType:false,
        processData:false

    });
});