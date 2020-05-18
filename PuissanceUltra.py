# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 08:21:38 2020

@author: victo
"""

import numpy as np
import time


profondeure=-1
profondeureMax=3

CRED = '\33[41m'
CBLUE   = '\33[44m'
CYEL   = '\33[36m'
CEND = '\033[0m'

def diag(s,k):
    d1,d2=[],[]
    i,j= (0,k) if(k>0) else (-k,0)
    while(i and j >0):
        i,j=i-1,j-1 
    while(i<len(s) and j<len(s[0])):
        d1.append(s[i,j])
        d2.append(s[i,len(s[0])-j-1])
        i,j=i+1,j+1
    return d1,d2



def TerminalUtility(s):


    for i in s:
        for n in range(9):
            if(i[n]==i[1+n]==i[2+n]==i[3+n]!=0):
                return [True,99999] if(i[n]==1) else [True,-99999]
                  
    for j in range(12):   
        x=s[:,j]
        for n in range(3):
            if(x[n]==x[1+n]==x[2+n]==x[3+n]!=0):
                return [True,99999] if(x[n]==1) else [True,-99999]
    

    for k in range(-2,9):
        d1,d2=diag(s,k)
        for n in range(len(d1)-3): 
            if(d1[n]==d1[1+n]==d1[2+n]==d1[3+n]!=0):
                return [True,99999] if(d1[n]==1) else [True,-99999]
            
            if(d2[n]==d2[1+n]==d2[2+n]==d2[3+n]!=0):
                return [True,99999] if(d2[n]==1) else [True,-99999]

    nbP=np.sum(s==0)
    if(nbP==30):
        return [True,50]
   
    return [False]
            
    


def heuristique(s):
    
    def checkLCD(tab):
        resLocal,resAdversaire=[True,0],[True,0]
        
        for k in tab:
            if(k==2):
                resLocal[0]=False
                resAdversaire[1]+=1

            elif(k==1):
                
                resAdversaire[0]=False
                resLocal[1]+=1

 
        return resLocal,resAdversaire

    def EvalLCD(LCD,index):


        tab1=LCD[index:] if(len(LCD)-1-index<4) else LCD[index:index+4]
        tab2=tab2=LCD[:index] if(index<4) else LCD[index-3:index]     
        tab = np.concatenate([tab2,tab1])

        fitnessLocal,fitnessAdversaire=0,0
         
        for k in range(len(tab)-3):

            check=checkLCD(tab[k:4+k])

            if(check[0][0]):
                fitnessLocal+=3**check[0][1]

            if(check[1][0]):
                fitnessAdversaire+=3**check[1][1]
            
                
        return fitnessLocal,fitnessAdversaire
    
    def EvalAction(a):
            
        fitnessLocal,fitnessAdversaire=0,0
        info=EvalLCD(s[a[0]],a[1])
        fitnessLocal+=info[0]
        fitnessAdversaire+=info[1]

        
        info=EvalLCD(s[:,a[1]],a[0])
        fitnessLocal+=info[0]
        fitnessAdversaire+=info[1]

        d1=[]
        i,j=a
        while(i>=0 and j >=0 ):
            d1.append(s[i,j])
            i,j=i-1,j-1 
            
        d1.reverse()
        i1=len(d1)-1
        i,j=a[0]+1,a[1]+1
        
        while(i<len(s) and j<len(s[0])):
            d1.append(s[i,j])
            i,j=i+1,j+1
              
        d2=[]
        i,j=a
        while(i<len(s) and j>=0):
            d2.append(s[i,j])
            i,j=i+1,j-1
            
        d2.reverse()
        i2=len(d2)-1
        i,j=a[0]-1,a[1]+1
        
        while(0<=i and j<len(s[0])):
            d2.append(s[i,j])
            i,j=i-1,j+1

          
        if(len(d1)>3):
            info=EvalLCD(d1,i1)
            fitnessLocal+=info[0]
            fitnessAdversaire+=info[1]
        
        if(len(d2)>3):
            info=EvalLCD(d2,i2)
            fitnessLocal+=info[0]
            fitnessAdversaire+=info[1]
 
        return fitnessLocal,fitnessAdversaire


    score=0

    for a in action(s):
        fitnessS=EvalAction(a)
        score+=1.7*fitnessS[0]
        score-=fitnessS[1]

    return round(score,1)
        


def action(s):

    actions=[]
    for k in range(12):
        tab=s[:,k]
        if tab[-1]==0:
            actions.append([len(tab)-1,k])
        elif(tab[0]==0):
            i=-1
            while(i-1>=-6 and tab[i-1]!=0 ):
                i-=1
            actions.append([len(tab)+i-1,k])
    return actions 
       


def Result(s,a,j):
    res=np.copy(s)
    res[a[0],a[1]]=j
    return res




def Max_Value(s,A,B):
    global profondeure
    profondeure+=1
    

    term=TerminalUtility(s)
    if(term[0]):
        return [term[1],profondeure]

    elif(profondeure>profondeureMax):
        return [heuristique(s),profondeure]

    else:

        v=[-9999999,profondeure]
        for a in action(s):
            mnV=Min_Value(Result(s,a,1),A,B)
            v=[max(v[0],mnV[0]),mnV[1]]
            profondeure-=1  
            if v[0]>=B:return v
            A=max(A,v[0])
                    
        return v


def Min_Value(s,A,B):

    global profondeure
    profondeure+=1
    
    term=TerminalUtility(s)
    if(term[0]):
        return [term[1],profondeure]
    elif(profondeure>profondeureMax):
        return [heuristique(s),profondeure]
    else:
        v=[9999999,profondeure]
        for a in action(s):
            mxV=Max_Value(Result(s,a,2),A,B)
            v=[min(v[0],mxV[0]),mxV[1]]
            profondeure-=1
            if v[0]<=A:return v
            B=min(B,v[0])
        return v
            


def MinMax(s):
    global profondeure
    act=[None]
    value=-9999999
    
    for a in action(s):
        
        profondeure=0
        coup=Min_Value(Result(s,a,1),-9999999,9999999)
        res=coup[0]
        profondeureCoup=coup[1]
        if(res>value):
            value=res
            act=[[a,profondeureCoup]]
        elif(res==value):
            act.append([a,profondeureCoup])
    return min(act,key=lambda x:x[1])[0]




def affichage(plateau):

    print("\n| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |11 |12 | ")
    print("\n------------------------------------------------- ")
    for i in plateau:
        print('| ',end='')
        for j in i:
            if(j==0):
                print('. | ',end='')           
            elif(j==1):
                print(CRED+'X'+CEND+' | ',end='') 
            else:
                print(CBLUE+'O'+CEND+' | ',end='')
        print('\n')
    print("\n")

def SaisieSecur(s):

    c=input("colonne n° : ")

    while ((c.isdigit()==True and 0<=int(c)-1<12 and 0 in s[:,int(c)-1] )==False ):
        c=input("colonne n° : ")
        
    i,j=0,int(c)-1
    for x in range(6):
        if(s[x,j]!=0):
            i=x-1
            break  
        if(x==5 and s[x,j]==0):            
            i=x
            break 
            
    return [i,j]



def MorpionGame():

    j=input("Qui commence ?\n 1: Notre IA \n 2: L'IA adverse \n\n →  ")
    j=1 if(j!="1" and j!="2") else int(j)
    

    Grid=np.zeros((6,12));
    listeT=[]
    affichage(Grid)
        
    
    term=TerminalUtility(Grid)
    nbCoup=0
    while term[0]==False:
        
        if(j==2):
            print("C'est le tour de l'adversaire, rentrez la colonne qu'elle a joué : ")
            t1=time.time()
            saisie=SaisieSecur(Grid)
            dt=time.time()-t1
            print("L'adversaire a réflechis "+CYEL+str(round(dt,1))+CEND+" sc et joue en "+CYEL+str(saisie[1]+1)+CEND)
                
            Grid[saisie[0],saisie[1]]=2
            affichage(Grid)
            j=1
         
        else:
            print("Le programme reflechi... :")
            t1=time.time()
            action=MinMax(Grid)
            dt=time.time()-t1
                
            listeT.append(dt)
            nbCoup+=1
            print("Notre IA a réflechie "+CYEL+str(round(dt,1))+CEND+" sc et joue en "+CYEL+str(action[1]+1)+CEND)
            Grid[action[0],action[1]]=1
            affichage(Grid) 
            j=2
        
        term=TerminalUtility(Grid)
        
        
    print("La partie est finie !")
    Tmoy=round(np.array(listeT).mean(),4)
    print("Notre IA a prie en moyenne ",Tmoy,"sc à répondre")
    
    
    res=TerminalUtility(Grid)[1]
    if(res==99999):
        print("Notre IA a gagnée !")
    elif(res==-99999):
        print("L'IA adverse a été plus forte..")
    else:
        print("Egalité!")
            
        
if __name__=="__main__":
    MorpionGame()