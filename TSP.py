from gurobipy import *
import networkx as nx

def distance(p1,p2):
    '''Euclidean distance'''
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def subtourelimination(model, where):
    '''callback to add subtour elimination constraints as lazy cuts'''
    if where == GRB.callback.MIPSOL:
        n=model._n
        sol={}
        x=[]
        for i in range(n):
            for j in range(i+1,n):
                if model.cbGetSolution(model._variables[i,j])>0.99:
                    x+= [(i,j)]
        
        cycle = subtour(x,n)
        if len(cycle) < n:
            l = 0
            
            for i,j in cycle:
                l += model._variables[i,j]
            model.cbLazy(l <= len(cycle)-1)

def subtour(edges,n):
    '''find a subtour in the given solution, networkx is used to find cycles'''
    g=nx.Graph()
    for (i,j) in edges:
        g.add_edge(i,j)
    all_cycles = []    
    visited = [0]*n
    v = 0
    while sum(visited) < n:
        all_cycles.append(nx.find_cycle(g,v))
        for (i,j) in all_cycles[-1]:
            visited[i] = 1
        if 0 in visited:
            v = visited.index(0)
    
    return min(all_cycles,key = lambda x: len(x))

def solve_tsp(points):
    '''solves a tsp on the given set of points. points are given as a list of tuples [(x1,y1),(x2,y2),...]'''
    
    n=len(points)
    m = Model()
    m.setParam('LogToConsole', 0)
    # Create Variables
    variables = {}
    for i in range(n):
        for j in range(i+1):
            variables[i,j] = m.addVar(0,1,distance(points[i],points[j]),GRB.BINARY,name='x_'+str(i)+'_'+str(j))
            variables[j,i] = variables[i,j]
        m.update()

    #Create Constraints
    for i in range(n):
        m.addConstr(quicksum(variables[i,j] for j in range(n) if j!=i) == 2)
    
    m.update()

    # Optimize model
    m._n = n
    m._variables = variables
    m.params.LazyConstraints = 1
    m.optimize(subtourelimination)

    
    x = [(i,j) for i in range(n) for j in range(i+1,n) if variables[i,j].X > 0.99]
    return x

if __name__ == '__main__':
    n=12
    a=solve_tsp([(0,0),(1,1),(2,1),(3,3),(4,9),(-10,3),(-6,-4),(-7,15),(5,-10),(4,-2),(1,4),(5,0)])
    print(a)
    