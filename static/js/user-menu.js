
$(document).ready(function(){
	menu_json = {'/':[0,0]}
	/*
	<ul class="submenu">
		<li class="">
			<a href="{% url 'applist' %}">
				<i class="menu-icon fa fa-caret-right"></i>
				应用列表
			</a>

			<b class="arrow"></b>
		</li>
	</ul>
	*/
	//思路：获取一级菜单数,即 ul下的li个数(ul->li)，再获取二级菜单，即li下的ul下的li个数(ul->li->ul->li),取ul->li->ul->li->a 标签的url作为key
	//格式为 {'applist':[1,0]} 表示applist在第二个一级目录，一级目录下第一个
	//开始获取一级菜单个数
	var first_menu_num = $(".nav-list").children("li");
	// 遍历一级菜单
	for (var i=0;i<first_menu_num.length;i++){
		// 获得指定一级目录下的二级目录数
		second_menu_num = $(first_menu_num[i]).children("ul").children("li");
		// 遍历二级目录，获取a url值
		for (var j=0;j<second_menu_num.length;j++){
			var href = $(second_menu_num[j]).find("a").attr("href");
			var key = href.split('/')[1];
			menu_json[key]=[];
			menu_json[key].push(i);
			menu_json[key].push(j);
		}
		
	}
	
	//获取 地址栏路径
	var currentURL = document.location.pathname;
	//把地址栏路径切割成list
	var currentURLList = currentURL.split('/');
	
	//获取一级菜单所有对象
	var lis = $(".nav-list").children("li");
	if(currentURLList[1]){
		// 先移所有菜单的active,open  class
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		
		//为一级菜单添加active,open class
		$(lis[menu_json[currentURLList[1]][0]]).addClass('active');
		$(lis[menu_json[currentURLList[1]][0]]).addClass('open');
		//为二级菜单添加active class
		$($(lis[menu_json[currentURLList[1]][0]]).children("ul").children("li")[menu_json[currentURLList[1]][1]]).addClass("active");
	
	// 首页情况
	}else{
		$(lis).removeClass('active');
		$(lis).removeClass('open');
		$(lis[0]).addClass('active');
	}
});
	