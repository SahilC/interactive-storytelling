document.getElementById("video_player").play();
document.getElementById("video_player").addEventListener("timeupdate", function(){
    if(this.currentTime >= 5) {
        this.pause();
    }
});