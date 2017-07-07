$(document).ready(function() {
      var vid = document.getElementById("video_player"); 
      $.ajax( {
        url: '/stories' ,
        method: 'POST',
        contentType:'application/json',
        data: JSON.stringify({file_name: 'data/VID_20170607_111002.txt'}),
        success: function(response) {
            var result = JSON.parse(response);
            var num_gaps = result['num_gaps'];
            var idx = result['idx'];
            for(var i =0;i<num_gaps;i++) {
                $("#gaps").append("<div id='id_"+idx[i]+"'></div>");
            }
            vid.muted = true;
            vid.play(); 
            check_and_wait(result);
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
                      document.getElementById('title').innerHTML = result.final[i].name;
                      document.getElementById('story').innerHTML = result.final_stories[result.final[i].name];
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
                            closeOnConfirm: true,
                            animation: "slide-from-top",
                            inputPlaceholder: "Enter choice here."
                          },
                          function(inputValue) {
                            if (inputValue === false) return false;
                            
                            if (inputValue === "") {
                              swal.showInputError("You need to write something!");
                              return false
                            }
                            
                            var id = result.final[i].idx;
                            if($('#id_'+id).html() != '' ) {
                                var story = $('#id_'+id).html();
                                console.log(story);
                                document.getElementById('title').innerHTML = story;
                                pause = pause + (new Date().getTime() - pause_start);
                                i += 1;
                                document.getElementById('story').innerHTML = result.stories[story][0];
                                vid.play();
                                return true;
                            } else {
                                if (result.final[i].story.opt1.includes(inputValue)) {
                                  document.getElementById('title').innerHTML = result.final[i].story.m1;
                                  pause = pause + (new Date().getTime() - pause_start);
                                  
                                  // responsiveVoice.speak(result.stories[result.final[i].story.m1][0]);
                                  console.log(result.final[i].story.m1);
                                  i += 1;
                                } else {
                                  document.getElementById('title').innerHTML = result.final[i].story.m2;
                                  pause = pause + (new Date().getTime() - pause_start);
                                  // responsiveVoice.speak(result.stories[result.final[i].story.m2][0]);
                                  console.log(result.final[i].story.m2);
                                  document.getElementById('story').innerHTML = result.stories[result.final[i].story.m2][0];
                                  i += 1;
                                }
                                vid.play();
                                var newvalue = $("#upvoted").val();
                                    newvalue = newvalue + "," + $("#title").html();
                                $("#upvoted").val(newvalue);
                                update_stories($("#upvoted").val(),$("#downvoted").val());
                                // swal("Nice!", "You wrote: " + inputValue, "success");
                                return true;
                            }
                            
                          });
                      }
                  }
              } else { 
                  return false; 
              }
      }, 250); 
  }

  function update_stories(upvoted, downvoted) {
      $.ajax({
          url: '/update_stories' ,
          method: 'POST',
          contentType:'application/json',
          data: JSON.stringify({file_name: 'data/FILE0573.MOV.txt',upvoted: upvoted, downvoted: downvoted}),
          success: function(response) {
              var result = JSON.parse(response);
              console.log(result);
              $.each(result, function (key, value) {
                    $("#id_"+key).html(value);
                });
              
              // check_and_wait(result);
              // console.log(result.stories)
              // responsiveVoice.speak(result['stories']['balahissardarwaza'][1]);
          },
          error: function(error) {
              console.log('error');
          }
        });
  }

        $('#up').click(function() {
            var newvalue = $("#upvoted").val();
            newvalue = newvalue + "," + $("#title").html();
            $("#upvoted").val(newvalue);
            update_stories($("#upvoted").val(),$("#downvoted").val());
        });
        $('#down').click(function() {
            var newvalue = $("#downvoted").val();
            newvalue = newvalue + "," + $("#title").html();
            $("#downvoted").val(newvalue);
            update_stories($("#upvoted").val(),$("#downvoted").val());
        });
});



