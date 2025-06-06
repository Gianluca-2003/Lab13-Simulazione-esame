import copy

import networkx as nx

from database.DAO import DAO
from model.driver import Driver


class Model:
    def __init__(self):
        self._bestTasso = None
        self._dreamTeam = None
        self._edges = None
        self._nodes = []
        self._graph = nx.DiGraph()
        self._idMap = {}


    def getAllYears(self):
        return DAO.getAllYears()




    def buildGraph(self,anno):
        self._graph.clear()
        self._nodes = DAO.getAllNodes(anno)
        self.fillIdMap()
        self._graph.add_nodes_from(self._nodes)
        self._edges = DAO.getAllEdges(anno,self._idMap)
        for edge in self._edges:
            self._graph.add_edge(edge[0],edge[1],weight=edge[2])




    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)


    def fillIdMap(self):
        self._idMap = {}
        for node in self._nodes:
            self._idMap[node.driverId] = node

    def calcolaVittorie(self,node: Driver):
        vittorie = 0
        sconfitte = 0
        for edge in self._edges:
            if node == edge[0]:
                vittorie += 1
            if node == edge[1]:
                sconfitte += 1
        return vittorie-sconfitte

    def calcolaVittoriePeso(self,node: Driver):
        vittorie = 0
        sconfitte = 0
        for edge in self._edges:
            if node == edge[0]:
                vittorie += self._graph[edge[0]][edge[1]]['weight']
            if node == edge[1]:
                sconfitte += self._graph[edge[0]][edge[1]]['weight']
        return vittorie-sconfitte

    def trovaVincitore(self):
        vincitore = None
        best_score = 0
        for node in self._nodes:
            if self.calcolaVittorie(node) > best_score:
                best_score = self.calcolaVittorie(node)
                vincitore = node
        return vincitore


    def trovaDreamTeam(self, k):
        self._bestTasso = 1000000
        self._dreamTeam = []
        #passo parziale[primo nodo]
        #passo ecslusi[tutti gli altri]
        #calcolo il tasso di sconfitta: numero di vittorie degli esclusi su parziale
        esclusi = copy.deepcopy(self._nodes)
        for node in self._nodes:
            parziale = [node]
            esclusi.remove(node)
            self.ricorsione(k,parziale, esclusi)
            parziale.pop()
            esclusi.append(node)

        return self._dreamTeam





    def ricorsione(self, k,parziale, esclusi):
        if len(parziale) == k:
            tasso = self.calcolaTassoSconfitta(parziale,esclusi)
            if  tasso < self._bestTasso:
                self._bestTasso = tasso
                self._dreamTeam = copy.deepcopy(parziale)
        else:
            for node in self._nodes:
                if node not in parziale:
                    parziale.append(node)
                    esclusi.remove(node)
                    self.ricorsione(k,parziale, esclusi)
                    parziale.pop()
                    esclusi.append(node)





    def calcolaTassoSconfitta(self,parziale,esclusi):
        tasso = 0
        for u in esclusi:
            for  v in parziale:
                if self._graph.has_edge(u,v):
                    tasso += self._graph[u][v]['weight']
        return tasso





