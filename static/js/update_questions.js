$(document).ready(function() {
  $.ajax( {
                url: '/stories' ,
                method: 'POST',
                contentType:'application/json',
                data: JSON.stringify({file_name: 'data/FILE0573.MOV.txt'}),
                success: function(response) {
                    console.log(response);
                    console.log('response');
                },
                error: function(error) {
                    console.log(error);
                    console.log('error');
                }
  });
});
