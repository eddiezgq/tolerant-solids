import io, contextlib, runpy, numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path("exp6a.py")
V, F = g["prism"](np.deg2rad(150))
def loop(T, n=4000):
    P = V[list(T)]; pts = []
    for k in range(3):
        t = np.linspace(0, 1, n, endpoint=False)[:, None]; pts.append(P[k] + t * (P[(k+1)%3] - P[k]))
    return np.vstack(pts)
a, b = loop((0,4,3)), loop((1,2,5))
da = np.roll(a,-1,0)-a; db = np.roll(b,-1,0)-b; ma = a+da/2; mb = b+db/2
s = 0.0
for i in range(len(ma)):
    r = ma[i]-mb; s += np.sum((r*np.cross(da[i], db)).sum(1)/np.linalg.norm(r,axis=1)**3)
print("Gauss linking integral:", s/(4*np.pi))
