import numpy as np
for _a, _t in (("float", float), ("int", int), ("complex", complex), ("bool", bool)):
    if not hasattr(np, _a): setattr(np, _a, _t)
from pyknotid.spacecurves import Knot
t = np.linspace(0, 2*np.pi, 400, endpoint=False)
K = np.stack([np.sin(t)+2*np.sin(2*t), np.cos(t)-2*np.cos(2*t), -np.sin(3*t)], 1)
Kxz = np.stack([K[:,0], K[:,2], K[:,1]], 1)   # diagram in x-z, depth y
for name, P in (("std", K), ("xz", Kxz)):
    for seed in (None, 3, 7):
        Q = np.eye(3) if seed is None else np.linalg.qr(np.random.default_rng(seed).normal(size=(3,3)))[0]
        k = Knot(P @ Q.T, verbose=False)
        print(name, seed, round(abs(k.determinant()),3))
print("---")
for n in (400, 3000):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    for sc, off in ((1, 0), (0.13, 0), (0.13, 20), (1, 20)):
        P = np.stack([0.6+sc*(np.sin(t)+2*np.sin(2*t)), 0.12/0.13*sc*(-np.sin(3*t)), off+sc*(np.cos(t)-2*np.cos(2*t))], 1)
        print(n, sc, off, round(abs(Knot(P, verbose=False).determinant()),3), round(abs(Knot(P - P.mean(0), verbose=False).determinant()),3))
