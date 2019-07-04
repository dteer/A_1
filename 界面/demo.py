import wx


class MainFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(500, 300))

        # 显示按钮功能
        self.buttonOK = wx.Button(self, -1, 'OK', (20, 20), (60, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.buttonOK)

        self.buttonCancel = wx.Button(self, -1, 'Cancel', (20, 80), (60, 30))
        self.Bind(wx.EVT_BUTTON, self.OnClick, self.buttonCancel)

    def onClick(self, event):
        if event.GetEventObject() == self.buttonOK:
            print("".format(event.GetEventObject().GetLabel()))
        elif event.GetEventObject() == self.buttonCancel:
            print("".format(event.GetEventObject().GetLabel()))
        else:
            print("")


class App(wx.App):
    def __init__(self):
        super(App, self).__init__(())

    def OnInit(self):
        self.version = '第二课'
        self.title = 'wxpython' + self.version
        frame = MainFrame(None,-1,self.title)
        frame.Show(True)

        return True

if __name__ == '__main__':
    app = App()
    app.MainLoop()