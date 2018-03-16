# -*- coding: utf-8 -*-
"""Created by Xiyang Luo in 1 Feb 2018
    the program is uesed to open and watch the card Digital Monster
    It is a remember
"""
"""打开浏览器""" 
import webbrowser
import wx
import re
import os
import pymysql.cursors
from PIL import Image

from show_card_name import Show_Card_Name
class MyFrame( wx.Frame ):
    def __init__( self):
        wx.Frame.__init__(self,None,-1,"My  Remember----Digital Monster",pos=(0,0),size=(1600,800),style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
        self.splitterwindow()
        self.create_statusbar()
        self.create_toolbar()
        self.create_main_menu()
        self.create_search_text()
        self.create_main_list()
        self.create_button()
        self.create_combobox()
        self.event_button()
        self.event_combobox()
        self.event_menu()
         
        
    def splitterwindow(self):
        self.sp=wx.SplitterWindow(self,style=wx.SP_LIVE_UPDATE)#分割出一个窗口
        self.panel1=wx.Panel(self.sp,-1,style=wx.SUNKEN_BORDER)#凹陷
        self.panel2=wx.Panel(self.sp,-1,style=wx.SUNKEN_BORDER)
        """设置颜色：蓝绿色：AQUAMARINE"""
        #self.panel1.SetBackgroundColour('MEDIUM TURQUOISE')
        #self.panel2.SetBackgroundColour('AQUAMARINE')
        """ self.sp.SplitHorizontally(self.p1, self.p2,0)水平分割"""
        self.sp.SplitVertically(self.panel1,self.panel2,150)
        """设置窗口最小值"""
        self.sp.SetMinimumPaneSize(150)
        
        self.sp1=wx.SplitterWindow(self.panel2,pos=(10,10),size=(1350,70),style=wx.SP_LIVE_UPDATE)
        self.panel3=wx.Panel(self.sp1,-1,style=wx.SUNKEN_BORDER)
        self.panel4=wx.Panel(self.sp1,-1,style=wx.SUNKEN_BORDER)
        self.panel3.SetBackgroundColour('sky blue')
        self.panel4.SetBackgroundColour('white')
        self.sp1.SplitHorizontally(self.panel4,self.panel3,1000)
        self.sp1.SetMinimumPaneSize(1000)
        
    def create_statusbar(self):
        self.statusBar1 = self.CreateStatusBar()
        self.statusBar1.SetFieldsCount(3)
        self.statusBar1.SetStatusWidths([-1, -2, -1])
        
    def create_main_menu(self):
        self.menubar=wx.MenuBar()
        self.menu1=wx.Menu()
        self.menu2=wx.Menu()
        self.menu3=wx.Menu()
        self.color=wx.Menu()
        
        self.color_red=self.color.Append(-1,'Red')
        self.color_blue=self.color.Append(-1,'Blue')
        self.color_yellow=self.color.Append(-1,'Yellow')
        self.color_green=self.color.Append(-1,'Green')
        self.color_purple=self.color.Append(-1,'Purple')
        self.color_orange=self.color.Append(-1,'Orange')
        self.color_pink=self.color.Append(-1,'Pink')
        """STEP3在菜单下面，建立选项栏，使用Append（-1，“name”）"""
        #self.m1open=self.menu1.Append(-1,"Open")
        self.m1network=self.menu1.Append(-1,"NetWork")
        self.m1SetColor=self.menu1.Append(-1,u'SetColor',self.color)
        self.m1quit=self.menu1.Append(-1,'Quit')
        self.m2about=self.menu2.Append(-1,"About")
        self.m3namelist=self.menu3.Append(-1,"Show Name - Digital Monster Card")
        self.m3download=self.menu3.Append(-1,"Down Load")
        #self.m3time5=self.menu3.Append(-1,"Change 5 Seconds")
        
        """STEP4将建好的菜单添加到菜单栏下面去，使用Append(菜单，“name”)"""
        self.menubar.Append(self.menu1,"FILE")
        self.menubar.Append(self.menu2,"HELP")
        self.menubar.Append(self.menu3,"Other")
        """STEP5将菜单栏设置到主窗口中，使用SetMenuBar（）"""
        self.SetMenuBar(self.menubar)
        
    def create_toolbar(self):
        self.m_toolBar1 = self.CreateToolBar() 
        self.m_toolBar1.Realize() 
        
    def create_main_list(self):
        self.main_list1=wx.ListBox(self.panel2,-1,pos=(10,90),size=(665,650),style=wx.TE_MULTILINE|wx.HSCROLL)
        self.main_list2=wx.ListBox(self.panel2,-1,pos=(690,90),size=(665,650),style=wx.TE_MULTILINE|wx.HSCROLL)
        
    def create_search_text(self):
        self.search_text=wx.TextCtrl(self.panel4,-1,pos=(5,5),size=(1280,30),style=wx.TE_PROCESS_ENTER|wx.TE_CENTER)#style=wx.TE_MULTILINE|wx.HSCROLL
        self.search_text.SetBackgroundColour('TURQUOISE')
        self.search_text.SetForegroundColour('Black')
        
        
        self.delete_text=wx.TextCtrl(self.panel1,-1,'delete please',pos=(10,265),size=(120,25),style=wx.TE_PROCESS_ENTER|wx.TE_NOHIDESEL|wx.TE_CENTER)
        self.update_text=wx.TextCtrl(self.panel1,-1,'update please',pos=(10,170),size=(120,25),style=wx.TE_CENTER)        
                          
    def create_button(self):
        self.button_insert=wx.Button(self.panel1,-1,'Insert',pos=(10,50),size=(120,50))
        self.button_update=wx.Button(self.panel1,-1,'Update',pos=(10,110),size=(120,50))
        self.button_delect=wx.Button(self.panel1,-1,'Delect',pos=(10,205),size=(120,50))
        self.button_search=wx.Button(self.panel4,-1,'Search',pos=(1295,5),size=(50,30))
        
    def create_combobox(self):
        #selection=['AErFaShou002','GaoLiShou','JuLongShou230','DanDanShou','CaiJueShou','GuangMingShou']
        #selection=['SELECTION']
        self.combobox_select=wx.ComboBox(self.panel1,-1,'Select',pos=(10,10),size=(120,30),style=wx.CB_SORT)
        self.combobox_select.SetBackgroundColour('LIGHT GREY')
        self.main_list1.Clear()
        """查询数据库，得到索引列表，加入到combobox中"""
        cursor.execute("SELECT DISTINCT name FROM UImage order by  id desc")
        name_item=cursor.fetchall()
        item=[]
        for ik in range(len(list(name_item))):
            a1=list(list(name_item)[ik])
            item.append(str(a1[0]))
            print('查询列表\n',str(item))
        self.combobox_select.Append(item)
        #self.combobox_select.Append(selection)
        
        self.combobox_select.SetSelection(0)
    
    
    def event_menu(self):
        """菜单file"""
        self.menu2.Bind(wx.EVT_MENU,self.OnMenuAbout,self.m2about)
        self.menu1.Bind(wx.EVT_MENU,self.OnMenuQuit,self.m1quit)
        self.menu1.Bind(wx.EVT_MENU,self.OnMenuNetWork,self.m1network)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorRed,self.color_red)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorBlue,self.color_blue)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorYellow,self.color_yellow)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorGreen,self.color_green)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorPurple,self.color_purple)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorOrange,self.color_orange)
        self.Bind(wx.EVT_MENU,self.OnMenuSetColorPink,self.color_pink)
        """菜单other"""
        self.menu3.Bind(wx.EVT_MENU,self.OnMenuShowCardName,self.m3namelist)
        self.menu3.Bind(wx.EVT_MENU,self.OnMenuDownLoad,self.m3download)
        #self.menu3.Bind(wx.EVT_MENU,self.OnMenuTime5,self.m3time5)
        
    def event_button(self):
        self.button_insert.Bind(wx.EVT_BUTTON,self.OnButtonInsert)
        self.button_delect.Bind(wx.EVT_BUTTON,self.OnButtonDelect)
        self.button_search.Bind(wx.EVT_BUTTON,self.OnButtonSearch)
        self.button_update.Bind(wx.EVT_BUTTON,self.OnButtonUpdate)
        
    def event_combobox(self):
        self.combobox_select.Bind(wx.EVT_COMBOBOX,self.OnComboboxSelect)
       
    def event_text(self):
        self.search_text.Bind(wx.EVT_TEXT,self.OnSearchText)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnTextEnterSearch,self.search_text)
        self.delete_text.Bind(wx.EVT_TEXT,self.OnDeleteText)
        self.update_text.Bind(wx.EVT_TEXT,self.OnUpdateText)
        
    def event_list(self):
        self.main_list1.Bind(wx.EVT_LISTBOX,self.OnMainList1)
        self.main_list2.Bind(wx.EVT_LISTBOX,self.OnMainList2)
    
    def OnMenuAbout(self,event):
        """子窗口界面创建wx.Dialog，在self.panel下面"""
        self.dialog_main_help=wx.Dialog(None,-1,title="Help",pos=(100,100),size=(800,500))
        listDatas = ['    这个软件是由重庆邮电大学学生罗夕洋制作\n','\n    在连接数据库（mysql）后，从服务器上得到数码宝贝卡片（图片）\n',
        '\n    将其正反面显示在画框中，是单纯的纪念形式\n','\n    点击SELECTION或者输入数码宝贝的名字（示例：BaoLongShou050）点击search查询\n',
        '\n    如果有该图片，便会显示\n','\n    其中输入名字时每个汉字拼音的首字母大写，并且加上Shou（兽）后面的编号是卡片上背后的编号\n',
        '\n    点击insert按钮可以将自己PS的数码宝贝卡片进行上传到数据库（图片路径）\n','\n    当然，如果不知道卡片名字或者编号，可以使用SELECTION，点击它之后，再点击便会出现数据库中所有卡片名称\n',
        '\n    Our Rememebr  ***   Digital Monster\n']
        self.help_listBox = wx.ListBox(self.dialog_main_help, -1, pos=(20, 20), size=(750, 430), style=wx.LB_SINGLE)
        """设置背景颜色和字体颜色"""
        self.help_listBox.SetBackgroundColour('white'), self.help_listBox.SetForegroundColour('SLATE BLUE') 
        self.dialog_main_help.SetTransparent(200)#设置透明
        """
        self.imagelist=wx.Image("helplistlogo.jpg",wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        self.bmplist=wx.StaticBitmap(self.dialog_main_help,bitmap=self.imagelist)
        """
        self.help_listBox.Append(listDatas)
    
        """显示子窗口"""
        self.dialog_main_help.ShowModal()
    def Ondownloadcurrently(self,event):
        print('test download currently')
        """子窗口DOWNLOAD对应的函数"""
        value_currently=self.combobox_select.GetValue()
        print('当前值：',str(value_currently))
        cursor.execute("select picturepath from UImage where name = '%s'"%value_currently)
        pathcurrently,d=[],[]
        pathcurrently.append(list(cursor.fetchall()))
        print(pathcurrently)
        for km in range(len(pathcurrently)):
            tem_path=((pathcurrently[km])[0])[0]
            d.append(tem_path)
            tem_path2=((pathcurrently[km])[1])[0]
            d.append(tem_path2)
        print(d)
        path=d
        for i in range(len(path)):
            download_image=Image.open(str(path[i]))
            with wx.FileDialog(self,"save file",wildcard="Text files (*.jpg)|*.jpg|(*.png)|*.png",style=wx.FD_SAVE) as fileDialog:
                if fileDialog.ShowModal()==wx.ID_OK:
                    pathname=fileDialog.GetPath()
                    print(pathname)
            download_image.save(pathname)
        self.statusBar1.SetStatusText('                                                             The Files Have Saved!!!',1)
        print('Save')
        
    def Ondownloadall(self,event):
        print('all')
        cursor.execute("select count(*) from UImage group by id")
        d=cursor.fetchall()
        print(d)
        os.makedirs('D:\\Digital_Monster\\Image')
        for i in range(len(d)):
            print(i)
            cursor.execute("select picturepath from UImage where id='%d'"%i)
            aaa=cursor.fetchall()
            aaa=(aaa[0])[0]
            print(aaa)
            im=Image.open(aaa)
            pa='D:\\Digital_Monster\\Image\\%d.jpg'%i
            im.save(pa)
        self.statusBar1.SetStatusText('                                                             All Files Have Saved!!!',1)
        print('all saved ')
    
    """
    def OnMenuTime5(self,event):
        cursor.execute("select count(*) from UImage group by id")
        totalnum=cursor.fetchall()
        print(totalnum)
        o=[]
        for m in range(len(totalnum)):
            cursor.execute("select picturepath from UImage where id=%d"%m)
            totalpath3=cursor.fetchall()
            o.append((totalpath3[0])[0])
        print(o)
        hh=['H:\ps_mysql_project\ju_long_shou\JuLongShou230.jpg', 
        'H:\ps_mysql_project\ju_long_shou\JuLongShou_BR230.jpg', 
        'H:\ps_mysql_project\dan_dan_shou\DanDanShou232.jpg', 
        'H:\ps_mysql_project\dan_dan_shou\DanDanShou_BR232.jpg']
        key = event.GetKeyCode()
        print(key)
        for n in range(0,len(hh),2):
            print(n)
            print(hh[n])
            print('go2')
            self.image22=wx.Image(str(hh[n]),wx.BITMAP_TYPE_JPEG)
            self.temp22=self.image22.ConvertToBitmap()
            self.bmp22=wx.StaticBitmap(self.main_list1,bitmap=self.temp22)
            self.bmp22.Center()   
            print('A2')
            
            print('go')
            print(hh[n+1])
            self.image21=wx.Image(str(hh[n+1]),wx.BITMAP_TYPE_JPEG)
            self.temp21=self.image21.ConvertToBitmap()
            self.bmp21=wx.StaticBitmap(self.main_list2,bitmap=self.temp21)
            self.bmp21.Center()
            
            os.system('systemctl stop nginx')
             
            time.sleep(3)
            os.system('systemctl start nginx')
            
            """
            
 
    def OnMenuDownLoad(self,event):
        self.dialog_download=wx.Dialog(None,-1,title="Down  Load",pos=(150,150),size=(500,350))
        self.dialog_download.SetTransparent(200)#透明度
        self.text_download=wx.ListCtrl(self.dialog_download,-1,pos=(10,10),size=(460,140),style=wx.LC_REPORT)
        self.text_download.InsertColumn(0,"Name",200)
        self.text_download.InsertColumn(1,"Number",400)
        #self.text_download.InsertColumn(2,"comment",100)
        self.button_download_currently=wx.Button(self.dialog_download,-1,"Down Load Currently",pos=(10,150),size=(140,50))
        self.button_download_all=wx.Button(self.dialog_download,-1,"Down Load All",pos=(10,210),size=(140,50))
        
        self.button_download_currently.Bind(wx.EVT_BUTTON,self.Ondownloadcurrently)
        self.button_download_all.Bind(wx.EVT_BUTTON,self.Ondownloadall)
        
        get_text_from_combobox=self.combobox_select.GetItems()#得到下拉列表（combobox）中所有的选项值
        print(get_text_from_combobox)
        num_digital_monster=len(get_text_from_combobox)
        """转化为中文显示"""
        en=Show_Card_Name(get_text_from_combobox,num_digital_monster)
        temcardname=en.Turn_English_To_Chinese()
        temlist=list(temcardname)
        cardcount=int(temlist[1])
        cardname=temlist[0]
        temp_no_file='Some Name No Such File !count： '
        no_file_num=temp_no_file+str(cardcount)
        sps=[no_file_num,'All File Have Shown! COUNT: 2/Name']
        if cardcount==0:
            for iq in range(len(cardname)):
                index=self.text_download.InsertStringItem(11,cardname[iq])
                self.text_download.SetStringItem(index,1,sps[1])
        else:
            for iq in range(len(cardname)):
                index=self.text_download.InsertStringItem(11,cardname[iq])
                self.text_download.SetStringItem(index,1,sps[0])
        
        
        self.dialog_download.ShowModal()
        
    def OnMenuShowCardName(self,event):
        print("test\n  show name of digital monster card")
        self.dialog_show_card_name=wx.Dialog(None,-1,title="Show Name of Ditigal Monster Card",pos=(150,150),size=(1000,650))
        self.dialog_show_card_name.SetTransparent(200)#透明度
        """列表显示"""
        self.listtext_showname=wx.ListCtrl(self.dialog_show_card_name,-1,pos=(100,10),size=(800,600),style=wx.LC_REPORT)
        self.listtext_showname.InsertColumn(0,"Name",width=300)
        self.listtext_showname.InsertColumn(1,"Path",width=400)
        self.listtext_showname.InsertColumn(2,"Station",width=250)
        get_text_from_combobox=self.combobox_select.GetItems()#得到下拉列表（combobox）中所有的选项值
        num_digital_monster=len(get_text_from_combobox)
        """转化为中文显示"""
        en=Show_Card_Name(get_text_from_combobox,num_digital_monster)
        temcardname=en.Turn_English_To_Chinese()
        temlist=list(temcardname)
        cardcount=int(temlist[1])
        print('没有的数量',str(cardcount))
        cardname=temlist[0]
        temp_no_file='Some Name No Such File !count： '
        no_file_num=temp_no_file+str(cardcount)
        sps=[no_file_num,'All File Have Shown!']
        """显示路径"""
        cardpath=[]
        for ij in range(len(cardname)):
            #print('test show path\n',str(get_text_from_combobox[ij]))
            temp=get_text_from_combobox[ij]
            cursor.execute("select picturepath from UImage where name = '%s'"%temp)
           # print(temp)
            cardpath.append(list(cursor.fetchall()))
        d=[]
        for km in range(len(cardpath)):
            tem_cardpath=((cardpath[km])[0])[0]
            d.append(tem_cardpath)
        print(d)
        cardpath=d
        
        if cardcount==0:
            for iq in range(len(cardname)):
                index=self.listtext_showname.InsertStringItem(11,cardname[iq])
                self.listtext_showname.SetStringItem(index,1,cardpath[iq])
            self.listtext_showname.SetStringItem(index,2,sps[1])
        else:
            for iq in range(len(cardname)):
                index=self.listtext_showname.InsertStringItem(11,cardname[iq])
                self.listtext_showname.SetStringItem(index,1,cardpath[iq])
            self.listtext_showname.SetStringItem(index,2,sps[0])
            """使用索引"""
            #index=self.listtext_showname.InsertStringItem(11,get_text_from_combobox[iq])
            #self.listtext_showname.SetStringItem(index,1,get_text_from_combobox[1])
            #self.listtext_showname.SetStringItem(index,2,get_tex_from_combobox[2])
        
        self.dialog_show_card_name.ShowModal()
    
    def OnComboboxSelect(self,event):
        self.main_list1.Clear()
        name=self.combobox_select.GetValue()
        sql = "SELECT picturepath FROM UImage WHERE name = '%s' "
        data = (name,)
        cursor.execute(sql % data)
        p=list(cursor.fetchall())
        print(p[1])
        if len(p)==2:
            name1=list(p[0])
            name1=name1[0]
            print(name1)
            self.image1=wx.Image(name1,wx.BITMAP_TYPE_JPEG)
            self.temp1=self.image1.ConvertToBitmap()
            self.bmp1=wx.StaticBitmap(self.main_list1,bitmap=self.temp1)
            self.bmp1.Center()
            name2=list(p[1])
            name2=name2[0]
            print('name2:\n',str(name2))
            self.image2=wx.Image(name2,wx.BITMAP_TYPE_JPEG)
            self.temp2=self.image2.ConvertToBitmap()
            self.bmp2=wx.StaticBitmap(self.main_list2,bitmap=self.temp2)
            self.bmp2.Center()
            self.statusBar1.SetStatusText('找到了数据：'+str(name1)+'和数据：'+str(name2),1)
        elif len(p)==1:
            name0=list(p[0])
            name0=name0[0]
            print(name0)
            self.image0=wx.Image(name0,wx.BITMAP_TYPE_JPEG)
            self.temp0=self.image0.ConvertToBitmap()
            self.bmp0=wx.StaticBitmap(self.main_list1,bitmap=self.temp0)
            self.bmp0.Center()
            self.statusBar1.SetStatusText('找到了数据：'+str(name0),1)
        else:
            print('No File!')
            self.statusBar1.SetStatusText('                                                                  Sorry！！！No Such File！！！',1)
    
    def OnTextEnterSearch(self,event):
        print('searchbutton000')
        namesearch=self.search_text.GetValue()
        namesearch=str(namesearch)
        namesearch=namesearch.replace("\\n","")
        print(namesearch)
        if namesearch==0:
            print('No File!')
        else:
            sql = "SELECT picturepath FROM UImage WHERE name = '%s' "
            data = (namesearch,)
            cursor.execute(sql % data)
            p1=list(cursor.fetchall())
            print(p1[1])
            if len(p1)==2:
                name11=list(p1[0])
                name11=name11[0]
                print('name11\n',str(name11))
                self.image11=wx.Image(name11,wx.BITMAP_TYPE_JPEG)
                self.temp11=self.image11.ConvertToBitmap()
                self.bmp11=wx.StaticBitmap(self.main_list1,bitmap=self.temp11)
                self.bmp11.Center()
                name22=list(p1[1])
                name22=name22[0]
                print('name22:\n',str(name22))
                self.image22=wx.Image(name22,wx.BITMAP_TYPE_JPEG)
                self.temp22=self.image22.ConvertToBitmap()
                self.bmp22=wx.StaticBitmap(self.main_list2,bitmap=self.temp22)
                self.bmp22.Center()
            elif len(p1)==1:
                name00=list(p1[0])
                name00=name00[0]
                print(name00)
                self.image00=wx.Image(name00,wx.BITMAP_TYPE_JPEG)
                self.temp00=self.image00.ConvertToBitmap()
                self.bmp00=wx.StaticBitmap(self.main_list1,bitmap=self.temp00)
                self.bmp00.Center()
            else:
                print('No File!')
                self.statusBar1.SetStatusText('                                                                  Sorry！！！No Such File！！！',1)
                
    def OnButtonSearch(self,event):
        print('searchbutton')
        namesearch=self.search_text.GetValue()
        print(namesearch)
        if namesearch==0:
            print('No File!')
        else:
            sql = "SELECT picturepath FROM UImage WHERE name = '%s' "
            data = (namesearch,)
            cursor.execute(sql % data)
            p1=list(cursor.fetchall())
            print(p1[1])
            if len(p1)==2:
                name11=list(p1[0])
                name11=name11[0]
                print('name11\n',str(name11))
                self.image11=wx.Image(name11,wx.BITMAP_TYPE_JPEG)
                self.temp11=self.image11.ConvertToBitmap()
                self.bmp11=wx.StaticBitmap(self.main_list1,bitmap=self.temp11)
                self.bmp11.Center()
                name22=list(p1[1])
                name22=name22[0]
                print('name22:\n',str(name22))
                self.image22=wx.Image(name22,wx.BITMAP_TYPE_JPEG)
                self.temp22=self.image22.ConvertToBitmap()
                self.bmp22=wx.StaticBitmap(self.main_list2,bitmap=self.temp22)
                self.bmp22.Center()
                self.statusBar1.SetStatusText('找到了数据：'+str(name11)+'和数据：'+str(name22),1)
            elif len(p1)==1:
                name00=list(p1[0])
                name00=name00[0]
                print(name00)
                self.image00=wx.Image(name00,wx.BITMAP_TYPE_JPEG)
                self.temp00=self.image00.ConvertToBitmap()
                self.bmp00=wx.StaticBitmap(self.main_list1,bitmap=self.temp00)
                self.bmp00.Center()
                self.statusBar1.SetStatusText('找到了数据：'+str(name00),1)
            else:
                print('No File!')
                self.statusBar1.SetStatusText('                                                                  Sorry！！！No Such File！！！',1)
            
    def OnButtonInsert(self,event):
        print('test\n insert')
        with wx.FileDialog(self,"Open file",wildcard="Text files (*.jpg)|*.jpg|(*.png)|*.png",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal()==wx.ID_OK:
                pathname_insert=fileDialog.GetPath()
                print(pathname_insert)
                w1=re.findall(r'(Shou[0-9]*).jpg',str(pathname_insert))
                w2=re.findall(r'([_BR]+)[0-9]*.jpg',str(pathname_insert))
                print('uptest')
                print(w1,w2)
                if w2==[]:
                    a=0
                else:
                    a=1
                print(a)
                print('999')
                if a==1:
                    
                    rule_number=re.findall(r'([0-9]*).jpg',str(pathname_insert))
                    print(rule_number)
                    rule_nonumber=re.findall(r'(\w*)_BR',str(pathname_insert))
                    print(rule_nonumber)
                    rule_name=rule_nonumber+rule_number
                    rule_name=''.join(map(str,rule_name))
                    #rule_name=re.findall('(\D*)',rule1[0])[0]
                    print(rule_name)
                
                    cursor.execute("SELECT id FROM UImage order by  id desc")
                    max_id11=cursor.fetchall()
                    max_id22=list(list(max_id11)[0])
                    max_id0=max_id22[0]
                    #print(max_id)
                    path1=[]
                    for i in str(pathname_insert):
                        if i=='\\':
                            path1.append("\\\\")
                        else:
                            path1.append(i)
                    print(path1)
                    path1=''.join(map(str,path1))
                    print('_BR:name\n',str(path1))
                    sql = "INSERT INTO UImage (id,name,picturepath) VALUES(%d,'%s','%s')"
                    data = (max_id0+1,str(rule_name),str(path1))#只可用英文
                    cursor.execute(sql %data)
                    connect.commit()
                    print('成功插入', cursor.rowcount, '条数据')
                    self.statusBar1.SetStatusText('                                     成功插入'+str(cursor.rowcount)+'条数据'+'已经插入了名字为：'+str(rule_name)+'的数据',1)
                elif a==0:
                    print('no')
                    rule_name1=re.findall(r'(\w*).jpg',str(pathname_insert))
                    #rule_name=re.findall('(\D*)',rule1[0])[0]
                    print(rule_name1[0])
                
                    cursor.execute("SELECT id FROM UImage order by  id desc")
                    max_id1=cursor.fetchall()
                    max_id2=list(list(max_id1)[0])
                    max_id=max_id2[0]
                    #print(max_id)
                    path2=[]
                    for i2 in str(pathname_insert):
                        if i2=='\\':
                            path2.append("\\\\")
                        else:
                            path2.append(i2)
                    print(path2)
                    path2=''.join(map(str,path2))
                    print('NO _BR:name\n',str(path2))
                    sql = "INSERT INTO UImage (id,name,picturepath) VALUES(%d,'%s','%s')"
                    data = (max_id+1,str(rule_name1[0]),str(path2))#只可用英文
                    cursor.execute(sql %data)
                    connect.commit()
                    print('成功插入', cursor.rowcount, '条数据')
                    self.statusBar1.SetStatusText('                                     成功插入'+str(cursor.rowcount)+'条数据'+'已经插入了名字为：'+str(rule_name1[0])+'的数据',1)
                else:
                    print('插入失败!')
                    self.statusBar1.SetStatusText('                                                              插入失败！！！',1)
            else:
                print('Sorry')
                self.statusBar1.SetStatusText('                                                                  Sorry！！！No Such File！！！',1)

    def OnButtonUpdate(self,event):
        print('update')
        up_name=self.update_text.GetValue()
        print('up_name',str(up_name))
        with wx.FileDialog(self,"Open file",wildcard="Text files (*.jpg)|*.jpg|(*.png)|*.png",style=wx.FD_OPEN|wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal()==wx.ID_OK:
                pathname_up=fileDialog.GetPath()
                print(pathname_up)
                w1=re.findall(r'(Shou[0-9]*).jpg',str(pathname_up))
                w2=re.findall(r'([_BR]+)[0-9]*.jpg',str(pathname_up))
                print(w1,w2)
                if w2==[]:
                    a=0
                else:
                    a=1
                print(a)
                print('9')
                if a==1:
                    rule_number=re.findall(r'([0-9]*).jpg',str(pathname_up))
                    print(rule_number)
                    rule_nonumber=re.findall(r'(\w*)_BR',str(pathname_up))
                    print(rule_nonumber)
                    rule_name=rule_nonumber+rule_number
                    rule_name=''.join(map(str,rule_name))
                    print(rule_name)
                    
                    r1=re.findall(r'(\w*)_BR',str(up_name))
                    print('r1',str(r1[0]))
                    r2=str(rule_nonumber[0])
                    if r2==str(r1[0]):
                        cursor.execute("select id from UImage where name='%s'"%str(rule_name))
                        id_up=cursor.fetchall()
                        print(id_up)
                        id_up=list(id_up)
                        id_up=list(id_up[1])
                        id_up=int(id_up[0])
                        print('id_up1:',str(id_up))
                        
                        cursor.execute("delete from UImage where id=%d"%id_up)
                        connect.commit()
                        print('成功删除', cursor.rowcount, '条数据')
                        
                        path1=[]
                        for i in str(pathname_up):
                            if i=='\\':
                                path1.append("\\\\")
                            else:
                                path1.append(i)
                        print(path1)
                        path1=''.join(map(str,path1))
                        print('_BR:name\n',str(path1))
                        sql = "INSERT INTO UImage (id,name,picturepath) VALUES(%d,'%s','%s')"
                        data = (id_up,str(rule_name),str(path1))#只可用英文
                        cursor.execute(sql %data)
                        connect.commit()
                        print('成功插入', cursor.rowcount, '条数据')
                        self.statusBar1.SetStatusText('                                     成功插入'+str(cursor.rowcount)+'条数据'+'已经插入了名字为：'+str(rule_name)+'的数据',1)
                    else:
                        self.statusBar1.SetStatusText(                                     '请重新输入名字',1)
                elif a==0:
                    print('no')
                    rule_name1=re.findall(r'(\w*).jpg',str(pathname_up))
                    #rule_name=re.findall('(\D*)',rule1[0])[0]
                    print(rule_name1[0])
                    
                    r11=re.findall(r'([A-Za-z]*)',str(up_name))
                    r22=re.findall(r'[\D*]',str(rule_name1[0]))
                    r22=''.join(map(str,r22))
                    print(r22)
                    print('r11',str(r11[0]))
                    if r22==str(r11[0]):
                        print('234')
                        cursor.execute("select id from UImage where name='%s'"%str(r22))
                        id_up2=cursor.fetchall()
                        print(id_up2)
                        id_up2=list(id_up2)
                        id_up2=list(id_up2[0])
                        id_up2=int(id_up2[0])
                        print('id_up1:',str(id_up2))
                        cursor.execute("delete from UImage where id=%d"%id_up2)
                        connect.commit()
                        print('成功删除', cursor.rowcount, '条数据')
                        
                        
                        path2=[]
                        for i2 in str(pathname_up):
                            if i2=='\\':
                                path2.append("\\\\")
                            else:
                                path2.append(i2)
                        print(path2)
                        path2=''.join(map(str,path2))
                        print('NO _BR:name\n',str(path2))
                        sql = "INSERT INTO UImage (id,name,picturepath) VALUES(%d,'%s','%s')"
                        data = (id_up2,str(rule_name1[0]),str(path2))#只可用英文
                        cursor.execute(sql %data)
                        connect.commit()
                        print('成功插入', cursor.rowcount, '条数据')
                        self.statusBar1.SetStatusText('                                     成功插入'+str(cursor.rowcount)+'条数据'+'已经插入了名字为：'+str(rule_name1[0])+'的数据',1)
                    else:
                        self.statusBar1.SetStatusText(                                     '请重新输入名字',1) 
                else:
                    print('插入失败!')
                    self.statusBar1.SetStatusText('                                                              插入失败！！！',1)
            else:
                print('Sorry')
                self.statusBar1.SetStatusText('                                                                  Sorry！！！No Such File！！！',1)

        
    def OnUpdateText(self,event):
        print('update please')
        self.update_text.SetValue('')

    def OnButtonDelect(self,event):
        print('test\n delect')
        delete_name=self.delete_text.GetValue()
        print('test1:delete_name\n',str(delete_name))
        
        cursor.execute("DELETE from UImage WHERE name= '%s' "%str(delete_name))
        #delete_name1=cursor.fetchall()
        connect.commit()
        print('成功删除', cursor.rowcount, '条数据')
        if cursor.rowcount==0:
            self.statusBar1.SetStatusText('                                     成功删除 0 条数据',1)
        else:
            self.statusBar1.SetStatusText('                                     成功删除'+str(cursor.rowcount)+'条数据'+'已经删除了数据：'+str(delete_name),1)
            
        self.delete_text.Clear()
    def OnDeleteText(self,event):
        self.delete_text.Clear()
        
        
    def OnSearchText(self,event):
        print('search')

    def OnMainList1(self,event):
        print('list')
        
    def OnMainList2(self,event):
        print('list2')
        
    def OnMenuSetColorRed(self,event):
        self.button_delect.SetForegroundColour('red') 
        self.button_insert.SetForegroundColour('red')
        self.button_search.SetForegroundColour('red')
        self.button_update.SetForegroundColour('red')
        self.search_text.SetForegroundColour('red')
        self.search_text.SetBackgroundColour('red')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorBlue(self,event):
        self.button_delect.SetForegroundColour('SLATE BLUE') 
        self.button_insert.SetForegroundColour('SLATE BLUE')
        self.button_search.SetForegroundColour('SLATE BLUE')
        self.button_update.SetForegroundColour('SLATE BLUE')
        self.search_text.SetForegroundColour('SLATE BLUE')
        self.search_text.SetBackgroundColour('SLATE BLUE')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorYellow(self,event):
        self.button_delect.SetForegroundColour('YELLOW') 
        self.button_insert.SetForegroundColour('YELLOW')
        self.button_search.SetForegroundColour('YELLOW')
        self.button_update.SetForegroundColour('YELLOW')
        self.search_text.SetForegroundColour('YELLOW')
        self.search_text.SetBackgroundColour('YELLOW')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorGreen(self,event):
        self.button_delect.SetForegroundColour('AQUAMARINE') 
        self.button_insert.SetForegroundColour('AQUAMARINE')
        self.button_search.SetForegroundColour('AQUAMARINE')
        self.button_update.SetForegroundColour('AQUAMARINE')
        self.search_text.SetForegroundColour('AQUAMARINE')
        self.search_text.SetBackgroundColour('AQUAMARINE')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorPurple(self,event):
        self.button_delect.SetForegroundColour('PURPLE') 
        self.button_insert.SetForegroundColour('PURPLE')
        self.button_search.SetForegroundColour('PURPLE')
        self.button_update.SetForegroundColour('PURPLE')
        self.search_text.SetForegroundColour('PURPLE')
        self.search_text.SetBackgroundColour('PURPLE')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorOrange(self,event):
        self.button_delect.SetForegroundColour('CORAL') 
        self.button_insert.SetForegroundColour('CORAL')
        self.button_search.SetForegroundColour('CORAL')
        self.button_update.SetForegroundColour('CORAL')
        self.search_text.SetForegroundColour('CORAL')
        self.search_text.SetBackgroundColour('CORAL')
        self.search_text.SetForegroundColour('Black')
    def OnMenuSetColorPink(self,event):
        self.button_delect.SetForegroundColour('ORANGE RED') 
        self.button_insert.SetForegroundColour('ORANGE RED')
        self.button_search.SetForegroundColour('ORANGE RED')
        self.button_update.SetForegroundColour('ORANGE RED')
        self.search_text.SetForegroundColour('ORANGE RED')
        self.search_text.SetBackgroundColour('ORANGE RED')
        self.search_text.SetForegroundColour('Black')
    def OnMenuNetWork(self,event):
        webbrowser.open("http://www.digimons.net/digimon/chn.html")#数码宝贝数据库，
        
    def OnMenuQuit(self,event):
        """关闭数据库连接 并结束程序"""
        cursor.close()
        connect.close()
        os.sys.exit()
  
      
app=wx.App()
# 连接数据库
connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='279813lxyz',
    db='ps_mysql_python_project',
    charset='gbk'
)
# 获取游标
cursor = connect.cursor()

win=MyFrame()
win.Show()
app.MainLoop()
