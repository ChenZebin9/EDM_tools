""" 一个用来测试电极自动测量的对话框 """

import wx
import EdmProgram
import MyFirstFrame
import os
import sqlite3
from decimal import Decimal

database_file = 'data\config.db'


class ConfigData( object ):

    def __init__(self):
        # 安全距离
        self.sfd = 2.0
        # 基准球直径
        self.pbr = 8.0
        # 测量公差
        self.ma = 0.01
        # 探测距离
        self.dd1 = 120
        # 探测速度
        self.ps = 100
        # 回退距离
        self.rd = 0.5
        # 测量距离
        self.dd2 = 1.0
        # 测量速度
        self.ms = 20
        # 超差时处理语句
        self.eh1 = 'SHOWDLG (HEY! OUT OF TOLERANCE!)'
        # 反模拟高度
        self.sim = 0.0
        # 整体测量速度 mm/min
        self.gps = 1000


def get_template_el_block():
    file_path = 'template\measurement_el_block'
    with open( file_path, 'r' ) as ff:
        r = ff.read()
    ff.close()
    return r


def get_template_el_block_2():
    file_path = 'template\measurement_el_block_2'
    with open( file_path, 'r' ) as ff:
        r = ff.read()
    ff.close()
    return r


def get_template_point(config_data_r: ConfigData):
    file_path = 'template\measurement_point'
    with open( file_path, 'r' ) as ff:
        r = ff.read()
    ff.close()
    dd1 = config_data_r.dd1
    ps = config_data_r.ps
    rd = config_data_r.rd
    dd2 = config_data_r.dd2
    ms = config_data_r.ms
    ma = config_data_r.ma
    # Z-
    sub_31 = r.format( pNr=31, d='Z', dd=2, dd1=-dd1, ps=ps, rd=rd, dd2=-dd2, ms=ms, ma=ma )
    # X+
    sub_32 = r.format( pNr=32, d='X', dd=1, dd1=dd1, ps=ps, rd=-rd, dd2=dd2, ms=ms, ma=ma )
    # X-
    sub_33 = r.format( pNr=33, d='X', dd=1, dd1=-dd1, ps=ps, rd=rd, dd2=-dd2, ms=ms, ma=ma )
    # Y+
    sub_34 = r.format( pNr=34, d='Y', dd=3, dd1=dd1, ps=ps, rd=-rd, dd2=dd2, ms=ms, ma=ma )
    # Y-
    sub_35 = r.format( pNr=35, d='Y', dd=3, dd1=-dd1, ps=ps, rd=rd, dd2=-dd2, ms=ms, ma=ma )
    tt = '\n'.join( [sub_31, sub_32, sub_33, sub_34, sub_35] )
    return tt.split( '\n' )


class ConfigDialog( MyFirstFrame.ConfigDialog ):

    def __init__(self, parent, config_data_r: ConfigData):
        MyFirstFrame.ConfigDialog.__init__( self, parent )
        # 读取配置文件
        self.data_dict = {}
        self.config_data = config_data_r
        self.conn = None
        init_cmd = []
        config_file = 'template\config'
        if not os.path.exists( config_file ):
            wx.MessageBox( '配置文件不存在！' )
            return
        with open( config_file, 'r' ) as ff:
            for line in ff.readlines():
                init_cmd.append( line )
        if os.path.exists( database_file ) is False:
            conn = sqlite3.connect( database_file )
            c = conn.cursor()
            c.execute( '''CREATE TABLE REAL_VALUE_CONFIG
            (DES CHAR(256) PRIMARY KEY NOT NULL,
            VALUE_CONFIG REAL NOT NULL);''' )
            c.execute( '''CREATE TABLE STRING_VALUE_CONFIG
            (DES CHAR(256) PRIMARY KEY NOT NULL,
            VALUE_CONFIG CHAR(512) NOT NULL);''' )
            for cmd in init_cmd:
                c.execute(cmd)
            conn.commit()
        else:
            self.conn = sqlite3.connect( database_file )
            self._read_data()

    def _read_data(self):
        c = self.conn.cursor()
        cursor = c.execute( 'SELECT DES, VALUE_CONFIG FROM REAL_VALUE_CONFIG' )
        for row in cursor:
            self.data_dict[row[0]] = row[1]
        cursor = c.execute( 'SELECT DES, VALUE_CONFIG FROM STRING_VALUE_CONFIG' )
        for row in cursor:
            self.data_dict[row[0]] = row[1]
        sfd = self.data_dict['sfd']
        self.safetyDisTextBox.SetValue( str( sfd ) )
        pbr = self.data_dict['pbr']
        self.probeDiamTextBox.SetValue( str( pbr ) )
        ma = self.data_dict['ma']
        self.toleranceTextBox.SetValue( str( ma ) )
        dd1 = self.data_dict['dd1']
        self.searchDisTextbox.SetValue( str( dd1 ) )
        ps = self.data_dict['ps']
        self.searchSpeedTextBox.SetValue( str( ps ) )
        rd = self.data_dict['rd']
        self.retractDisTextBox.SetValue( str( rd ) )
        dd2 = self.data_dict['dd2']
        self.measureDicTextBox.SetValue( str( dd2 ) )
        ms = self.data_dict['ms']
        self.measureSpeedTextBox.SetValue( str( ms ) )
        eh1 = self.data_dict['eh1']
        self.alertBlockTextBox.SetValue( eh1 )
        sim = self.data_dict['sim']
        self.simHeightTextBox.SetValue( str( sim ) )
        gps = self.data_dict['gps']
        self.globalSpeedTextBox.SetValue( str( gps ) )

    @staticmethod
    def read_config_first(config_data_r: ConfigData):
        if os.path.exists( database_file ) is False:
            return
        conn = sqlite3.connect( database_file )
        c = conn.cursor()
        cursor = c.execute( 'SELECT DES, VALUE_CONFIG FROM REAL_VALUE_CONFIG' )
        data_s = {}
        for row in cursor:
            data_s[row[0]] = row[1]
        cursor = c.execute( 'SELECT DES, VALUE_CONFIG FROM STRING_VALUE_CONFIG' )
        for row in cursor:
            data_s[row[0]] = row[1]
        config_data_r.dd1 = data_s['dd1']
        config_data_r.dd2 = data_s['dd2']
        config_data_r.ma = data_s['ma']
        config_data_r.ms = data_s['ms']
        config_data_r.pbr = data_s['pbr']
        config_data_r.ps = data_s['ps']
        config_data_r.rd = data_s['rd']
        config_data_r.sfd = data_s['sfd']
        config_data_r.eh1 = data_s['eh1']
        config_data_r.sim = data_s['sim']
        config_data_r.gps = data_s['gps']
        conn.close()

    def _set_data(self):
        try:
            sfd = Decimal( self.safetyDisTextBox.GetValue() )
            self.config_data.sfd = sfd
            pbr = Decimal( self.probeDiamTextBox.GetValue() )
            self.config_data.pbr = pbr
            ma = Decimal( self.toleranceTextBox.GetValue() )
            self.config_data.ma = ma
            dd1 = Decimal( self.searchDisTextbox.GetValue() )
            self.config_data.dd1 = dd1
            ps = Decimal( self.searchSpeedTextBox.GetValue() )
            self.config_data.ps = ps
            rd = Decimal( self.retractDisTextBox.GetValue() )
            self.config_data.rd = rd
            dd2 = Decimal( self.measureDicTextBox.GetValue() )
            self.config_data.dd2 = dd2
            ms = Decimal( self.measureSpeedTextBox.GetValue() )
            self.config_data.ms = ms
            eh1 = self.alertBlockTextBox.GetValue()
            self.config_data.eh1 = eh1
            sim = Decimal( self.simHeightTextBox.GetValue() )
            self.config_data.sim = sim
            gps = Decimal( self.globalSpeedTextBox.GetValue() )
            self.config_data.gps = gps
            c = self.conn.cursor()
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( sfd, 'sfd' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( pbr, 'pbr' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( ma, 'ma' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( dd1, 'dd1' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( ps, 'ps' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( rd, 'rd' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( dd2, 'dd2' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( ms, 'ms' ) )
            c.execute( "UPDATE STRING_VALUE_CONFIG SET VALUE_CONFIG='{0}' WHERE DES='{1}'".format( eh1, 'eh1' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( sim, 'sim' ) )
            c.execute( "UPDATE REAL_VALUE_CONFIG SET VALUE_CONFIG={0} WHERE DES='{1}'".format( gps, 'gps' ) )
            self.conn.commit()
            return 0
        except Exception as e:
            wx.MessageBox( e.__str__(), '保存出错', wx.OK | wx.ICON_ERROR )
            return -1

    def OnCancelButton(self, event):
        self._close_conn()
        self.Close()

    def OnOkButton(self, event):
        r = self._set_data()
        if r >= 0:
            self._close_conn()
            self.Close()

    def _close_conn(self):
        if self.conn is not None:
            self.conn.close()


class MyFrame( MyFirstFrame.MyFrame1 ):

    def __init__(self, parent, config_data_r: ConfigData):
        MyFirstFrame.MyFrame1.__init__( self, parent )
        self.config_data = config_data_r
        # 读取程序
        self.current_program = None
        self.current_electrode = None
        self.programs_dir = 'C:\OPS_ING\Programs'
        if os.path.exists(self.programs_dir) is False:
            wx.MessageBox('未找到程序文件夹')
            return
        all_programs_t = os.listdir( self.programs_dir )
        self.all_programs_dict = {}
        for a in all_programs_t:
            if a == 'SYSTEM':
                continue
            seq_file = '{0}\{1}\{1}.SEQ'.format( self.programs_dir, a )
            pp = EdmProgram.EdmProgram( seq_file, a )
            self.all_programs_dict[a] = pp
        self.programListBox.AppendItems( list( self.all_programs_dict.keys() ) )

    def OnMenuOptionSelected(self, event):
        config_dialog = ConfigDialog( parent=self, config_data_r=self.config_data )
        config_dialog.ShowModal()

    def OnMenuExitSelected(self, event):
        self.Close()

    def OnCancelButton(self, event):
        self.Close()

    def OnClickInProgramsList(self, event):
        selected_program = self.programListBox.GetStringSelection()
        pp = self.all_programs_dict[selected_program]
        self.current_program = pp
        self.elListBox.Clear()
        self.elListBox.AppendItems( list( pp.el_dict.keys() ) )
        self.current_electrode = None
        self._clean_input()

    def OnClickInElList(self, event):
        selected_el = self.elListBox.GetStringSelection()
        self.current_electrode = selected_el
        el_data = self.current_program.el_dict[selected_el]
        wp_name = self.current_program.el_2_wp[selected_el]
        self.measureElCheckBox.SetValue( el_data[0] )
        self.elDimXTextBox.SetValue( str( el_data[1] ) )
        self.elDimYTextBox.SetValue( str( el_data[2] ) )
        self.elDimZTextBox.SetValue( str( el_data[3] ) )
        self.elDownZTextBox.SetValue( str( el_data[4] ) )
        self.elHeightXOffsetTextBox.SetValue( str( el_data[5] ) )
        self.elHeightYOffsetTextBox.SetValue( str( el_data[6] ) )
        self.elHeightZRapidTextBox.SetValue( str( el_data[7] ) )
        self.elCenterXOffsetTextBox.SetValue( str( el_data[8] ) )
        self.elCenterYOffsetTextBox.SetValue( str( el_data[9] ) )
        if wp_name is not None:
            self.elInfoTextBox.SetValue( wp_name )
        else:
            self.elInfoTextBox.SetValue( '' )

    def _clean_input(self):
        self.measureElCheckBox.SetValue( False )
        self.elDimXTextBox.SetValue( '' )
        self.elDimYTextBox.SetValue( '' )
        self.elDimZTextBox.SetValue( '' )
        self.elDownZTextBox.SetValue( '' )
        self.elHeightXOffsetTextBox.SetValue( '' )
        self.elHeightYOffsetTextBox.SetValue( '' )
        self.elHeightZRapidTextBox.SetValue( '' )
        self.elCenterXOffsetTextBox.SetValue( '' )
        self.elCenterYOffsetTextBox.SetValue( '' )
        self.elInfoTextBox.SetValue( '' )

    def OnSaveElData(self, event):
        if self.current_program is not None and self.current_electrode is not None:
            cc = self.measureElCheckBox.GetValue()
            par21 = self.elDimXTextBox.GetValue()
            par22 = self.elDimYTextBox.GetValue()
            par23 = self.elDimZTextBox.GetValue()
            par24 = self.elDownZTextBox.GetValue()
            par25 = self.elHeightXOffsetTextBox.GetValue()
            par26 = self.elHeightYOffsetTextBox.GetValue()
            par27 = self.elHeightZRapidTextBox.GetValue()
            par28 = self.elCenterXOffsetTextBox.GetValue()
            par29 = self.elCenterYOffsetTextBox.GetValue()
            data = [cc, Decimal( par21 ), Decimal( par22 ), Decimal( par23 ), Decimal( par24 ),
                    Decimal( par25 ), Decimal( par26 ), Decimal( par27 ), Decimal( par28 ), Decimal( par29 )]
            self.current_program.el_dict[self.current_electrode] = data

    def OnOkButton(self, event):
        if self.current_program is None:
            return
        need_sub = False
        done_el = []
        while True:
            el_name = None
            current_command = None
            command_index = -1
            i = 0
            for c in self.current_program.cmd_list:
                if c.add_cmd is False and c.is_call_el is True and c.el_done is False:
                    el_name = c.get_prt_info()
                    current_command = c
                    command_index = i + 1
                    break
                i += 1
            if el_name is None:
                break
            # 该电极已经被处理过了
            if el_name in done_el:
                current_command.el_done = True
                continue
            if el_name in self.current_program.el_dict is False:
                wx.MessageBox( '程序列表中没有出现该电极' )
                current_command.el_done = True
                continue
            el_data = self.current_program.el_dict[el_name]
            if el_data[0] is False:
                wx.MessageBox( '电极{0}不用测试。'.format( el_name ) )
                current_command.el_done = True
                continue
            done_el.append( el_name )
            new_commands = ';;;__start Check {el_name} el\nPAR21 = {0}\nPAR22 = {1}\nPAR23 = {2}\nPAR24 = {3}\nPAR25 ' \
                           '= {4}\nPAR26 = {5}\nPAR27 = {6}\nPAR28 = {7}\nPAR29 = {8}\nCALL_SUB(17)'. \
                format( el_data[1], el_data[2], el_data[3], el_data[4], el_data[5], el_data[6], el_data[7], el_data[8],
                        el_data[9], el_name=el_name )
            new_commands_1 = 'PRT_ELCALL({0},0,0,0)'.format( el_name )
            new_commands_2 = 'CALL_SUB(18)'
            new_commands_3 = 'PRT_WPCALL({0},0,0)'.format(self.current_program.el_2_wp[el_name])
            new_commands_4 = ';;;__end Check {0} el'.format( el_name )
            insert_lines = '\n'.join( [new_commands, new_commands_1, new_commands_2, new_commands_1, new_commands_3,
                                       new_commands_4] )
            new_commands_list = insert_lines.split( '\n' )
            for l in new_commands_list:
                t = '{1}\t\t{0}'.format( l, command_index + 1 )
                the_cmd = EdmProgram.CommandLine( t, 0 )
                the_cmd.add_cmd = True
                self.current_program.cmd_list.insert( command_index, the_cmd )
                command_index += 1
            current_command.el_done = True
            need_sub = True
        # 增加子程序
        if need_sub is True:
            new_def_sub = []
            r_sfd = self.config_data.sfd + self.config_data.pbr / 2
            eh1 = self.config_data.eh1
            el_block = get_template_el_block().format( sfd = self.config_data.sfd, sfdp=r_sfd,
                                                       eh1=eh1, eh2=eh1, eh3=eh1, eh4=eh1, eh5=eh1,
                                                       sim=self.config_data.sim, gps=self.config_data.gps )
            el_block.strip()
            new_def_sub.extend( el_block.split( '\n' ) )
            el_block_2 = get_template_el_block_2().strip()
            new_def_sub.extend( el_block_2.split( '\n' ) )
            new_def_sub.extend( get_template_point( self.config_data ) )
            for cl in new_def_sub:
                t = '1\t{0}'.format( cl )
                the_cmd = EdmProgram.CommandLine( t, 0 )
                the_cmd.add_cmd = True
                self.current_program.cmd_list.append( the_cmd )
        # 重新整合所有 commands
        new_program_file = '{0}{1}.SEQ'.format( self.current_program.get_seq_path(),
                                                self.current_program.program_name )
        # 对源文件进行备份
        bak_file = new_program_file + '.bak'
        if os.path.exists( bak_file ):
            os.remove( bak_file )
        os.renames( new_program_file, bak_file )
        wf = open( new_program_file, 'w' )
        i = -1
        for c in self.current_program.cmd_list:
            if i >= 0:
                c.row_number = '{:05}'.format( i )
            i += 1
            wf.write( '{0}\n'.format( c ) )
        wf.close()
        mes = '生成完毕！'
        say_warning = False
        if self.config_data.sim > 0.0:
            say_warning = True
            mes += '模拟高度为{0:.0f}mm！'.format( self.config_data.sim )
        wx.MessageBox( mes, style=(wx.ICON_WARNING | wx.OK) if say_warning else (wx.ICON_INFORMATION | wx.OK) )
        self.Close()


if __name__ == '__main__':
    app = wx.App()
    config_data = ConfigData()
    # 初始化参数
    ConfigDialog.read_config_first( config_data )
    mainWin = MyFrame( None, config_data )
    app.SetTopWindow( mainWin )
    mainWin.Show()
    app.MainLoop()
