#!/usr/bin/python3

import os

class Image:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.texts = []

    def add_text(self, text, left=True):
        fname = 'imgur/temp/' + str(len(self.texts)) + '.png'

        args = ['convert']
        args.append('-size 200x30')
        args.append('xc:transparent')
        args.append('-draw "text 0,20 \'' + text + '\'"')
        args.append(fname)
        os.system(' '.join(args))

        args = ['convert']
        args.append('-trim')
        args.append(fname)
        args.append(fname)
        os.system(' '.join(args))

        s = os.system('identify ' + fname)
        print(s.split(' '))

    def make(self):
        args = ['convert']
        args.append('-size ' + str(self.width) + 'x' + str(self.height))
        args.append('xc:transparent')
        args.append('imgur/test.png')
        os.system(' '.join(args))

if __name__ == '__main__':
    im = Image(700,50)
    im.add_text('MarineKing')
    im.add_text('Ryung')
    im.make()
