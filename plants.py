from collections import namedtuple

Plant = namedtuple('Plant', ['name', 'temp', 'minMoist', 'maxMoist'])
Plants = {
            'Agawa':Plant('Agawa',25,1,40),
            'Cebula':Plant('Cebula',12,75,90),
            'Kaktus':Plant('Kaktus',30,1,40),
            'Kocimiętka':Plant('Kocimiętka',15,21,40),
            'Malina':Plant('Malina',15,21,60),
            'Ogórek':Plant('Ogórek',25,60,80),
            'Pomidor':Plant('Pomidor',20,60,80),
            'Sałata':Plant('Sałata',15,70,75),
            'Truskawka':Plant('Truskawka',10,21,60),
            'Tulipan':Plant('Tulipan',6,21,60),
            'Żurawina':Plant('Żurawina',22,61,80)
        }
