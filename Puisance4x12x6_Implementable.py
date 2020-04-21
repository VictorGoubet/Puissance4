# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 08:21:38 2020

@author: victo
"""

import numpy as np

profondeure=-1

def TerminalUtility(s,joueurs):
    
    #Gagnant sur les lignes
    for i in s:
        for n in range(9):
            if(i[n]==i[1+n]==i[2+n]==i[3+n]!="."):
                return [True,99999] if(i[n]==joueurs[0]) else [True,-99999]
                  
    #Gagnant sur les colonnes :
    for j in range(12):   
        x=s[:,j]
        for n in range(3):
            if(x[n]==x[1+n]==x[2+n]==x[3+n]!="."):
                return [True,99999] if(x[n]==joueurs[0]) else [True,-99999]
    
    
    #Gagnant sur les diagonales :
    #on retourne les colonnes pour avoir les diagonales inverses
    s2=np.array([np.flip(s[i]) for i in range(len(s))])
    
    for k in range(-len(s)+1,len(s[0,:])):
        #On ajoutes la diagonale exentré de k et la diagonale inverse
        d1=s.diagonal(k)
        d2=np.flip(s2.diagonal(k)) 
        #Si elle sont au moins de longueure 4 on regarde si il y a un gagant
        if(len(d1)>=4):
            for n in range(len(d1)-3): 
                if(d1[n]==d1[1+n]==d1[2+n]==d1[3+n]!='.'):
                    return [True,99999] if(d1[n]==joueurs[0]) else [True,-99999]
            for n in range(len(d2)-3): 
                if(d2[n]==d2[1+n]==d2[2+n]==d2[3+n]!='.'):
                    return [True,99999] if(d2[n]==joueurs[0]) else [True,-99999]

    #Plus de jetons:
    if(np.sum(s=='.')==30):
        return [True,300]
   
    return [False]
            
    



def heuristique(s,joueurs):
    
    def EvalLCD(LCD,index,joueurs):
        #On évalue le potentiel d'un Ligne Colonne ou Diagonale:
            
        #On commence par restreindre la recherhe aux 3 pions de part et d'autre du point concerné
        tab1=LCD[index:] if(len(LCD)-1-index<4) else LCD[index:index+4]
        tab2=tab2=LCD[:index] if(index<4) else LCD[index-3:index]  
                 
        tab = np.concatenate([tab2,tab1])
            
        #Ensuite on compte le nb de possibilité de gagner 
        nbPossibilite,nbPionsTot=0,0
               
        for k in range(len(tab)-4):
            if(joueurs[1] not in tab[k:4+k]):
                nbPossibilite+=1
                nbPionsTot+=np.sum(tab[k:4+k]==joueurs[0])

        return [nbPossibilite,nbPionsTot]
    
    
    def EvalAction(a,joueurs):
            
        #On evalue une action part sont potentiel sur les lignes colonnes et diagos
        fitness=0
        
        #Evaluation de la ligne
        fitness1=0
        info=EvalLCD(s[a[0]],a[1],joueurs)
        if(info[0]>0):
            fitness1+=info[0]**2+info[1]**3
    
            
        #Evaluation de la colonne
        fitness2=0
        info=EvalLCD(s[:,a[1]],a[0],joueurs)
        if(info[0]>0):
            fitness2+=info[0]**2+info[1]**3
    
    

        #On récupére les deux diagonales concernées:
        fitness3=0
        
        d1=[]
        i,j=a
        while(0<i and 0<j):
            i,j=i-1,j-1 
        x1=i,j
        while(i<len(s) and j<len(s[0,:])):
            d1.append(s[i,j])
            i,j=i+1,j+1
              
        d2=[]
        i,j=a
        while(i<len(s)-1 and 0<j):
            i,j=i+1,j-1
        x2=i,j
        while(0<=i and j<len(s[0,:])):
            d2.append(s[i,j])
            i,j=i-1,j+1
            
        #Evaluation des deux diagonales :
        fitness31=0
        info=EvalLCD(d1,a[0]-x1[0],joueurs)
        if(info[0]>0):
            fitness31+=info[0]**2+info[1]**3
    
        fitness32=0
        info=EvalLCD(d2,x2[0]-a[0],joueurs)
        if(info[0]>0): 
            fitness32+=info[0]**2+info[1]**3
                
        fitness3=fitness31+fitness32 
            
        #On favorise légerement les colonnes car il est plus probable que
        #les pions à placer ne sois pas dans le vide
        #On ajoute également un poid pour favoriser une attaque sur les diagnale
        #En effet ce genre d'attaque est moin prévisible pour l'adversaire
        fitness=fitness1+1.1*fitness2+1.5*fitness3

        return fitness

    #Ici on favorise l'attaque plutot que la défense
    score=0
    coefAttaque=1.5
    coefDefense=1
    
    for a in action(s):
        #On evalue le score de la grille pour le programme (domicile):
        score+=coefAttaque*EvalAction(a,joueurs)
        #On evalue le score de la grille pour l'adversaire
        score-=coefDefense*EvalAction(a,[joueurs[1],joueurs[0]])

    return score
        


def action(s):
    #On parcours à partir du bas pour gagner du temps au debut
    actions=[]
    for k in range(12):
        tab=s[:,k]
        if tab[-1]=='.':
            actions.append([len(tab)-1,k])
        elif(tab[0]=='.'):
            i=-1
            while(i-1>=-6 and tab[i-1]!='.' ):
                i-=1
            actions.append([len(tab)+i-1,k])
    return actions 
       


def Result(s,a,j):
    res=np.copy(s)
    res[a[0],a[1]]=j
    return res


#On regarde 3 coups dans le futur (minimum pour contrer des attaques typiques)

def Max_Value(s,A,B,joueurs):
    #A chaque descente en profondeure on met à jour la variable
    global profondeure
    profondeure+=1
    
    #Pour chaque action on retournera sa valeure ainsi que la profondeure d'ou viens cette valeure
    
    #Avant tout on verifie si on se trouve dans un etat terminal
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return [term[1],profondeure]
    elif(profondeure>3):
        return [heuristique(s,joueurs),profondeure]
    else:
        #On appel récursivement avec coupure Beta
        v=[-9999999999,profondeure]
        for a in action(s):
            mnV=Min_Value(Result(s,a,joueurs[0]),A,B,joueurs)
            v=[max(v[0],mnV[0]),mnV[1]]
            profondeure-=1  
            if v[0]>=B:
                return v
            A=max(A,v[0])
                    
        return v

def Min_Value(s,A,B,joueurs):
    global profondeure
    profondeure+=1
    
    term=TerminalUtility(s,joueurs)
    if(term[0]):
        return [term[1],profondeure]
    elif(profondeure>3):
        return [heuristique(s,joueurs),profondeure]
    else:
        #On appel récursivement avec coupure Beta
        v=[9999999999,profondeure]
        for a in action(s):
            mxV=Max_Value(Result(s,a,joueurs[1]),A,B,joueurs)
            v=[min(v[0],mxV[0]),mxV[1]]
            profondeure-=1
            if v[0]<=A:
                return v
            B=min(B,v[0])
        return v
            


def MinMax(s,joueurs):
    act=[None]
    value=-9999999999
    for a in action(s):
        
        global profondeure
        profondeure=0
        coup=Min_Value(Result(s,a,joueurs[0]),-9999999999,9999999999,joueurs)
        res=coup[0]
        profondeureCoup=coup[1]
        if(res>value):
            value=res
            act=[[a,profondeureCoup]]
        elif(res==value):
            act.append([a,profondeureCoup])
    #Si on a le choix entre plusieurs coups de même score on choisi le coups se
    #situant le moins profondement dans l'arbre
    return min(act,key=lambda x:x[1])[0]

    





    