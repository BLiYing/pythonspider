python写的一个爬虫

标签： python3，BeautifulSoup，urllib，csv

---

项目需求：
朋友的工作中要从一个[美国化学物质发布网站][1]提取所有MS/MS属性为experimental的物质。而该网站恰恰不提供这个关键字的查询，所以只好轮询查找。不过可以同时运行多个该程序，按序分批查找（一个程序查找一段）。如果同时跑十个程序，每晚上（12小时）能找10万条左右（开太多，怕封ip，不过貌似老美这个网站不封ip）。如图：
![image](https://github.com/BLiYing/pythonspider/blob/master/image/huaxue.png)[2]

说明：
①该爬虫不涉及图片验证码，代码里直接登录，保存cookie即可。处理了http连接超时，报错等情况。用到了BeautifulSoup等html解析库；
②python环境为python3


  [1]: https://metlin.scripps.edu/landing_page.php?pgcontent=mainPage
  [2]: http://pan.baidu.com/s/1sl4Ztnf
