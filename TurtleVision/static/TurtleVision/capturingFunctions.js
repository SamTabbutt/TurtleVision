//Code adapted from https://html5multimedia.com/code/ch9/video-canvas-screenshot.html
// Get handles on the video and canvas elements
var video = document.querySelector('video');
var BreathCanvas = document.getElementById('breathshot');
var ApneaCanvas = document.getElementById('apneashot');
// Get a handle on the 2d context of the canvas element
var BreathContext = BreathCanvas.getContext('2d');
var ApneaContext = ApneaCanvas.getContext('2d');
// Define some vars required later
var w, h, ratio;
var tag;
var image;
		
// Add a listener to wait for the 'loadedmetadata' state so the video's dimensions can be read
video.addEventListener('loadedmetadata', function() {
		        // Calculate the ratio of the video's width to height
			ratio = video.videoWidth / video.videoHeight;
			// Define the required width as 100 pixels smaller than the actual video's width
			w = video.videoWidth - 100;
			// Calculate the height based on the video's width and the ratio
			h = parseInt(w / ratio, 10);
			// Set the canvas width and height to the values just calculated
			ApneaCanvas.width = w;
			ApneaCanvas.height = h;
			BreathCanvas.width = w;	
			BreathCanvas.height = h;		
		}, false);
		
// Takes a snapshot of the video
function snap(a) {
        if(a==1){
             context=BreathContext;
        }else{
             context=ApneaContext;
        }
	// Define the size of the rectangle that will be filled (basically the entire element)
	context.fillRect(0, 0, w, h);
	// Grab the image from the video
	context.drawImage(video, 0, 0, w, h);
}


// Saves the image of context a as the image file for new instance of frame along with tag
//for later versions vonsider using https://www.w3schools.com/tags/canvas_createimagedata.asp
function save(a){
	var canvas;
	if(a==1){
             canvas=BreathCanvas;
             tag="breath";
        }else{
	     canvas=ApneaCanvas;
             tag="apnea";
	}
        //taken from https://stackoverflow.com/questions/10673122/how-to-save-canvas-as-an-image-with-canvas-todataurl
        image = canvas.toDataURL("image/png");

	$.ajax({
            url:'/TurtleVision/ajax/saveframe/',
	    dataType: 'json',
            data: {
                 'image':image,
                 'tag':tag
            },
            success: function(data){
            	console.log("Marked "+tag);
           },

    });
}


