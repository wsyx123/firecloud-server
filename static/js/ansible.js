//添加步骤
function addStep(obj){
	div_id = div_id + 1;
	var id = div_id;
	var ul_str='<ul class="nav nav-tabs">\
					<li class="active">\
						<a data-toggle="tab" href="#task'+id+'"><span class="red"> *</span>tasks</a>\
					</li>\
					<li>\
						<a data-toggle="tab" href="#handler'+id+'">handlers</a>\
					</li>\
					<li>\
						<a data-toggle="tab" href="#var'+id+'">vars</a>\
					</li>\
					<li>\
						<a data-toggle="tab" href="#template'+id+'">templates</a>\
					</li>\
					<li>\
						<a data-toggle="tab" href="#file'+id+'">files</a>\
					</li>\
					<li>\
						<a data-toggle="tab" href="#host'+id+'"><span class="red"> *</span>hosts(已选服务器) <span class="badge badge-danger">0</span></a>\
					</li>\
				</ul>'
	var task_div_str='<div id="task'+id+'" class="tab-pane in active">\
						备注:<span class="smaller green">这里所编写的任务会保存在此步骤（角色）下的<strong class="red"> tasks </strong>目录下的main.yml文件中</span>\
						<p></p>\
						<div id="task-editor'+id+'" class="ace_editor" style="min-height:200px"></div>\
					</div>'
	var handler_div_str='<div id="handler'+id+'" class="tab-pane">\
						备注:<span class="smaller green">这里所编写的任务会保存在此步骤（角色）下的<strong class="red"> handlers </strong>目录下的main.yml文件中</span>\
						<p></p>\
						<div id="handler-editor'+id+'" class="ace_editor" style="min-height:200px"></div>\
					</div>'
	var var_div_str='<div id="var'+id+'" class="tab-pane">\
						备注:<span class="smaller green">这里所编写的任务会保存在此步骤（角色）下的<strong class="red"> vars </strong>目录下的main.yml文件中</span>\
						<p></p>\
						<div id="var-editor'+id+'" class="ace_editor" style="min-height:200px"></div>\
					</div>'
	var template_div_str='<div id="template'+id+'" class="tab-pane">\
							备注:<span class="smaller green">这里所上传的文件会保存在此步骤（角色）下的<strong class="red"> templates </strong>目录下</span>\
							<p></p>\
							<div class="widget-box">\
								<div class="widget-body">\
									<table class="table">\
										<thead>\
											<tr><th>文件名</th><th>状态</th><th>大小</th><th>动作</th></tr>\
										</thead>\
										<tbody id="templatefilelist'+id+'">\
										</tbody>\
									</table>\
								</div>\
								<div class="widget-footer">\
									<div id="templatecontainer'+id+'" class="center">\
										<a id="templatepickfile'+id+'" href="javascript:;"><button class="btn btn-white btn-info btn-xs btn-bold" type="button">选择文件</button></a>\
										<a id="templateuploadfile'+id+'" href="javascript:;"><button class="btn btn-white btn-info btn-xs btn-bold">上传文件</button></a>\
									</div></div></div></div>'
	var file_div_str='<div id="file'+id+'" class="tab-pane">\
							备注:<span class="smaller green">这里所上传的文件会保存在此步骤（角色）下的<strong class="red"> files </strong>目录下</span>\
							<p></p>\
							<div class="widget-box">\
								<div class="widget-body">\
									<table class="table">\
										<thead>\
											<tr><th>文件名</th><th>状态</th><th>大小</th><th>动作</th></tr>\
										</thead>\
										<tbody id="filefilelist'+id+'">\
										</tbody>\
									</table>\
								</div>\
								<div class="widget-footer">\
									<div id="filecontainer'+id+'" class="center">\
										<a id="filepickfile'+id+'" href="javascript:;"><button class="btn btn-white btn-info btn-xs btn-bold" type="button">选择文件</button></a>\
										<a id="fileuploadfile'+id+'" href="javascript:;"><button class="btn btn-white btn-info btn-xs btn-bold">上传文件</button></a>\
									</div></div></div></div>'
	var host_div_str='<div id="host'+id+'" class="tab-pane">\
							备注:<span class="smaller green">以下列表的主机会被保存在<strong class="red"> roles </strong>同级目录的<strong class="red"> hosts </strong>文件里，组名为步骤名</span>\
							<p></p>\
							<div class="widget-box">\
								<div class="widget-body">\
							<table class="table">\
								<tr>\
									<th>主机名</th>\
									<th>状态</th>\
									<th>帐号</th>\
									<th>IP</th>\
									<th>动作</th>\
								</tr>\
							</table>\
							</div>\
							</div>\
						</div>'
	var widget_header_str='<div class="widget-header">\
								<div style="padding-top:5px;display:inline-block;">\
									<span class="white">步骤名称<span class="red"> *</span></span><input name="step'+id+'" type="text" style="line-height:15px;" />\
								</div>\
								<div class="widget-toolbar" onclick="delStep(this);">\
									<label class="white">\
										<i class="fa fa-times"></i>\
									</label>\
								</div>\
								<div class="widget-toolbar">\
									<label class="white">\
										<i class="fa fa-angle-double-up" onclick="switchUpDown(this);"></i>\
									</label>\
								</div>\
								<div class="widget-toolbar" onclick="setModalRelID(this);">\
									<label class="white">\
										<i class="fa fa-plus" aria-hidden="true"></i>\
										<b data-toggle="modal" data-target="#myselect">选择服务器</b>\
									</label>\
								</div>\
							</div>'
	var tab_content_str='<div class="tab-content">'+task_div_str+handler_div_str+var_div_str+template_div_str+file_div_str+host_div_str+'</div>'
	var widget_body_str='<div class="widget-body">\
							<div class="widget-main">\
								<div class="tabbable">'+ul_str+tab_content_str+
								'</div>\
							</div>\
						</div>'
	var widget_box_str='<div class="widget-box" id="step'+id+'">'+widget_header_str+widget_body_str+'</div>'
	
	$(obj).parent().before(widget_box_str);
	setAceEditMode('task-editor'+id,'yaml','');
	setAceEditMode('handler-editor'+id,'yaml','');
	setAceEditMode('var-editor'+id,'yaml','');
	InitFileUpload('templatepickfile'+id,'templatecontainer'+id,'templatefilelist'+id,'templateuploadfile'+id);
	InitFileUpload('filepickfile'+id,'filecontainer'+id,'filefilelist'+id,'fileuploadfile'+id);
	
}

//删除步骤
function delStep(obj){
	$(obj).parent().parent().remove();
}

// 清除ace editor中所有内容
function removeAllLines(editor){
	AllLines = $(".ace_line");
	for(var i=0;i<AllLines.length;i++){
		editor.removeLines();
	}
}

// 设置ace-editor 模式
function setAceEditMode(id,model,content) {
	var editor = ace.edit(id);
	var langTools = ace.require("ace/ext/language_tools");
	editor.setTheme("ace/theme/monokai");
	//editor.removeLines();
	removeAllLines(editor);
	editor.insert(content);
	editor.getSession().setMode("ace/mode/" + model);
	editor.setShowPrintMargin(false);
	editor.setOptions({
	    enableBasicAutocompletion: true,
	    enableSnippets: true,
	    enableLiveAutocompletion: true
	});
};


//文件上传初始化
function InitFileUpload(pickfileID,containerID,filelistID,uploadfileID){
	var uploader = new plupload.Uploader({
	runtimes : 'html5,flash,silverlight,html4',
	browse_button : pickfileID, // you can pass an id...
	container: document.getElementById(containerID), // ... or DOM Element itself
	url : '/ansible/add/file/',
	flash_swf_url : '/static/plupload-2.3.6/js/Moxie.swf',
	silverlight_xap_url : '/static/plupload-2.3.6/js/Moxie.xap',
	
	filters : {
		max_file_size : '10mb',
		mime_types: [
			{title : "Template files", extensions : "*"},
		]
	},

	init: {
		PostInit: function() {
			document.getElementById(filelistID).innerHTML = '';
			document.getElementById(uploadfileID).onclick = function() {
				uploader.start();
				return false;
			};
		},

		FilesAdded: function(up, files) {
			plupload.each(files, function(file) {
				var txt = '<tr><td>' + file.name + '</td><td id="'+file.id+'">0%</td><td>' + plupload.formatSize(file.size) + '</td><td><button type="button" onclick="delFile(this);" class="btn btn-minier btn-danger">删除</button></td></tr>';
				document.getElementById(filelistID).innerHTML += txt;
			});
		},
		
		BeforeUpload: function(up,file){
			var TmpStepNum = uploadfileID.charAt(uploadfileID.length-1);
			var playbook_name = $("input[name='playbook_name']").val();
			var role_name = $("input[name='step"+TmpStepNum+"']").val();
			var file_type =  "";
			if(containerID.indexOf("template") != -1){
				var file_type = 'templates';
			}else if(containerID.indexOf("file") != -1){
				var file_type = 'files';
			}
			if(playbook_name==''|| role_name==''){
				uploader.stop();
				alert("请输入剧本名称和步骤名称!");
				
			}
			uploader.setOption("multipart_params",{"playbook_name":playbook_name,"role_name":role_name,"file_type":file_type});
		},

		UploadProgress: function(up, file) {
			document.getElementById(file.id).innerHTML = '<span>' + file.percent + "%</span>";
		},

		Error: function(up, err) {
			document.getElementById('console').appendChild(document.createTextNode("\nError #" + err.code + ": " + err.message));
		}
	}
});

uploader.init();
	
}

//expand or collapse step input feild
function switchUpDown(obj){
	classStr = $(obj).attr('class');
	if(classStr.indexOf("fa-angle-double-up") !=-1){
		$(obj).removeClass('fa-angle-double-up');
		$(obj).addClass('fa-angle-double-down');
		$(obj).parent().parent().parent().next().css('display','none');
	}else{
		$(obj).removeClass('fa-angle-double-down');
		$(obj).addClass('fa-angle-double-up');
		$(obj).parent().parent().parent().next().css('display','block');
	}
}

//保存提交ansible, 提交给后台的数据格式为：
/*  templates 和files 通过上传先提交了
	{
		"playbook_name":"lamp",
		"step1":{
			"role_name":"install_db",
			"tasks": "contents",
			"handlers": "contents",
			"vars": "contents",
			"hosts": "192.168.10.3:root,192.168.10.4:clouder"
		}
	}
*/
function saveAnsible(actionType){
	var playbook_data = {}
	var playbook_name = $("input[name='playbook_name']").val();
	if(playbook_name.trim().length==0){
		alert("请输入剧本名称!");
		return;
	}
	playbook_data["playbook_name"] = playbook_name;
	var allStep = $(".widget-box[id^='step']");
	for(var i=0;i<allStep.length;i++){
		var oneStepID = $(allStep[i]).attr('id');
		playbook_data[oneStepID] = {};
		var oneStepNum = oneStepID.charAt(oneStepID.length-1);
		var role_name = $("input[name='step"+oneStepNum+"']").val();
		if(role_name.trim().length==0){
			alert("请输入步骤名称!");
			return;
		}
		playbook_data[oneStepID]["role_name"] = role_name;
		var task_editor = ace.edit("task-editor"+oneStepNum);
		var task_content = task_editor.getSession().getValue();
		if(task_content.length==0){
			alert("请输入"+role_name+"步骤的tasks内容!");
			return;
		}
		playbook_data[oneStepID]["tasks"] = task_content;
		
		var handler_editor = ace.edit("handler-editor"+oneStepNum);
		var handler_content = handler_editor.getSession().getValue();
		playbook_data[oneStepID]["handlers"] = handler_content;
		var var_editor = ace.edit("var-editor"+oneStepNum);
		var var_content = var_editor.getSession().getValue();
		playbook_data[oneStepID]["vars"] = var_content;
		var checked_host_array = getHostAccount("host"+oneStepNum);
		if(checked_host_array.length==0){
			alert("请选择要执行"+role_name+"步骤的主机!");
			return;
		}
		playbook_data[oneStepID]["hosts"]=checked_host_array;
	}
	
	var playbook_id = $("input[name='playbook_id']").val();
	
	$.ajax({
		type: "POST",
		url:  "/ansible/add/save/",
		processData: true,
		data: {"playbook_data":JSON.stringify(playbook_data),"action_type":actionType,"playbook_id":playbook_id},
		success: function(data){
			if(data['status']==200){
				location.href='/ansible/list/';
			}else{
				$("#err-div").css('display','block');
				$("#err-msg").text(data['msg']);
			}
				
		}
		
	})
}

//获取已选择的主机和帐号,返回一个数组['192.168.10.3:root','192.168.10.4:clouder']
function getHostAccount(hostId){
	var checked_host_array = new Array();
	var checkedHostTrObj = $("#"+hostId+" table tr");
	for(var i=1;i<checkedHostTrObj.length;i++){
		var ip = $(checkedHostTrObj[i]).children().eq(3).text();
		var accountObj = $(checkedHostTrObj[i]).children().eq(2);
		var account = $(accountObj).children("select").find('option:selected').text();
		checked_host_array.push(ip+':'+account);
	}
	return checked_host_array;
}

//当“选择服务器”时, 获取当前步骤StepNum,以便从主机列表modal 选择主机添加时知道添加到哪个步骤中
function setModalRelID(obj){
	var stepID = $(obj).parent().parent().attr('id');
	StepNum = stepID.charAt(stepID.length-1);	
}

//服务器全选，取消全选
//备注：easysearch过滤的原理是使不匹配的元素不可见，所有在全选时需要先过滤掉不可见的元素
function allChecked(obj){
	if($(obj).is(':checked')){
		var visible_tr = $(".tr-select-modal:visible");
		for(var i=0;i<visible_tr.length;i++){
			$(visible_tr[i]).find("input[type='checkbox']").prop('checked','true');
		}
	}else{
		$(obj).find("input[type='checkbox']").removeAttr('checked','true');
		$(".tr-select-modal input[type='checkbox']").removeAttr("checked");
	}
	
}

// 添加已选择服务器
function addHost(){
	var checked = $(".tr-select-modal:visible input[type='checkbox']:checked");
	var hostTabObj = $("a[href='#host"+StepNum+"']");
	var currCheckedHostNum = $(hostTabObj).children().eq(1).text();
	$(hostTabObj).children().eq(1).text(checked.length+parseInt(currCheckedHostNum));
	for(var i=0;i<checked.length;i++){
		var checkTempObj = $($(checked[i]).parent().parent()).clone();
		$(checkTempObj).children().eq(0).remove();
		var del_txt="<td id='delButton' onclick='delChecked(this);'>删除</td>";
		$(checkTempObj).append(del_txt);
		$(checkTempObj).appendTo("#host"+StepNum+" table");
	}
}

// 删除已选择服务器
function delChecked(obj){
	var stepID = $(obj).parent().parent().parent().parent().parent().parent().attr('id');
	StepNum = stepID.charAt(stepID.length-1);
	$(obj).parent().remove();
	var hostTabObj = $("a[href='#host"+StepNum+"']");
	var currCheckedHostNum = $(hostTabObj).children().eq(1).text();
	$(hostTabObj).children().eq(1).text(parseInt(currCheckedHostNum)-1);
}

function delFile(obj){
	var stepID = $(obj).parent().parent().parent().parent().parent().parent().parent().attr('id');
	var num = stepID.charAt(stepID.length-1);
	var playbook_name = $("input[name='playbook_name']").val();
	var role_name = $("input[name='step"+num+"']").val();
	var file_type = stepID.slice(0,-1);
	var file_name = $(obj).parent().siblings().eq(0).text();
	$(obj).parent().parent().remove();
	$.ajax({
		type: 'POST',
		url: '/ansible/delete/file/',
		data: {'playbook_name':playbook_name,'role_name':role_name,
			   'file_type':file_type,'file_name':file_name}
	})
}