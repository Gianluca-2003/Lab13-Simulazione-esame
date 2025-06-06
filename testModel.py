from model.model import Model

myModel = Model()


myModel.buildGraph(2009)


print("N nodi:",myModel.getNumNodes(),"N archi:", myModel.getNumEdges())


bestTeam = myModel.trovaDreamTeam(3)
for node in bestTeam:
    print(node)