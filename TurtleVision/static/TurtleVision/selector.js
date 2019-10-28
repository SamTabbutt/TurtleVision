
$('select[name=session-select]').change(function(){
    var session_choice = $(this).val();
    var request_url = $("#session-select").attr("data-movies-list");
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

$( document ).ready(function(){
 var player = videojs("my_video",{
	 withCredintials:true,
         allowSeeksWithinUnsafeLiveWindow:true,
         fluid:true,
         playbackRates: [0.5, 1, 1.5, 2, 3, 4, 5]
    });
    
})


$('select[name=movie-select]').change(function(){
    var movie_choice = $(this).val();
    $("#my_video").attr("src",movie_choice);
    var video = videojs('my_video');
    video.src([{
         src:movie_choice,
         type:"video/mp4"
	}]);
})

$('select[name=anal-select]').change(function(){
	var anal_choice = $(this).val();
	var request_url = $("#tags").attr("tag_choices_list");
	if(anal_choice!=''){

		$.ajax({
			url: request_url,
			data:{
				'anal_choice':anal_choice
			},
			success: function(data){
				$("#tags").val(data);
			}
		});
	}

})