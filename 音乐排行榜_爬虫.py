import time
import requests
from lxml import etree
import pymysql

#加载mysql数据库
conn=pymysql.connect(host='localhost',
                    user='root',#用户名
                    passwd='root',#密码
                    port=3306,#端口号
                    charset='utf8')
cursor=conn.cursor()
print("连接数据库成功!")

#创建数据库
CreateShuJuKu='''create database if not exists music'''
cursor.execute(CreateShuJuKu)
cursor.execute("use music")

#创建数据表
#酷狗音乐
CreateShuJuBiao='''create table if not exists kugou_music(
        排名 int auto_increment primary key,
        歌曲名字 varchar(100),
        歌手 varchar(50),
        歌曲时长 varchar(30));
        '''
cursor.execute(CreateShuJuBiao)

#酷我音乐
CreateShuJuBiao='''create table if not exists kuwo_music(
        排名 int auto_increment primary key,
        歌曲名字 varchar(100),
        歌手 varchar(50),
        歌曲时长 varchar(30));
        '''
cursor.execute(CreateShuJuBiao)

#QQ音乐
CreateShuJuBiao='''create table if not exists qq_music(
        排名 int auto_increment primary key,
        歌曲名字 varchar(100),
        歌手 varchar(50),
        歌曲时长 varchar(30));
        '''
cursor.execute(CreateShuJuBiao)

#九酷音乐
CreateShuJuBiao='''create table if not exists jiuku_music(
        排名 int auto_increment primary key,
        歌曲名字 varchar(100),
        歌手 varchar(50),
        歌曲时长 varchar(30));
        '''
cursor.execute(CreateShuJuBiao)

#一听音乐
CreateShuJuBiao='''create table if not exists yiting_music(
        排名 int auto_increment primary key,
        歌曲名字 varchar(100),
        歌手 varchar(50),
        歌曲时长 varchar(30));
        '''
cursor.execute(CreateShuJuBiao)

#清空表中的数据
cursor.execute("truncate table kugou_music")
cursor.execute("truncate table kuwo_music")
cursor.execute("truncate table qq_music")
cursor.execute("truncate table jiuku_music")
cursor.execute("truncate table yiting_music")

#表头
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}

#酷狗音乐
def get_kugou(url_1):
    res=requests.get(url_1,headers=headers)
    sector=etree.HTML(res.text)
    infos=sector.xpath("//*[@id='rankWrap']/div[2]/ul/li")
    for info in infos:
        try:
            歌曲名字=info.xpath("a/text()")[0].split('-')[1]
        except:
            歌曲名字="这首歌格式错误(酷狗)"
        歌手=info.xpath("a/text()")[0].split("-")[0]
        歌曲时长=info.xpath("span[4]/span/text()")[0].strip().split("\xa0/\xa0")[0]
        cursor.execute("insert into kugou_music (歌曲名字,歌手,歌曲时长) values (%s,%s,%s)",(歌曲名字,歌手,歌曲时长))
    print("酷狗音乐榜_爬取完毕")
#酷我音乐
def get_kuwo(url_2):
     headers = { 
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
	'Cookie': 'kw_token=8HA6E6HE879',
	'csrf': '8HA6E6HE879'
        }
     resp = requests.get(url_2, headers=headers)
     resp_json = resp.json()
     musicList = resp_json['data']['musicList']
     music_list = []
     dit = {}
     for music in musicList:
        dit['歌名'] = music['name']
        dit['歌手'] = music['artist']
        dit['时间'] = music['songTimeMinutes']
        music_list.append(dit.copy())
        cursor.execute("insert into kuwo_music (歌曲名字,歌手,歌曲时长) values (%s,%s,%s)",(dit['歌名'],dit['歌手'],dit['时间']))
#qq音乐
def get_qq(url_3):
    res=requests.get(url_3,headers=headers)
    sector=etree.HTML(res.text)
    infos=sector.xpath("//*[@id='app']/div/div[2]/div[2]/div[3]/ul[2]/li")
    for info in infos:
        歌曲名字=info.xpath("div/div[3]/span/a[2]/text()")[0]
        歌手=info.xpath("div/div[4]/a/text()")[0]
        歌曲时长=info.xpath("div/div[5]/text()")[0]
        cursor.execute("insert into qq_music (歌曲名字,歌手,歌曲时长) values (%s,%s,%s)",(歌曲名字,歌手,歌曲时长))
    print("qq音乐榜_爬取完毕")
#九酷音乐
def get_jiuku(url_6):
    res=requests.get(url_6,headers=headers)
    sector=etree.HTML(res.text)
    for i in range(1,11):
        ttt="//*[@id='f{}']/ol/li".format(str(i))
        infos=sector.xpath(ttt)
        for info in infos:
            歌曲名字=info.xpath("a/text()")
            歌手="暂无"
            歌曲时长="暂无"
            cursor.execute("insert into jiuku_music (歌曲名字,歌手,歌曲时长) values (%s,%s,%s)",(歌曲名字,歌手,歌曲时长))
    print("九酷音乐榜_爬取完毕")
#一听音乐网
def get_yiting(url_7):
    res=requests.get(url_7,headers=headers)
    sector=etree.HTML(res.text)
    for i in range(0,73,24):
        ttt="//*[@id='list-{}']/li".format(str(i))
        infos=sector.xpath(ttt)
        for info in infos:
                歌曲名字=info.xpath("a/text()")[0].split("-")[0]
                歌手=info.xpath("a/text()")[0].split("-")[1]
                歌曲时长="暂无"
                cursor.execute("insert into yiting_music (歌曲名字,歌手,歌曲时长) values (%s,%s,%s)",(歌曲名字,歌手,歌曲时长))
    print("一听音乐榜_爬取完毕")

if __name__ == "__main__":
    print("本程序将爬取“酷狗top500(前22)”、“酷我飙升榜(前330)”、“qq飙升榜(前20)”、“九酷音乐TOP500(前300)”、“一听音乐网(最新歌曲)(前96)” ")
    time.sleep(5)
    #酷狗top500(前22)
    url_1="https://www.kugou.com/yy/rank/home/1-8888.html?from=homepage"
    get_kugou(url_1)
    time.sleep(1)
    
    #酷我飙升榜(前330) 
    for i in range(11):
        url_2="http://www.kuwo.cn/api/www/bang/bang/musicList?bangId=93&pn={}&rn=30&httpsStatus=1&reqId=2e371710-d7ef-11eb-8d31-9773923da8c1".format(i)
        get_kuwo(url_2)
    print("酷我音乐榜_爬取完毕")
    time.sleep(1)
   
    #qq飙升榜(前20)
    url_3="https://y.qq.com/n/ryqq/toplist/62"
    get_qq(url_3)
    time.sleep(1)
    
    #九酷音乐TOP500(前300)
    url_6="https://www.9ku.com/music/t_m_hits.htm"
    get_jiuku(url_6)
    time.sleep(1)

    #一听音乐网(最新歌曲)(前96)
    url_7="https://www.1ting.com/song_n.html"
    get_yiting(url_7)
    time.sleep(1)
        
    conn.commit()

print("\n已全部爬完,并保存到Mysql中的（music）中\n")