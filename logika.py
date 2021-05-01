# Logika za igro
IGRALEC_R = 1
IGRALEC_Y = 2
PRAZNO = 0

NEODLOCENO = 3
NI_KONEC = 4

NUM_COLS = 7
NUM_ROWS = 6
MAX_POTEZ = NUM_COLS * NUM_ROWS

def nasprotnik(igralec):
    if igralec == IGRALEC_R:
        return IGRALEC_Y
    elif igralec == IGRALEC_Y:
        return IGRALEC_R
    else:
        assert False, f"neveljaven nasprotnik: {igralec}"

class ConnectFour:
    def __init__(self, na_potezi=IGRALEC_R):
        # Ustvarimo igralno povrsino
        self.board = [[PRAZNO]*NUM_ROWS for _ in range(NUM_COLS)]

        # Ustvarimo seznam, ki bo vodil stevilo krozcev v vsakem stolpcu
        self.vrstice = [0] * NUM_COLS

        # Dolocimo igralca, ki je na potezi
        self.na_potezi = na_potezi

        # Stejemo stevilo odigranih potez
        self.stevilo_potez = 0
    
    def kopija(self):
        G = ConnectFour(self.na_potezi)
        G.board = [[i for i in col] for col in self.board]
        G.vrstice = [i for i in self.vrstice]
        G.stevilo_potez = self.stevilo_potez
        return G
    
    def veljavne_poteze(self):
        '''Vrne seznam veljavnih potez.'''
        # Veljavne poteze so vsi stolpci, ki imajo vsaj eno prazno mesto
        # return [i for i in range(len(self.board)) if self.board[i][-1] == PRAZNO]
        return [i for i in range(NUM_COLS) if self.vrstice[i] < NUM_ROWS]
    
    def stanje_po_potezi(self, p):
        # Odigrana je bila poteza p s pripadajoco vrstico j
        j = self.vrstice[p] - 1
        barva = self.board[p][j]

        # Preverimo, ce je del vertikalne resitve
        if j>=3:
            for i in range(3):
                if self.board[p][j-i-1] != barva:
                    break
            else:
                stirka = [(p,j-3+i) for i in range(4)]
                return self.na_potezi, stirka

        # Preverimo, ce je del vodoravne resitve
        stevec = 1
        min_col = p
        i = 1
        while p+i < NUM_COLS and self.board[p+i][j] == barva:
            i += 1
        stevec += i-1
        i = 1
        while p-i >= 0 and self.board[p-i][j] == barva:
            min_col = p-i
            i += 1
        stevec += i-1
        if stevec == 4:
            # Nasli smo vodoravno resitev
            stirka = [(min_col+i,j) for i in range(4)]
            return self.na_potezi, stirka
        
        # Preverimo, ce je del narascujoce diagonalne resitve
        stevec = 1
        i = 1
        while p+i < NUM_COLS and j+i < NUM_ROWS and self.board[p+i][j+i] == barva:
            i += 1
        stevec += i-1
        i = 1
        while p-i >= 0 and j-i >= 0 and self.board[p-i][j-i] == barva:
            i += 1
        dx = i-1
        stevec += i-1
        if stevec == 4:
            # Nasli smo resitev na narascujoci diagonali
            stirka = [(p-dx+i,j-dx+i) for i in range(4)]
            return self.na_potezi, stirka
        
        # Preverimo, ce je del padajoce diagonalne resitve
        stevec = 1
        i = 1
        while p+i < NUM_COLS and j-i >= 0 and self.board[p+i][j-i] == barva:
            i += 1
        stevec += i-1
        i = 1
        while p-i >= 0 and j+i < NUM_ROWS and self.board[p-i][j+i] == barva:
            i += 1
        dx = i-1
        stevec += i-1
        if stevec == 4:
            # Nasli smo resitev
            stirka = [(p-dx+i,j+dx-i) for i in range(4)]
            return self.na_potezi, stirka
        
        # Ni zmagovalca -> preverimo, ce je igre konec
        if self.stevilo_potez == MAX_POTEZ:
            return NEODLOCENO, None
        else:
            return NI_KONEC, None

    
    def odigraj_potezo(self, p, check=False):
        '''Odigraj potezo p, ce je veljavna, sicer ne naredi nic.
        V primeru, da je check=False, ne preverimo, ce je poteza veljavna.'''
        if check and self.vrstice[p] < NUM_ROWS:
            # Poteza p ni veljavna
            return None
        
        # Dolocimo v katero vrstico bo dodan krozec pri potezi p
        j = self.vrstice[p]
        self.vrstice[p] += 1

        # Odigramo potezo
        self.board[p][j] = self.na_potezi
        self.stevilo_potez += 1

        # Preverimo, ce je igre konec
        zmagovalec, stirka = self.stanje_po_potezi(p)

        if zmagovalec == NI_KONEC:
            # Igra se nadaljuje
            self.na_potezi = nasprotnik(self.na_potezi)
            return None
        else:
            self.na_potezi = None
            return zmagovalec, stirka
    
    def odstrani_potezo(self, p, check=False):
        '''Odstrani potezo p, ce je veljavna, sicer ne naredi nic.
        V primeru, da je check=False, ne preverimo, ce je poteza veljavna.'''
        if check and self.vrstice[p] == 0:
            # Poteza p ni veljavna
            return None
        
        # Dolocimo iz katere vrstice brisemo krogec
        j = self.vrstice[p]
        self.vrstice[p] -= 1

        # Odstranimo potezo
        self.board[p][j] = PRAZNO
        self.stevilo_potez -= 1