//Code adapted from https://html5multimedia.com/code/ch9/video-canvas-screenshot.html
// Get handles on the video and canvas elements
var video= document.getElementById('my_video');
var canvas = document.getElementById('snapcanvas');
// Get a handle on the 2d context of the canvas element
var context = canvas.getContext('2d');
// Define some vars required later
var w, h, ratio;
	
// Add a listener to wait for the 'loadedmetadata' state so the video's dimensions can be read

video.addEventListener('loadedmetadata', function() {
		        // Calculate the ratio of the video's width to height
			ratio = video.videoWidth / video.videoHeight;
			// Define the required width as 100 pixels smaller than the actual video's width
			w = video.videoWidth - 100;
			// Calculate the height based on the video's width and the ratio
			h = parseInt(w / ratio, 10);
			// Set the canvas width and height to the values just calculated
			canvas.width = w;
			canvas.height = h;		
		}, false);


		
// Takes a snapshot of the video
function snap() {
	// Define the size of the rectangle that will be filled (basically the entire element)
	context.fillRect(0, 0, w, h);
	// Grab the image from the video
	context.drawImage(video, 0, 0, w, h);
        t = video.currentTime;
        document.getElementById('secToLog').innerHTML=t;
}


// Saves the image of context a as the image file for new instance of frame along with tag
//for later versions vonsider using https://www.w3schools.com/tags/canvas_createimagedata.asp
function save(a){
        var src = $("#my_video").attr('src');
        var second_count=$("#secToLog").html();
        var tag = a;
	$.ajax({
            url:'/TurtleVision/ajax/saveframe/',
	    dataType: 'json',
            data: {
                 'tag':a,
                 'sec':second_count,
                 'src':src
            },
            success: function(data){
            	console.log("Marked "+tag);
           },

    });
}


