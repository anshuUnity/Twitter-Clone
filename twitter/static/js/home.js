const realFileBtn = document.getElementById("id_media");
const customFileBtn = document.getElementById("customfile--choose__button");
const fileName = document.getElementById("file--name_custom");
const tweetText = document.getElementById("id_tweet_content");
const submitBtn = document.getElementById("submit__btn");


tweetText.addEventListener("keyup", function(){
    if(tweetText.value != ""){
        submitBtn.removeAttribute("disabled");
        submitBtn.classList.remove('disabled');
    }else{
        submitBtn.setAttribute("disabled", null)
        submitBtn.classList.add('disabled');
    }
})

customFileBtn.addEventListener('click', function(){
    realFileBtn.click();
});

realFileBtn.addEventListener("change", function(){
    if(realFileBtn.value){
        fileName.innerHTML = realFileBtn.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
        submitBtn.removeAttribute("disabled");
        submitBtn.classList.remove('disabled');
    }else{
        submitBtn.setAttribute("disabled", null)
        submitBtn.classList.add('disabled');
    }
});

// ajax tweet request

const progressBar = document.getElementById("progress-box");
const fileInput = document.getElementById("id_media");
const tweetUploadForm = document.getElementById("tweet-form");
const snack = document.getElementById("snackbar");

$("#tweet-form").submit(function(e){
    e.preventDefault();
    $form = $(this);
    var formData = new FormData(this);

    const media_data = fileInput.files[0];
    if(media_data != null){
        console.log(media_data);
        progressBar.classList.remove("not-visible");
    }

    $.ajax({
        type: 'POST',
        url: '/',
        data: formData,
        dataType: 'json',
        before:function(){

        },
        xhr:function(){
            const xhr = new window.XMLHttpRequest();
            xhr.upload.addEventListener("progress", e=>{
                if(e.lengthComputable){
                    const percentProgress = (e.loaded/e.total)*100;
                    progressBar.innerHTML = `<div class="progress-bar progress-bar-striped bg-success" 
                    role="progressbar" style="width: ${percentProgress}%" aria-valuenow="${percentProgress}" aria-valuemin="0" 
                    aria-valuemax="100"></div>`
                }
            });
            return xhr;
        },
        success:function(response){
            tweetUploadForm.reset();
            progressBar.classList.add("not-visible")
            fileName.innerHTML = "";
            snack.className = "show";
            submitBtn.setAttribute("disabled", null)
            submitBtn.classList.add('disabled');

            // After 3 seconds, remove the show class from DIV
            setTimeout(function(){ snack.className = snack.className.replace("show", ""); }, 3000);

        },
        error:function(error){
            console.log(error);
        },
        cache: false,
        contentType:false,
        processData:false

    });
});

// ajax tweet request


// modal video tweet
var modal = document.getElementById("myModal");
var modalImg = document.getElementById("img01");

// image.addEventListener("click", function(){
//     modal.style.display = "block"
//     modalImg.src = this.src;
// });

function openModal(id) {
    var imageSrc = document.getElementById(`tweet_image-${id}`).src;
    // console.log(imageSrc);
    modal.style.display = "block";
    modalImg.src = imageSrc;
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// modal video tweet
var modalV = document.getElementById("vModal");
var videoPlayer = document.getElementById("tweet-video-modal");

function openVideoModal(url){
    // var videoSrc = document.querySelector(`#tweet-video-${id} > source`).src;
    console.log(url);
    modalV.style.display = "block";
    videoPlayer.innerHTML = ` <source src=${url} type="video/mp4" id='modal-video-source'>
                                Your browser does not support the video tag.`
    console.log(videoPlayer);
}

// Get the <span> element that closes the modal
var spanV = document.getElementsByClassName("close-videoModal")[0];

// When the user clicks on <span> (x), close the modal
spanV.onclick = function() {
  modalV.style.display = "none";
  videoPlayer.pause();
  videoPlayer.load();
  videoPlayer.innerHTML = "";
}


$(window).scroll(function () {
    //set scroll position in session storage
    sessionStorage.scrollPos = $(window).scrollTop();
  });
var init = function () {
     //return scroll position in session storage
     $(window).scrollTop(sessionStorage.scrollPos || 0)
};
window.onload = init;


// ajax like tweet

function likeTweet(id){
    const like_input_btn = document.getElementById(`not-visible-${id}`);
    like_input_btn.click();
}

$('.like-form').submit(function(e){
    e.preventDefault();
    const tweet_id = $(this).attr('id');
    const url = $(this).attr('action');
    const like_span = document.getElementById(`like-icon-ajax--${tweet_id}`);
    $.ajax({
        type: 'POST',
        url: url,
        data: {
            "tweet_id": tweet_id,
        },
        dataType: 'json',
        success:function(response){
            console.log(response.count);
            if(!response.liked){
                like_span.innerHTML = `<img class="tweet-interact_icon--images interact-3" onclick="likeTweet('${tweet_id}')" src="static/images/icons/heart.svg" alt="like">
                                        <span class="count-interaction">${response.count}</span>`
            }else{
                like_span.innerHTML = `<img class="tweet-interact_icon--images when-liked interact-3" onclick="likeTweet('${tweet_id}')" src="static/images/icons/liked.svg" alt="like">
                                        <span class="count-interaction">${response.count}</span>`
            }
        },
        error:function(error){
            console.log(error);
        },
    });

});

