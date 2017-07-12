$(document).ready(function() {
      var vid = document.getElementById("video_player");
      var music = document.getElementById("music_control"); 
      $.ajax( {
        url: '/stories' ,
        method: 'POST',
        contentType:'application/json',
        data: JSON.stringify({file_name: 'data/VID_20170607_111002.txt'}),
        success: function(response) {
            music.play();
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
                      console.log(result.final[i].name);
                      document.getElementById('title').innerHTML = result.final[i].name;
                      document.getElementById('story').innerHTML = result.final_stories[result.final[i].name];
                      i += 1;
                      responsiveVoice.speak(result.stories[result.final[i].name][0]);
                  } else {
                      var r = Math.random();
                      var upvalue = $("#upvoted").val();
                      var downvalue = $("#downvoted").val();
                      l = upvalue.split(",").length;
                      l2 = downvalue.split(",").length;

                      document.getElementById('title').innerHTML = result.final[i].value;
                      document.getElementById('story').innerHTML = result.stories[result.final[i].value][0];
                      if( r < 1.0/(l+l2)) {
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
                                // console.log(story);
                                document.getElementById('title').innerHTML = story;
                                pause = pause + (new Date().getTime() - pause_start);
                                i += 1;
                                document.getElementById('story').innerHTML = result.stories[story][0];
                                responsiveVoice.speak(result.stories[story][0]);
                                vid.play();
                                return true;
                            } else {
                                var newval = '';
                                var stor = result.final[i].value;
                                if (result.final[i].story.opt1.includes(inputValue)) {
                                  newval = result.final[i].story.m1;
                                  pause = pause + (new Date().getTime() - pause_start);
                                  console.log(result.final[i].story.m1);
                                  i += 1;
                                } else {
                                  newval = result.final[i].story.m2;
                                  pause = pause + (new Date().getTime() - pause_start);
                                  console.log(result.final[i].story.m2);
                                  i += 1;
                                }
                                vid.play();
                                console.log(result.final[i]);
                                responsiveVoice.speak(result.stories[stor][0]);
                                upvalue = upvalue + "," + newval;
                                $("#upvoted").val(upvalue);
                                update_stories($("#upvoted").val(),$("#downvoted").val());
                                // swal("Nice!", "You wrote: " + inputValue, "success");
                                return true;
                            }
                            
                          });
                      }

                      } else {
                        console.log("WHO");
                      }
                  }
              } else { 
                  return false; 
              }
      }, 1000); 
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



