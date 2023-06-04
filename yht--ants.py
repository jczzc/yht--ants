import threading
import math
import random
import copy
import json
import os
import tqdm
lock=threading.Lock()
class node:
    def __init__(self,line,colume,value,code):
        self.line=line
        self.col=colume
        self.value=value
        self.code=code
        self.smell=5
    def connections(self):
        global maxium
        if self.col!=0:
            if self.line!=0:
                if self.col!=self.line-1:
                    if self.line!=maxium:
                        return ((self.line-1,self.col),(self.line-1,self.col-1),(self.line+1,self.col),(self.line+1,self.col+1))
                    else:
                        return ((self.line-1,self.col),(self.line-1,self.col-1))
                else:
                    return ((self.line-1,self.col-1),(self.line+1,self.col),(self.line+1,self.col+1))
            else:
                return ((self.line+1,self.col),(self.line+1,self.col+1))
        else:
            if self.line!=0:
                return ((self.line-1,self.col),(self.line+1,self.col),(self.line+1,self.col+1))
            else:
                return ((self.line+1,self.col),(self.line+1,self.col+1))
class ant:
    def __init__(self,code,lock,position):
        global nodes
        self.code=code
        self.lock=lock
        self.position=position
        self.start_position=position
        self.history=[self.start_position]
        ln,col=self.position
        self.sum=nodes[ln][col].value
    def move(self):
        global nodes
        ln,col=self.position
        directions=nodes[ln][col].connections()
        available=[]
        for node in directions:
            if not node in self.history:
                available.append(node)
        if not len(available)==0:
            weight=[]
            cont=0
            reavailable=copy.deepcopy(available)
            for posi in available:
                ln,col=posi
                try:
                    _=nodes[ln][col]
                    n=True
                except Exception as e:
                    #print(e)
                    del reavailable[reavailable.index((ln,col))]
                    n=False
                if n:
                    weight.append(nodes[ln][col].smell)
                #print(cont)
                cont+=1
                #print(reavailable)
                #print(weight)
            if len(reavailable)==0:
                return False
            choice=random.choices(reavailable,weights=weight,k=1)[0]
            self.position=choice
            self.history.append(self.position)
            ln,col=copy.deepcopy(choice)
            self.sum+=nodes[ln][col].value
            return True
        else:
            return False
    def brain(self,times):
        global record,path,nodes,long,his
        for i in range(times):
            self.position=self.start_position
            self.history=[self.start_position]
            ln,col=self.position
            self.sum=nodes[ln][col].value
            con=True
            while con:
                con=self.move()
            if self.sum>record:
                self.lock.acquire()
                record=self.sum
                path=self.history
                his=[]
                his.append(path)
                for ln in nodes:
                    for node in ln:
                        if not (node.line,node.col) in self.history:
                            if node.smell>1:
                                node.smell-=1
                """for ln,col in path:
                    if nodes[ln][col].smell<=1:
                        pass
                    else:
                        nodes[ln][col].smell-=1"""
                for ln,col in self.history:
                    if nodes[ln][col].smell>=5:
                        pass
                    else:
                        nodes[ln][col].smell+=1
                print('\n\r------------------------------')
                print('thread',self.code)
                print('maxium',self.sum)
                print('path',self.history)
                self.lock.release()
            if self.sum>=record-10 and self.history!=path and len(self.history)>=len(long):
                self.lock.acquire()
                #record=self.sum
                long=self.history
                for ln in nodes:
                    for node in ln:
                        if not (node.line,node.col) in self.history:
                            if node.smell>1:
                                node.smell-=1
                for ln,col in self.history:
                    if nodes[ln][col].smell>=4:
                        pass
                    else:
                        nodes[ln][col].smell+=1
                print('\n\r------------------------------')
                print('thread',self.code)
                print('lenth',self.sum)
                print('path',self.history)
                self.lock.release()
            if (self.sum>=record-1000 and self.history!=path and len(self.history)>=len(long)+10) or len(self.history)>=len(path)+15:
                self.lock.acquire()
                #record=self.sum
                long=self.history
                for ln in nodes:
                    for node in ln:
                        if not (node.line,node.col) in self.history:
                            if node.smell>1:
                                node.smell-=1
                for ln,col in self.history:
                    if nodes[ln][col].smell>=4:
                        pass
                    else:
                        nodes[ln][col].smell+=1
                for ln,col in self.history:
                    if nodes[ln][col].smell>=4:
                        pass
                    else:
                        nodes[ln][col].smell+=1
                print('\n\r------------------------------')
                print('thread',self.code)
                print('long_lenth',self.sum)
                print('path',self.history)
                self.lock.release()
            if self.sum==record and self.history!=path and not self.history in his:
                self.lock.acquire()
                record=self.sum
                his.append(path)
                path=self.history
                for ln in nodes:
                    for node in ln:
                        if not (node.line,node.col) in self.history:
                            if node.smell>1:
                                node.smell-=1
                for ln,col in self.history:
                    if nodes[ln][col].smell>=4:
                        pass
                    else:
                        nodes[ln][col].smell+=1
                print('\n\r------------------------------')
                print('thread',self.code)
                print('remaxium',self.sum)
                print('path',self.history)
                self.lock.release()
nodes=[]
if __name__=='__main__':
    lines=eval(input('//line>>'))
    ant_num=eval(input('//ant>>'))
    cicle_num=eval(input('//cil>>'))
    result_name=input('//RFN>>')
    code=0
    record=0
    his=[]
    path=[]
    long=[]
    maxium=lines-1
    for ln in range(lines):
        nodes.append([])
        for col in range(ln+1):
            #print('(',ln,',',col,')')
            if col==0:
                nodes[ln].append(node(ln,col,1,code))
            elif col==ln:
                nodes[ln].append(node(ln,col,1,code))
            else:
                nodes[ln].append(node(ln,col,nodes[ln-1][col].value+nodes[ln-1][col-1].value,code))
            code+=1
    for line in nodes:
        for node in line:pass
            #print(node.value,end=' ')
        #print()
    objects=[]
    threads=[]
    for code in tqdm.tqdm(range(ant_num)):
        objects.append(ant(code,lock,(lines-1,0)))
    cont=0
    for ant in objects:
        threads.append(threading.Thread(ant.brain(cicle_num)))
        threads[cont].start()
        cont+=1
    for thread in tqdm.tqdm(threads):
        thread.join()
    with open(result_name,'w') as f:
        json.dump((record,his),f)
    print(record)
    os.system('pause')
