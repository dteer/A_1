import wx
import re
import os
import time
from run import Baidu as B,Meizitu as M


# 由于当前对布局管理器不是很熟悉，所系使用的是固定位置，导致窗口拉伸的效果不是很好
class MyApp(wx.App):
    def __init__(self):
        wx.App.__init__(self)
        self.Baidu = B()
        self.Meizi = M()

        self.entry_load = None
        self.entry_fileName = None


        frame = wx.Frame(parent=None, title='Login', size=(532, 420))
        # 设置窗口的左上角的图标
        # 其中参数type表示图片的类型，还有ico，jpgm等类型
        # icon_1 = wx.Icon(name='./1.png',type=wx.BITMAP_TYPE_PNG)
        # frame.SetIcon(icon_1)

        self.panel = wx.Panel(frame, -1)
        # 向panel中添加图片
        # image =wx.Image("./1.png", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        # wx.StaticBitmap(panel, -1, bitmap=image, pos=(0, 0))

        #添加分类标签
        label_baidu = wx.StaticText(self.panel, -1, "百度批量下载图片:",pos=(200, 20))
        label_meizi = wx.StaticText(self.panel, -1, "妹子网批量下载图片:", pos=(200, 160))
        label_baidu.SetBackgroundColour("#0a74f7")
        label_meizi.SetBackgroundColour("#0a74f7")

        # 添加静态标签
        label_picture = wx.StaticText(self.panel, -1, "图片名:", pos=(80, 55))
        label_year = wx.StaticText(self.panel, -1, "年份:", pos=(80, 200))
        label_meizi_path = wx.StaticText(self.panel, -1, "目录:", pos=(80, 250))

        # 添加文本输入框 百度
        self.entry_picture = wx.TextCtrl(self.panel, -1, size=(200, 30), pos=(130, 50))
        # 添加文本输入框   妹子
        self.entry_year = wx.TextCtrl(self.panel, -1, size=(200, 30), pos=(130, 200))
        #添加妹子网下载的目录
        self.entry_meizi_path = wx.TextCtrl(self.panel, -1, size=(200, 30), pos=(130, 250),)

        # 添加按钮
        self.but_picture = wx.Button(self.panel, -1, "查找", size=(120, 45), pos=(350, 45))
        self.but_year = wx.Button(self.panel, -1, "一键下载", size=(120, 50), pos=(350, 300))
        self.but_meizi_path = wx.Button(self.panel, -1, "...", size=(25, 30), pos=(335, 250))

        # 设置按钮的颜色
        self.but_picture.SetBackgroundColour("#0a74f7")
        self.but_year.SetBackgroundColour("#0a74f7")

        # 给按钮绑定事件
        self.Bind(wx.EVT_BUTTON, self.on_btn_search, self.but_picture)
        self.Bind(wx.EVT_BUTTON, self.on_but_meizi, self.but_year)
        self.Bind(wx.EVT_BUTTON, lambda event, mark=(self.panel, self.entry_meizi_path): self.get_path(event, mark), self.but_meizi_path)
        #
        frame.Center()
        frame.Show(True)

    # 定义一个消息弹出框的函数
    def show_message(self, word=''):
        dlg = wx.MessageDialog(None, word, u"详情", wx.YES_NO | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            # self.Close(True)
            pass
        dlg.Destroy()

    #定义一个下载百度图片提示框
    def load_baidu_title(self, url, word, load_count, file_Name_path):
        frame_title = wx.Frame(parent=None, title='正在下载图片.....', size=(300, 60),pos=(500,200))
        panel_title = wx.Panel(frame_title, -1)
        frame_title.Show()
        Recommends = self.Baidu.recommend(url)
        self.Baidu.save(url, word, load_count, file_Name_path)
        re_lis = []
        for recommend in Recommends:
            re_lis.append(recommend)
        self.show_message('下载完毕' + '\n' + ','.join(re_lis))
        frame_title.Hide()

    #定义一个下载妹子网图片提示框
    def load_meizi_title(self,year,path):
        frame_title = wx.Frame(parent=None, title='正在下载图片.....', size=(300, 60),pos=(500,200))
        panel_title = wx.Panel(frame_title, -1)
        frame_title.Show()
        #添加内容
        self.Meizi.run(year,path)
        frame_title.Hide()

    #定义一个提示框
    def show_title(self,word=''):
        frame_title = wx.Frame(parent=None, title='正在加载数据.....', size=(300, 60),pos=(500,200))
        panel_title = wx.Panel(frame_title, -1)
        frame_title.Show()
        url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
        num = self.Baidu.Find(url)
        frame_title.Hide()
        return num,url


    #对查找百度图片做判断
    def search_ack(self, event, mark):
        panel2 = mark[0]

        load_count = mark[1].GetValue()
        entry_path = mark[2].GetValue()
        file_Name = mark[3].GetValue()
        url = mark[4]
        word = mark[5]
        load_count = re.findall('^\d+', load_count)
        if load_count != []:
            load_count = int(load_count[0])
            if os.path.exists(entry_path) is False:
                self.show_message("目录路径有误，请重新输入")
            else:
                if file_Name == '':
                    self.show_message("请输入正确的文件名")
                else:
                    # 判断是否存在相同的文件名，是否覆盖
                    file_Name_path = os.path.join(entry_path,file_Name)
                    if os.path.exists(file_Name_path) is False:
                        os.mkdir(file_Name_path)
                    else:
                        print('下载中....')
                        self.load_baidu_title(url, word, load_count, file_Name_path)

        else:
            self.show_message("请输入正确的下载量")


    #获得路径
    def get_path(self, event, mark):
        panel2 = mark[0]
        entry_path = mark[1]
        dlg = wx.DirDialog(panel2, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()  # 文件夹路径
            entry_path.SetValue(path)
        dlg.Destroy()

    #对查找出来的图片做处理
    def show_dlg(self,word,num,url):
        if num > 0 :
            frame2 = wx.Frame(parent=None, title='Login', size=(532, 420))
            panel2 = wx.Panel(frame2, -1)
            show_count = wx.StaticText(panel2, -1, "共加载图片%s张图片" % num, pos=(200, 20))
            label_title = wx.StaticText(panel2, -1, "请输入需要下载数量和保存的文件名: ", pos=(50, 50))

            # 添加静态标签
            label_load = wx.StaticText(panel2, -1, "下载量:", pos=(80, 100))
            label_path = wx.StaticText(panel2, -1, "存储路径:", pos=(75, 170))
            label_fileName = wx.StaticText(panel2, -1, "存储文件名:", pos=(65, 220))

            # 添加文本输入框
            entry_load = wx.TextCtrl(panel2, -1, size=(200, 30), pos=(130, 100))
            entry_path = wx.TextCtrl(panel2, -1, size=(200, 30), pos=(130, 170), )
            entry_fileName = wx.TextCtrl(panel2, -1, size=(200, 30), pos=(130, 220))  # style=wx.TE_PASSWORD 密码框
            entry_fileName.SetValue(word)
            # 添加按钮
            but_path = wx.Button(panel2, -1, "...", size=(40, 30), pos=(330, 170))
            but_picture = wx.Button(panel2, -1, "下载", size=(120, 45), pos=(350, 250))

            # 给按钮绑定事件
            but_path.Bind(wx.EVT_BUTTON, lambda event, mark=(panel2, entry_path): self.get_path(event, mark), but_path)
            but_picture.Bind(wx.EVT_BUTTON,
                             lambda event,
                                    mark=(panel2, entry_load, entry_path, entry_fileName, url, word): self.search_ack(
                                 event, mark),
                             but_picture)

            frame2.Center()
            frame2.Show(True)
        else:
            self.show_message('此关键字查找为空，请更换关键字')



    #查找百度图片
    def on_btn_search(self, event):
        picture_name = self.entry_picture.GetValue()
        if picture_name.strip() is '':
            self.show_message('内容不能为空/纯空格')
        else:
            num,url = self.show_title('正在加载中。。。。')
            self.show_dlg(picture_name,num,url)


    def on_but_meizi(self, event):
        year = self.entry_year.GetValue()
        path = self.entry_meizi_path.GetValue()
        self.load_meizi_title(year,path)
        self.show_message(word="密码错误")


if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
