function pullCSV(){
	var sess = $("#session-select").children("option:selected").val();
	if(sess!=''){
		window.location='/TurtleVision/export/CSV_from_session/' +sess;
	}
}

function load_and_train(){
	var anal = $("#analysis-select").children("option:selected").val();
	if(anal!=''){
		window.location='/TurtleVision/dataAnalyze/upload_and_train/' +'BreathStat';
	}
}

function occupy_seconds(){
	var anal = $("#analysis-select").children("option:selected").val();
	if(anal!='' && sess!=''){
		window.location='/TurtleVision/dataAnalyze/update_seconds/' +'BreathStat'+'/'+sess;
	}
}