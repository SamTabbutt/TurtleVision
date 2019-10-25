

$('select[name=session-select]').change(function(){
    var session_choice = $(this).val();
    var request_url = $("#session-select").attr("data-movies-list") ;
        $.ajax({
            url: request_url,
            data: {
                 'session_choice':session_choice
            },
            success: function(data){
            	$("#movie-set").html(data);
           }
    });
})

$('select[name=movie-select]').change(function(){
    var movie_choice = $(this).val();
    $("#my_video").attr("src",movie_choice);
    var player = videojs("my_video");
    player.src({
         src:movie_choice,
         type:"video/mp4",
         withCredentials:true,
         allowSeeksWithinUnsafeLiveWindow:true
    });
})