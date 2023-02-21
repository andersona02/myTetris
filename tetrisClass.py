# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 17:02:13 2022

@author: Anderson
"""

import tkinter as tk
from numpy.random import permutation 
import time


def functionTimer(functionName,*args):
    start = time.perf_counter()
    temp = functionName(*args)
    end = time.perf_counter()
    print(f'{end - start} for {functionName}')
    return temp
    
    
def addList(*lists):
    return [sum(i) for i in zip(*lists)]
        


def getKeyN(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 
    
    
    

class Piece:
    legalShapes = ('i', 'j', 'l', 'o', 's', 't', 'z', 'I', 'J', 'L', 'O', 'S', 'T', 'Z')
    
    tetrominoes = { 'I':[[ 0,  0], [-1,  0], [ 1,  0], [ 2,  0]], 
                    'J':[[ 0,  0], [-1, -1], [-1,  0], [ 1,  0]], 
                    'L':[[ 0,  0], [-1,  0], [ 1,  0], [ 1, -1]], 
                    'O':[[ 0,  0], [ 0, -1], [ 1,  0], [ 1, -1]], 
                    'S':[[ 0,  0], [-1,  0], [ 0, -1], [ 1, -1]], 
                    'T':[[ 0,  0], [-1,  0], [ 0, -1], [ 1,  0]], 
                    'Z':[[ 0,  0], [-1, -1], [ 0, -1], [ 1,  0]]}

    
    
    def __init__(self,shape):
        if shape in self.legalShapes:
            self.shape = shape.upper()
            self.position = self.tetrominoes[self.shape]
            self.center = [4, 1]
        else:
            raise(ValueError(f'only support {self.legalShapes}'))
            
    
    def getExactPosition(self):
        return [addList(self.center, i) for i in self.position]
        """
        positions = []
        for i in self.position:
            print(i,self.center)
            positions.append([i[0] + self.center[0], i[1] + self.center[1]])
        
        return positions
        """
        
    def rotate(self,direction = 'clockwise'):
        if direction == 'clockwise':
            sin = 1
            cos = 0
        if direction == 'counterclockwise':
            sin = -1
            cos = 0
        if direction == '180':
            sin = 0
            cos = -1
            
        self.position = [[i[0] * cos - i[1] * sin, i[0] * sin + i[1] * cos] for i in self.position]
        
        
        
        
        
class Field:
    colors = ['gray', 'skyblue', 'blue', 'orange', 'yellow', 'green', 'purple', 'red']
    pieceColor = {'I' : 1,
                  'J' : 2,
                  'L' : 3,
                  'O' : 4, 
                  'S' : 5, 
                  'T' : 6, 
                  'Z' : 7,
                  'blank' : 0}
    
    def __init__(self,size = [10,20]):
        
        if len(size)!= 2:
            raise(IndexError('must be 2-dimension'))
            
        if not all(type(i) == int for i in size):
            raise(TypeError('field size should be int'))

        self.size = tuple(size)
        self.playField = [[0]*size[0] for i in range (size[1] + 2)]
        self.canvas = tk.Canvas(root, width = size[0] * blockSize + 1, height = size[1] * blockSize + 1, bg = self.colors[0])
        self.canvas.pack(anchor = 'center')
        self.now = None
        self .drawPlayField()
    
    
    
    def __del__(self):
        self.canvas.destroy()
        
          

    def drawBlocks(self, coordinate, color):
        for i in coordinate:
            px = i[0] * blockSize + 2
            py = i[1] * blockSize + 2
            self.canvas.create_rectangle(px, py, px + blockSize, py + blockSize, fill = color, width = 1 if i[1] > 1 or color != 'gray' else 0)
        
        
        
    def drawPlayField(self):
        
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.drawBlocks([[i,j]],self.colors[self.playField[j][i]])



    def showNow(self):
        self.drawBlocks(self.now.getExactPosition(),self.colors[self.pieceColor[self.now.shape]])
        
        
        
    def hideNow(self):
        self.drawBlocks(self.now.getExactPosition(),self.colors[0])
        self.canvas.create_rectangle(0, 0, blockSize*10 + 3, blockSize*2 + 2, fill = 'gray', width = 0)
        #self.drawPlayField()
    
    
    
    def isLegal(self, blocks):
        
        for i in blocks:
            if not(self.size[0] > i[0] >= 0 and
                self.size[1] > i[1] >= 0 and
                self.playField[i[1]][i[0]] == 0):
                return False

        return True
    
    
    
    def setPlayField(self, coordinate, color):
        
        for i in coordinate:
            self.playField[i[1]][i[0]] = color

        self.drawPlayField()
        
        
        
    def placeNow(self):
        while(not self.move(self.now,(0,1))):
            pass

        self.setPlayField(self.now.getExactPosition(), self.pieceColor[self.now.shape])
        
    

    def checkLine(self):
        full = []
        count = 0
        for i in range(len(self.playField)):
            if 0 not in self.playField[i]:
                count += 1
                full.append(i)
        if count:
            full.reverse()
            for i in full:
                del self.playField[i]
            self.playField = [[0]*self.size[0] for i in range(count)] + self.playField
            self.drawPlayField()
            return count
        return 0
    
    def isGameOver(self):
        if any(self.playField[1]):
            return True
        
        return False
    
    
    
    def move(self, piece, movement):
        """
        blocks = piece.getExactPosition()
        moved = [addList(i, movement) for i in blocks]
        
        if self.isLegal(moved):
            self.hideNow()
            self.now.center = addList(self.now.center, movement)
            self.showNow()
            #print(f'move to {moved}')
            return 0
        else:
            print('move failed!')
            return 1
        """

        blocks = functionTimer(piece.getExactPosition)
        moved = [functionTimer(addList, i, movement) for i in blocks]
        
        if functionTimer(self.isLegal, moved):
            functionTimer(self.hideNow)
            self.now.center = functionTimer(addList, self.now.center, movement)
            functionTimer(self.showNow)
            #print(f'move to {moved}')
            return 0

        else:
            print('move failed!')
            return 1
    
    
    
    
    def rotate(self, direction):
        before = self.now.position
        self.hideNow()
        self.now.rotate(direction)
        
        if self.isLegal(self.now.getExactPosition()):
            #print(f'rotated to {self.now.getExactPosition()}')
            self.showNow()
            return 0
        else:
            print('rotate failed')
            self.now.position = before
            self.showNow()
            return 1
        
        
        
        
        
class Game:
    
    def __init__(self):
        self.score = 0
        self.scoreLabel = tk.Label(root, text = f'score : {self.score}')
        self.scoreLabel.pack()
        self.field = Field()
        self.piecePack = []
        self.dropTime = 1000
        self.dropTimer = None
        root.bind('<Key>',self.keyboardEventHandler)
        
        
    def start(self):
        self.getNewPiece()
        self.dropByTime()
        
        
    def getNewPiece(self):
        
        if not self.piecePack:
            self.generatePiecePack()
            
        self.field.now = Piece(self.piecePack.pop())
        self.field.showNow()
        
    
    def generatePiecePack(self):
        
        #self.piecePack = list(permutation(['I', 'J', 'L', 'O', 'S', 'T', 'Z']))
        self.piecePack = ['I']
    
    
    
    def setScore(self, newScore = None):
        
        if newScore != None:
            self.score = newScore
            self.scoreLabel['text'] = f'score : {self.score}'
        
        
        
    def placePiece(self):
        self.field.placeNow()
        self.setScore(self.score + self.field.checkLine())
        if self.field.isGameOver():
            del self.field
            self.field = Field()
            self.setScore(0)
        self.getNewPiece()
        self.dropTimerReset
        
        
    def dropByTime(self):
        if self.field.move(self.field.now, (0, 1)):
                self.placePiece()
        self.dropTimer = root.after(self.dropTime, self.dropByTime)
        
    
    def dropTimerReset(self):
        root.after_cancel(self.dropTimer)
        self.dropTimer = root.after(self.dropTime, self.dropByTime)
        
        
    def keyboardEventHandler(self, event):
        
        if(event.keysym == 'Up'):
            self.field.move(self.field.now, (0, -1))
        if(event.keysym == 'Down'):
            if self.field.move(self.field.now, (0, 1)):
                self.placePiece()
            self.dropTimerReset()
        if(event.keysym == 'Left'):
            self.field.move(self.field.now,(-1, 0))
        if(event.keysym == 'Right'):
            self.field.move(self.field.now,(1, 0))
        if(event.keysym == 'z'):
            self.field.rotate('clockwise')
        if(event.keysym == 'x'):
            self.field.rotate('counterclockwise')
        if(event.keysym == 'space'):
            self.placePiece()
        
        

root = tk.Tk()
root.geometry('900x600')
blockSize = 20
g = Game()
g.start()
root.mainloop()