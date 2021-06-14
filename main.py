import turtle
import random, time

import os
import gtts, pyttsx3
import playsound
import hashlib
import re
import sys
import random


def terbilang( val):
    # terbilang: mengubah bilangan menjadi rangkaian kata

    if type(val) != type('123'):
        val = str(val)

    # master
    digit = ['nol', 'satu', 'dua', 'tiga', 'empat', 'lima', \
            'enam', 'tujuh', 'delapan', 'sembilan']
    unit1 = ['ratus', 'puluh', '']
    unit3 = ['', 'ribu', 'juta', 'miliar', 'triliun']

    # hanya menerima digit 0-9
    if not val.isnumeric() or len(val) > 3*len(unit3):
        print('Parameter harus berisi angka dg panjang ' \
                +'maks {} digit'.format( 3*len(unit3)))
        sys.exit(1)

    # init empty return value
    retval = []

    for i3 in range(len(unit3)):

        # potong dan proses 3 angka terakhir
        val2 = val[-3:].zfill(3)
        val = val[:-3]
        # siapkan penampungan
        t = []
        for i in range(3):
            if val2[i] != '0':
                t.append(digit[int(val2[i])])
                if unit1[i]: t.append(unit1[i])

        if unit3[i3]: t.append(unit3[i3]+',')
        ts = ' '.join(t)

        # ganti terminologi dengan yang baku
        ts = re.sub('^satu ribu', 'seribu', ts)
        ts = re.sub('^satu ratus', 'seratus', ts)
        ts = re.sub('satu puluh', 'sepuluh', ts)
        ts = re.sub('sepuluh satu', 'sebelas', ts)
        for i in range(2, 10):
            ts = re.sub('sepuluh '+digit[i], digit[i]+' belas', ts)

        # sisip di depan
        retval.insert(0, ts)
        if val == '':
            break

    return ' '.join(retval) if retval[0] else 'nol'


# text to speech using pyttsx3 or gTTS
class Speech: #threading.Thread):

    die = False
    busy = False
    mute = False
    debug = True

    def __init__(self):
        # init tts
        self.tts = pyttsx3.init()
        self.tts.setProperty('voice', 'indonesian')
        #self.gtts = gtts.gTTS()

    def set_mute(self, isMute=True):
        self.__class__.mute = isMute

    def set_busy(self, isBusy=True):
        self.__class__.busy = isBusy

    def bilangan(self, num, using_gtts=True):
        if num==' ':
            self.say('kosong')
        else:
            numText = terbilang(num).split()
            for t in numText:
                self.say(t)

    def say(self, txt, using_gtts=True):

        if not self.busy:
            if self.mute and self.debug:
                print('SPEECH>> ', txt)

            else:
                self.set_busy()

                if using_gtts:
                    sfname = hashlib.sha1(txt.encode()).hexdigest()
                    sfname = 'speech/{}.mp3'.format(sfname)
                    if not os.path.exists(sfname):
                        try:
                            speech = gtts.gTTS(txt, lang='id')
                            speech.save(sfname)
                        except:
                            os.unlink(sfname)
                            self.tts.say(txt)
                        else:
                            playsound.playsound(sfname)
                    else:
                        playsound.playsound(sfname)
                else:
                    self.tts.say(txt)
                    self.tts.runAndWait()

                self.set_busy(False)


#turtle.forward(100)
class CharPlot(turtle.Turtle):

    charMap = {}
    charMap['0'] = [(0,4),(0,0),(2,0),(2,4),(0,4)]
    charMap['1'] = [(1,4),(1,0)]
    charMap['2'] = [(0,4),(2,4),(2,3),(0,0),(2,0)]
    charMap['3'] = [(0,4),(1.5,4),(1.5,2),(0,2),(2,2),(2,0),(0,0)]
    charMap['4'] = [(0.5,4),(0,2),(2,2),(2,4),(2,0)]
    charMap['5'] = [(0.5,4),(0,2),(2,2),(2,0),(0,0),(-1,-1),(0.5,4),(2,4)]
    charMap['6'] = [(2,4),(0,2),(0,0),(2,0),(2,2),(0,2)]
    charMap['7'] = [(0,4),(2,4),(0,0),(-1,-1),(0,2),(2,2)]
    charMap['8'] = [(0.5,4),(0.5,2.5),(2,2),(2,0),(0,0),(0,2),(1.5,2.5),(1.5,4),(0.5,4)]
    charMap['9'] = [(2,4),(0.5,4),(0.5,2),(2,2),(2,4),(2,0),(0,0)]
    charMap['x'] = [(0,3),(2,1),(-1,-1),(2,3),(0,1)]
    charMap['+'] = [(0,2),(2,2),(-1,-1),(1,3),(1,1)]
    charMap['-'] = [(0,2),(2,2)]
    charMap[':'] = [(1,3),(1,3),(-1,-1),(1,1),(1,1)]
    charMap['='] = [(0,3),(2,3),(-1,-1),(0,1),(2,1)]
    charMap['^'] = [(0,2),(3,2)]
    charMap['_'] = [(0,0),(2,0)]
    charMap[' '] = [(0,0),(-1,-1)]

    charScaleX = 10
    charScaleY = 10

    basePos= (0,0)
    oriX0, oriY0 = (0, 0)

    charPenSize = 4

    charPenColor = {'figure':'blue', 'op':'red'}

    def __init__(self):
        super(CharPlot,self).__init__()
        self.set_home()
        self.shape('circle')
        self.set_char_pensize()

    def set_char_pensize(self):
        self.charPenSize = 0.6 * max(self.charScaleX, self.charScaleY)
        self.shapesize(self.charPenSize/16)
        self.pensize(self.charPenSize)

    def set_char_scale(self, scale):
        self.charScaleX = self.charScaleY = scale
        self.set_char_pensize()

    def set_char_dim(self, w, h):
        self.charScaleX = w/4
        self.charScaleY = h/5
        self.set_char_pensize()

    def set_home(self):
        w, h = turtle.screensize()
        midW = w//2
        midH = h//2
        self.oriX0 = -midW
        self.oriY0 = midH
        turtle.penup()
        #print('screensize', turtle.screensize())
        #print('set_home', self.oriX0, self.oriY0)

    def char_goto(self, pos):
        x, y = pos
        x1 = self.oriX0 + x
        y1 = self.oriY0 - y
        self.penup()
        self.goto(x1, y1)
        #print('turtle goto', x1, y1)

    def char_position(self):
        x, y = self.position()
        x1 = x - self.oriX0
        y1 = y + self.oriY0
        return x1, y1

    def set_base_pos(self, pos=None):
        if pos == None:
            self.basePos = self.position()
        else:
            self.basePos = pos
        #print('basePos', self.basePos)

    def coord_transform(self, coord):
        x, y = coord
        newX = self.basePos[0] + x * self.charScaleX
        newY = self.basePos[1] + y * self.charScaleY
        return newX, newY

    def plot(self, n):
        '''plot character based on charMap'''
        map = self.charMap.get(n,None)
        if map:
            # next position is based on current possition
            turtle.penup()
            if n in '01234567890_':self.pencolor(self.charPenColor['figure'])
            else: self.pencolor(self.charPenColor['op'])
            self.set_base_pos()
            # plot character based on map scallable
            for p in map:
                if (p[0]<0):
                    self.penup()
                    continue
                self.goto(self.coord_transform(p))
                self.down()
            # ready on next base position
            self.penup()
            self.shape('classic')
            self.goto(self.coord_transform([3.5,0]))
        else:
            print('mapplot', n, 'tidak tersedia')


    def plot_string(self, txt, cr=False):
        '''plot txt string based on charMap'''
        if type(txt) != type('abc'):
            txt = str(txt)

        cur_pos = self.position()
        self.shape('circle')
        self.set_char_pensize()
        for t in txt:
            self.plot(t)
        if cr:
            self.goto(cur_pos[0],cur_pos[1]-6*self.charScaleY)
            #self.set_base_pos(cur_pos[0],cur_pos[1]-self.charScaleY)


if __name__ == '__main__':

    Speech().set_mute(False)

    myplot = CharPlot()
    #myplot.set_char_dim(100, 150)
    myplot.set_char_scale(7)

    layer1 = CharPlot()
    layer1.pensize(1)
    layer1.set_char_scale(5)
    layer1.pencolor('red')

    layer_simpan = CharPlot()
    layer_simpan.set_home()
    layer_simpan.set_char_scale(5)

    #time.sleep(20)
    # prepare frame
    
    frame = []
    for r in range(7):
        rTrans = 70 - r*42 
        row = []
        for c in range(5):
            cTrans = -120 + c*25
            pos = (cTrans, rTrans)
            row.append(pos)
            #if r>0:
            #    prepos = frame[r-1][c]
            #    layer1.goto(prepos)
            #layer1.goto(pos)
        frame.append(row)

    #turtle.screensize(canvwidth=600, canvheight=400)
    myplot.clear()
    myplot.home()

    #turtle.goto(-200, 150)

    myplot.char_goto((0, 0))
    style = ('Courier', 20, 'italic')
    myplot.write('Soal perkalian', font=style)

    Speech().say('perhatikan soal perkalian '+ \
        'dua buah bilangan berikut ini')

    myplot.char_goto((0, 40))

    x1 = random.randint(11,999)
    myplot.plot_string(x1)
    Speech().bilangan(x1)

    op = 'x'
    myplot.plot_string(op)
    Speech().say('dikali')

    x2 = random.randint(1,99)
    myplot.plot_string(x2)
    Speech().bilangan(x2)

    eq = '= ____'
    myplot.plot_string(eq, True)
    Speech().say('sama dengan berapa?')


    print('x1', x1, 'x2',x2)

    #myplot.plot_string('{}{}{}{}{}'.format(x1,op,x2,eq,'___'),True)

    # print secara menurun
    time.sleep(2)

    Speech().say('untuk mempermudah penyelesaian, '+ \
        'persamaan tersebut dituliskan susun ke bawah '+\
        'rata kanan seperti berikut ini')

    # rata kanan
    layer1.penup()
    layer1.goto((frame[0][4][0]+10,frame[0][4][1]))
    layer1.pendown()
    layer1.goto((frame[2][4][0]+10,frame[2][4][1]))

    myplot.char_goto((0, 100))
    Speech().say('baris pertama')
    myplot.plot_string(str(x1).rjust(8), True)

    Speech().say('baris kedua')
    myplot.plot_string(str(x2).rjust(8), True)

    myplot.plot_string('^^^^^ x'.rjust(10), True)
    layer1.clear()

    def draw_line( a, b):
        layer1.penup()
        layer1.goto(a)
        layer1.pendown()
        layer1.goto(b)

    # 
    jawab = {}
    for r,q in enumerate(str(x2)[::-1]):
        jawab[r] = []
        if r==1:
            jawab[r].append(' ')
            
        hasil_simpan = 0

        layer1.penup()
        layer1.goto((frame[1][4-r][0],frame[1][4-r][1]-28))
        layer1.pendown()
        layer1.circle(20)

        Speech().say('perhatikan angka')
        Speech().bilangan(q)
        Speech().say('pada baris ke dua.')
        Speech().say('setiap angka pada bilangan baris pertama '+\
            'satu persatu akan dikalikan dengan angka tersebut')
                
        #layer1.clear()

        for c,p in enumerate(str(x1)[::-1]):

            #perkalian
            draw_line(frame[0][4-c], frame[1][4-r])

            layer1.penup()
            layer1.goto((frame[3][4][0]+100, frame[3][4][1]))

            Speech().say('selanjutnya kalikan')
            Speech().bilangan(p)
            Speech().say('dengan')
            Speech().bilangan(q)

            layer1.plot_string('{}x{}='.format(p,q))


            hasil = int(p)*int(q)
            layer1.plot_string(hasil,True)
            Speech().say('hasilnya adalah')
            Speech().bilangan(hasil)
         
            if hasil_simpan:
                layer1.plot_string('{}+'.format(hasil))
                hasil += hasil_simpan
                Speech().say('ditambah lagi angka simpanan sebelumya')

                Speech().bilangan(hasil_simpan)
                layer1.plot_string('{}='.format(hasil_simpan))
                layer_simpan.clear()

                Speech().say('sehingga menjadi')
                layer1.plot_string('{}'.format(hasil))
                Speech().bilangan(hasil)

            hasil_cetak = hasil % 10
            hasil_simpan = hasil // 10            
            if r==0:
                myplot.goto(frame[r+3][4-c])
            else:
                myplot.goto(frame[r+3][3-c])

            if hasil_simpan:
                Speech().say('angka satuan')
                Speech().bilangan(hasil_cetak)

            else:
                Speech().say('bilangan tersebut')

            myplot.plot_string(hasil_cetak)

            if r==1 and c==0:
                Speech().say('dituliskan menjorok 1 digit disini')
            else:
                Speech().say('dituliskan disini')

            jawab[r].append(str(hasil_cetak))

            # simpan
            if c+1 >= len(str(x1)):
                if hasil_simpan:
                    if r==0:
                        myplot.goto(frame[r+3][3-c])
                    else:
                        myplot.goto(frame[r+3][2-c])

                    Speech().say('karena sudah tidak ada angka '+\
                        'yang akan dikalikan lagi pada baris pertama, '+\
                        'angka puluhannya tidak perlu disimpan')

                    myplot.plot_string(hasil_simpan)
                    Speech().bilangan(hasil_simpan)
                    Speech().say('ditulis disini')

                    jawab[r].append(str(hasil_simpan))
                    layer_simpan.clear()
            else:
                layer_simpan.clear()
                if hasil_simpan:
                    Speech().say('angka puluhannya yaitu')
                    layer_simpan.penup()
                    layer_simpan.goto((frame[1][4][0]+100, frame[1][4][1]))
                    layer_simpan.plot_string(hasil_simpan)
                    Speech().bilangan(hasil_simpan)
                    Speech().say('disimpan dulu disini')

            time.sleep(3)
            layer1.clear()
            layer1.pencolor('red')
            time.sleep(2)

    if x2 > 9:
        hasil_akhir = []

        print('mulai dijumlah')
        myplot.goto(frame[5][0])
        myplot.plot_string('^^^^^ +', True)
        Speech().say('dibuat garis, dan mulai dijumlahkan')

        hasil_simpan = 0
        lenJawab = max(len(jawab[0]),len(jawab[1]))
        for i in range(lenJawab):
            if i >= len(jawab[0]):
                jawab[0].append(' ')
            if i >= len(jawab[1]):
                jawab[0].append(' ')

            x1 = jawab[0][i]
            x2 = jawab[1][i]

            nx1 = 0 if x1==' ' else int(x1)
            nx2 = 0 if x2==' ' else int(x2)

            layer1.penup()
            layer1.goto(frame[2][4-i])
            layer1.pendown()
            layer1.goto(frame[5][4-i])

            Speech().say('jumlahkan')
            Speech().bilangan(x1)
            Speech().say('dengan')
            Speech().bilangan(x2)

            hasil = nx1 + nx2
            Speech().say('hasilnya')
            Speech().bilangan(hasil)

            if hasil_simpan:
                hasil += hasil_simpan
                Speech().say('ditambah simpanan')
                Speech().bilangan(hasil_simpan)
                Speech().say('menjadi')
                Speech().bilangan(hasil)

            hasil_cetak = hasil % 10
            hasil_simpan = hasil // 10

            if hasil_simpan:
                Speech().say('angka satuannya')
                Speech().bilangan(hasil_cetak)

            myplot.goto(frame[6][4-i])
            myplot.plot_string(hasil_cetak)
            Speech().say('dituliskan disini')

            
            hasil_akhir.append(hasil_cetak)

            if hasil_simpan:
                Speech().say('dan angka puluhannya disimpan disini')
                myplot.goto(frame[5][3-i])
                myplot.plot_string(hasil_simpan)
                
            layer1.clear()

    else:
        hasil_akhir = jawab[0]


    hasil_akhir.reverse()
    hasil_akhir=''.join(list(map(str,hasil_akhir)))
    
    print('hasil_akhir', hasil_akhir)

    Speech().say('hasil akhir adalah')
    Speech().bilangan(hasil_akhir)

    print('Selesai...')
    input()

