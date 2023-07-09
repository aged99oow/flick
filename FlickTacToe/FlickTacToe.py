#
# FlickTacToe.py 2022/11/20
#
import pyxel
WIDTH, HEIGHT = 109, 160
BOARD_X, BOARD_Y = -16, 10
INHAND_X1, INHAND_Y1 = 4, 5
INHAND_X2, INHAND_Y2 = 4, 135
INHAND_WIDTH, INHAND_HEIGHT = 101, 21
NONE, P1, P2, DRAW, MUSTWIN, MUSTLOSS, NOTLOSS, OTHER = 0, 1, 2, 3, 4, 5, 6, 7
OPP = {P1:P2, P2:P1}
MD_MAN, MD_COMLV1, MD_COMLV2, MD_COMLV3 = 0, 1, 2, 3
VSMODE_TXT = {MD_MAN:'   Human vs Human', MD_COMLV1:'Human vs Com Level 1', MD_COMLV2:'Human vs Com Level 2', MD_COMLV3:'Human vs Com Level 3',}
ST_TITLE, ST_START, ST_COMPUTE, ST_TAKE, ST_PLACE, ST_FLICK, ST_JUDGE, ST_END = 101, 102, 103, 104, 105, 106, 107, 108
AROUND = (8, 9, 10, 11, 12, 15, 19, 22, 26, 29, 33, 36, 37, 38, 39, 40)
CANPLACE = {8:16, 9:16, 10:17, 11:18, 12:18, 15:16, 19:18, 22:23, 26:25, 29:30, 33:32, 36:30, 37:30, 38:31, 39:32, 40:32}
DIR = {8:8, 9:7, 10:7, 11:7, 12:6, 15:1, 19:-1, 22:1, 26:-1, 29:1, 33:-1, 36:-6, 37:-7, 38:-7, 39:-7, 40:-8}
WARP = (40,36,37,38,39,40,36, 12,0,0,0,0,0,8, 19,0,0,0,0,0,15, 26,0,0,0,0,0,22, 33,0,0,0,0,0,29, 40,0,0,0,0,0,36, 12,8,9,10,11,12,8)

class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title='Flick Tac Toe')
        pyxel.load('assets/FlickTacToe.pyxres')
        pyxel.mouse(True)
        self.rept = 0
        self.debug = False
        self.wait = 0
        self.vsmode = 1
        self.board = [0]*49
        self.board[8], self.board[12], self.board[24], self.board[36], self.board[40] = P1, P1, P1, P1, P1
        self.board[16], self.board[18], self.board[30], self.board[32] = P2, P2, P2, P2
        self.inhand = [0,0,1]
        self.win = [False, False, False]
        self.turn = 0
        self.same_pos = 0
        self.st = ST_TITLE 
        pyxel.run(self.update, self.draw)

    def holddown(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT, 60, 1):
            if self.rept==0:
                self.rept = 1
            elif self.rept==1:
                self.rept = 2
                self.debug = not self.debug
        else:
            self.rept = 0

    def append_hist_move(self):
        add = self.board[8:13]+self.board[15:20]+self.board[22:27]+self.board[29:34]+self.board[36:41]
        self.hist_move.append(add)
        return self.hist_move.count(add)

    def get_precanplace(self, take_pos, board):
        canplace = []
        for i in AROUND:
            cp = CANPLACE[i]
            b1 = board[i]
            if i==take_pos:
                b1 = 0
            b2 = board[cp]
            if cp==take_pos:
                b2 = 0
            if cp and b1==0 and b2==0:
                canplace.append(i)
        return canplace

    def get_precantake(self, turn, board, inhand):
        list_precantake = []
        if not self.get_precanplace(-1, board) or inhand[turn]==0:  # 置けないor持ち駒なし -> 盤面から
            for i in range(8,41):
                if board[i]==turn:
                    list_precantake.append(i)
        else:  # -> 持ち駒から
            list_precantake.append(-1)
        return list_precantake

    def get_list_canplace(self, take_pos):
        list_canplace = []
        for eachmove in self.list_all1move:
            if eachmove[0]==take_pos:
                list_canplace.append(eachmove[1])
        return list_canplace

    def judge(self, turn, board):
        win = [False, False, False]
        threerow = [0]*49
        for y in range(1,6):
            for x in range(1,4):
                if board[y*7+x] in (P1,P2) and board[y*7+x]==board[y*7+x+1]==board[y*7+x+2]:
                    win[board[y*7+x]] = True
                    threerow[y*7+x], threerow[y*7+x+1], threerow[y*7+x+2] = 1, 1, 1
        for y in range(1,4):
            for x in range(1,6):
                if board[y*7+x] in (P1,P2) and board[y*7+x]==board[y*7+x+7]==board[y*7+x+14]:
                    win[board[y*7+x]] = True
                    threerow[y*7+x], threerow[y*7+x+7], threerow[y*7+x+14] = 1, 1, 1
        for y in range(2,5):
            for x in range(2,5):
                if board[y*7+x] in (P1,P2) and board[y*7+x]==board[y*7+x-8]==board[y*7+x+8]:
                    win[board[y*7+x]] = True
                    threerow[y*7+x], threerow[y*7+x-8], threerow[y*7+x+8] = 1, 1, 1
                if board[y*7+x] in (P1,P2) and board[y*7+x]==board[y*7+x-6]==board[y*7+x+6]:
                    win[board[y*7+x]] = True
                    threerow[y*7+x], threerow[y*7+x-6], threerow[y*7+x+6] = 1, 1, 1
        if win[turn] and not win[OPP[turn]]:
            return turn
        elif not win[turn] and win[OPP[turn]]:
            return OPP[turn]
        elif win[turn] and win[OPP[turn]]:
            return DRAW
        return NONE

    def get_result(self, turn, board, inhand, take_pos, place_pos):
        new_board = board[:]
        new_inhand = inhand[:]
        if take_pos>=0:
            new_board[take_pos] = 0
        else:
            new_inhand[turn] -= 1
        this_pos = place_pos
        this_piece = turn
        new_board[this_pos] = this_piece
        dir = DIR[place_pos]
        for move_loop in range(5):
            if new_board[this_pos+dir]==0:
                this_piece = new_board[this_pos]
                new_board[this_pos] = 0
                new_board[this_pos+dir] = this_piece
            this_pos += dir
        this_piece = new_board[this_pos]
        new_board[this_pos] = 0
        new_board[WARP[this_pos]] = this_piece
        return new_board, new_inhand, self.judge(turn, new_board)

    def get_2move(self, turn, board, inhand):
        set_cantake = set()
        list_all2move = []
        self.list_all1move = []
        self.list_win = []
        self.list_draw = []
        self.list_loss = []
        self.list_mustwin = []
        self.list_notloss = []
        self.list_mustloss = []
        self.list_other = []
        for take_pos_1 in self.get_precantake(turn, board, inhand):
            for place_pos_1 in self.get_precanplace(take_pos_1, board):
                board_1, inhand_1, winloss_1 = self.get_result(turn, board, inhand, take_pos_1, place_pos_1)
                if winloss_1==NONE:
                    win = True
                    loss = False
                    mustloss = True
                    for take_pos_2 in self.get_precantake(OPP[turn], board_1, inhand_1):
                        for place_pos_2 in self.get_precanplace(take_pos_2, board_1):
                            board_2, inhand_2, winloss_2 = self.get_result(OPP[turn], board_1, inhand_1, take_pos_2, place_pos_2)
                            list_all2move.append([take_pos_1, place_pos_1, winloss_1, take_pos_2, place_pos_2, winloss_2])
                            set_cantake.add(take_pos_1)
                            if winloss_2!=turn:
                                win = False
                            if winloss_2==OPP[turn]:
                                loss = True
                            if winloss_2!=OPP[turn]:
                                mustloss = False
                    if win:
                        self.list_mustwin.append([take_pos_1, place_pos_1, winloss_1])
                        self.list_all1move.append([take_pos_1, place_pos_1, MUSTWIN])
                    elif mustloss:
                        self.list_mustloss.append([take_pos_1, place_pos_1, winloss_1])
                        self.list_all1move.append([take_pos_1, place_pos_1, MUSTLOSS])
                    elif not loss:
                        self.list_notloss.append([take_pos_1, place_pos_1, winloss_1])
                        self.list_all1move.append([take_pos_1, place_pos_1, NOTLOSS])
                    else:
                        self.list_other.append([take_pos_1, place_pos_1, winloss_1])
                        self.list_all1move.append([take_pos_1, place_pos_1, OTHER])
                else:
                    list_all2move.append([take_pos_1, place_pos_1, winloss_1, 0, 0, 0])
                    set_cantake.add(take_pos_1)
                    self.list_all1move.append([take_pos_1, place_pos_1, winloss_1])
                    if winloss_1==turn:
                        self.list_win.append([take_pos_1, place_pos_1, winloss_1])
                    elif winloss_1==OPP[turn]:
                        self.list_loss.append([take_pos_1, place_pos_1, winloss_1])
                    else:
                        self.list_draw.append([take_pos_1, place_pos_1, winloss_1])
        list_cantake = list(set_cantake)
        return list_all2move, list_cantake

    def rnd_select(self, move):
        r = pyxel.rndi(0, len(move)-1)
        return move[r][0], move[r][1]

    def com_move(self, com_level, list_all2move):
        if com_level==MD_COMLV1:
            move = self.list_win + self.list_mustwin + self.list_notloss + self.list_draw + self.list_other + self.list_mustloss
            if move:
                take_pos, place_pos = self.rnd_select(move)
            else:
                take_pos, place_pos = self.rnd_select(self.list_loss)
        elif com_level==MD_COMLV2:
            move1 = self.list_win + self.list_mustwin + self.list_notloss
            move2 = self.list_draw + self.list_other + self.list_mustloss
            if move1:
                take_pos, place_pos = self.rnd_select(move1)
            elif move2:
                take_pos, place_pos = self.rnd_select(move2)
            else:
                take_pos, place_pos = self.rnd_select(self.list_loss)
        elif com_level==MD_COMLV3:
            if self.list_win:
                take_pos, place_pos = self.rnd_select(self.list_win)
            elif self.list_mustwin:
                take_pos, place_pos = self.rnd_select(self.list_mustwin)
            elif self.list_notloss:
                take_pos, place_pos = self.rnd_select(self.list_notloss)
            elif self.list_draw:
                take_pos, place_pos = self.rnd_select(self.list_draw)
            elif self.list_other:
                take_pos, place_pos = self.rnd_select(self.list_other)
            elif self.list_mustloss:
                take_pos, place_pos = self.rnd_select(self.list_mustloss)
            else:
                take_pos, place_pos = self.rnd_select(self.list_loss)
        else:
            take_pos, place_pos = self.rnd_select(list_all2move)
        return take_pos, place_pos

    def preflick(self):
        if self.inhand_pos>=0:
            self.inhand[self.turn] -= 1
        elif self.take_pos>=0:
            self.board[self.take_pos] = 0
        self.this_pos = self.place_pos
        self.board[self.this_pos] = self.turn
        self.dir = DIR[self.place_pos]
        self.move_loop = 0
        self.move_count = 0
        self.this_piece = self.turn
        pyxel.play(0, [1])

    def update(self):
        self.holddown()

        if self.wait>0:
            self.wait -= 1
            return

        if self.st==ST_TITLE:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_BUTTON_UP
                if INHAND_X1<=pyxel.mouse_x<INHAND_X1+INHAND_WIDTH and INHAND_Y1+1<=pyxel.mouse_y<INHAND_Y1+INHAND_HEIGHT:
                    self.vsmode += 1
                    if self.vsmode>MD_COMLV3:
                        self.vsmode = MD_MAN
                elif INHAND_X2<=pyxel.mouse_x<INHAND_X2+INHAND_WIDTH and INHAND_Y2+1<=pyxel.mouse_y<INHAND_Y2+INHAND_HEIGHT:
                    self.preset_loop = 0
                    self.st = ST_START

        if self.st==ST_START:
            # -------- DEBUG
            #self.turn = P2
            #self.inhand = [0,0,0]
            #self.board = [0,0,0,0,0,0,0, 0,0,0,0,2,1,0, 0,1,1,0,0,0,0, 0,0,2,0,1,0,0, 0,0,2,1,0,2,0, 0,0,0,0,0,2,0, 0,0,0,0,0,0,0]
            #self.win = [False, False, False]
            #self.hist_move = []
            #self.st = ST_COMPUTE
            #return
            # --------
            if self.preset_loop==0:
                self.turn = pyxel.rndi(P1, P2)
                self.inhand = [0,5,5]
                self.board = [0]*49
                self.win = [False, False, False]
                self.preset_loop = 1
                self.preset_count = 0
                self.this_piece = self.turn
                self.this_pos = -1
            else:
                if self.preset_count==0:
                    while True:
                        self.this_pos = pyxel.rndi(1,5)*7+pyxel.rndi(1,5)
                        if self.board[self.this_pos]==0:
                            break
                    self.inhand[self.turn] -= 1
                    self.preset_count = 1
                elif self.preset_count>=9:
                    self.board[self.this_pos] = self.this_piece
                    self.turn = OPP[self.turn]
                    self.this_piece = self.turn
                    self.this_pos = -1
                    self.preset_count = 0
                    self.preset_loop += 1
                    if self.preset_loop>3:
                        self.hist_move = []
                        self.st = ST_COMPUTE
                else:
                    self.preset_count += 1

        if self.st==ST_COMPUTE:
            list_all2move, self.list_cantake = self.get_2move(self.turn, self.board, self.inhand)
            if self.vsmode in (MD_COMLV1, MD_COMLV2, MD_COMLV3) and self.turn==P1:
                self.take_pos, self.place_pos = self.com_move(self.vsmode, list_all2move)
                self.wait = 20
            self.st = ST_TAKE

        elif self.st==ST_TAKE:
            if self.vsmode in (MD_COMLV1, MD_COMLV2, MD_COMLV3) and self.turn==P1:
                if self.take_pos>=0:
                    self.inhand_pos = -1
                else:
                    self.inhand_pos = self.inhand[self.turn]-1
                self.list_canplace = self.get_list_canplace(self.take_pos)
                self.wait = 20
                pyxel.play(0, [0])
                self.st = ST_PLACE
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_UP
                take_x = (pyxel.mouse_x-BOARD_X)//20
                take_y = (pyxel.mouse_y-BOARD_Y)//20
                if self.turn==P1:
                    inhand_x = (pyxel.mouse_x-2-INHAND_X1)//18
                    inhand_y = (pyxel.mouse_y-INHAND_Y1)//20
                else:
                    inhand_x = (pyxel.mouse_x-2-INHAND_X2)//18
                    inhand_y = (pyxel.mouse_y-INHAND_Y2)//20
                self.take_pos = -1
                if 1<=take_x<6 and 1<=take_y<6:
                    self.take_pos = take_y*7+take_x
                    if not self.take_pos in self.list_cantake:
                        self.take_pos = -1
                self.inhand_pos = -1
                if 0<=inhand_x<self.inhand[self.turn] and inhand_y==0 and -1 in self.list_cantake:
                    self.inhand_pos = inhand_x
                if not (self.take_pos==-1 and self.inhand_pos==-1):
                    self.list_canplace = self.get_list_canplace(self.take_pos)
                    pyxel.play(0, [0])
                    self.st = ST_PLACE

        elif self.st==ST_PLACE:
            if self.vsmode in (MD_COMLV1, MD_COMLV2, MD_COMLV3) and self.turn==P1:
                self.preflick()
                self.st = ST_FLICK
            elif pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_UP
                place_x = (pyxel.mouse_x-BOARD_X)//20
                place_y = (pyxel.mouse_y-BOARD_Y)//20
                if 1<=place_x<6 and 1<=place_y<6:
                    self.place_pos = place_y*7+place_x
                    if self.place_pos in self.list_canplace:
                        self.preflick()
                        self.st = ST_FLICK
                    else:
                        pyxel.play(0, [2])
                        self.st = ST_TAKE
                else:
                    pyxel.play(0, [2])
                    self.st = ST_TAKE

        elif self.st==ST_FLICK:
            if self.move_loop==5:
                if self.move_count==0:
                    self.this_piece = self.board[self.this_pos]
                    self.board[self.this_pos] = 0
                    self.this_pos = WARP[self.this_pos]
                elif self.move_count>=9:
                    self.board[self.this_pos] = self.this_piece
                    pyxel.stop(0)
                    self.st = ST_JUDGE
                self.move_count += 1
            else:
                if self.move_count==0:
                    if self.board[self.this_pos+self.dir]==0:
                        self.this_piece = self.board[self.this_pos]
                        self.board[self.this_pos] = 0
                        self.move_count = 5-self.move_loop//2
                    else:
                        pyxel.play(0, [1])
                        self.this_pos += self.dir
                        self.this_piece = self.board[self.this_pos]
                        self.move_loop += 1    
                elif self.move_count>19:
                    self.this_pos += self.dir
                    self.board[self.this_pos] = self.this_piece
                    self.move_count = 0
                    self.move_loop += 1
                else:
                    self.move_count += 5-self.move_loop//2

        elif self.st==ST_JUDGE:
            self.win = [False, False, False]
            self.same_pos = self.append_hist_move()
            if self.same_pos>3:
                self.win = [True, True, True]
            self.threerow = [0]*49
            for y in range(1,6):
                for x in range(1,4):
                    if self.board[y*7+x] in (P1,P2) and self.board[y*7+x]==self.board[y*7+x+1]==self.board[y*7+x+2]:
                        self.win[self.board[y*7+x]] = True
                        self.threerow[y*7+x], self.threerow[y*7+x+1], self.threerow[y*7+x+2] = 1, 1, 1
            for y in range(1,4):
                for x in range(1,6):
                    if self.board[y*7+x] in (P1,P2) and self.board[y*7+x]==self.board[y*7+x+7]==self.board[y*7+x+14]:
                        self.win[self.board[y*7+x]] = True
                        self.threerow[y*7+x], self.threerow[y*7+x+7], self.threerow[y*7+x+14] = 1, 1, 1
            for y in range(2,5):
                for x in range(2,5):
                    if self.board[y*7+x] in (P1,P2) and self.board[y*7+x]==self.board[y*7+x-8]==self.board[y*7+x+8]:
                        self.win[self.board[y*7+x]] = True
                        self.threerow[y*7+x], self.threerow[y*7+x-8], self.threerow[y*7+x+8] = 1, 1, 1
                    if self.board[y*7+x] in (P1,P2) and self.board[y*7+x]==self.board[y*7+x-6]==self.board[y*7+x+6]:
                        self.win[self.board[y*7+x]] = True
                        self.threerow[y*7+x], self.threerow[y*7+x-6], self.threerow[y*7+x+6] = 1, 1, 1
            if self.win[P1] or self.win[P2]:
                self.st = ST_END
            else:
                self.turn = OPP[self.turn]
                self.st = ST_COMPUTE
        
        elif self.st==ST_END:
            if pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT):  # LEFT_UP
                if self.vsmode in (MD_COMLV1, MD_COMLV2) and self.win[P2] and not self.win[P1]:
                    self.vsmode += 1
                self.st=ST_TITLE

    def predraw_placepos(self, draw_pos, turn, take_pos):
        if draw_pos in self.list_canplace:
            for e in self.list_all1move:
                if e[0]==take_pos and e[1]==draw_pos:
                    if self.debug:  # DEBUG
                        c = 11 if e[2]==turn else 3 if e[2]==MUSTWIN else 10 if e[2]==NOTLOSS else 7 if e[2]==DRAW else 4 if e[2]==OTHER else 2 if e[2]==MUSTLOSS else 8
                    else:
                        c = 10
                    break
            return c
        return -1

    def draw_board(self):
        pyxel.rect(BOARD_X+20, BOARD_Y+20, 20*5, 20*5, 1)
        for i in range(1,7):
            pyxel.line(BOARD_X+20, BOARD_Y+i*20, BOARD_X+6*20, BOARD_Y+i*20, 0)
            pyxel.line(BOARD_X+i*20, BOARD_Y+20, BOARD_X+i*20, BOARD_Y+6*20, 0)
    
    def draw_menu(self):
        pyxel.text(INHAND_X1+12, INHAND_Y1+9, VSMODE_TXT[self.vsmode], 1)
        pyxel.text(INHAND_X1+11, INHAND_Y1+8, VSMODE_TXT[self.vsmode], 10)
        pyxel.text(INHAND_X2+24, INHAND_Y2+9, 'Click to START', 1)
        pyxel.text(INHAND_X2+23, INHAND_Y2+8, 'Click to START', 10)

    def draw_piece(self):
        for y in range(1,6):
            for x in range(1,6):
                # pyxel.text(BOARD_X+3+x*20, BOARD_Y+3+y*20, f'{y*7+x}', 0)  # DEBUG
                p = self.board[y*7+x]
                if p==P1 or p==P2:
                    if not (p==self.turn and self.st==ST_PLACE and y*7+x==self.take_pos):  # 取った位置以外に円を表示(P1,P2)
                        pyxel.blt(BOARD_X+3+x*20, BOARD_Y+3+y*20, 0, 0, p*16, 16, 16, 1)
                    if p==self.turn:
                        if self.st==ST_TAKE and y*7+x in self.list_cantake:
                            pyxel.circb(BOARD_X+10+x*20, BOARD_Y+10+y*20, 8, 10)  # 取れる位置に円を表示(Turn)
                        elif self.st==ST_PLACE and y*7+x==self.take_pos:
                            pyxel.circb(BOARD_X+10+x*20, BOARD_Y+10+y*20, 7, 10)  # 取った位置に円を表示(Turn)
                    if self.win[P1] or self.win[P2]:
                        if self.threerow[y*7+x]:
                            pyxel.circb(BOARD_X+10+x*20, BOARD_Y+10+y*20, 8, 7 if pyxel.frame_count//8%2 else 8)  # ３つ並んだ位置に円を表示
                if self.st==ST_TAKE and self.debug:  # DEBUG
                    for win in self.list_win:
                        if win[0]==y*7+x:
                            pyxel.circ(BOARD_X+2+x*20, BOARD_Y+19+y*20, 1, 11)
                    for mustwin in self.list_mustwin:
                        if mustwin[0]==y*7+x:
                            pyxel.circ(BOARD_X+5+x*20, BOARD_Y+19+y*20, 1, 3)
                    for notloss in self.list_notloss:
                        if notloss[0]==y*7+x:
                            pyxel.circ(BOARD_X+8+x*20, BOARD_Y+19+y*20, 1, 10)
                    for draw in self.list_draw:
                        if draw[0]==y*7+x:
                            pyxel.circ(BOARD_X+11+x*20, BOARD_Y+19+y*20, 1, 7)
                    for other in self.list_other:
                        if other[0]==y*7+x:
                            pyxel.circ(BOARD_X+14+x*20, BOARD_Y+19+y*20, 1, 4)
                    for mustloss in self.list_mustloss:
                        if mustloss[0]==y*7+x:
                            pyxel.circ(BOARD_X+17+x*20, BOARD_Y+19+y*20, 1, 2)
                    for loss in self.list_loss:
                        if loss[0]==y*7+x:
                            pyxel.circ(BOARD_X+20+x*20, BOARD_Y+19+y*20, 1, 8)

        if self.st==ST_START and self.preset_loop>0:
            this_x = self.this_pos%7
            this_y = self.this_pos//7
            pyxel.blt(BOARD_X+3+this_x*20, BOARD_Y+3+this_y*20, 0, (self.preset_count//2+1)*16, self.this_piece*16, 16, 16, 1)
        elif self.st==ST_FLICK:
            this_x = self.this_pos%7
            this_y = self.this_pos//7
            this_dx = (self.dir+1)%7-1
            this_dy = (self.dir+1)//7
            if self.move_loop==5:
                pyxel.blt(BOARD_X+3+this_x*20, BOARD_Y+3+this_y*20, 0, (self.move_count//2+1)*16, self.this_piece*16, 16, 16, 1)
            else:
                pyxel.blt(BOARD_X+3+this_x*20+this_dx*self.move_count, BOARD_Y+3+this_y*20+this_dy*self.move_count, 0, 0, self.this_piece*16, 16, 16, 1)

    def draw_canplace(self):
        for i in range(2,5):
            c = self.predraw_placepos(i*7+1, self.turn, self.take_pos)  # 左
            if (c>=0):
                pyxel.tri(BOARD_X+20+8, BOARD_Y+i*20+8, BOARD_X+20+8, BOARD_Y+i*20+12, BOARD_X+20+15, BOARD_Y+i*20+10, c)
            c = self.predraw_placepos(i*7+5, self.turn, self.take_pos)  # 右
            if (c>=0):
                pyxel.tri(BOARD_X+5*20+13, BOARD_Y+i*20+8, BOARD_X+5*20+13, BOARD_Y+i*20+12, BOARD_X+5*20+6, BOARD_Y+i*20+10, c)
            c = self.predraw_placepos(1*7+i, self.turn, self.take_pos)  # 上
            if (c>=0):
                pyxel.tri(BOARD_X+i*20+8, BOARD_Y+20+8, BOARD_X+i*20+12, BOARD_Y+20+8, BOARD_X+i*20+10, BOARD_Y+20+15, c)
            c = self.predraw_placepos(5*7+i, self.turn, self.take_pos)  # 下
            if (c>=0):
                pyxel.tri(BOARD_X+i*20+8, BOARD_Y+5*20+13, BOARD_X+i*20+12, BOARD_Y+5*20+13, BOARD_X+i*20+10, BOARD_Y+5*20+6, c)
        c = self.predraw_placepos(1*7+1, self.turn, self.take_pos)  # 左上
        if (c>=0):
            pyxel.tri(BOARD_X+20+11, BOARD_Y+20+8, BOARD_X+20+8, BOARD_Y+20+11, BOARD_X+20+15, BOARD_Y+20+15, c)
        c = self.predraw_placepos(1*7+5, self.turn, self.take_pos)  # 右上
        if (c>=0):
            pyxel.tri(BOARD_X+5*20+11, BOARD_Y+20+8, BOARD_X+5*20+14, BOARD_Y+20+11, BOARD_X+5*20+7, BOARD_Y+20+15, c)
        c = self.predraw_placepos(5*7+1, self.turn, self.take_pos)  # 左下
        if (c>=0):
            pyxel.tri(BOARD_X+20+11, BOARD_Y+5*20+14, BOARD_X+20+8, BOARD_Y+5*20+11, BOARD_X+20+15, BOARD_Y+5*20+7, c)
        c = self.predraw_placepos(5*7+5, self.turn, self.take_pos)  # 右下
        if (c>=0):
            pyxel.tri(BOARD_X+5*20+11, BOARD_Y+5*20+14, BOARD_X+5*20+14, BOARD_Y+5*20+11, BOARD_X+5*20+7, BOARD_Y+5*20+7, c)

    def draw_turn(self):
        if self.turn==P1:
            pyxel.rectb(INHAND_X1, INHAND_Y1, INHAND_WIDTH, INHAND_HEIGHT, 6)
            pyxel.text(INHAND_X1+80, INHAND_Y1+9, 'Turn', 1)
            pyxel.text(INHAND_X1+79, INHAND_Y1+8, 'Turn', 10)
        else:
            pyxel.rectb(INHAND_X2, INHAND_Y2, INHAND_WIDTH, INHAND_HEIGHT, 14)
            pyxel.text(INHAND_X2+80, INHAND_Y2+9, 'Turn', 1)
            pyxel.text(INHAND_X2+79, INHAND_Y2+8, 'Turn', 10)

    def draw_inhand(self):
        pyxel.rect(INHAND_X1, INHAND_Y1, INHAND_WIDTH, INHAND_HEIGHT, 0)
        for i in range(self.inhand[P1]):
            if not (self.st==ST_PLACE and self.turn==P1 and i==self.inhand_pos):
                pyxel.blt(INHAND_X1+3+i*18, INHAND_Y1+3, 0, 0, P1*16, 16, 16, 1)
            if self.st==ST_TAKE and self.turn==P1 and -1 in self.list_cantake:
                pyxel.circb(INHAND_X1+10+i*18, INHAND_Y1+10, 8, 10)
            elif self.st==ST_PLACE and self.turn==P1 and i==self.inhand_pos:
                pyxel.circb(INHAND_X1+10+i*18, INHAND_Y1+10, 7, 10)
        pyxel.rect(INHAND_X2, INHAND_Y2, INHAND_WIDTH, INHAND_HEIGHT, 0)
        for i in range(self.inhand[P2]):
            if not (self.st==ST_PLACE and self.turn==P2 and i==self.inhand_pos):
                pyxel.blt(INHAND_X2+3+i*18, INHAND_Y2+3, 0, 0, P2*16, 16, 16, 1)
            if self.st==ST_TAKE and self.turn==P2 and -1 in self.list_cantake:
                pyxel.circb(INHAND_X2+10+i*18, INHAND_Y2+10, 8, 10)
            elif self.st==ST_PLACE and self.turn==P2 and i==self.inhand_pos:
                pyxel.circb(INHAND_X2+10+i*18, INHAND_Y2+10, 7, 10)
    
    def draw_win(self):
        if self.win[P1] and self.win[P2]:
            if self.win[0]:
                pyxel.rectb(INHAND_X1, INHAND_Y1, INHAND_WIDTH, INHAND_HEIGHT, 6)
                pyxel.text(INHAND_X1+21, INHAND_Y1+8, 'Repetition Draw', 7 if pyxel.frame_count//8%2 else 8)
                pyxel.rectb(INHAND_X2, INHAND_Y2, INHAND_WIDTH, INHAND_HEIGHT, 14)
                pyxel.text(INHAND_X2+21, INHAND_Y2+8, 'Repetition Draw', 7 if pyxel.frame_count//8%2 else 8)
            else:
                pyxel.rectb(INHAND_X1, INHAND_Y1, INHAND_WIDTH, INHAND_HEIGHT, 6)
                pyxel.text(INHAND_X1+43, INHAND_Y1+8, 'Draw', 7 if pyxel.frame_count//8%2 else 8)
                pyxel.rectb(INHAND_X2, INHAND_Y2, INHAND_WIDTH, INHAND_HEIGHT, 14)
                pyxel.text(INHAND_X2+43, INHAND_Y2+8, 'Draw', 7 if pyxel.frame_count//8%2 else 8)
        elif self.win[P1]:
            pyxel.rectb(INHAND_X1, INHAND_Y1, INHAND_WIDTH, INHAND_HEIGHT, 6)
            pyxel.text(INHAND_X1+45, INHAND_Y1+8, 'Win', 7 if pyxel.frame_count//8%2 else 8)
        elif self.win[P2]:
            pyxel.rectb(INHAND_X2, INHAND_Y2, INHAND_WIDTH, INHAND_HEIGHT, 14)
            pyxel.text(INHAND_X2+45, INHAND_Y2+8, 'Win', 7 if pyxel.frame_count//8%2 else 8)

    def draw_same_pos(self):
        if self.same_pos==3:
            if self.turn==P1:
                pyxel.text(INHAND_X2+10, INHAND_Y2+9, '3 times same position', 1)
                pyxel.text(INHAND_X2+9 , INHAND_Y2+8, '3 times same position', 10)
            else:
                pyxel.text(INHAND_X1+10, INHAND_Y1+9, '3 times same position', 1)
                pyxel.text(INHAND_X1+9 , INHAND_Y1+8, '3 times same position', 10)

    def draw_debug(self):
        if self.debug:
            pyxel.text(INHAND_X1+INHAND_WIDTH-20, INHAND_Y1+1, 'DEBUG', 1)

    def draw(self):
        pyxel.cls(3)
        self.draw_board()
        self.draw_piece()
        self.draw_inhand()
        if self.st==ST_PLACE:
            self.draw_canplace()
        if self.st==ST_TITLE:
            self.draw_menu()
        elif self.st==ST_START:
            pass
        elif self.st==ST_END:
            self.draw_win()
        else:
            self.draw_turn()
            self.draw_same_pos()
        self.draw_debug()
        
App()
