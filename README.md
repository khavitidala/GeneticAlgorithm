# Genetic Algorithm
Solving Function Optimization Problem using Genetic Algorithm

## How to
Make sure you have installed python beforehand, then clone this repository to your desktop.
```
python main.py
```
or if you use linux and python3
```
python3 main.py
```

## Customization
You can customize function you want, this algorithm aim is to find x and y value which make the function reach a maximum value.
```
60. def fungsi(self, x, y):
61.     return math.cos(x*x)*math.sin(y*y) + (x+y)
```
In class setup, you can customize the paramater also
```
self.maks_populasi = 100
self.rate_mutasi = 0.01
self.rate_crossover = 0.7
self.batasX = [-1, 2]
self.batasY = [-1, 1]
self.panjang_gen = 10
self.alpha = 0.00001
self.max_loop = 500
```

