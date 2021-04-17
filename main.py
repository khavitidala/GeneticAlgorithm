#Ryan
import math
import random

class Setup:
    def __init__(self):
        self.maks_populasi = 100
        self.rate_mutasi = 0.01
        self.rate_crossover = 0.7
        self.batasX = [-1, 2]
        self.batasY = [-1, 1]
        self.panjang_gen = 10
        self.alpha = 0.00001
        self.max_loop = 500

class DNA:
    def __init__(self, gen):
        self.setup = Setup()
        self.gen = gen
    
    def generateGen(self, panjang_gen):
        gen = []
        random.seed()
        for _ in range(panjang_gen):
            gen.append(random.randint(0,1))
        return gen

class Kromosom:
    def __init__(self, genX, genY):
        self.setup = Setup()
        self.panjang_kromosom = 2 * self.setup.panjang_gen
        self.genX = genX
        self.genY = genY
        self.kromosom = self.genX.gen + self.genY.gen
        self.fenotip = self.decodeKromosom(self.setup.batasX, self.setup.batasY, self.panjang_kromosom)
        self.a = self.setup.alpha
        self.fitness = self.fungsi(self.fenotip["x"], self.fenotip["y"])
        self.probability = 0

    def decodeKromosom(self, batasX, batasY, panjang_kromosom):
        fenotip = {}
        fenotip["x"] = self.decodeGen(0, int(panjang_kromosom/2), batasX)
        fenotip["y"] = self.decodeGen(int(panjang_kromosom/2), panjang_kromosom, batasY)
        return fenotip
    
    def decodeGen(self, a, b, batas):
        temp1 = 0
        temp2 = 0
        batasBawah = batas[0]
        batasAtas = batas[1]
        for i in range(1, int(self.panjang_kromosom/2)):
            temp1 += math.pow(2, -1*i)
        i=0
        for j in range(a, b):
            i+=1
            temp2 += self.kromosom[j]*math.pow(2, -1*i)
        feno = batasBawah + temp2*(batasAtas-batasBawah)/temp1
        return feno

    def fungsi(self, x, y):
        return math.cos(x*x)*math.sin(y*y) + (x+y)

    def crossover(self, target):
        anak1 = [i for i in self.kromosom]
        anak2 = [j for j in target.kromosom]
        singlePoint = random.randint(1, self.panjang_kromosom-1)
        for i in range(self.panjang_kromosom):
            if i > singlePoint:
                anak2[i] = self.kromosom[i]
            else:
                anak1[i] = target.kromosom[i]
        childX = DNA(anak1[:int(self.panjang_kromosom/2)])
        childY = DNA(anak1[int(self.panjang_kromosom/2):])
        child1 = Kromosom(childX, childY)
        childX = DNA(anak2[:int(self.panjang_kromosom/2)])
        childY = DNA(anak2[int(self.panjang_kromosom/2):])
        child2 = Kromosom(childX, childY)
        return child1, child2

    def mutasi(self):
        for i in range(self.panjang_kromosom):
            if random.uniform(0, 1) < self.setup.rate_mutasi:
                if self.kromosom[i] == 0:
                    self.kromosom[i] = 1
                else:
                    self.kromosom[i] = 0

class Populasi:
    def __init__(self, populasi):
        self.setup = Setup()
        self.populasi = populasi
    
    def normalisasi(self):
        normalisasi = []
        sum = 0

        for i in range(self.setup.maks_populasi):
            normalisasi.append(self.populasi[i].fitness+10)
            sum += self.populasi[i].fitness+10
        
        for i in range(self.setup.maks_populasi):
            self.populasi[i].probability = normalisasi[i]/sum
    
    def evaluasiFitness(self):
        maxtemp=0
        for i in range(self.setup.maks_populasi):
            if self.populasi[i].fitness > maxtemp:
                maxtemp = self.populasi[i].fitness
                temp = self.populasi[i]
        return temp

    def seleksiOrtu(self):
        random.seed()
        #Lahh nanti ortunya kalo kepilih dua kali gimana? masa nikahin diri sendiri?
        r = random.uniform(0, 1)
        index = 0
        while r > 0 and index < self.setup.maks_populasi:
            r -= self.populasi[index].probability
            index+=1
        index-=1

        return self.populasi[index], index

    def newGeneration(self, bestKromosom):
        i = 0
        while i < self.setup.maks_populasi:
            suami, index = self.seleksiOrtu()
            temp = self.populasi[index].probability
            self.populasi[index].probability = 0
            istri, _ = self.seleksiOrtu()
            self.populasi[index].probability = temp
            if random.uniform(0, 1) < self.setup.rate_crossover:
                anak1, anak2 = suami.crossover(istri)
                anak1.mutasi()
                anak2.mutasi()
                if anak1.fitness < bestKromosom.fitness and i == 0:
                    self.populasi[i] = bestKromosom
                else:
                    self.populasi[i] = anak1
                self.populasi[i+1] = anak2
            i+=2
        
class Main:
    def __init__(self):
        self.setup = Setup()
        self.instance = self.create(self.setup.maks_populasi)
        self.populasi = Populasi(self.instance)
        self.generasi = 0

    def create(self, maks):
        pop = []
        for _ in range(maks):
            genX = DNA([])
            genX.gen = genX.generateGen(self.setup.panjang_gen)
            genY = DNA([])
            genY.gen = genY.generateGen(self.setup.panjang_gen)
            obj = Kromosom(genX, genY)
            pop.append(obj)
        return pop
    
    def clearscreen(self):
        print(chr(27)+'[2j')
        print('\033c')
        print('\x1bc')

    def run(self):
        self.populasi.normalisasi()
        bestKromosom = self.populasi.evaluasiFitness()
        indx = 0
        while indx < self.setup.max_loop:
            #uncomment baris kode di bawah jika ingin mengaktifkan auto clear screen
            self.clearscreen()
            #Jika setelah diuncomment terjadi error, harap ubah ke comment lagi baris kode di atas
            print("Individu terbaik dari Generasi ke-", self.generasi)
            print("Nilai Maksimum Fungsi (Nilai Fitness) :", bestKromosom.fitness)
            print("Nilai x :", bestKromosom.fenotip["x"])
            print("Nilai y :", bestKromosom.fenotip["y"])
            print("Kromosom :", bestKromosom.kromosom)
            
            self.populasi.newGeneration(bestKromosom)
            self.populasi.normalisasi()
            temp = bestKromosom
            bestKromosom = self.populasi.evaluasiFitness()
            if temp == bestKromosom:
                indx += 1
            else:
                indx = 0
                
            self.generasi+=1

if __name__ == '__main__':
    #instansiasi class utama lalu jalankan method utama
    ga = Main()
    ga.run()
