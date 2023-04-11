# ===========================================================================================
# ATSAUCES :
# (1) SPĒLES KOKA IZVEIDES ALGORITMS - PARAUGS, KAS TIKA DOTS 2.MODULĪ: 
# https://estudijas.rtu.lv/mod/resource/view.php?id=2826268
# (2) Yiğit PIRILDAK - Mastering Tic-Tac-Toe with Minimax Algorithm in Python:
# https://levelup.gitconnected.com/mastering-tic-tac-toe-with-minimax-algorithm-3394d65fa88f
# ===========================================================================================

# Pakešu imports ============================================================================
# Importēt visu pilnībā no tkinter pakotnes, nācās 2 reizes vadīt, jo dažas pakotnes tikai ar 2. rindu neievadījās.
import tkinter as tk
from tkinter import *
# Messagebox tiek izmantots pie Settings izveides, lai varētu izvadīt paziņojumus par nepareizu izvēli Settings parametriem.
from tkinter import messagebox
# Functools partial tiek izmantots tā kā tkinter pogās, ja ir nepieciešams ievadīt komandas funkcijas parametrus, tad to 
# nevar izdarīt bez partial(funkcija, parametrs/-i)
from functools import partial
# ===========================================================================================

# Spēles loģika un inicializācija ===========================================================
# Pašas spēles klase, kurā es izveidoju visas nepieciešamās spēles loģikai funkcijas, lai tās var izmantot no jauna pēc nepieciešamības.
class Game:
    # Inicializācijā izveidoju 2 parametrus, kas ir score jeb šī brīža rezultāts un gājieni, lai spēles loģika varētu noteikt, kurš spēlētājs
    # tagad veiks savu gājienu. Kā arī uzsāk spēles koka ģenerāciju, tad izvada to konsolē, lai varētu pārbaudīt vai tas ģenerējas pareizi
    def __init__(self, score=3, maxScore=21, startingPlayer="Player"):
        # Izveido spēles sākuma parametrus
        self.score = score
        self.maxScore = maxScore
        self.startingPlayer = startingPlayer
        self.currentPlayer = startingPlayer
        # Spēles inicializācijā ievelk iekšā global vērtību j, kas tiek izmantota spēles koka elementu ID izveidei. (1)
        global j 
        # Te tas atkārtojas, lai ja restartē spēli, koks ģenerētos ar pareiziem virstoņu elementu ID
        j = 2
        self.turns = 1

        # (1) ATSAUCE
        # Spēles koka izveide, kurā izmantoju kursā sniegto materiālu paraugu spēles koka izveidei. Koks ir diezgan vienkāršs 
        # līdz ar to pie maziem gala rezultātiem varu ģenerēt pilno koku uzreiz.
        self.gTree = gameTree()
        self.generatedNodes = []
        # Izveido pirmo virsotni kokā ar sākuma rezultātu un 0.līmeni
        self.gTree.addNode(treeElement('A1', score, 0))
        self.generatedNodes.append(['A1', score, 0])
        # Pievieno virsotnes līdz vairs nevienas virsotnes nav pie generatedNodes
        while len(self.generatedNodes)>0:
            # Pārliecinās, ka virsotnes score daļai nav lielāks rezultāts par max rezultātu.
            if self.generatedNodes[0][1] >= self.maxScore:
                pass
            else:
                # Pievieno virsotni uz kreiso pusi, jeb virsotni kurā pie rezultāta pieskaita 3
                checkMoves(3, self.generatedNodes, self.generatedNodes[0], self.gTree)
                # Pievieno virsotni uz labo pusi, jeb virsotni kurā pie rezultāta pieskaita 4
                checkMoves(4, self.generatedNodes, self.generatedNodes[0], self.gTree) 
            # Kad virsotne tiek pārbaudīta to izņem no generatedNodes.
            self.generatedNodes.pop(0)
        
        # Šis ir nepieciešams, lai varētu pārbaudīt koka vērtības konsolē un salīdzinātu ar roku zīmēto koku
        #for x in self.gTree.treeNodes:
        #    print(x.elementID, x.score, x.level)
        # Šis izvada visus savienojumus starp vērtībām.
        #for x, y in self.gTree.nodeConnections.items():
        #    print(x, y)         
        # (1) ATSAUCES BEIGAS

    # Addition jeb pieskaitīšana tiek izmantota gājienā, lai pieskaitītu 3 vai 4 (+pieskaita 1 gājienu)
    def add(self, addition):
        self.score += addition
        self.turns += 1

    # (2) ATSAUCE
    # Izmantojot sniegto estudijās paraugu pārveidoju šo algoritmu priekš savas spēles
    def minimax(self, currentNode, isMax):
        # Sākumā tiek pārbaudīts vai vispār ir vērts iet cauri tālākajām rekursijas iterācijām,
        # tas pārbauda principā vai tā jau nav gala virsotne. Ja ir tā vienkārši atgriež šī brīža
        # rezultātu.
        if currentNode.score >= self.maxScore:
            return currentNode.score
        # Tālāk ar else if palīdzību tiek pārbaudīts vai vērtība ir jāparbauda kā maksimizēšanas vērtība
        elif isMax:
            # Uzliek mazāko iespējamo vērtību
            maxSC = float('-inf')
            # Iet cauri nodeConnections vērtībām, līdz atrod noteiktās virsotnes pēcteču elementu ID
            for nextNode in self.gTree.nodeConnections[currentNode.elementID]:
                # Tad izmantojot izveidoto findNode funkciju(nācās izveidot, lai vieglāk varētu atrast šīs vērtības),
                # atrod katru pēcteci un pārbauda tos izmantojot minimax algoritmu.
                nextNode = self.gTree.findNode(nextNode)
                score = self.minimax(nextNode, False)
                maxSC = max(maxSC, score)
            return maxSC
        # Viss tieši tas pats ar minimizācijas vērtību, kas augstāk ar maksimizācijas vērtību.
        else:
            minSC = float('inf')
            for nextNode in self.gTree.nodeConnections[currentNode.elementID]:
                nextNode = self.gTree.findNode(nextNode)
                score = self.minimax(nextNode, True)
                minSC = min(minSC, score) 
            return minSC     
    
    # Iegūst "labāko" maksimuma gājienu(pēc minimax algoritma), jo šajā gadījumā esmu izveidojis, ka dators ir maksimizātors jebkurā gadījumā
    def getBestMove(self, currentNode):
        bestVal = float('-inf')
        bestMove = None # bestVal un bestMove tiek izmantoti priekš salīdzināšanas gājienu
        # Atkal iet cauri pēctečiem, lai varētu tos salīdzināt un nodot tieši labāko.
        for nextNode in self.gTree.nodeConnections[currentNode.elementID]:
            nextNode = self.gTree.findNode(nextNode)
            # Nodod mazāko minimax rezultātu 
            nextVal =  self.minimax(nextNode, True)
            # pārbauda vai jaunā vērtība ir lielāka un ja ir to samaina ar bestVal
            if nextVal > bestVal:
                bestVal = nextVal
                # pieliek labāko gājienu pie bestMove, ko arī atgriež 
                bestMove = nextNode.score - currentNode.score
        # Lai pārbaudītu kādas vērtības viņš izvēlās ( atkal konsolē )
        #print(bestMove)
        return bestMove # Atgriež labāko vērtību par kuru kustēties.
    # (2) ATSAUCES BEIGAS
# ===========================================================================================

# Spēles koka datu struktūras izveide =======================================================
# (1) ATSAUCE
# Šī klase ir izveidota, lai izveidotu katras virsotnes datu struktūru, tajā ietilpst elementa ID piem(A1 ; A2 ; A3 ; Ai...), noteiktā stāvokļa rezultāts un virsotnes līmenis
class treeElement:
    def __init__(self, elementID, score, level):
        # elementID ir paredzēts katras virsotnes unikālai identificēšanai
        self.elementID = elementID
        # virsotnes stāvokļa rezultāts
        self.score = score
        # virsotnes līmenis
        self.level = level

# Koka klases inicializācija/struktūra. Veidota pēc (1) atsauces parauga, bet pievienoju vēl divas funkcijas, viena ir findNode, kas atrod pēc ID un findCurrentState,
# kura meklē pēc rezultāta un līmeņa, lai vieglāk varētu atrast tā brīža virsotni un atrast vēlreiz ātrāko ceļu negaidītu izmaiņu gadījumā.
class gameTree:
    # Inicializācija, kurā ietilpst masīvs ar katru virsotni un vārdnīca ar visiem savienojumiem teiksim A1 : ('A2', 'A3')
    def __init__(self):
        self.treeNodes = []
        self.nodeConnections = dict()
    # Šo funckiju izmanto, lai pievienotu katru izveidoto treeElement klases struktūru pie koka jeb katru virsotni pievienotu.
    def addNode(self, node):
        self.treeNodes.append(node)
    # Šo funckiju izmanto, lai pievienotu pie virsotnes pēctečus. (Tikai elementID tiek pievienots, ko vēlāk izmantoju priekš minimax algoritma realizācijas, jo tur jāskatās pēcteči)
    def addConnection(self, fromNode, toNode):
        self.nodeConnections[fromNode] = self.nodeConnections.get(fromNode,[])+[toNode]
    # Šī funkcija tiek izmantota, lai atrastu virsotnes struktūrā pēc elementa ID, tas atvieglo dzīvi teiksim minimax algoritmā, kur pārbauda virsotnes pēctečus un iegūst tikai elementa
    # ID, bet netiek nekādi dati no tā iegūti
    def findNode(self, elementID):
        for selNode in self.treeNodes:
            if elementID == selNode.elementID:
                return selNode
    # Šī funkcija tiek izmantota, lai atrastu šī brīža stāvokli kokā, jo lai katru reizi neņemtu ārā virsotnes ātrāk ir atrast to vēlreiz un uzsākt minimax algoritma pārbaudi vēlreiz tieši
    # no noteiktā stāvokļa nekā pārbaudīt atkal pilnībā visas virsotnes.
    def findCurrentState(self, score, level):
        for selNode in self.treeNodes:
            if score == selNode.score and level == selNode.level:
                return selNode

# Koka ģenerācijas algoritms, kas tiek izmantots Game klasē. (Šī funkcija nav zem nevienas klases palika, tā ir main atstāta)
# Šis algoritms pamatā ir paņemts no arī (1) atsauces parauga, bet izveidoju pēc savas spēles vajadzībām.
# Funkcijai tiek nodots gājiena veids(+3 vai +4), tad nodod jau ģenerētās pirmstam virsotnes, tad tā brīža stāvokli nodod
# un kā pēdējo nodod pašu koku. Nācās pievienot koka nodošanu, jo koku inicializēju iekš citas klases.
def checkMoves(moveType, generatedNodes, currentNode, gTree):
        # Tiek ievilkts globālais mainīgais j, lai to varētu izmantot elementa ID izveidē. Pēc katras iterācijas tas pieskaita vieninieku
        # lai nākamās virsotnes ID būtu savādāks
        global j
        newID = 'A' + str(j)
        j+=1
        # Tiek izveidota pati virsotne ar jauno ID, šī brīža stāvoklis + gājiena tips(nākamais rezultāts) un protams līmeņa maiņa jeb par vienu tā tiek palielināta
        newNode = treeElement(newID, currentNode[1] + moveType, currentNode[2] + 1)
        # Šis mainīgais tiek izmantots skenēšanas laikā, lai pārbaudītu vai neatkārtosies virsotne
        nodeExists = False
        # Iterācijas mainīgais
        i=0
        # Cikls, kas iterē cauri visām virsotnēm līdz vai nu tiek atrasta tāda pati virsotne(kurai sakrīt gan rezultāts, gan līmenis) vai tiek iziets cauri
        # visām virsotnēm (len(virsotņu kopa)-1, jo len izvada par vienu vairāk, bet masīvs sākās no nulles indeksa)
        while(not nodeExists) and (i<=len(gTree.treeNodes)-1):
            if (gTree.treeNodes[i].score==newNode.score) and (gTree.treeNodes[i].level==newNode.level):
                # ja sakrīt līmenis un rezultāts, tad atzīmē, ka tāda virsotne ir
                nodeExists = True
            else:
                # ja ne ar vienu nesakrīt, tad tas turpina iterēt cauri.
                i+=1
        # Šis if pārbauda, ja nodeExists==False, tad tas pievieno augstāk izveidoto virsotni pie spēles koka gTree un pievieno to pie izveidotajām virsotnēm, un
        # un izveido savienojumu starp iepriekšējo un tagadējo virsotni(pievieno to kā pēcteci)
        if not nodeExists:
            # Pievieno jauno virsotni
            gTree.addNode(newNode)
            # Pievieno pie izveidotajām virsotnēm, ko izmanto ciklā Game funkcijā
            generatedNodes.append([newID, currentNode[1] + moveType, currentNode[2] + 1])
            # Pievieno savienojumu starp iepriekš izveidoto virsotni un pēcteci
            gTree.addConnection(currentNode[0], newID)
        # Ja neizpildās pirmais if statement, tad tas pievieno savienojumu ar iepriekš jau izveidoto pēcteci.
        else:
            # noņem vienu iterāciju no globālā j mainīgā, jo netiek izveidota jauna virsotne tā kā tāda jau eksistē.
            j-=1
            gTree.addConnection(currentNode[0], gTree.treeNodes[i].elementID)
# (1) ATSAUCES BEIGAS
# ===========================================================================================

# GUI izveide ===============================================================================
# Šī klase ģenerē interfeisu un līdz ar to arī uzsāk NewGame mainīgo pie spēles sākuma.
class interface:
    def __init__(self, startingScore=3, maxScore=21, startingPlayer='Player'):
        # izveido root kā mainīgo, jeb tkinter izsaukšanas metodi/logu
        self.root = tk.Tk()
        # Nomaina augšā logā nosaukumu no Untitled uz Summē!
        self.root.title('Summē!')
        # Izveido sākumvērtības, lai tās varētu mainīt zem Settings
        self.startingScore = startingScore
        self.maxScore = maxScore
        self.startingPlayer = startingPlayer
        # Nomaina loga ģeometriju un noņem iespēju mainīt izmēru, jo dizains ir izveidots noteiktam loga izmēram
        self.root.geometry("400x400")
        self.root.resizable(0,0)
        # Nomaina fonu uz toni ar hex krāsām
        self.root.configure(background='#1d1e22')
        # Izsauc funkciju, kas izveido pogas Menu
        self.menuButtons()
        # Inicializē logu
        self.root.mainloop()

    # Šo funkciju izmanto, lai vairākkārtīgi varētu mainīt starp logiem pie nepieciešamības
    def menuButtons(self):
        # Logo izveide ( neizmantoju bildi, bet vienkārši tekstu ar formatējumu )
        self.logo = tk.Label(self.root, text = "Summē!", bg='#1d1e22', fg='#d4d4dc', padx = 16, pady = 3, font="Ariel 70 bold", justify ='center')
        self.logo.grid(row=1, column=1)
        # Start poga, kas izsauc funkciju startGame
        self.startButton = tk.Button(self.root, text = "Start", command = self.startGame, bg='#393f4d', fg='#d4d4dc') 
        self.startButton.grid(row = 2, column = 1, pady = 3, ipadx=150, ipady=20)
        # Settings poga, izsauc funkciju gameSettings, kurā iespēja ievadīt izmaiņas spēles nosacījumos.
        self.settingsButton = tk.Button(self.root, text = "Settings", command = self.gameSettings, bg='#393f4d', fg='#d4d4dc') 
        self.settingsButton.grid(row = 3, column = 1, padx=10, pady = 3, ipadx=141, ipady=20)
        # Quit poga, lai varētu aizvērt logu.
        self.quitButton = tk.Button(self.root, text = "Quit", command = self.quit, bg='#393f4d', fg='#d4d4dc') 
        self.quitButton.grid(row = 4, column = 1, pady = 3, ipadx=151, ipady=20) 

    # Spēles sākšanas poga, inicializē spēli un izveido Game objektu, lai ar to veiktu manipulācijas, izdzēš menu pogas un izveido jaunas atkarībā no
    # spēles iesācēja.
    def startGame(self):
        # Spēles objekts
        self.NewGame = Game(self.startingScore, self.maxScore, self.startingPlayer)  
        # Izdzēš menu pogas
        self.menuDestroy()
        # Pārbīda logo
        self.logo.grid(row=1, column=1, columnspan=3)
        # Score nosaukums un cipari
        self.staticScoreLabel = Label(self.root, text = "Score", bg='#1d1e22', fg='#d4d4dc', font="Ariel 15 bold").grid(row=2, column=2)
        self.scoreLabel = Label(self.root, text = self.NewGame.score, bg='#1d1e22', fg='#d4d4dc', font="Ariel 25 bold")
        self.scoreLabel.grid(row = 3, column = 2, padx = 3, pady = 5)
        # Ja pirmais spēlētājs ir Player, tas izveido 2 pogas +3 un +4, lai varētu veikt gājienu
        if self.NewGame.currentPlayer == "Player":
            self.plusThree = tk.Button(self.root, text = "+3", command = partial(self.addIT, 3), bg='#393f4d', fg='#d4d4dc', font="Ariel 15 bold")
            self.plusThree.grid(row = 4, column = 1, padx = 3, pady = 3)           
            self.plusFour = tk.Button(self.root, text = "+4", command = partial(self.addIT, 4), bg='#393f4d', fg='#d4d4dc', font="Ariel 15 bold") 
            self.plusFour.grid(row = 4, column = 3, padx = 3, pady = 3)
        # Ja nav, tad atrod šī brīža stāvokli kokā un atrod labāko gājienu
        else:
            # Šī brīža stāvoklis
            currentState = self.NewGame.gTree.findCurrentState(self.NewGame.score, self.NewGame.turns-1)
            # Atrod labāko gājienu
            bestMove = self.NewGame.getBestMove(currentState)
            # Pievieno rezultātu jauno
            self.addIT(bestMove)
        # Izveido reset pogu, kas vienkārši izmanto zemāk esošo resetUI
        self.resetGame = tk.Button(self.root, text = "Go Back", command = self.resetUI, bg='#393f4d', fg='#d4d4dc') 
        self.resetGame.grid(row = 5, column = 2, padx = 3, pady = 3)    

    # Iznīcina menu pogas, lai spēles laikā tās nevarētu izmantot.
    def menuDestroy(self):
        self.startButton.destroy()
        self.settingsButton.destroy()
        self.quitButton.destroy()        

    # Pārbauda rezultātus vai nav gala rezultāts sasniegts, maina spēlētājus.
    def checkScore(self):
        # Ja score ir mazāks par max score, tad spēle turpinās
        if self.NewGame.score<self.NewGame.maxScore:
            # Pārbauda vai šobrīdējais spēlētājs ir "Player"
            if self.NewGame.currentPlayer == "Player":
                # Nomaina uz nākamo spēlētāju, kas ir "Computer"
                self.NewGame.currentPlayer = "Computer"
                # Iznīcina gājiena pogas
                self.plusThree.destroy()
                self.plusFour.destroy()
                # Atrod šī brīža stāvokli un labāko gājienu
                currentState = self.NewGame.gTree.findCurrentState(self.NewGame.score, self.NewGame.turns-1)
                bestMove = self.NewGame.getBestMove(currentState)
                # Izmantojot funkciju pievieno nākamo
                self.addIT(bestMove)
                self.scoreLabel.config(text = self.NewGame.score)
            # Šis izpildīsies, ja spēlētājs ir "Computer"
            else:
                # Nomaina uz parasto spēlētāju
                self.NewGame.currentPlayer = "Player"
                # Izveido pogas pa jaunam.
                self.plusThree = tk.Button(self.root, text = "+3", command = partial(self.addIT, 3), bg='#393f4d', fg='#d4d4dc', font="Ariel 15 bold")
                self.plusThree.grid(row = 4, column = 1, padx = 3, pady = 3)           
                self.plusFour = tk.Button(self.root, text = "+4", command = partial(self.addIT, 4), bg='#393f4d', fg='#d4d4dc', font="Ariel 15 bold") 
                self.plusFour.grid(row = 4, column = 3, padx = 3, pady = 3)
            pass
        # Ja score ir lielāks vai vienāds ar max score, tad spēle tiek pabeigta un tiek izvadīts uzvarētājs
        else:
            self.plusThree.destroy()
            self.plusFour.destroy()
            if self.NewGame.currentPlayer == "Player":
                self.winLabel = Label(self.root, text = 'WIN!', bg='#1d1e22', fg='#d4d4dc', font="Ariel 15 bold").grid(row = 4, column = 2, padx = 3, pady = 3)
            else:
                self.winLabel = Label(self.root, text = 'LOST!', bg='#1d1e22', fg='#d4d4dc', font="Ariel 15 bold").grid(row = 4, column = 2, padx = 3, pady = 3)
            
    # Ja nospiež pogas +3 vai +4, tas pievieno rezultātu un atjauno rezultātu redzamo UI
    def addIT(self, addition):
        self.NewGame.add(addition)
        self.scoreLabel.config(text = self.NewGame.score)
        self.checkScore()

    # Izveido settings logu
    def gameSettings(self):
        # Iznīcina menu pogas
        self.menuDestroy()
        # Pārbīda logo
        self.logo.grid(row=1, column=1, columnspan=2)
        # Izveido spēlētāju variantus
        self.whoStarts = ["Player", "Computer"]
        # Izveido tekstu un izvēli starp sākošajiem spēlētājiem  
        self.plChoiceLabel = Label(self.root, text='Starting player:', bg='#1d1e22', fg='#d4d4dc', font="Ariel 10 bold")
        self.plChoiceLabel.grid(row=2, column=1, padx = 3, pady = 3)
        self.firstChoice = StringVar()
        self.firstChoice.set(self.startingPlayer)
        self.playerChoice = OptionMenu(self.root, self.firstChoice, *self.whoStarts)
        self.playerChoice.grid(row=2, column=2)
        self.playerChoice.config(bg='#393f4d',fg='#d4d4dc')
        # Izveido ievadi un aprakstu ievadei max rezultātam
        self.maxScLabel = Label(self.root, text='Max score:', bg='#1d1e22', fg='#d4d4dc', font="Ariel 10 bold")
        self.maxScLabel.grid(row=3, column=1, padx = 3, pady = 3)
        self.maxScEntry = Entry(self.root, bg='#393f4d', fg='#d4d4dc', justify=CENTER)
        self.maxScEntry.insert(END, self.maxScore)
        self.maxScEntry.grid(row=3, column=2)
        # Izveido ievadi un aprakstu ievadei sākuma rezultātam
        self.startingScLabel = Label(self.root, text='Starting Score:', bg='#1d1e22', fg='#d4d4dc', font="Ariel 10 bold")
        self.startingScLabel.grid(row=4, column=1, padx = 3, pady = 3)
        self.startingScEntry = Entry(self.root, bg='#393f4d', fg='#d4d4dc', justify=CENTER)
        self.startingScEntry.insert(END, self.startingScore)
        self.startingScEntry.grid(row=4, column=2)
        # Izveido Save pogu.
        self.saveSettingsButton = tk.Button(self.root, text = "Save", command = self.saveSettings)
        self.saveSettingsButton.grid(row = 5, column = 1, padx = 3, pady = 3, columnspan=2)

    # Save settings funkcija, ko izsauc settingos Save poga, lai saglabātu jaunos iestatījumus spēlei
    def saveSettings(self):
        # Pārbauda vai var pārvērst uz skaitļiem, lai nebūtu, ka spēlētājs ievada piemēram burtu k.
        try:
            # pārbauda vai ievade ir sākuma rezultāts ir mazāka par gala rezultātu
            if int(self.maxScEntry.get())>int(self.startingScEntry.get()):
                # Izmaina mainīgos
                self.maxScore = int(self.maxScEntry.get())
                self.startingScore = int(self.startingScEntry.get())
                self.startingPlayer = self.firstChoice.get()
                # Iznīcina settings pogas un ievades
                self.plChoiceLabel.destroy()
                self.playerChoice.destroy()
                self.maxScLabel.destroy()
                self.maxScEntry.destroy()
                self.startingScLabel.destroy()
                self.startingScEntry.destroy()
                self.saveSettingsButton.destroy()
                self.logo.destroy()
                # Izveido menu pa jaunam
                self.menuButtons()
            # Izvada, ka sākuma skaitlis nav mazāks par gala skaitli
            else:
                tk.messagebox.showerror(title="WRONG INPUT", message="Max score is lower than starting score")
        # Izvada, ka gala rezultāts ir ar nepareizu ievadi piemēram kāds burts
        except:
            tk.messagebox.showerror(title="WRONG INPUT", message="Starting/Max score must only contain integers")

    # resetUI izmantoju, lai varētu pa jaunam inicializēt logu pie restart pogas.
    def resetUI(self):
        self.quit()
        # inicializē __init__, lai nemainās vērtības, ja tika mainīti iekš iestatījumiem.
        self.__init__(self.startingScore, self.maxScore, self.startingPlayer)
    
    # Iznīcina root un beidz koda darbību
    def quit(self):
        self.root.destroy()
# ===========================================================================================

# Globālo mainīgo izveide un koda inicializācija (main)======================================
j = 2 # (1)
NewObj = interface()
# ===========================================================================================

# ===========================================================================================
# ATSAUCES :
# (1) SPĒLES KOKA IZVEIDES ALGORITMS - PARAUGS, KAS TIKA DOTS 2.MODULĪ: 
# https://estudijas.rtu.lv/mod/resource/view.php?id=2826268
# (2) Yiğit PIRILDAK - Mastering Tic-Tac-Toe with Minimax Algorithm in Python:
# https://levelup.gitconnected.com/mastering-tic-tac-toe-with-minimax-algorithm-3394d65fa88f
# ===========================================================================================