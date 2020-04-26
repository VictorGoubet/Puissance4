# -*- coding: utf-8 -*-
"""

@author: Chloe Daems, Titouan Damestoy, Bruce Dakin


"""
# on a rajouté 2* profondeur
##Le ALPHA BETA

##------------------------------------------------
def Min_Value(s,profondeur,a,b):
    #print("MIN")
   
    if(Terminal_Test(s)):
        victoire=Utility(s)
        if(victoire==1):
            return (1000 - profondeur) #On prend en compte la profondeur
        elif(victoire==-1):
            #print("je passe 1")
            return (profondeur - 1000)
        else:
            return 0

        #INSERTION DE L'HEURISTIQUE
        #----------------------------
    elif(profondeur>=4):
           
            return Heuristique(s)
    else:
        #----------------------------
      
        profondeur+=1

        v=10000
        for action in Actions(s):
            v= min(v,Max_Value(Result(s,action),profondeur,a,b))
            if(v<=a): return v
            b=min(b,v)
          

    return v

def Max_Value(s,profondeur,a,b):
    #print("MAX")
    
    if(Terminal_Test(s)):
        victoire=Utility(s)
        
        if(victoire==1):
            return (1000 - profondeur) #On prend en compte la profondeur
        elif(victoire==-1):
            return (-1000 + profondeur)
        else:
            return 0
    #INSERTION DE L'HEURISTIQUE
    #----------------------------
    elif(profondeur>=4):
        
        return Heuristique(s)
    #----------------------------
    else:
        profondeur+=1
        v=-10000
        count=0
        for action in Actions(s):
            
            v= max(v,Min_Value(Result(s,action),profondeur,a,b))
       
            if(v>=b): return v
            a=max(a,v)
            
            count+=1
            
        
        return v
# si deux valeurs égales alors choisir la colonne la plus vide, a faire
def Alpha_Beta_Search(s):
    
    if (NbdeJetonsActuel(s)==0):
        return 6
    
    a=-10000
    b=10000
    bestValue=-10000
    bestMove=-1
    for action in Actions(s):
        value=Min_Value(Result(s,action),0,a,b)
        #print("Value :",value," BestValue : ",bestValue)
        
        if(value>bestValue):
            bestValue=value
            bestMove=action
    print("L'IA joue en colonne ",bestMove,".")
    return bestMove
##------------------------------------------------

#LISTE DES ACTIONS POSSIBLE
#-------------------------------------------------
def Actions(x):
    actions=[]
    for i in range(12):
        if(x[0][i]==0):
            actions.append(i)
    
    return actions
#-------------------------------------------------

#CONNAITRE LE NB DE JETONS DEJA JOUE PUIS QUI DOIT JOUER

#-------------------------------------------------
def NbdeJetonsActuel(s):

    jetonsJoues=0
    for i in s:
        jetonsJoues+=i.count(1)+i.count(2)
    return jetonsJoues
def quidoitjouer(s):
    # Cette fonction retourne le numero du joueur qui doit jouer
    if(iAJoueur1==True):
        if (NbdeJetonsActuel(s) % 2 == 0):
            player = 1
        else:
            player = 2
    else:
        if (NbdeJetonsActuel(s) % 2 == 0):
            player = 2
        else:
            player = 1
    #print("iAJoueur1=",iAJoueur1,"Player ",player)
    return player

#-------------------------------------------------

#TERMINAL STATE (La partie est elle finie ?)

#-------------------------------------------------
def Terminal_Test(P):
        
    test=False
    
    # test si tout les jetons ont été joués
    
    if (NbdeJetonsActuel(P)==42):
        test=True
        return test
 
    # test d'une succession horizontale
    i=j=0
    while(i<=5 and j<=8):
        if (P[i][j]==P[i][j+1] and P[i][j]==P[i][j+2] and P[i][j]==P[i][j+3] and P[i][j]!=0 ):
            test=True
            return test
        if (j==8):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'une succession verticale
    i=j=0
    while(i<=2 and j<=11):
        if (P[i][j]==P[i+1][j] and P[i][j]==P[i+2][j] and P[i][j]==P[i+3][j] and P[i][j]!=0 ):
            test=True
            return test
        if (j==11):
            i=i+1
            j=0
        else:
            j=j+1
            
    # test d'une succession diagonale vers la droite
    i=j=0
    while(i<=2 and j<=8):
        if (P[i][j]==P[i+1][j+1] and P[i][j]==P[i+2][j+2] and P[i][j]==P[i+3][j+3]and P[i][j]!=0):
            test=True
            return test
        if (j==8):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'une succession diagonale vers la gauche 
    
    i=0
    j=11
    while(i<=2 and j>=3):
        if (P[i][j]==P[i+1][j-1] and P[i][j]==P[i+2][j-2] and P[i][j]==P[i+3][j-3] and P[i][j]!=0):
            test=True
            return test
        if (j==3):
            i=i+1
            j=11
        else:
            j=j-1
    
    
    return test
#-------------------------------------------------

#RESULT (Coup effectué sur la grille)

#-------------------------------------------------
def Result(x,colonne):

    #On fait une deep copie du state actuel
    #-----------------------------------
    Grille=[]
    for i in range(6):
        Grille.append([])
        for j in range(12):
            Grille[i].append(x[i][j])
    #------------------------------------

    #On remonte la colonne jusqu'a trouver une case vide
    #-----------------------------------------------------
    i=0
    while(i<6):
        if(Grille[5-i][colonne]==0):
           Grille[5-i][colonne]=quidoitjouer(Grille)
           return Grille 
            
        i+=1
    #------------------------------------------------
    #Si a ce point la, Result n'a rien renvoyer c'est que la colonne est déjà complete
    print("Vous ne pouvez pas jouer la, la colonne ",colonne," est deja complète")
    return Grille
#-------------------------------------------------

#UTILITY (Qui a gagné ? -Heuristique faible-)

#-------------------------------------------------
def Utility(P):
        
    test=0
    
    # test si tout les jetons ont été joués
    
    if (NbdeJetonsActuel==42):
        test=0
        return test
 
    # test d'une succession horizontale
    i=j=0
    while(i<=5 and j<=8):
        if (P[i][j]==P[i][j+1] and P[i][j]==P[i][j+2] and P[i][j]==P[i][j+3]):
            if (P[i][j]==1):
                test=-1
                return test
            elif(P[i][j]==2):
                test=1
                return test
        if (j==8):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'une succession verticale
    i=j=0
    while(i<=2 and j<=11):
        if (P[i][j]==P[i+1][j] and P[i][j]==P[i+2][j] and P[i][j]==P[i+3][j]):
            if (P[i][j]==1):
                test=-1
                return test
            elif(P[i][j]==2):
                test=1
                return test
        if (j==11):
            i=i+1
            j=0
        else:
            j=j+1
            
    # test d'une succession diagonale vers la droite
    i=j=0
    while(i<=2 and j<=8):
        if (P[i][j]==P[i+1][j+1] and P[i][j]==P[i+2][j+2] and P[i][j]==P[i+3][j+3]):
            if (P[i][j]==1):
                test=-1
                return test
            elif(P[i][j]==2):
                test=1
                return test
        if (j==8):
            i=i+1
            j=0
        else:
            j=j+1
 
    # test d'une succession diagonale vers la gauche 
    
    i=0
    j=11
    while(i<=2 and j>=3):
        if (P[i][j]==P[i+1][j-1] and P[i][j]==P[i+2][j-2] and P[i][j]==P[i+3][j-3]):
            if (P[i][j]==1):
                test=-1
                return test
            elif(P[i][j]==2):
                test=1
                return test
        if (j==3):
            i=i+1
            j=11
        else:
            j=j-1
    
    
    return test
#-------------------------------------------------

#HEURISTIQUE DE NOTATION DE GRILLE

#-------------------------------------------------
def Heuristique(s):
    
    tableauEvaluation = [[3, 4, 5, 7, 7, 7, 7, 7, 7, 5, 4, 3],
                         [4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4],
                         [5, 8, 11, 13, 13, 13, 13, 13, 13, 11, 8, 5],
                         [5, 8, 11, 13, 13, 13, 13, 13, 13, 11, 8, 5],
                         [4, 6, 8, 10, 10, 10, 10, 10, 10, 8, 6, 4],
                         [3, 4, 5, 7, 7, 7, 7, 7, 7, 5, 4, 3]]

    evaluation = 0

    for i in range(6):
        for j in range(12):
            if(s[i][j]==2):
                evaluation = evaluation + tableauEvaluation[i][j]
            elif(s[i][j]==1):
                evaluation = evaluation - tableauEvaluation[i][j]
    
    return evaluation

#-------------------------------------------------

#AFFICHAGE DE LA GRILLE ( deux possibilités )
 
#-------------------------------------------------
# AFFICHAGE SUR SPYPER UNIQUEMENT

def Affichage(x):
    affect = {
        1 : "\033[41m0\033[0m",#rouge
        2 : "\033[42m0\033[0m",#vert
        0: "\033[37m.\033[0m"}
    for i in x:
        print ('| {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} |'.format(affect[i[0]], affect[i[1]],affect[i[2]],
                                                                                                                        affect[i[3]], affect[i[4]],affect[i[5]],
                                                                                                                       affect[i[6]], affect[i[7]],affect[i[8]],
                                                                                                                       affect[i[9]], affect[i[10]],affect[i[11]]))
'''
#-------------------------------------------------  
# AFFICHAGE SUR AUTRE QUE SPYDER
def Affichage(x):
    affect = {
        1 : "X",
        2 : "Y",
        0: "."}
    for i in x:
        print ('| {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} | {:^4} |'.format(affect[i[0]], affect[i[1]],affect[i[2]],
                                                                                                                        affect[i[3]], affect[i[4]],affect[i[5]],
                                                                                                                        affect[i[6]], affect[i[7]],affect[i[8]],
                                                                                                                       affect[i[9]], affect[i[10]],affect[i[11]]))
'''
#------------------------------------------------- 
               
#Gestionnaire du jeu

#-------------------------------------------------
iAJoueur1=False #On crée une variable global pour savoir si l'IA joue en premier ou en deuxieme
def playP1vsIA():
    s=[[0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0]]
    p1=0
    
    while(p1!=1 and p1!=2):
        p1=int(input("Voulez vous jouer en premier ou en deuxieme ? ( 1 ou 2) "))
    if(p1==1):
        global iAJoueur1
        iAJoueur1=True
   
    Affichage(s)

    while (not Terminal_Test(s)):
        if(quidoitjouer(s)==1):
            print("C'est à vous de jouer, veuillez mettre le numero de colonne (0 à 11) :")
            colonne=int(input("x = "))
            
            s = Result(s,colonne)
            
        else:
            print("Au tour de IA ... ")
            s=Result(s,Alpha_Beta_Search(s))
            
        Affichage(s)
        
    print("\n")
    if(Utility(s)==-1):
        print("Bravo, vous avez gagné !!!")
    elif(Utility(s)==0):
        print("Match nul !")
        
    else:
       print("Mince, l'IA a été plus forte que vous ! ")
#-------------------------------------------------

#ZONE TEST
#-------------------------------------------------
#s=  [[0,0,0,0,0,0,0,0,2,0,0,0],
#     [0,0,0,0,2,0,0,0,1,0,0,0],
#     [0,0,0,0,1,0,1,0,1,0,0,0],
#     [0,0,0,0,1,0,2,0,1,0,0,0],
#     [0,0,2,0,1,0,2,0,2,0,0,0],
#     [0,1,2,2,2,1,1,2,2,0,0,0]]
#iAJoueur1=False
#print(Affichage(s))
#print("Terminé ? ",Terminal_Test(s))

#print("Qui a gagné ? ",Utility(s))
#s=Result(s,Alpha_Beta_Search(s))
#print("JE JOUE la colonne " ,MinMax(s))
#print(Affichage(s))
#-------------------------------------------------


#ZONE DE JEU
#-------------------------------------------------
playP1vsIA()
#-------------------------------------------------



