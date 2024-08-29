# zonda 14 mai

```
nbrun=1
Summary:
	- blockSize: 1250, init: 9864.0, compute: 4861.0
	- blockSize: 400, init: 10421.0, compute: 5252.0
	- blockSize: 625, init: 10317.0, compute: 5480.0
	- blockSize: 250, init: 9807.0, compute: 5600.0
	- blockSize: 500, init: 10172.0, compute: 5973.0
	- blockSize: 200, init: 10351.0, compute: 5993.0
	- blockSize: 10000, init: 10539.0, compute: 6112.0
	- blockSize: 1000, init: 10094.0, compute: 6231.0
	- blockSize: 125, init: 9971.0, compute: 7055.0
	- blockSize: 100, init: 10269.0, compute: 7941.0
	- blockSize: 2000, init: 10579.0, compute: 11734.0
	- blockSize: 2500, init: 10176.0, compute: 18059.0
	- blockSize: 5000, init: 10454.0, compute: 70895.0
```

```
nbrun=3
Summary:
	- blockSize: 1250, 	init: 10513.7, 	compute: 4990.0
	- blockSize: 400, 	init: 10425.7, 	compute: 5389.0
	- blockSize: 625, 	init: 10387.7, 	compute: 5498.0
	- blockSize: 500, 	init: 10275.0, 	compute: 5909.3
	- blockSize: 10000, 	init: 10270.7, 	compute: 5980.7
	- blockSize: 1000, 	init: 10259.0, 	compute: 6253.3
```

## avec MKL_DEBUG_CPU_TYPE=5

```
nbrun=3
Summary:
	- blockSize: 1250, 	init: 6393.0, 	compute: 1272.7
	- blockSize: 1000, 	init: 6367.7, 	compute: 1656.0
	- blockSize: 625, 	init: 6106.7, 	compute: 1679.7
	- blockSize: 10000, 	init: 6283.7, 	compute: 1695.7
	- blockSize: 500, 	init: 6238.3, 	compute: 1928.0
	- blockSize: 400, 	init: 6231.3, 	compute: 1956.3

```

siwtch MKL/OMP
matrice entre 2000 et 3000
thread > 32

## switch sur mkl2023

```
nbrun=3
Summary:
	- blockSize: 1250, 	init: 6549.7, 	compute: 1265.3
	- blockSize: 10000, 	init: 6397.3, 	compute: 1639.7
	- blockSize: 1000, 	init: 6200.0, 	compute: 1640.0
	- blockSize: 625, 	init: 6518.7, 	compute: 1670.7
	- blockSize: 400, 	init: 6580.0, 	compute: 1956.7
	- blockSize: 500, 	init: 6440.3, 	compute: 1965.3
```
LD_PRELOAD
Summary:
	- blockSize: 1250, 	init: 6087.7, 	compute: 1385.3
	- blockSize: 1000, 	init: 6530.3, 	compute: 1708.3
	- blockSize: 10000, 	init: 6245.3, 	compute: 1709.7
	- blockSize: 625, 	init: 6285.7, 	compute: 1735.0
	- blockSize: 500, 	init: 6548.0, 	compute: 1997.7
	- blockSize: 400, 	init: 6791.3, 	compute: 2061.0

Fonction
Summary:
	- blockSize: 1250, 	init: 6782.3, 	compute: 1303.3
	- blockSize: 10000, 	init: 6414.0, 	compute: 1682.3
	- blockSize: 1000, 	init: 7114.7, 	compute: 1696.3
	- blockSize: 625, 	init: 6302.3, 	compute: 1757.0
	- blockSize: 500, 	init: 6653.0, 	compute: 1999.3
	- blockSize: 400, 	init: 6503.3, 	compute: 2024.7

Rien
Summary:
	- blockSize: 1250, 	init: 6778.7, 	compute: 1333.7
	- blockSize: 1000, 	init: 6193.0, 	compute: 1684.7
	- blockSize: 625, 	init: 6586.0, 	compute: 1717.0
	- blockSize: 10000, 	init: 6411.0, 	compute: 1751.7
	- blockSize: 500, 	init: 6374.0, 	compute: 1999.7
	- blockSize: 400, 	init: 7198.0, 	compute: 2074.0