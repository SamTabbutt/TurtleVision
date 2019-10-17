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
    var request_url = $("#movie-list").attr("data-video") ;
        $.ajax({
            url: request_url,
            data: {'movie_choice':movie_choice},
            success: function(data){
		$("#vidc").html(data);
	   }
    });
})