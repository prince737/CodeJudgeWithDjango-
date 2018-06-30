var code = $(".codemirror-textarea")[0];
var editor = CodeMirror.fromTextArea(code, {
	lineNumbers: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    mode: "text/x-c++src", //"text/x-java", "text/x-csrc", "text/x-python", 
    indentUnit : 4,
    lineWrapping : true,
    extraKeys : {"Ctrl-Space": "autocomplete"}
});
editor.setSize(null,400);
	 	
function changeMode(){
	var x = document.getElementById("mode").value;
	editor.setOption("mode", x);		
}

/*--------GETTING QUESTION ID--------*/

var val = 1;

$("#q1").click(function(){
	alert("1")
	val = 1;
});

$("#q2").click(function(){
	alert("2")
	val = 2;
});

$("#q3").click(function(){
	alert("3")
	val = 3;
});

$("#q4").click(function(){
	alert("4")
	val = 4;
});

$("#q5").click(function(){
	alert("5")
	val = 5;
});



/*Submission of code*/
$('#codeform').on('submit', function(e){
	e.preventDefault();
	
	
	$("#output").hide();

	var code = $('#code').val();
	var ciw = $('#custom-input').val();
	var mode = $("#mode :selected").text();
	var qid = val;
	var url = "/contest/begin/";

	if(code.trim()==""){
		M.toast({html: 'Atleast print "hello world!"',classes: 'rounded custom'});
		return false;
	}

	var $btn = $(document.activeElement);
	var event = $btn.prop("id");

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
			var a;
			console.log(context.op);
			if(event == 'submit'){
				if(context.op == 'Accepted!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").hide();
					$("accepted").show()
				}
				else if(context.op == 'Wrong Answer!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").show();
					$("#compile").hide();
					$("#tle").hide();
					$("accepted").hide()
				}
				else if(context.op == 'Time Limit Exceeded!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").show();
					$("accepted").hide()
				}
				else if(context.op == 'Compilation Error!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").show();
					$("#tle").hide();
					$("accepted").hide()
				}
			}
			else{
				if(context.err === ""){
					$("#succ").show();
					$("#err").hide();
				}
				else{
					$("#err").show();
					$("#succ").hide();
				}
					
				$("#output").show();
				$("#op").html(context.op);
			}
			
		}
	});

	return false;
});



