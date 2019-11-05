$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $("#videoButton").click(function () {
    $("#video_file_field").click();
  });

  var startTime, curTime;
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#video_file_field").fileupload({
    dataType: 'json',
    start: function(e) {
	startTime = new Date();
	$(".upload-progress").css("display", "block")
    },
    stop: function (e){
        $(".upload-progress").css("display", "none")
    },
    progressall: function (e, data) {
      curTime = new Date();
      var dif = curTime - startTime
      dif/=1000;
      var progress = parseFloat(data.loaded / data.total * 100, 10);
      var strProgress = progress + "%";
      var strTime = "" +dif;
      $(".bar").css({"width": strProgress});
      $(".time").text(strProgress);
      $(".label").text(strTime);
    },
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
	console.log("it worked!");
      }
    }
  });


   /*ADAPTED FROM https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data*/
   /* 3. BIND formData loader to the upload event */

  $('#video_file_field').bind('fileuploadsubmit', function (e, data) {
      // The example input, doesn't have to be part of the upload form:
      var input = $('select[name=session-select]');
      data.formData = {session_pk: input.val()};
      if (!data.formData.session_pk) {
        //data.context.find('button').prop('disabled', false);
        input.focus();
        return false;
      }
  });

});

$(function () {

  /* 1. OPEN THE FILE EXPLORER WINDOW */
  $("#csvButton").click(function () {
    $("#csv_file_field").click();
  });

 
  /* 2. INITIALIZE THE FILE UPLOAD COMPONENT */
  $("#csv_file_field").fileupload({
    dataType: 'json',
    done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
      if (data.result.is_valid) {
	console.log("this doesn't work");
      }
    }
  });


   /*ADAPTED FROM https://github.com/blueimp/jQuery-File-Upload/wiki/How-to-submit-additional-form-data*/
   /* 3. BIND formData loader to the upload event */

  $('#csv_file_field').bind('fileuploadsubmit', function (e, data) {
      // The example input, doesn't have to be part of the upload form:
      var input = $('select[name=session-select]');
      data.formData = {session_pk: input.val()};
      if (!data.formData.session_pk) {
        //data.context.find('button').prop('disabled', false);
        input.focus();
        return false;
      }
  });

});


