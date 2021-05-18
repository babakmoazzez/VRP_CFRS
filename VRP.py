from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import random
from TSP import solve_tsp

'''solves a VRP problem using Cluster-First-Route-Second algorithm. Clustering is done using K-Means and Routing is done by solving a tsp to optimality using Gurobi.'''

#total number of points
n=400

#points are generated randomly on the plane
X=np.array([[random.randint(-1000,1000),random.randint(-1000,1000)] for i in range(n)])

#Cluster points using K-Means algorithm 
kmeans = KMeans().fit(X)
#if you want a certain number of clusters like p, do "kmeans = KMeans(n_clusters = p).fit(X)" instead 
#print(kmeans.labels_)
#print(kmeans.n_clusters)

#show clustered points
#plt.scatter(X[:, 0], X[:, 1], c=kmeans.labels_)

#each cluster is a class
Classes=[[] for i in range(max(kmeans.labels_)+1)]
for i in range(len(X)):
    Classes[kmeans.labels_[i]]+=[(X[i][0],X[i][1])]


#pass each cluster to TSP solver and get the optimal solution
tours=[]
for i in Classes:
    if len(i)==1:
        tours.append([[(0,0),i[0]]])
    else:
        sol_raw = solve_tsp([(0,0)]+i)
        j = [(0,0)]+i
        sol=[[j[x],j[y]] for x,y in sol_raw]
        tours.append(sol)

#plot the solution
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

plt.show()







