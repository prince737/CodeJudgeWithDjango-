var code = $(".codemirror-textarea")[0];
var editor = CodeMirror.fromTextArea(code, {
	lineNumbers: true,
    matchBrackets: true,
    mode: "text/x-c++src", //"text/x-java", "text/x-csrc", "text/x-python", 
    indentUnit : 4,
    lineWrapping : true,
    extraKeys : {"Ctrl-Space": "autocomplete"}
});
editor.setSize(null,600);
	 	
function changeMode(){
	var x = document.getElementById("mode").value;
	editor.setOption("mode", x);		
}

/*--------GETTING QUESTION ID--------*/

var val = $("#qid1").html();
$("#hqid").val(val);

$("#q1").click(function(){
	var val = $("#qid1").html()
	$("#hqid").val(val);
});

$("#q2").click(function(){
	var val = $("#qid2").html()
	$("#hqid").val(val);
});

$("#q3").click(function(){
	var val = $("#qid3").html()
	$("#hqid").val(val);
});


/*Submission of code*/
$('#codeform').on('submit', function(e){
	e.preventDefault();
	
	var code = $('#code').val();
	var ciw = $('#custom-input').val();
	var mode = $("#mode :selected").text();
	var qid = $("#hqid").val();

	$.ajax({
		url: "/contest/begin/",
		type: "POST",
		data: {
			code: code,
			mode: mode,
			qid: qid,
			ciw: ciw,
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
		},
		success: function(){
			alert("submitted");
		}
	});

	return false;
});



