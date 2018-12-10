function addStep(obj){
	div_id = div_id + 1;
	var id = div_id;
	var ul_str='<ul class="nav nav-tabs">\
					<li class="active">\
						<a data-toggle="tab" href="#task'+id+'">tasks</a>\
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
						<a data-toggle="tab" href="#host'+id+'">hosts(已选服务器)<span class="badge badge-danger">0</span></a>\
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
						备注:<span class="smaller green">这里所编写的任务会保存在此步骤（角色）下的<strong class="red"> handlers </strong>目录下的main.yml文件中</span>\
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
									<span class="white">步骤名称 </span><input type="text" style="line-height:15px;" />\
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
								<div class="widget-toolbar">\
									<label class="white">\
										<i class="fa fa-plus" aria-hidden="true"></i>\
										<b>选择服务器</b>\
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
	setAceEditMode('task-editor'+id,'yaml','--');
	setAceEditMode('handler-editor'+id,'yaml','--');
	setAceEditMode('var-editor'+id,'yaml','--');
	InitFileUpload('templatepickfile'+id,'templatecontainer'+id,'templatefilelist'+id,'templateuploadfile'+id);
	InitFileUpload('filepickfile'+id,'filecontainer'+id,'filefilelist'+id,'fileuploadfile'+id);
	
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

function delStep(obj){
	$(obj).parent().parent().remove();
}

function InitFileUpload(pickfileID,containerID,filelistID,uploadfileID){
	var uploader = new plupload.Uploader({
	runtimes : 'html5,flash,silverlight,html4',
	browse_button : pickfileID, // you can pass an id...
	container: document.getElementById(containerID), // ... or DOM Element itself
	url : 'upload.php',
	flash_swf_url : '/static/plupload-2.3.6/js/Moxie.swf',
	silverlight_xap_url : '/static/plupload-2.3.6/js/Moxie.xap',
	
	filters : {
		max_file_size : '10mb',
		mime_types: [
			{title : "Image files", extensions : "jpg,gif,png"},
			{title : "Zip files", extensions : "zip"}
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
				var txt = '<tr><td>' + file.name + '</td><td>0%</td><td>' + plupload.formatSize(file.size) + '</td><td><button class="btn btn-minier btn-danger">删除</button></td></tr>';
				document.getElementById(filelistID).innerHTML += txt;
			});
		},

		UploadProgress: function(up, file) {
			document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
		},

		Error: function(up, err) {
			document.getElementById('console').appendChild(document.createTextNode("\nError #" + err.code + ": " + err.message));
		}
	}
});

uploader.init();
	
}