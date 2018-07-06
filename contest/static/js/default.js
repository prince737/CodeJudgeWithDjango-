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
	val = 1;
});

$("#q2").click(function(){
	val = 2;
});

$("#q3").click(function(){
	val = 3;
});

$("#q4").click(function(){
	val = 4;
});

$("#q5").click(function(){
	val = 5;
});

if(localStorage.getItem("q1") != null){
	localStorage.getItem("q1");
}
else{
	"Not Attempted Yet!"
}

var temp = (localStorage.getItem("q1")) ? localStorage.getItem("q1") : "Not Attempted Yet!";
$("#q1").html(temp);
temp = (localStorage.getItem("q2")) ? localStorage.getItem("q2") : "Not Attempted Yet!";
$("#q2").html(temp);
temp = (localStorage.getItem("q3")) ? localStorage.getItem("q3") : "Not Attempted Yet!";
$("#q3").html(temp);
temp = (localStorage.getItem("q4")) ? localStorage.getItem("q4") : "Not Attempted Yet!";
$("#q4").html(temp);
temp = (localStorage.getItem("q5")) ? localStorage.getItem("q5") : "Not Attempted Yet!";
$("#q5").html(temp);

/*Submission of code*/
$('#codeform').on('submit', function(e){
	e.preventDefault();
	
	
	$("#output").hide();

	var time= $('#timestamp').html();
	var code = $('#code').val();
	var ciw = $('#custom-input').val();
	var mode = $("#mode :selected").text();
	var qid = val;
	var url = "/contest/begin/";

	var q = 'q'+qid;


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
			time: time,
			event: event,
			csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
		},
		success: function(context){
			$("#load").hide();
			if(event == 'submit'){
				if(context.op == 'Accepted!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").hide();
					$("#accepted").show();
					a = "Accepted! Score = 20";
				}
				else if(context.op == 'Wrong Answer!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").show();
					$("#compile").hide();
					$("#tle").hide();
					$("#accepted").hide();
					a = context.op;
				}
				else if(context.op == 'Time Limit Exceeded!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").show();
					$("#accepted").hide();
					a = context.op;
				}
				else if(context.op == 'Compilation Error!'){
					$("#err").hide();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").show();
					$("#tle").hide();
					$("#accepted").hide();
					a = context.op;
				}
			}
			else{
				if(context.err === ""){
					$("#succ").show();
					$("#err").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").hide();
					$("#accepted").hide();
				}
				else{
					$("#err").show();
					$("#succ").hide();
					$("#wrong").hide();
					$("#compile").hide();
					$("#tle").hide();
					$("#accepted").hide();
				}
					
				$("#output").show();
				$("#op").html(context.op);
				var a = "Not Attempted Yet!"
			}

			localStorage.setItem(q,a);
			$("#"+q).html(localStorage.getItem(q));
			
		}
	});
 
	return false;
});





