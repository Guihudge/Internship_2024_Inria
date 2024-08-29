import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

mS = 1.988900e30
mT = 5.9e24
mL = 7.3e22

dTL = 3.8e8
dTS = 1.4e11
dSL = dTL+dTS

G = 6.67e-11

time_max = 365
delta_t = 3600*24 # en seconde (=1h)

xS = 0
yS = 0
xT = dTS
yT = dTS
xL = dTS+dTL
yL = dTS+dTL
y = np.array([mT, mS, mL])

vTx = 29800
vTy = 29800

vSx = 0
vSy = 0

vLx = 1024
vLy = 1024

TerreX = [xT]
TerreY = [yT]
LuneX = [xL]
LuneY = [yL]
SoleilX = [xS]
SoleilY = [yS]


for i in range(1, time_max):
    Ax = np.array([
        [0,                       G*(mT/(dTS**3))*(xT-xS), G*(mT/(dTL**3))*(xT-xL)],
        [G*(mS/(dTS**3))*(xS-xT), 0,                       G*(mS/(dSL**3))*(xS-xL)],
        [G*(mL/(dTL**3))*(xL-xT), G*(mL/(dSL**3))*(xL-xS), 0]
    ])
    
    Ay = np.array([
        [0,                     G*(mT/dTS**3)*(yT-yS), G*(mT/dTL**3)*(yT-yL)],
        [G*(mS/dTS**3)*(yS-yT), 0,                     G*(mS/dSL**3)*(yS-yL)],
        [G*(mL/dTL**3)*(yL-yT), G*(mL/dSL**3)*(yL-yS), 0]
    ])

    

    Fy = Ay@y
    Fx = Ax@y

    print(Fx)
    
    FxT, FxS, FxL = Fx
    FyT, FyS, FyL = Fy
    
    # calcule accélération
    aTx = 1/mT*FxT
    aTy = 1/mT*FyT
    
    aSx = 1/mS*FxS
    aSy = 1/mS*FyS
    
    aLx = 1/mL*FxL
    aLy = 1/mL*FyL

    # calcule vitesse
    vTx = delta_t*aTx + vTx
    vTy = delta_t*aTy + vTy

    vSx = delta_t*aSx + vSx
    vSy = delta_t*aSy + vSy

    vLx = delta_t*aLx + vLx
    vLy = delta_t*aLy + vLy

    #calcule position
    xT = delta_t*vTx + TerreX[i-1]
    yT = delta_t*vTy + TerreY[i-1]

    xS = delta_t*vSx + SoleilX[i-1]
    yS = delta_t*vSy + SoleilY[i-1]

    xL = delta_t*vLx + LuneX[i-1]
    yL = delta_t*vLy + LuneY[i-1]

    TerreX.append(xT)
    TerreY.append(yT)
    LuneX.append(xL)
    LuneY.append(yL)
    SoleilX.append(xS)
    SoleilY.append(yS)

    #x_min = min(x_min, min(xT, xL, xS))
    #y_min = min(y_min, min(yT, yL, yS))

    #x_max = max(x_max, max(xT, xL, xS))
    #y_max = max(y_max, max(yT, yL, yS))

#Calcule des limite du dessin
min_x = min(min(TerreX), min(LuneX), min(SoleilX))
min_y = min(min(TerreY), min(LuneY), min(SoleilY))

max_x = max(max(TerreX), max(LuneX), max(SoleilX))
max_y = max(max(TerreY), max(LuneY), max(SoleilY))

idx = 1
print("Terre: {},{}\nLune: {}, {}\nSoleil: {},{}".format(TerreX[idx], TerreY[idx], LuneX[idx], LuneY[idx], SoleilX[idx], SoleilY[idx]))


fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-1e12, 1e12)  # Arbitrary units for visualization
ax.set_ylim(-1e12, 1e12)

sun, = ax.plot([], [], 'yo', markersize=12, label='Sun')
earth, = ax.plot([], [], 'bo', markersize=6, label='Earth')
moon, = ax.plot([], [], 'go', markersize=4, label='Moon')


# Initialize the animation
def init():
    sun.set_data([], [])
    earth.set_data([], [])
    moon.set_data([], [])
    return sun, earth, moon,


# Update the animation
def update(frame):
    sun.set_data(SoleilX[:frame], SoleilY[:frame])
    earth.set_data(TerreX[:frame], TerreY[:frame])
    moon.set_data(LuneX[:frame], LuneY[:frame])
    return sun, earth, moon,


ani = FuncAnimation(fig, update, frames=time_max,
                    init_func=init, blit=True)

# Display the animation
plt.legend()
#plt.show()
f = open("animation.html", "w")
html = ani.to_jshtml()
f.write(html)
f.close()