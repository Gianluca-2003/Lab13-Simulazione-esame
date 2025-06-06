import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._yearSelected = None

    def handleDDYearSelection(self, e):
        self._yearSelected = self._view._ddAnno.value



    def handleCreaGrafo(self,e):
        if self._yearSelected is  None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore. Devi selezionare un anno", color='red'))
            self._view.update_page()
            return
        self._model.buildGraph(self._yearSelected)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamnte creato.\n"
                                                      f"N nodi: {self._model.getNumNodes()} e "
                                                      f"N archi: {self._model.getNumEdges()}"))
        bestPilota = self._model.trovaVincitore()
        self._view.txt_result.controls.append(ft.Text(f"Il vincitore è {bestPilota}! "))

        self._view._txtIntK.disabled = False
        self._view._btnCerca.disabled = False

        self._view.update_page()


    def handleCerca(self, e):
        kInput = self._view._txtIntK.value
        if kInput is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore. Devi insire un valore k.", color='red'))
            self._view.update_page()
            return
        try:
            k = int(kInput)
            dreamTeam = self._model.trovaDreamTeam(k)
            if len(dreamTeam) != 0:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"I piloti del dream team sono:"))
                for pilota in dreamTeam:
                    self._view.txt_result.controls.append(ft.Text(f"{pilota}"))
                self._view.update_page()
            else:
                self._view.txt_result.controls.clear()
                self._view.txt_result.controls.append(ft.Text(f"Non è possibile trovare un dream team."))
                self._view.update_page()

        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Errore. Devi insire un valore k intero.", color='red'))
            self._view.update_page()
            return



    def fillDDYears(self):
        anni = self._model.getAllYears()
        for year in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(year))
