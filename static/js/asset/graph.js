$(window).resize(function(){
	cpuLoadChart.resize();
	cpuUsageChart.resize();
	memUsageChart.resize();
	diskTpsChart.resize();
	diskSpeedChart.resize();
	diskUsageChart.resize();
	networkChart.resize();
	netstatChart.resize();
	processChart.resize();
	threadChart.resize();
	
});
$(document).ready(function(){
	var hei = (document.documentElement.clientHeight*28/100);
//	var diskI_hei_t = $("#diskId").css('height');
//	var diskU_hei_t = $("#diskUd").css('height');
//	var diskI_hei = hei-(diskI_hei_t.substring(0,diskI_hei_t.length-2)) +113;
//	var diskU_hei = hei-(diskU_hei_t.substring(0,diskU_hei_t.length-2)) +113;

	draw_percent();
	set_percent();
	select_time(60);
	
	var cpuLoadOption = {
			color: ["red","blue","green"],
		    title: {
		        text: 'cpu 负载 ',
		    },
		    legend:{
		    	data:['1分钟','5分钟','15分钟'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		        {
		            name:'1分钟',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'5分钟',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'15分钟',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
	
	
	var cpuUsageOption = {
			color: ["#DC143C","#CD853F","#FFDD55","#00CC00"],
		    title: {
		        text: 'cpu 利用率',
		    },
		    legend:{
		    	data:['idle','user','system','iowait'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'iowait',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'system',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'user',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'idle',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
	
	var memUsageOption = {
			color: ['#00CC33','#ddd','#3398DB','#ddd'],
		    title: {
		        text: '内存利用率',
		    },
		    legend:{
		    	right: '10%',
		    	data:['可用内存','已用内存','可用交换','已用交换'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: true,
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}%'}
		        
		    },
		    series: [
		    	{
		            name:'可用内存',
		            type:'bar',
		            stack: 'virt',
		            data: [],
		        },
		        {
		            name:'已用内存',
		            type:'bar',
		            stack: 'virt',
		            data: [],
		        },
		        {
		            name:'可用交换',
		            type:'bar',
		            stack: 'swap',
		            data: [],
		        },
		        {
		            name:'已用交换',
		            type:'bar',
		            stack: 'swap',
		            data: [],
		        }
		    ]
		};
	
	
	var diskTpsOption = {
			color: ['#3398DB'],
		    title: {
		        text: '磁盘 IOPS',
		    },
		    legend:{
		    	data:['IOPS'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'IOPS',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
	
	var diskSpeedOption = {
			color: ['#3398DB'],
		    title: {
		        text: '磁盘读写速度',
		    },
		    legend:{
		    	data:['speed'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}KB'}
		        
		    },
		    series: [
		    	{
		            name:'speed',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
		
	var diskUsageOption = {
			color: ['#3398DB','#BC8F8F '],
		    title: {
		        text: '磁盘利用率',
		    },
		    legend:{
		    	data:['available','used'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'available',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'used',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
			
	var networkOption = {
			color: ['#3398DB','#FFCC22'],
		    title: {
		        text: '网络收发速度',
		    },
		    legend:{
		    	data:['kb_recv','kb_sent'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}KB/秒'}
		        
		    },
		    series: [
		    	{
		            name:'kb_recv',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'kb_sent',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
		
	var netstatOption = {
			color: ['#3398DB',"#00CC33"],
		    title: {
		        text: '网络socket数',
		    },
		    legend:{
		    	data:['established','listen'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'established',
		            type:'line',
		            data: [],
		        },
		        {
		            name:'listen',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
	
	var processOption = {
			color: ['#3398DB'],
		    title: {
		        text: '进程数',
		    },
		    legend:{
		    	data:['processes'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'processes',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
	
	var threadOption = {
			color: ['#3398DB'],
		    title: {
		        text: '线程数',
		    },
		    legend:{
		    	data:['threads'],
		    
		    },
		    grid: {
		    	show: true,
		    	left: '4%',
		    	right: '5%',
		    	top: '20%',
		    	bottom: '8%',
		    	containLabel: true,
		    },
		    tooltip: {
		        trigger: 'axis',
		        axisPointer: {
		            type: 'cross'
		        }
		    },
		    xAxis:  {
		        type: 'category',
		        boundaryGap: false,
		        splitLine:{
		        	show:true
		        },
		        data: [],
		    	
		    },
		    yAxis: {
		        type: 'value',
		        axisLabel:{formatter:'{value}'}
		        
		    },
		    series: [
		    	{
		            name:'threads',
		            type:'line',
		            data: [],
		        }
		    ]
		}; 
		
		cpuLoadChart = drawGraph("load",hei,cpuLoadOption);
		cpuUsageChart = drawGraph("cpu",hei,cpuUsageOption);
		memUsageChart = drawGraph("mem",hei,memUsageOption);
		diskTpsChart = drawGraph("disk-tps",hei,diskTpsOption);
		diskSpeedChart = drawGraph("disk-speed",hei,diskSpeedOption);
		diskUsageChart = drawGraph("diskU",hei,diskUsageOption);
		networkChart = drawGraph("network",hei,networkOption);
		netstatChart = drawGraph("netstat",hei,netstatOption);
		processChart = drawGraph("process",hei,processOption);
		threadChart = drawGraph("thread",hei,threadOption);
})

function drawGraph(id,height,options) {
	$('#'+id).css({'width': '100%' , 'height': height});
    this.chart = echarts.init(document.getElementById(id))
    this.chart.setOption(options);
	return this.chart;
};


function set_cpu_load(dataobj){
	cpuLoadChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.cpuload.collect_time,
	    },
	    series: [
	        {
	            name:'1分钟',
	            type:'line',
	            data: dataobj.cpuload.load1,
	        },
	        {
	            name:'5分钟',
	            type:'line',
	            data: dataobj.cpuload.load5,
	        },
	        {
	            name:'15分钟',
	            type:'line',
	            data: dataobj.cpuload.load15,
	        }
	    ]
	});
}

function set_cpu_usage(dataobj){
	cpuUsageChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.cpuusage.collect_time,
	    },
	    series: [
	    	{
	            name:'iowait',
	            type:'line',
	            data: dataobj.cpuusage.iowait,
	        },
	        {
	            name:'system',
	            type:'line',
	            data: dataobj.cpuusage.system,
	        },
	        {
	            name:'user',
	            type:'line',
	            data: dataobj.cpuusage.user,
	        },
	        {
	            name:'idle',
	            type:'line',
	            data: dataobj.cpuusage.idle,
	        }
	    ]
	});
}

function set_mem_usage(dataobj){
	memUsageChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: true,
	        data: dataobj.memusage.collect_time,
	    },
	    series: [
	    	{
	            name:'可用内存',
	            type:'bar',
	            stack: 'virt',
	            data: dataobj.memusage.virt_available,
	        },
	        {
	            name:'已用内存',
	            type:'bar',
	            stack: 'virt',
	            data: dataobj.memusage.virt_used,
	        },
	        {
	            name:'可用交换',
	            type:'bar',
	            stack: 'swap',
	            data: dataobj.memusage.swap_available,
	        },
	        {
	            name:'已用交换',
	            type:'bar',
	            stack: 'swap',
	            data: dataobj.memusage.used,
	        }
	    ]
	});
}

function set_disk_tps(dataobj){
	diskTpsChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.disktps.collect_time,
	    },
	    series: [
	    	{
	            name:'IOPS',
	            type:'line',
	            data: dataobj.disktps.tps
	        }
	    ]
    });
}

function set_disk_speed(dataobj){
	diskSpeedChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.diskspeed.collect_time,
	    },
	    series: [
	    	{
	            name:'speed',
	            type:'line',
	            data: dataobj.diskspeed.blks
	        }
	    ]
	});
	
}

function set_disk_usage(dataobj){
	diskUsageChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.diskusage.collect_time,
	    },
	    series: [
	    	{
	            name:'available',
	            type:'line',
	            data: dataobj.diskusage.available,
	        },
	        {
	            name:'used',
	            type:'line',
	            data: dataobj.diskusage.used,
	        }
	    ]
	});
}

function set_network(dataobj){
	networkChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.network.collect_time,
	    },
	    series: [
	    	{
	            name:'kb_recv',
	            type:'line',
	            data: dataobj.network.kb_recv,
	        },
	        {
	            name:'kb_sent',
	            type:'line',
	            data: dataobj.network.kb_sent,
	        }
	    ]
	});
}

function set_netstat(dataobj){
	netstatChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.netstat.collect_time,
	    },
	    series: [
	    	{
	            name:'established',
	            type:'line',
	            data: dataobj.netstat.ESTABLISHED,
	        },
	        {
	            name:'listen',
	            type:'line',
	            data: dataobj.netstat.LISTEN,
	        }
	    ]
	});
}

function set_process(dataobj){
	processChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.process.collect_time,
	    },
	    series: [
	    	{
	            name:'processes',
	            type:'line',
	            data: dataobj.process.processes,
	        }
	    ]
	});
}

function set_thread(dataobj){
	threadChart.setOption({
		xAxis:  {
	        type: 'category',
	        boundaryGap: false,
	        data: dataobj.process.collect_time,
	    },
	    series: [
	    	{
	            name:'threads',
	            type:'line',
	            data: dataobj.process.threads,
	        }
	    ]
	});
}


function select_time(time_value){
	$("#"+time_value).siblings().removeClass("active");
	$("#"+time_value).addClass("active");
	var data = {};
	host = $("#private_ip").text();
	data["host"] = host;
	data["time_value"] = time_value;
	$.ajax({
		url: '/host/monitor/',
		type: 'POST',
//		data: {"data": JSON.stringify(data)},
		data: data,
		success: function(data){
//			dataobj = eval('('+data+')');
			set_cpu_load(data);
			set_cpu_usage(data);
			set_mem_usage(data);
			set_disk_tps(data);
			set_disk_speed(data);
			set_disk_usage(data);
			set_network(data);
			set_netstat(data);
			set_process(data);
			set_thread(data);
		}
	})
}

function draw_percent(){
	$('.easy-pie-chart.percentage').each(function(){
		$(this).easyPieChart({
			barColor: $(this).data('color'),
			trackColor: '#DDDDDD',
			scaleColor: false,
			lineCap: 'butt',
			lineWidth: 20,
			animate: ace.vars['old_ie'] ? false : 1000,
			size:($('.easy-pie-chart').parent().width())*65/100
		});
	});

};

function init_percent_chart(id){
	$("#"+id).easyPieChart({
		barColor: $(this).data('color'),
		trackColor: '#DDDDDD',
		scaleColor: false,
		lineCap: 'butt',
		lineWidth: 20,
		animate: ace.vars['old_ie'] ? false : 1000,
		size:($('.easy-pie-chart').parent().width())
	});
}

function set_percent(){
	host = $("#private_ip").text();
	$.ajax({
		url: '/host/status/',
		type: 'POST',
		data: {"host":host},
		success: function(data){
			var cpuUtil = data.cpu;
			$('#cpu-percent').data('easyPieChart').update((data.cpu).toFixed(0));
			$('#cpu-percent-span').text((data.cpu).toFixed(0));
			
			$('#mem-percent').data('easyPieChart').update((data.mem).toFixed(0));
			$('#mem-percent-span').text((data.mem).toFixed(0));
			$('#mem-percent').data('easyPieChart').options.barColor = "#FFAA33";
			
			$('#disk-percent').data('easyPieChart').update((data.disk).toFixed(0));
			$('#disk-percent-span').text((data.disk).toFixed(0));
			
			$('#uptime-span').text(data.uptime);
		}
	})
};

function agentInstall(){
	$("#manual-install").css("display","none");
	$("#auto-install-form").css("display","block");
	$("#auto-install-btn").css("display","none");
}
function startInstall(){
	var private_ip = $("#breadcrumbs li:last").text();
	console.log(private_ip);
}

function cancelInstall(){
	$("#manual-install").css("display","block");
	$("#auto-install-form").css("display","none");
	$("#auto-install-btn").css("display","block");
}



