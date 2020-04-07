import json
from collections import deque
import turtle

# slovar
with open('slovar_besed_ter_sosedov.txt', 'r') as f:
    data = f.read()  # oblike str in ne iowrapper
    slovar = json.loads(data)


class Graph(object):

    def __init__(self, graph_slovar=None):
        """ Inicializira objekt graf.
            Če ni slovarja naredi prazen slovar.
        """
        if graph_slovar is None:
            graph_slovar = {}
        self.__graph_slovar = graph_slovar

    def vozlisca(self):
        """ Vrne seznam vozlišč grafa. """
        return list(self.__graph_slovar.keys())

    def __generiraj_stranice(self):
        """ Metoda ki generira stranice grafa.
            Stranice so predstavljene kot množice z enim ali dvema vozliščema.
            Vrne seznam množic.
        """
        stranice = []
        for vozlisce in self.__graph_slovar:
            for sosed in self.__graph_slovar[vozlisce]:
                if {sosed, vozlisce} not in stranice:  # izberem tipa množica ker nima vrstnega reda
                    stranice.append({vozlisce, sosed})
        return stranice

    def stranice(self):
        """ Vrne seznam stranic grafa. """
        return self.__generiraj_stranice()

    def __str__(self):
        """ Izpiše graf kot niz oblike
            vozlišča: ...
            stranice: ..."""
        niz = "vozlišča: "
        for i in self.__graph_slovar:
            niz += str(i) + " "
        niz += "\nstranice: "
        for stranica in self.__generiraj_stranice():
            niz += str(stranica) + " "
        return niz

    def osamljena_vozlisca(self):
        """ Vrne seznam vseh vozlišč ki so stopnje 0. """
        graph = self.__graph_slovar
        osamljena = []
        for voz in graph:
            if not graph[voz]:  # nima prijateljev
                osamljena.append(voz)
        return osamljena

    def najkrajsa_pot(self, bes1, bes2):
        """ Z uporabo algoritma 'Breadth-first-search'
        vrne najkrajšo pot med dvema besedama."""
        srecane = {bes1: [bes1]}
        x = deque()
        x.append(bes1)
        while len(x):  # len(x) > 0 is True
            trenutno = x.popleft()  # isto kot x.pop(0) samo hitreje
            for naslednji in self.__graph_slovar[trenutno]:  # po prijateljih
                if naslednji not in srecane:
                    srecam_zdaj = srecane[trenutno] + [naslednji]
                    srecane[naslednji] = srecam_zdaj
                    x.append(naslednji)
        return srecane.get(bes2)

    def narisi_pot(self, start, end, pot):
        """ Z uporabo Turtle grafično prikaže
            najkrajšo pot med dvema besedama."""
        slovar = self.__graph_slovar
        if len(pot) == 0:
            return 'ni povezave'
        if len(pot) == 1:
            risi_pot.write(start, align='center')
            return
        risi_pot.write(start, align='center', font=("Arial", 15, "normal"))
        pot = pot[1:]
        kot = 360 / len(slovar[start])
        # nariše vse prijatelje
        for bes1 in slovar[start]:
            risi_prijatelje.right(kot)
            risi_prijatelje.forward(70)
            risi_prijatelje.write(bes1, align='right')
            risi_prijatelje.back(70)
        # nariše naslednji korak v poti
        risi_pot.penup()
        risi_pot.forward(100)
        risi_pot.pendown()
        risi_pot.forward(300)
        risi_pot.penup()
        risi_pot.forward(100)
        risi_pot.pendown()
        risi_prijatelje.penup()
        risi_prijatelje.forward(500)
        risi_prijatelje.pendown()
        self.narisi_pot(pot[0], end, pot)


graph = Graph(slovar)

print('Naš graf vsebuje: {0} osamljenih besed'.format(len(graph.osamljena_vozlisca())))
print('Najkrajša pot med besedama jagoda ter zadremati je: {0}'.format(graph.najkrajsa_pot('jagoda', 'zadremati')))
print('Pot je dolžine: {0}'.format(len(graph.najkrajsa_pot('jagoda', 'zadremati'))))

turtle.setup()
turtle.screensize(6000, 6000)
risi_pot = turtle.Turtle()
risi_prijatelje = turtle.Turtle()
risi_pot.color('red')
risi_pot.pensize(2)
risi_pot.speed('fast')
risi_prijatelje.speed('fast')
pot = graph.najkrajsa_pot('slon', 'maček')
graph.narisi_pot('slon', 'maček', pot)
risi_pot.screen.exitonclick()

