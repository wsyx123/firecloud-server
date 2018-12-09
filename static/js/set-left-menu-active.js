
$(document).ready(function(){
	var menu_json = {'/': 0,
	'host':[1,0],'hostAdd':[1,0],'hostEdit':[1,0],'hostImport':[1,0],'hostGroup':[1,1],'enterprise':[1,[2,{'list':0,'project':1,'employee':2}]],
	'optlog':[2,0],'command':[2,1],'file':[2,2],'cron':[2,3],'cronMonitor':[2,3],'template':[2,4],'templateCreate':[2,4],
	'cluster':[3,[0,{'mesos':0,'kubernetes':1}]],'resource':[3,[1,{'network':0,'storage':1}]],'repository':[3,[2,{'host':0,'image':1}]],
	'appList':[4,0],'appCreate':[4,0],'appDetail':[4,0],
	'appMonitor':[5,0],'hostMonitor':[5,1],'eventList':[5,2],'alertPolicy':[5,[3,{'list':0,'add':0,'group':1}]],
	'web':[7,0],'logic':[7,1],'storage':[7,2]
	}
	var currentURL = document.location.pathname;
	var currentURLList = currentURL.split('/');
	var lis = $(".nav-list").children("li");
	if(currentURLList[1] == 'appDetail' || currentURLList[1] == 'appMonitor' || currentURLList[1] == 'hostMonitor'){
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('active');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('open');
		$($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1]]).addClass("active");
	}else if(currentURLList[1] && currentURLList[2]){
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('active');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('open');
		$($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1][0]]).addClass("active");
		$($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1][0]]).addClass("open");
		var temp_lis = $($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1][0]]);
		var children_lis = $(temp_lis).children("ul").children("li");
		
		$(children_lis[menu_json[currentURLList[1]][1][1][currentURLList[2]]]).addClass("active");
		
	}else if(currentURLList[1]){
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('active');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('open');
		$($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1]]).addClass("active");
	}else{
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		$(lis[0]).addClass('active');
	}
});
	