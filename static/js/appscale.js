function notify(message, title){
  $("#notification").remove();
  msg = $("<div>").append(message).attr("id","notification");
  $("#notification-dialog").append(msg);
  if (title){
    $("#ui-dialog-title-notification-dialog").html(title);
  }
  else{
    $("#ui-dialog-title-notification-dialog").html("Notification Message");
  }
  $("#notification-dialog").dialog("open");
}

function run_instance_response(data){
	if (data.email_success == "false") {
		notify("Provide a Valid email Id");
	}
	else if (data.pswd_success == "false") {
		notify("Password field cannot be left blank");
	}
	else {
	$("#new_data").empty(); 
	$("#new_data").append("\nMessage: "+data.message);
	}
}

function post_run_instance(){
  var email = $("#email").val();
  var pswd = $("#pswd").val();
  $.get("/run_instances_post", {'email':email,'pswd':pswd},run_instance_response ,"json");
}

function upload_app_response(data){
	if (data.file_success == "false") {
		notify("Provide a Valid path to the app you are uploading");
	}
	if (data.email_success == "false") {
		notify("Provide a Valid email Id");
	}
	else if (data.pswd_success == "false") {
		notify("Password field cannot be left blank");
	}
	else {
	$("#new_data").empty(); 
	$("#new_data").append("\nMessage: "+data.message);
	}
}

function post_upload_app(){
  var appfile = $("#appfile").val();
  var email = $("#email").val();
  var pswd = $("#pswd").val();
  $.get("/upload_app_post", {'email':email,'pswd':pswd,'appfile':appfile},upload_app_response ,"json");
}

function remove_app_response(data){
	if (data.app_success == "false") {
		notify("Provide a Valid app name that has to be removed!");
	}
	
	else {
	$("#new_data").empty(); 
	$("#new_data").append("\nMessage: "+data.message);
	}
}

function post_remove_app(){
  var appname = $("#appname").val();
  $.get("/remove_app_post", {'appname':appname},remove_app_response ,"json");
}



function add_key_response(data){
	if (data.ip_success == "false") {
		notify("IP Address field cannot be blank! Please enter a valid IP.")
	}
	if (data.success == "false") {
		notify("Password field cannot be blank! Please enter a valid password.")
	}
	else {
	$("#new_data").empty();
	message = data.message.split("\n");
	$("#new_data").append("Message: ");
	for (i=0;i<message.length;i++) {
		if(message[i]!=""){
		$("#new_data").append("<br/>");
		$("#new_data").append(message[i]);
		}
	 }
	}
}


function post_add_key(){
 
  var ip = $("#ip").val();
  var pswd = $("#pswd").val();  
  
  $.get("/addkeypairpost", {'ip': ip, 'pswd':pswd}, add_key_response,"json");
  
}
function post_edit(){
	var controller = $("#controller").val();
	var server1 = $("#server1").val();
	var server2 = $("#server2").val();
	var server3 = $("#server3").val();
	var pswd = $("#pswd").val();  
	$.get("/editpost", {'controller': controller,'server1': server1,'server2': server2, 'server3': server3, 'pswd':pswd}, edit_response,"json");
}
function post_home(){
	 
	  var controller = $("#controller").val();
	/*  var server1 = $("#server1").val();
	  var server2 = $("#server2").val();
	  var server3 = $("#server3").val();*/
	  var pswd = $("#pswd").val();  
	  $.get("/homepost", {'controller': controller,'pswd':pswd}, home_response,"json");
	  
	  $("#home").append("<p>Enter the IP's of the Appservers if you want to edit the ips.yaml file. Enter 'NA' if you do not need them.</p>");
	  
	  $("#home").append("<label>Server1:</label>");
      $("#home").append("<input id=\"server1\" name=\"server1\" size=\"30\" type=\"text\" />");
	  $("#home").append("<br/>");
	  $("#home").append("<label>Server2:</label>");
      $("#home").append("<input id=\"server2\" name=\"server2\" size=\"30\" type=\"text\" />");
	  $("#home").append("<br/>");
	  $("#home").append("<label>Server3:</label>");
      $("#home").append("<input id=\"server3\" name=\"server3\" size=\"30\" type=\"text\" />");
	  $("#home").append("<br/>");
	  $("#home").append("<br/><br/>");
	  $("#home").append("<a id=\"password_button\" class=\"ui-button ui-widget ui-state-default ui-corner-all ui-button-text-only\" type=\"submit\" role=\"button\" href=\"javascript:post_edit()\">Edit</a>");
	  
	  
	}

function home_response(data){
	if (data.ip_success == "false") {
		notify("IP Address field cannot be blank! Please enter a valid IP.")
	}
	if (data.success == "false") {
		notify("Password field cannot be blank! Please enter a valid password.")
	}
	else {
	$("#new_data").empty();
	message = data.message.split("\n");
	$("#new_data").append("Message: "+message);
	
	}
}

function edit_response(data){
	if (data.ip_success == "false") {
		notify("IP Address field cannot be blank! Please enter a valid IP.")
	}
	if (data.success == "false") {
		notify("Password field cannot be blank! Please enter a valid password.")
	}
	else {
	$("#new_data").empty();
	message = data.message.split("\n");
	$("#new_data").append("Message: "+message);
	
	}
}

function reset_pwd_response(data){
	if (data.email_success == "false") {
		notify("Provide a Valid email Id");
	}
	else if (data.pswd_success == "false") {
		notify("Password field cannot be left blank");
	}
	else if (data.pswd2_success == "false") {
		notify("Verify Password field cannot be left blank");
	}
	else {
	$("#new_data").empty(); 
	$("#new_data").append("\nMessage: "+data.message);
	}
}

function post_reset_pwd(){
  var email = $("#email").val();
  var pswd = $("#pswd").val();
  var pswd2 = $("#pswd2").val();
  if(pswd !== pswd2){
	  notify("Passwords do not match!");
  }
  else {
  $.get("/reset_pwd_post", {'email':email,'pswd':pswd,'pswd2':pswd2},reset_pwd_response ,"json");
  }
}

function setup_notification_dialog(){
    var confirmed = function(){
      $("#notification-dialog").dialog("close");
    };

    var dialogOpts = {
      autoOpen: false,
      draggable: true,
      hide: 'fold',
      position: 'center',
      modal: true,
      buttons: {
        "Close": confirmed
      }
    };

    $("#notification-dialog").dialog(dialogOpts);
}

function init_appscale(){
  setup_notification_dialog();
  $("#password_button").button();
}
