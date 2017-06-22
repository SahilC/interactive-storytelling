$(document).ready(function() {
  $.ajax( {
                url: '/stories' ,
                method: 'POST',
                contentType:'application/json',
                data: JSON.stringify({file_name: 'data/FILE0573.MOV.txt'}),
                success: function(response) {
                    swal({
                      title: 'Error!',
                      text: 'Do you want to continue',
                      type: 'error',
                      confirmButtonText: 'Cool'
                    });
                    var result = JSON.parse(response);
                    // console.log(result.stories)
                    responsiveVoice.speak(result['stories']['balahissardarwaza'][1]);
                },
                error: function(error) {
                    console.log('error');
                }
  });
});
