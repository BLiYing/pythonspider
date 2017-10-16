python写的一个爬虫

标签（空格分隔）： python

---

项目需求：
朋友的工作中要从一个[美国化学物质发布网站][1]提取所有MS/MS属性为experimental的物质。而该网站恰恰不提供这个关键字的查询，所以只好轮询查找。不过可以同时运行多个该程序，按序分批查找（一个程序查找一段）。每晚上能找10万条左右（开太多，怕封ip，不过貌似老美这个网站不封ip）。如图：
![说明][2]


  [1]: https://metlin.scripps.edu/landing_page.php?pgcontent=mainPage
  [2]: http://pan.baidu.com/s/1sl4Ztnf