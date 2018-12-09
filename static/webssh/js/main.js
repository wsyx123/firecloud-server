jQuery(function($){

socket = new WebSocket('ws://192.168.10.1:9000/hostLogin/');
term = new Terminal({
  cursorBlink: true,
  rows: 32,
});
term.open(document.getElementById('image-detail'));

term.on('data', function(data) {
  // console.log(data);
  socket.send(data);
});

socket.onopen = function(e) {
  
};

socket.onmessage = function(msg) {
  // console.log(msg);
  term.write(msg.data);
};

socket.onerror = function(e) {
  console.log(e);
};

socket.onclose = function(e) {
  console.log(e);
  term.destroy();
};


});

function reconnect(){
	var host = '20.26.25.153'
	$("#connect-notify").html('正在远程使用<span>'+host+'...</span>');
	$("#connect-button").html('<button onclick="close_connect();" class="btn btn-danger">关闭连接</button>');
	socket = new WebSocket('ws://192.168.10.1:9000/asset/host/20.26.25.153');
	term = new Terminal({
	  cursorBlink: true,
	  rows: 25,
	});
	term.open(document.getElementById('image-detail'));

	term.on('data', function(data) {
	  // console.log(data);
	  socket.send(data);
	});

	socket.onopen = function(e) {
	  
	};

	socket.onmessage = function(msg) {
	  // console.log(msg);
	  term.write(msg.data);
	};

	socket.onerror = function(e) {
	  console.log(e);
	};

	socket.onclose = function(e) {
	  console.log(e);
	  term.destroy();
	};

}
