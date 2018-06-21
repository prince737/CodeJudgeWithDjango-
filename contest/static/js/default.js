var code = $(".codemirror-textarea")[0];
var editor = CodeMirror.fromTextArea(code, {
	lineNumbers: true,
    matchBrackets: true,
    mode: "text/x-c++src", //"text/x-java", "text/x-csrc", "text/x-python", 
    indentUnit : 4,
    lineWrapping : true,
    extraKeys : {"Ctrl-Space": "autocomplete"}
});
editor.setSize(null,200);
	 	
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
	var url = "/contest/begin/";

	if(code==""){
		M.toast({html: 'Atleast print "hello world!"',classes: 'rounded custom'});
		return false;
	}

	var $btn = $(document.activeElement);
	var event = $btn.prop("id");

	console.log(event);

	$("#load").show();
	$.ajax({
		url: url,
		type: "POST",
		data: {
			code: code,
			mode: mode,
			qid: qid,
			ciw: ciw,
			event: event,
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
		},
		success: function(context){
			$("#load").hide();
			var a = context.op;
			var html = '';
			for (i = 0; i < a.length; ++i) {
			    html += a[i]+'<br>';
			}
			$("#op").html(html);
		}
	});

	return false;
});



