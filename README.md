# pythonspider
学完python写爬虫，不亦乐乎

##网站化学物质排布方式

![image](https://github.com/BLiYing/pythonspider/blob/master/image/huaxue.png)

##找到符合要求的数据，插入到Excel表格中的结果：

![image](https://github.com/BLiYing/pythonspider/blob/master/image/result.png)

代码说明：
网站说明中说它一共有96万条及以上数据。朋友需要的数据只有1万6千条符合条件。需要全部检索出来并插入excel表格。

1.解析html库BeautifulSoup。

2.网络请求使用的是python3的urllib，包含cookies的配置。

3.改进的地方有：增加登录失效后自动重连，错误catch处理，代码复用。

该网站基本没有ip禁入的设置，美国人真是大方，花了几亿美金做的[医药类化学物质分类网站](https://metlin.scripps.edu/landing_page.php?pgcontent=advanced_search)。
