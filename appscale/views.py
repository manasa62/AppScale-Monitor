# Create your views here.
from django.conf import settings
from django.shortcuts import render_to_response
from django.core import serializers
from django.http import HttpResponse
import simplejson
json = simplejson
import os
import re
import string
import paramiko
import sys
import logging
import pexpect

logger = logging.getLogger(__name__)
head_node='';
password='';
path = '/root/appscale_tools/appscale-tools-1.4/templates/';

def home(request):
    return render_to_response('index.html');

def homepost(request):
    home = {};
    global head_node,password,path;
    password = request.GET['pswd'];
    head_node = request.GET['controller'];
    
    if password == "" :
        home["success"] = "false";
    if head_node == "" :
        home["ip_success"] = "false";
    else:
        home["success"] = "true";  
    home["message"]="Information submitted Successfully!";
    
    return HttpResponse(json.dumps(home));  


def editpost(request):
    home = {};
    global head_node,password,path;
    password = request.GET['pswd'];
    head_node = request.GET['controller'];
    server1 = request.GET['server1'];
    server2 = request.GET['server2'];
    server3 = request.GET['server3'];
      
    if password == "" :
        home["success"] = "false";
    if head_node == "" :
        home["ip_success"] = "false";
    else:
        home["success"] = "true";
        ssh_session = pexpect.spawn ('ssh root@'+head_node);
        ssh_session.expect('.*password:');
        ssh_session.sendline(password);
        login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
        if login_index == 0:
                ssh_session.sendline('echo --- > '+path+'ips.yaml');
                ssh_session.sendline('echo :controller: '+head_node+' >> '+path+'ips.yaml');
                ssh_session.sendline('echo :servers: '+' >> '+path+'ips.yaml');
                
                if server1 != 'NA':
                    ssh_session.sendline('echo - '+server1+' >> '+path+'ips.yaml');
                    ssh_session.expect('root@appscale-image0:~#');
                if server2 != 'NA':
                    ssh_session.sendline('echo - '+server2+' >> '+path+'ips.yaml');
                    ssh_session.expect('root@appscale-image0:~#');                
                if server3 != 'NA':   
                    ssh_session.sendline('echo - '+server3+' >> '+path+'ips.yaml');
                    ssh_session.expect('root@appscale-image0:~#');
                
                ssh_session.sendline('cat '+path+'ips.yaml');
                
                
                
        home["message"]="ips.yaml edited submitted Successfully!";
    
    return HttpResponse(json.dumps(home));   
        
def addkeypair(request):
    return render_to_response('add.html');
    

def addkeypairpost(request):
    key_status = {};
    global head_node,password,path;
    #try:
    message = "Permission denied. Please try again";
    
   
    password = request.GET['pswd'];
    head_node = request.GET['ip'];  
    if password == "" :
        key_status["success"] = "false";
    if head_node == "" :
        key_status["ip_success"] = "false";
    
        return HttpResponse(json.dumps(key_status));
    #return render_to_response('add.html', {'key_status':key_status})
    
    else :
        key_status["success"] = "true";
        key_status["password"] = password;
          
        ssh_session = pexpect.spawn ('ssh root@'+head_node);
        ssh_session.expect('.*password:');
        ssh_session.sendline(password);
        login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
        if login_index == 0:
       
            ssh_session.sendline('appscale-add-keypair --ips '+path+'ips.yaml');
           
            
            end_session = "false";
            while end_session == "false":
                index = ssh_session.expect(['root@appscale-image0:~#','.*password:','.*connecting (yes/no)?']);
                if index == 0:
                    message = ssh_session.before;
                    split_message = message.splitlines();
                    end_session = "true";
               
                if index == 1:
                   ssh_session.sendline(password);
                
                if index == 2:
                    ssh_session.sendline('yes');
               # message = split_message[1];
           
            message = "";       
            i=2;
            while i != (len(split_message) -1) :
                message = message + "\n" + split_message[i];
                i=i+1;
            
        if login_index == 1:
            ssh_session.sendline(password);
            
        
           # key_status["error"] = "Addition of Key Pair Failed";
        key_status["success"] = "true";
           # message = stderr.readline();
        key_status["message"] = message;
        return HttpResponse(json.dumps(key_status));
 
    
def describe_instances(request):
  
    global head_node,password;
    
    empty_status = 'empty';
    if head_node=='' or password =='':
            return render_to_response('view.html', {'empty_status':empty_status});
        
    ssh_session = pexpect.spawn ('ssh root@'+head_node);
    ssh_session.expect('.*password:');
    ssh_session.sendline(password);
    login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
    if login_index == 0:
        ssh_session.sendline('appscale-describe-instances');
        ssh_session.expect('root@appscale-image0:~#');
    
        message = ssh_session.before;
        split_message = message.splitlines();
    
        as_status =[];
        i=2;
        if len(split_message) < 5 :
            return render_to_response('view.html', {'as_status':as_status})
            
        else :
            while i < len(split_message):
                line = split_message[i];
                cpu = re.findall('\d+\.\d+',line);
                as_status.append(cpu[0]);
                as_status.append(cpu[1]);
              
                line = split_message[i+1];
                hdd = re.findall('\d+',line);
                as_status.append(hdd[0]);
                
                line = split_message[i+2];
                parts = re.split(':',line);
                
                new_parts =  re.split(',',parts[1]);
                fn = '';
                for part in new_parts :
                    fn = fn + part+ ",";
                fn = fn.rstrip(fn[-1:]);
                as_status.append(fn);
                    
                line = split_message[i+3];
                ip = re.findall('\d+\.\d+\.\d+\.\d+', line);
               # print "IP "+ip[0];
                as_status.append(ip[0]);
                
                line = split_message[i+4];    
                status = re.split(':',line);
               # print "Status "+status[1];
                as_status.append(status[1]);
                
                line = split_message[i+5];
                if line.find('apps') > -1:
                    parts = re.split(':',line);
                    
                    new_parts =  re.split(',',parts[1]);
                    #print "Apps ";
                    apps ='';
                    for part in new_parts :
                        apps = apps +part+",";
                    apps = apps.rstrip(apps[-1:]);
                    as_status.append(apps);
                   # print apps;
                    i=i+7;
             #   as_status = [cpu[0],cpu[1],hdd[0],fn,ip[0],status[1],apps];
                else:
                    as_status.append('');
                    i=i+6;
            
    if login_index == 1:
                as_status = ['View of Appscale instances failed due to failure of login into head node'];        
    
    return render_to_response('view.html', {'as_status':as_status}) 
    
def terminate_instances(request):
  
    as_status =[];
    ssh_session = pexpect.spawn ('ssh root@'+head_node);
    ssh_session.expect('.*password:');
    ssh_session.sendline(password);
    login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
    if login_index == 0:
        ssh_session.sendline('appscale-terminate-instances --ips '+path+'ips.yaml');
        ssh_session.expect('root@appscale-image0:~#');
    
    message = ssh_session.before;
    split_message = message.splitlines();
        
    i=2;
    message ="";
    while i != (len(split_message) -1) :
       as_status.append(split_message[i]);
       i=i+1;
    
    if login_index == 1:
        as_status = ['Terminating Appscale instances failed due to failure of login into head node'];
  #  as_status = [message];
    return render_to_response('term.html', {'as_status':as_status})  

def run_instances(request):
    
    return render_to_response('run.html');

def run_instances_post(request):
    as_status = {};
    global head_node,password,path;
    
    email = request.GET['email'];
    ad_password = request.GET['pswd'];
       
    if email == "" :
        as_status["email_success"] = "false";
    if ad_password == "" :
        as_status["pswd_success"] = "false";
    
    
        return HttpResponse(json.dumps(as_status));
    #return render_to_response('add.html', {'key_status':key_status})
    
    else :
         as_status["email_success"] = "true";
         as_status["pswd_success"] = "true";
    
    
    ssh_session = pexpect.spawn ('ssh root@'+head_node);
    ssh_session.expect('.*password:');
    ssh_session.sendline(password);
    login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
    if login_index == 0:
        ssh_session.sendline('appscale-run-instances --ips '+path+'ips.yaml');
        index = ssh_session.expect(['.*e-mail address:', 'root@appscale-image0:~#']);
        if index==0:
            ssh_session.sendline(email);
            ssh_session.expect('.*password:');
            ssh_session.sendline(ad_password);
            ssh_session.expect('.*verify:');
            ssh_session.sendline(ad_password);
            
            ssh_session.expect('root@appscale-image0:~#', timeout=150);
            
        
        message = ssh_session.before;
        split_message = message.splitlines();
            
        i=2;
        message ="";
        while i != (len(split_message) -1) :
           message = message + split_message[i];
           i=i+1;
        as_status["message"] = message;
        
    if login_index == 1:
                as_status["message"] = 'Starting Appscale instances failed due to failure of login into head node';  
    
   
    return HttpResponse(json.dumps(as_status));

def upload_app(request):
    return render_to_response('upload.html');
    
def upload_app_post(request):
    up_status={};
    
    appfile = request.GET['appfile'];
    email = request.GET['email'];
    ad_password = request.GET['pswd'];
     
    if appfile == "" :
        up_status["file_success"] = "false";
    if email == "" :
        up_status["email_success"] = "false";
    if ad_password == "" :
        up_status["pswd_success"] = "false";
    
    
        return HttpResponse(json.dumps(up_status));
    #return render_to_response('add.html', {'key_status':key_status})
    
    else :
         up_status["email_success"] = "true";
         up_status["pswd_success"] = "true";
         up_status["file_success"] = "true";
         ssh_session = pexpect.spawn ('ssh root@'+head_node);
         ssh_session.expect('.*password:');
         ssh_session.sendline(password);
         login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
         if login_index == 0:
             ssh_session.sendline('appscale-upload-app --file ' + appfile);
             email_index = ssh_session.expect(['.*e-mail address','root@appscale-image0:~#']);
             if email_index == 0:
                 ssh_session.sendline(email);
                 index = ssh_session.expect(['.*password:','root@appscale-image0:~#']);
                 if index==0 :
                    ssh_session.sendline(ad_password);
                    ssh_session.expect('.*verify:');
                    ssh_session.sendline(ad_password);
                    ssh_session.expect('root@appscale-image0:~#');
        
    
             message = ssh_session.before;
             split_message = message.splitlines();
                
             i=2;
             message ="";
             while i != (len(split_message) -1) :
               message = message + split_message[i];
               i=i+1;
            
             up_status["message"] = message;
         if login_index == 1:
                up_status["message"] = 'Uploading app into Appscale failed due to failure of login into head node';
             
         return HttpResponse(json.dumps(up_status));
         
     
def remove_app(request):
    return render_to_response('remove.html');

def remove_app_post(request):
    rm_status={};
    
    appname = request.GET['appname'];
    
    if appname == "" :
        rm_status["app_success"] = "false";
 
        return HttpResponse(json.dumps(rm_status));
    
    else :
         rm_status["app_success"] = "true";
         ssh_session = pexpect.spawn ('ssh root@'+head_node);
         ssh_session.expect('.*password:');
         ssh_session.sendline(password);
         login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
         if login_index == 0:
             ssh_session.sendline('appscale-remove-app --appname '+appname);
             ssh_session.expect('application (Y/N)?');
             ssh_session.sendline('Y');
             ssh_session.expect('root@appscale-image0:~#');
            
             message = ssh_session.before;
             split_message = message.splitlines();
                
             i=1;
             message ="";
             while i != (len(split_message) -1) :
               message = message + split_message[i];
               i=i+1;
            
             rm_status["message"] = message;
         
         if login_index ==1:
             rm_status["message"] = 'Removing app from Appscale failed due to failure of login into head node';
         return HttpResponse(json.dumps(rm_status));
     
def reset_pwd(request):
    
    return render_to_response('reset.html');

def reset_pwd_post(request):
    as_status = {};
    global head_node,password,path;
    
    email = request.GET['email'];
    ad_password = request.GET['pswd'];
    ad_password2 = request.GET['pswd2'];   
    
    if email == "" :
        as_status["email_success"] = "false";
    if ad_password == "" :
        as_status["pswd_success"] = "false";
    if ad_password2 == "" :
        as_status["pswd2_success"] = "false";
    
        return HttpResponse(json.dumps(as_status));
    #return render_to_response('add.html', {'key_status':key_status})
    
    else :
         as_status["email_success"] = "true";
         as_status["pswd_success"] = "true";
         as_status["pswd2_success"] = "true";
    
    ssh_session = pexpect.spawn ('ssh root@'+head_node);
    ssh_session.expect('.*password:');
    ssh_session.sendline(password);
    login_index = ssh_session.expect(['root@appscale-image0:~#','.*password:']);
    if login_index == 0:
        ssh_session.sendline('appscale-reset-pwd');
        ssh_session.expect('.*e-mail address:');
        
        ssh_session.sendline(email);
        ssh_session.expect('.*password:');
        ssh_session.sendline(ad_password);
        ssh_session.expect('.*verify:');
        ssh_session.sendline(ad_password2);
        ssh_session.expect('root@appscale-image0:~#');
        
        message = ssh_session.before;
        split_message = message.splitlines();
            
        i=0;
        message ="";
        while i != (len(split_message) -1) :
           message = message + split_message[i];
           i=i+1;
        as_status["message"] = message;
        
    if login_index == 1:
                as_status["message"] = 'Reset Password failed due to failure of login into head node';  
    
   
    return HttpResponse(json.dumps(as_status));
     
    