from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import random
from sklearn.cluster import DBSCAN
from TSP import solve_tsp


n=300

X=np.array([[random.randint(-1000,1000),random.randint(-1000,1000)] for i in range(n)])
'''X1=np.array([[random.randint(50,100),random.randint(50,100)] for i in range(n)])
X2=np.array([[random.randint(-100,-50),random.randint(50,100)] for i in range(n)])
X3=np.array([[random.randint(-100,-50),random.randint(-100,-50)] for i in range(n)])
X4=np.array([[random.randint(50,100),random.randint(-100,-50)] for i in range(n)])
X=np.concatenate((X1,X2,X3,X4))'''

kmeans = KMeans(n_clusters = 5).fit(X)
print(kmeans.labels_)
print(kmeans.n_clusters)
#a=kmeans.predict([[0, 0], [12, 3],[2,3]])


plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)
Classes=[[] for i in range(max(kmeans.labels_)+1)]
for i in range(len(X)):
    Classes[kmeans.labels_[i]]+=[(X[i][0],X[i][1])]



tours=[]
for i in Classes:
    print([(0,0)]+i)
    if len(i)==1:
        tours.append([(0,np.where(X==i)[0][0])])
    else:
        sol_raw = solve_tsp([(0,0)]+i)
        j = [(0,0)]+i
        sol=[[j[x],j[y]] for x,y in sol_raw]
        tours.append(sol)
        print("...",sol)
    

print(tours)
#np.insert(X,0,[0,0],axis=0)
from matplotlib import collections  as mc
import pylab as pl
fig, ax = pl.subplots()
colors=["r","g","b", "c","y","m","k"]
c=0
for i in tours:
    
    lc = mc.LineCollection(i, color = colors[c%7], linewidths=2)
    c+=1
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    #plt.plot([(X[c[0]][0],X[c[0]][1]) for c in i])

plt.show()







