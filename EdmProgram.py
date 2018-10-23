""" 代表一个EDM的程序 """

from decimal import Decimal


class CommandLine:

    def __init__(self, cmd, index):
        self.index = index
        self.is_call_el = False
        self.is_call_wp = False
        self.el_done = False
        # 新增加
        self.add_cmd = False
        t = cmd.strip()
        if t == '0':
            self.row_number = '0'
            self.command = ''
            return
        tab_index = t.find( '\t' )
        self.row_number = t[0:tab_index]
        self.command = (t[tab_index:]).strip()

    def get_prt_info(self):
        if self.command.strip().find(';') == 0:
            return None
        if self.command.find( 'PRT_ELCALL' ) >= 0:
            self.is_call_el = True
        elif self.command.find( 'PRT_WPCALL' ) >= 0:
            self.is_call_wp = True
        else:
            return None
        i_1 = self.command.find( '(' )
        i_2 = self.command.find( ',' )
        return self.command[i_1 + 1:i_2].strip()

    def __str__(self):
        tab_s = '\t\t'
        if self.row_number[-3:] == '000':
            tab_s = '\t'
        return self.row_number + tab_s + self.command


class EdmProgram:

    def __init__(self, seq_file, program_name):
        self.seq_file = seq_file
        self.program_name = program_name
        self.el_dict = {}
        # el所对应的wp，el上面的、最近的wp
        self.el_2_wp = {}
        self.cmd_list = []
        current_wp = None
        with open( seq_file, 'r' ) as ff:
            dd = ff.readlines()
            i = 0
            while i < len( dd ):
                d = dd[i]
                c = CommandLine( d, i )
                self.cmd_list.append( c )
                if c.command.strip() == 'END':
                    break
                prt = c.get_prt_info()
                if c.is_call_wp:
                    current_wp = prt
                    i += 1
                    continue
                if c.is_call_el:
                    # 查看有关电极的数据
                    td = dd[i + 1]
                    tc = CommandLine( td, i + 1 )
                    if tc.command.find( ';;;__start' ) >= 0:
                        i += 2
                        el_data = [False, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                        el_data[0] = True
                        while True:
                            td = dd[i]
                            tc = CommandLine( td, i )
                            if tc.command.find( ';;;__end' ) >= 0:
                                break
                            p = self._get_cmd_data( tc.command )
                            if p[0] is not None:
                                el_data[int( p[0] ) - 20] = p[1]
                            i += 1
                        self.el_dict[prt] = el_data
                    self.el_2_wp[prt] = current_wp
                if prt is not None and prt not in self.el_dict:
                    self.el_dict[prt] = [False, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                i += 1
        ff.close()

    @staticmethod
    def _get_cmd_data(the_string: str) -> tuple:
        try:
            p_i = the_string.find( 'PAR' )
            p_s = the_string[p_i + 3:p_i + 5]
            v_i = the_string.find( '=' )
            v_s = the_string[v_i + 1:].strip()
            return p_s, Decimal( v_s )
        except:
            return None, None

    def get_seq_path(self):
        index = self.seq_file.rfind( '\\' )
        return self.seq_file[0:index + 1]

    def __str__(self):
        return self.program_name
