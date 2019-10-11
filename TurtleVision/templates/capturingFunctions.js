// Get handles on the video and canvas elements
		var video = document.querySelector('video');
		var canvas = document.querySelector('canvas');
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
		}