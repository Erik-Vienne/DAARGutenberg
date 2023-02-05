import networkx as nx

from livre.models import Index

# l1 et l2 deux liste de tuples correspondant à des id de mots et leur nombre d'occurence
def distanceLent (l1, l2) :

    print("distance")
    #listeOcc = []

    numerateur = 0
    denom = 0

    for elem1 in l1 :
        matching = False
        for elem2 in l2 :
            #print(elem1.idMot.id)
            #print(elem2.idMot.id)
            if elem1.idMot.id == elem2.idMot.id :
                #listeOcc.append( (elem1[1], elem2[1]) )
                #print("match")

                #print(elem1.nbOccurrence)
                nbo1 = elem1.nbOccurrence
                nbo2 = elem2.nbOccurrence
                numerateur = numerateur + max(nbo1, nbo2) - min(nbo1, nbo2)
                denom = denom + max(nbo1, nbo2)
                #print("fin")
                matching = True
                break
        
        if matching == False :
            #listeOcc.append( (elem1[1], 0) )
            numerateur = numerateur + elem1.nbOccurrence
            denom = denom + elem1.nbOccurrence

    for elem2 in l2 :
        for elem1 in l1 :
            if elem2.idMot.id == elem1.idMot.id :
                matching = True
                break
        
        if matching == False :
            #listeOcc.append( (0, elem2[1]) )
            numerateur = numerateur + elem2.nbOccurrence 
            denom = denom + elem2.nbOccurrence

   
    
    #for w in listeOcc :
    #numerateur = numerateur + max(w[0], w[1]) - min(w[0], w[1])
    #denom = denom + max(w[0], w[1])

    print(numerateur / denom)
    return numerateur / denom


def jaccard(l) :

    
    G = nx.Graph()

    for i in l :
        G.add_node(i)

    for i in l :
        for j in l :
            if i > j :
                
                iIndex = Index.objects.filter(idLivre=i).order_by('idMot_id')
                jIndex = Index.objects.filter(idLivre=j).order_by('idMot_id')
                print("fin recherche")

                # listeI = []
                # listeJ = []

                # #print(len(iIndex))
                # #print(len(jIndex))

                # for li in iIndex :
                #     #print(li.idMot.id)
                #     #print(li.nbOccurrence)
                #     listeI.append( (li.idMot.id, li.nbOccurrence) )

                # for lj in jIndex :
                #     listeJ.append( (lj.idMot.id, lj.nbOccurrence) )

                print(i)
                print(j)
                if ( distance( iIndex, jIndex  ) ) < 0.1 :
                    G.add_edge(i,j)

    return betweeness(G)


def distance (liste1, liste2):
    numerateur = 0
    denom = 0
    
    indice1 = 0
    indice2 = 0

    stop1 = False
    stop2 = False

    #print(len(liste1))
    #print(len(liste2))
    while True :
        #print( (indice1, indice2))
        if(indice1 >= len(liste1) and indice2 >= len(liste2)):
            print(numerateur / denom)
            return numerateur / denom 
        elif ((not stop1) and indice1 >= len(liste1) ):
            #print("stop1")
            stop1 = True
        elif ((not stop2) and indice2 >= len(liste2) ):
            #print("stop2")
            stop2 = True
            #indice2 = len(liste1) * 2
        
        else :
            if (not (stop1 or stop2)) and liste1[indice1].idMot.id == liste2[indice2].idMot.id :
                nbo1 = liste1[indice1].nbOccurrence
                nbo2 = liste2[indice2].nbOccurrence
                numerateur = numerateur + max(nbo1, nbo2) - min(nbo1, nbo2)
                denom = denom + max(nbo1, nbo2)
                indice1 = indice1 + 1
                indice2 = indice2 + 1
            elif stop2 :
                numerateur = numerateur + liste1[indice1].nbOccurrence
                denom = denom + liste1[indice1].nbOccurrence
                indice1 = indice1 + 1
            elif stop1 :
                numerateur = numerateur + liste2[indice2].nbOccurrence
                denom = denom + liste2[indice2].nbOccurrence
                indice2 = indice2 + 1
            elif  (liste1[indice1].idMot.id < liste2[indice2].idMot.id) :
                numerateur = numerateur + liste1[indice1].nbOccurrence
                denom = denom + liste1[indice1].nbOccurrence
                indice1 = indice1 + 1
            elif  (liste2[indice2].idMot.id < liste1[indice1].idMot.id) :
                numerateur = numerateur + liste2[indice2].nbOccurrence
                denom = denom + liste2[indice2].nbOccurrence
                indice2 = indice2 + 1


def distanceDic (liste1, liste2):
    numerateur = 0
    denom = 0
    
    dic1 = dict()
    dic2 = dict()

    for i1 in liste1:
        dic1[i1.idMot.id] = i1.nbOccurrence

    print("fin dic1")


    for i2 in liste2:
        dic2[i2.idMot.id] = i2.nbOccurrence
    
    print("fin dic2")

    for w in dic1.keys():
        if w not in dic2:
            numerateur = numerateur + dic1[w]
            denom = denom + dic1[w]
        else :
            numerateur = numerateur + max(dic1[w], dic2[w]) - min(dic1[w], dic2[w])
            denom = denom + max(dic1[w], dic2[w])

    print("retour")
    
    for w in dic2.keys():
        if w not in dic1:
            numerateur = numerateur + dic2[w]
            denom = denom + dic2[w]


    print(numerateur / denom)
    return numerateur / denom


    #listeResultat = []
    #listeResultat.sort(reverse=True, key=lambda a: a[1])









# 3 30
def distanceRequete (l1, l2, i1, i2) :

    print("distance")
    #listeOcc = []

    numerateur = 0
    denom = 0

    for elem1 in l1 :
        #matching = False

        res = Index.objects.filter(idMot_id = elem1.idMot.id, idLivre_id=i2)
        #print(res)

        if len(res) == 0 :
            numerateur = numerateur + elem1.nbOccurrence
            denom = denom + elem1.nbOccurrence
        else:
            elem2 = res[0]
            numerateur = numerateur + max(elem1.nbOccurrence, elem2.nbOccurrence) - min(elem1.nbOccurrence, elem2.nbOccurrence)
            denom = denom + max(elem1.nbOccurrence, elem2.nbOccurrence)
   
    for elem2 in l2 :
        res = Index.objects.filter(idMot_id = elem2.idMot.id, idLivre_id=i1)
        if len(res) == 0 :
            numerateur = numerateur + elem2.nbOccurrence 
            denom = denom + elem2.nbOccurrence

    print(numerateur / denom)
    return numerateur / denom


def betweeness (G) :
    res = []
    for v in G :
        bet = 0
        for t in G :
            for s in G :
                if s > t and s != v and t != v and nx.has_path(G,s,t):
                    shortestPathList = [ p for p in nx.all_shortest_paths(G, s, t) ]
                    nbPath = len(shortestPathList)

                    for x in shortestPathList :
                        if v in x : 
                            bet = bet + 1/nbPath
        
        res.append( (v, bet) )
    
    res.sort(reverse=True, key=lambda a: a[1])
    return res


