# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"电极测量", pos = wx.DefaultPosition, size = wx.Size( 571,514 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menu1 = wx.Menu()
		self.m_menuItem1 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"设置", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem1 )
		
		self.m_menu1.AppendSeparator()
		
		self.m_menuItem2 = wx.MenuItem( self.m_menu1, wx.ID_ANY, u"退出", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menu1.AppendItem( self.m_menuItem2 )
		
		self.m_menubar1.Append( self.m_menu1, u"操作" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"程序", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer2.Add( self.m_staticText1, 0, wx.ALL, 2 )
		
		programListBoxChoices = []
		self.programListBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, programListBoxChoices, 0 )
		bSizer2.Add( self.programListBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"电极", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		bSizer2.Add( self.m_staticText2, 0, wx.ALL, 2 )
		
		elListBoxChoices = []
		self.elListBox = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, elListBoxChoices, 0|wx.VSCROLL )
		bSizer2.Add( self.elListBox, 1, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel4 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer10 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer1 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.measureElCheckBox = wx.CheckBox( self.m_panel4, wx.ID_ANY, u"加工前测量电极", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.measureElCheckBox, 0, wx.ALL, 5 )
		
		self.elInfoTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elInfoTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText4 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"X方向长度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		gSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
		
		self.elDimXTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elDimXTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Y方向长度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
		
		self.elDimYTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elDimYTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText6 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"Z方向长度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		gSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		self.elDimZTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elDimZTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"分中时电极下降深度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer1.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		self.elDownZTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elDownZTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText8 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"测高度X方向偏移", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gSizer1.Add( self.m_staticText8, 0, wx.ALL, 5 )
		
		self.elHeightXOffsetTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elHeightXOffsetTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText9 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"测高度Y方向偏移", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText9.Wrap( -1 )
		gSizer1.Add( self.m_staticText9, 0, wx.ALL, 5 )
		
		self.elHeightYOffsetTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elHeightYOffsetTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText111 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"测量高度的快速下探距离", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText111.Wrap( -1 )
		gSizer1.Add( self.m_staticText111, 0, wx.ALL, 5 )
		
		self.elHeightZRapidTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elHeightZRapidTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText10 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"电极中心X方向偏移", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText10.Wrap( -1 )
		gSizer1.Add( self.m_staticText10, 0, wx.ALL, 5 )
		
		self.elCenterXOffsetTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elCenterXOffsetTextBox, 0, wx.ALL, 5 )
		
		self.m_staticText11 = wx.StaticText( self.m_panel4, wx.ID_ANY, u"电极中心Y方向偏移", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText11.Wrap( -1 )
		gSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )
		
		self.elCenterYOffsetTextBox = wx.TextCtrl( self.m_panel4, wx.ID_ANY, u"0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.elCenterYOffsetTextBox, 0, wx.ALL, 5 )
		
		
		bSizer10.Add( gSizer1, 1, wx.EXPAND, 5 )
		
		self.saveElDataButton = wx.Button( self.m_panel4, wx.ID_ANY, u"保存电极数据", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.saveElDataButton, 0, wx.ALIGN_RIGHT|wx.ALL, 2 )
		
		
		bSizer10.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		self.m_panel4.SetSizer( bSizer10 )
		self.m_panel4.Layout()
		bSizer10.Fit( self.m_panel4 )
		self.m_notebook2.AddPage( self.m_panel4, u"操作", False )
		
		bSizer3.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer1, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.okButton, 0, wx.ALL, 2 )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.cancelButton, 0, wx.ALL, 2 )
		
		
		bSizer7.Add( bSizer9, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.OnMenuOptionSelected, id = self.m_menuItem1.GetId() )
		self.Bind( wx.EVT_MENU, self.OnMenuExitSelected, id = self.m_menuItem2.GetId() )
		self.programListBox.Bind( wx.EVT_LISTBOX, self.OnClickInProgramsList )
		self.elListBox.Bind( wx.EVT_LISTBOX, self.OnClickInElList )
		self.measureElCheckBox.Bind( wx.EVT_CHECKBOX, self.OnMeasureOrNotCheckBox )
		self.saveElDataButton.Bind( wx.EVT_BUTTON, self.OnSaveElData )
		self.okButton.Bind( wx.EVT_BUTTON, self.OnOkButton )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.OnCancelButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnMenuOptionSelected( self, event ):
		event.Skip()
	
	def OnMenuExitSelected( self, event ):
		event.Skip()
	
	def OnClickInProgramsList( self, event ):
		event.Skip()
	
	def OnClickInElList( self, event ):
		event.Skip()
	
	def OnMeasureOrNotCheckBox( self, event ):
		event.Skip()
	
	def OnSaveElData( self, event ):
		event.Skip()
	
	def OnOkButton( self, event ):
		event.Skip()
	
	def OnCancelButton( self, event ):
		event.Skip()
	

###########################################################################
## Class ConfigDialog
###########################################################################

class ConfigDialog ( wx.Dialog ):
	
	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"设置", pos = wx.DefaultPosition, size = wx.Size( 422,329 ), style = wx.DEFAULT_DIALOG_STYLE )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer7 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.VERTICAL )
		
		gSizer2 = wx.GridSizer( 0, 2, 0, 0 )
		
		self.m_staticText12 = wx.StaticText( self, wx.ID_ANY, u"安全距离", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		gSizer2.Add( self.m_staticText12, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.safetyDisTextBox = wx.TextCtrl( self, wx.ID_ANY, u"2.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.safetyDisTextBox, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText13 = wx.StaticText( self, wx.ID_ANY, u"基准球直径", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText13.Wrap( -1 )
		gSizer2.Add( self.m_staticText13, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.probeDiamTextBox = wx.TextCtrl( self, wx.ID_ANY, u"8.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.probeDiamTextBox, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText14 = wx.StaticText( self, wx.ID_ANY, u"测量公差", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText14.Wrap( -1 )
		gSizer2.Add( self.m_staticText14, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.toleranceTextBox = wx.TextCtrl( self, wx.ID_ANY, u"0.01", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.toleranceTextBox, 1, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText15 = wx.StaticText( self, wx.ID_ANY, u"探测距离", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText15.Wrap( -1 )
		gSizer2.Add( self.m_staticText15, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.searchDisTextbox = wx.TextCtrl( self, wx.ID_ANY, u"120", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.searchDisTextbox, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText16 = wx.StaticText( self, wx.ID_ANY, u"探测速度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText16.Wrap( -1 )
		gSizer2.Add( self.m_staticText16, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.searchSpeedTextBox = wx.TextCtrl( self, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.searchSpeedTextBox, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText17 = wx.StaticText( self, wx.ID_ANY, u"回退距离", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText17.Wrap( -1 )
		gSizer2.Add( self.m_staticText17, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.retractDisTextBox = wx.TextCtrl( self, wx.ID_ANY, u"0.5", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.retractDisTextBox, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText18 = wx.StaticText( self, wx.ID_ANY, u"测量距离", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText18.Wrap( -1 )
		gSizer2.Add( self.m_staticText18, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.measureDicTextBox = wx.TextCtrl( self, wx.ID_ANY, u"1.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.measureDicTextBox, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText19 = wx.StaticText( self, wx.ID_ANY, u"测量速度", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText19.Wrap( -1 )
		gSizer2.Add( self.m_staticText19, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.measureSpeedTextBox = wx.TextCtrl( self, wx.ID_ANY, u"20", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.measureSpeedTextBox, 0, wx.ALL|wx.EXPAND, 2 )
		
		self.m_staticText20 = wx.StaticText( self, wx.ID_ANY, u"超差时处理语句", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText20.Wrap( -1 )
		gSizer2.Add( self.m_staticText20, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.alertBlockTextBox = wx.TextCtrl( self, wx.ID_ANY, u"SHOWDLG (OUT OF TOLERANCE)", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.alertBlockTextBox, 0, wx.ALL|wx.EXPAND, 2 )
		
		
		bSizer9.Add( gSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer9.Add( ( 0, 0), 1, wx.EXPAND, 5 )
		
		
		bSizer7.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.okButton = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.okButton, 0, wx.ALL, 2 )
		
		self.cancelButton = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.cancelButton, 0, wx.ALL, 2 )
		
		
		bSizer7.Add( bSizer8, 0, wx.ALIGN_RIGHT, 5 )
		
		
		self.SetSizer( bSizer7 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnDialogClose )
		self.okButton.Bind( wx.EVT_BUTTON, self.OnOkButton )
		self.cancelButton.Bind( wx.EVT_BUTTON, self.OnCancelButton )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnDialogClose( self, event ):
		event.Skip()
	
	def OnOkButton( self, event ):
		event.Skip()
	
	def OnCancelButton( self, event ):
		event.Skip()
	

