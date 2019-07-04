import re
import requests
from urllib import error
from lxml import etree
from bs4 import BeautifulSoup
import os



class Baidu():
    def __init__(self):
        self.num = 0
        self.numPicture = 0
        self.List = []

    def Find(self,url):
        print('正在检测图片总数，请稍等.....')
        page,count = 0,0
        while page < 1000:
            Url = url + str(page)
            try:
                Result = requests.get(Url, timeout=7)
            except BaseException:
                page = page + 60
                continue
            else:
                result = Result.text
                pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
                count += len(pic_url)
                if len(pic_url) == 0:
                    break
                else:
                    self.List.append(pic_url)
                    page = page + 60
        return count


    def recommend(self,url):
        Re = []
        try:
            html = requests.get(url)
        except error.HTTPError as e:
            return
        else:
            html.encoding = 'utf-8'
            bsObj = BeautifulSoup(html.text, 'html.parser')
            div = bsObj.find('div', id='topRS')
            if div is not None:
                listA = div.findAll('a')
                for i in listA:
                    if i is not None:
                        Re.append(i.get_text())
            return Re


    def dowmloadPicture(self,html, keyword,file):
        pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url

        print('找到关键词:' + keyword + '的图片，即将开始下载图片...')

        for each in pic_url:
            print('正在下载第' + str(self.num + 1) + '张图片，图片地址:' + str(each))
            try:
                if each is not None:
                    pic = requests.get(each, timeout=7)
                else:
                    continue
            except BaseException:
                print('错误，当前图片无法下载')
                continue
            else:
                string = file + r'\\' + keyword + '_' + str(self.num) + '.jpg'
                with open(string,'wb') as fp:
                    fp.write(pic.content)
                self.num += 1
            if self.num >= self.numPicture:
                print('下载完毕')
                return

    def save(self,url,word,numPicture,filename):
        t,tmp = 0,url

        self.numPicture = numPicture
        file = filename
        y = os.path.exists(file)
        if y == 1:
            pass
        else:
            os.mkdir(file)

        while t < self.numPicture:
            try:
                url = tmp + str(t)
                result = requests.get(url, timeout=10)
                print(url)
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 60
            else:
                self.dowmloadPicture(result.text, word, file)
                t = t + 60

    def close(self):
        self.num = 0
        self.numPicture = 0
        self.List.clear()


    def run(self):
        word = input("请输入搜索关键词(可以是人名，地名等): ")
        # add = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%E5%BC%A0%E5%A4%A9%E7%88%B1&pn=120'
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='

        tot = self.Find(url)
        Recommend = self.recommend(url)  # 记录相关推荐
        print('经过检测%s类图片共有%d张' % (word, tot))

        self.save(url,word)

        print('猜你喜欢')
        for re in Recommend:
            print(re, end='  ')



# from time import sleep

class Meizitu(object):
    """爬取妹子图中的图片"""

    def __init__(self):
        self.url = "http://www.mzitu.com/all/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }

    # 获取页面
    def get_page(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.content.decode()

    # 提取列表页中的urls
    def get_detail_urls_list(self, page_content, year):
        html_content = etree.HTML(page_content)
        year_list = html_content.xpath("//div[@class='year']/text()")
        index = 2019 - int(year)
        # 提取某一年的相关主题的urls
        xpath_var = "//div[@class='year'][{}]/following-sibling::*[1]//p[@class='url']/a/@href".format(index)
        if index <= len(year_list):
            urls_list = html_content.xpath(xpath_var)
            # print(urls_list)
        else:
            urls_list = None
        return urls_list

    # 构造保存路径并创建目录
    def save_path(self, detail_html_content, first_img_url, img_name,path):
        # 构造保存路径
        path_prefix1 = detail_html_content.xpath("//div[@class='currentpath']/a/text()")[1]
        # print(path_prefix1)
        path_prefix2 = first_img_url[20:29]
        # print(path_prefix2)
        save_path = path + "/妹子图/" + path_prefix1 + path_prefix2 + img_name + "/"

        # 如果目录不存在，则创建目录
        if not os.path.exists(save_path):
            os.makedirs(save_path)

        return save_path

    # 请求和保存图片
    def save_img(self, img_url, img_headers, img_save_path):
        # 请求图片
        img_content = requests.get(img_url, headers=img_headers).content
        # 保存图片
        with open(img_save_path, "wb") as f:
            f.write(img_content)

    # 构造图片请求地址
    def img_url(self, first_img_url, img_index):
        if img_index < 10:
            img_url = first_img_url[:32] + "0" + str(img_index) + ".jpg"
        else:
            img_url = first_img_url[:32] + str(img_index) + ".jpg"
        # print(img_url)
        return img_url

    # 构造图片的请求头
    def img_headers(self, url, img_index):
        if img_index == 1:
            refer_url = url
        else:
            refer_url = url + "/" + str(img_index)
        # print(refer_url)

        img_headers = {
            # "Accept":"image/webp,image/apng,image/*,*/*;q=0.8",
            # "Accept-Encoding":"gzip, deflate",
            # "Accept-Language":"zh-CN,zh;q=0.9",
            # "Connection":"keep-alive",
            "Host": "i.meizitu.net",
            "Referer": refer_url,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }
        # print(img_headers,end="\n\n")
        return img_headers

    # 构造每个主题的图片请求地址 并保存
    def get_img_urls(self, url, detail_html_content, first_img_url, img_name, save_path):
        # 每个主题中的图片总数
        img_total_num = int(detail_html_content.xpath("//div[@class='pagenavi']/a/span/text()")[4])

        # 构造图片地址 http://i.meizitu.net/2018/02/18c01.jpg
        for img_index in range(1, img_total_num + 1):
            img_url = self.img_url(first_img_url, img_index)
            img_headers = self.img_headers(url, img_index)
            # 构造图片具体保存路径
            img_save_path = save_path + img_name + str(img_index) + ".jpg"
            # sleep(10)
            # 请求和保存图片
            self.save_img(img_url, img_headers, img_save_path)

    # 获取图片
    def get_image(self, detail_urls_list,path):
        for url in detail_urls_list:
            detail_page = self.get_page(url, headers=self.headers)
            detail_html_content = etree.HTML(detail_page)
            # 第一页图片地址
            first_img_url = detail_html_content.xpath("//div[@class='main-image']/p/a/img/@src")[0]
            # print(first_img_url)
            # 获取图片保存的名字
            img_name = detail_html_content.xpath("//h2[@class='main-title']/text()")[0]
            # print(img_name)

            # 构建保存路径并创建目录
            save_path = self.save_path(detail_html_content, first_img_url, img_name,path)

            # 构建图片请求地址并下载
            self.get_img_urls(url, detail_html_content, first_img_url, img_name, save_path)

    # 启动爬虫
    def run(self,year,path):
        # 获取妹子图中的列表页内容
        page_content = self.get_page(self.url, self.headers)
        # 获取详情页的地址列表
        detail_urls_list = self.get_detail_urls_list(page_content, year)
        # 获取图片
        self.get_image(detail_urls_list,path)



if __name__ == '__main__':  # 主函数入口
    pass
    #百度搜索图片
    # obj = Baidu()
    # obj.run()
    #
    # year = int(input("请输入您要爬取的年份："))
    # meizitu = Meizitu(year)
    # meizitu.run()




