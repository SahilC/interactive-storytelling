$(document).ready(function() {
      var vid = document.getElementById("video_player"); 
      $.ajax( {
        url: '/stories' ,
        method: 'POST',
        contentType:'application/json',
        data: JSON.stringify({file_name: 'data/FILE0573.MOV.txt'}),
        success: function(response) {
            
            var result = JSON.parse(response);
            vid.muted = true;
            vid.play(); 
            check_and_wait(result)
            // console.log(result.stories)
            // responsiveVoice.speak(result['stories']['balahissardarwaza'][1]);
        },
        error: function(error) {
            console.log('error');
        }
      });

function check_and_wait(result) {
    var  start = new Date().getTime();
    var pause = 0;
    var i = 0;
    var interval = setInterval(function() {
            var time = (new Date().getTime() - pause - start)/(1000.0);

            if(  time > result.final[i].time ) {
                if(result.final[i].type == 'story') {
                    // responsiveVoice.speak(result.stories[result.final[i].name][0]);
                    console.log(result.final[i].name);
                    i += 1;
                } else {
                    if(vid.paused != true) {
                        var pause_start = new Date().getTime();
                        vid.pause()
                        swal({
                          title: "An input!",
                          text: "Would you like to listen to a story about "+result.final[i].story.opt1 + " or " + result.final[i].story.opt2+"?" ,
                          type: "input",
                          showCancelButton: true,
                          closeOnConfirm: false,
                          animation: "slide-from-top",
                          inputPlaceholder: "Enter choice here."
                        },
                        function(inputValue) {
                          if (inputValue === false) return false;
                          
                          if (inputValue === "") {
                            swal.showInputError("You need to write something!");
                            return false
                          }
                          console.log(i);
                          console.log(result.final[i].story.opt1);
                          if (result.final[i].story.opt1.includes(inputValue)) {
                            pause = pause + (new Date().getTime() - pause_start);
                            vid.play();
                            // responsiveVoice.speak(result.stories[result.final[i].story.m1][0]);
                            console.log(result.final[i].story.m1);
                            i += 1;
                          } else {
                            pause = pause + (new Date().getTime() - pause_start);
                            vid.play();
                            // responsiveVoice.speak(result.stories[result.final[i].story.m2][0]);
                            console.log(result.final[i].story.m2);
                            i += 1;
                          }
                          // swal("Nice!", "You wrote: " + inputValue, "success");
                        });
                    }
                }
            } else { 
                return false; 
            }
    }, 250); 
}
});



