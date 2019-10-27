function pullCSV(){
	var sess = $("#session-select").children("option:selected").val();
	if(sess!=''){
		window.location='/TurtleVision/export/CSV_from_session/' +sess;
	}
}

function load_and_train(){
	var anal = $("#analysis-select").children("option:selected").val();
	if(anal!=''){
		window.location='/TurtleVision/dataAnalyze/upload_and_train/' +anal;
	}
}

function occupy_seconds(){
	var sess = $("#session-select").children("option:selected").val();
	var anal = $("#analysis-select").children("option:selected").val();
	if(anal!=''&&sess!=''){
		window.location='/TurtleVision/dataAnalyze/update_seconds/' +sess +'/'+anal;
	}
}