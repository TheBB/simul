#!/usr/bin/python3

import subprocess

class Struct:
    pass

class Image:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._texts = []
        self._rectangles = []

    def add_text(self, text, left, top, left_align=True):
        fname = 'imgur/temp/' + str(len(self._texts)) + '.png'

        args = ['convert']
        args += ['-size', '200x30']
        args += ['xc:transparent']
        args += ['-draw', 'text 0,20 \'' + text + '\'']
        args += [fname]
        subprocess.call(args)

        args = ['convert']
        args += ['-trim', fname, fname]
        subprocess.call(args)

        args = ['identify', fname]
        s = subprocess.check_output(args).decode().split(' ')
        s = [int(x) for x in s[2].split('x')]

        struct = Struct()
        struct.top = top
        if left_align:
            struct.left = left
        else:
            struct.left = left - s[0]
        struct.width = s[0]
        struct.height = s[1]
        struct.fname = fname

        self._texts.append(struct)

    def add_rectangle(self, left, top, right, bottom, fill, stroke=(0,0,0)):
        struct = Struct()
        struct.top = top
        struct.left = left
        struct.right = right
        struct.bottom = bottom
        struct.fill = fill
        struct.stroke = stroke
        self._rectangles.append(struct)

    def make(self, fname):
        args = ['convert']
        args += ['-size', str(self.width) + 'x' + str(self.height)]
        args += ['xc:transparent']

        for text in self._texts:
            args += ['-draw']
            args += ['image over ' + str(text.left) + ',' + str(text.top) +\
                    ' 0,0 ' + text.fname]
        
        for rect in self._rectangles:
            args += ['-fill', 'rgb' + str(rect.fill)]
            args += ['-stroke', 'rgb' + str(rect.stroke)]
            args += ['-draw']
            args += ['rectangle ' + str(rect.left) + ',' + str(rect.top) + ' '\
                    + str(rect.right) + ',' + str(rect.bottom)]

        args += ['imgur/' + fname + '.png']
        subprocess.call(args)

        return 'imgur/' + fname + '.png'

def make_match_image(m):
    clarity = 50

    im = Image(700,35)
    im.add_text(m.get_player(0).name, 5, 5, True)
    im.add_text(m.get_player(1).name, 695, 5, False)

    instances = sorted(m._outcomes, key=lambda a: a[1]-a[2], reverse=True)
    prev = 5
    dist = 690
    for inst in instances:
        next = round(prev + dist * inst[0])
        red = round(((255-clarity)*inst[1]) / (inst[1]+inst[2]))
        blue = round(((255-clarity)*inst[2]) / (inst[1]+inst[2]))
        if inst[1] > inst[2]:
            red += clarity
        else:
            blue += clarity
        im.add_rectangle(prev, 20, next, 30, (red,0,blue), (0,0,0))
        prev = next

    im.make('match')

if __name__ == '__main__':
    im = Image(700,35)
    im.add_text('MarineKing', 5, 5, True)
    im.add_text('Ryung', 695, 5, False)
    im.add_rectangle(5, 20, 150, 30, (255,0,0), (0,0,0))
    im.add_rectangle(150, 20, 300, 30, (180,0,90), (0,0,0))
    im.add_rectangle(300, 20, 450, 30, (90,0,180), (0,0,0))
    im.add_rectangle(450, 20, 695, 30, (0,0,255), (0,0,0))
    im.make('test')
