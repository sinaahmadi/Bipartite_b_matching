#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
"""
    Created on Mon July 24 2018
    @author: Sina Ahmadi  (sina.ahmadi@insight-centre.org)
    Based on the code for IJCAI 2017 paper titled "Diverse Weighted Bipartite b-Matching"
    by Ahmed, Faez, John P. Dickerson, and Mark Fuge
    https://github.com/faezahmed/diverse_matching/
"""
from gurobipy import *
import numpy as np

class WBbM:
    """Weighted Bipartite b-Matching (WBbM) algorithm"""
    def __init__(self, num_left, num_right, W, lda, uda, ldp, udp, LogToConsole=0):
        self.num_left = num_left
        self.num_right = num_right
        self.W = W
        self.lda = lda
        self.uda = uda
        self.ldp = ldp
        self.udp = udp
        self.LogToConsole = LogToConsole

    def linkmatr(self, num_left, num_right):
        """ Creates link matrix A for constraint satisfaction """
        num_nodes = self.num_left + self.num_right
        str1 = [1] * self.num_right
        str2 = [0] * self.num_right
        A = [None] * (num_nodes)
        for i in range(self.num_left):
            A[i] = str2 * self.num_left
            #print A[i]
            idx = self.num_right * i
            A[i][idx:idx + self.num_right] = str1
        for j in range(self.num_right):
            A[self.num_left+j] = str2 * self.num_left
            idx = [j + self.num_right * l for l in range(self.num_left)]
            for k in range(self.num_left):
                A[self.num_left + j][idx[k]] = 1      
        return A
    
    def Bb_matching(self, optimization_mode="max"):
        """ Solves the matching problem """
        m = Model("naisc_matching")
        m.setParam("LogToConsole", self.LogToConsole)

        total_nodes = self.num_left + self.num_right
        total_vars = self.num_left * self.num_right
        
        if((self.num_left * self.lda > self.num_right * self.udp) or (self.num_right * self.ldp > self.num_left * self.uda)):
            raise Exception("Infeasible Problem")
        
        # Maximum Number of authors matched to node paper
        if type(self.udp).__name__ == "int":
            Dmax = list(self.udp * np.ones((total_nodes,)))
        elif type(self.udp).__name__ == "list":
            Dmax = list(0 * np.ones((self.num_right,))) + self.udp
        else:
            raise Exception("udp value not correct.")
        
        # Minimum Number of authors matched to a paper
        Dmin = list(self.ldp * np.ones((total_nodes,)))
        
        # Minimum Number of papers matched to an author
        Dmina = list(self.lda * np.ones((total_nodes,)))
        
        # Maximum number of papers matched to author
        if type(self.uda).__name__ == "int":
            Dmaxa = list(1 * np.ones((total_nodes,)))
        elif type(self.uda).__name__ == "list":
            Dmaxa = self.uda
        else:
            raise Exception("uda value not correct.")
        
        A = self.linkmatr(self.num_left, self.num_right)
        
        x = dict()
        for j in range(total_vars):
          x[j] = m.addVar(vtype=GRB.BINARY, name="x" + str(j))
        
        # objective
        if optimization_mode=="max":
            m.setObjective((quicksum(self.W[i]*x[i] for i in range(total_vars))), GRB.MAXIMIZE)
        elif optimization_mode=="min":
            m.setObjective((quicksum(self.W[i]*x[i] for i in range(total_vars))), GRB.MINIMIZE)
        else:
            raise ValueError("Optimization mode not recognized.")
        
        # constraint on paper cardinality
        for i in range(self.num_left, total_nodes):
            m.addConstr(quicksum(A[i][j] * x[j] for j in range(total_vars)) <= Dmax[i])
            m.addConstr(quicksum(A[i][j] * x[j] for j in range(total_vars)) >= Dmin[i])
                
        # constraint on authors
        for i in range(self.num_left):
            m.addConstr(quicksum(A[i][j]*x[j] for j in range(total_vars)) <= Dmaxa[i])
            m.addConstr(quicksum(A[i][j]*x[j] for j in range(total_vars)) >= Dmina[i])  

        #m.write("lp.mps")    
        
        m.optimize()   
        
        res = np.zeros((self.num_left, self.num_right))
        for i in range(self.num_left):
            for j in range(self.num_right):
                idx = self.num_right*i + j
                res[i,j] = m.getVars()[idx].x
           
        status = m.status
        if status == GRB.Status.UNBOUNDED:
            print('The model cannot be solved because it is unbounded')
        elif status == GRB.Status.OPTIMAL:
            print('The optimal objective is %g' % m.objVal)
        elif status != GRB.Status.INF_OR_UNBD and status != GRB.Status.INFEASIBLE:
            print('Optimization was stopped with status %d' % status)
            
        return res, m.objVal