# firecloud

安装步骤: 
1 修改settings.py 中的mysql redis连接地址

2 创建firecloud 数据库

3 python manage.py makemigrations

4 python manage.py migrate

5 导入1级菜单列表webapp_level1menu.sql

6 导入2级菜单列表webapp_level2menu.sql

7 向homepage表插入数据 INSERT INTO homepage VALUES ('1', '概览面板', '/', 'home/dashboard.html');

8 在sysrole中创建admin角色

9 在sysuser中创建admin用户

10 运行应用即可使用
