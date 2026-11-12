"""Review of Prop B' checker: run reintersect_curved.check (imported; no files written) on the table's models."""
import sys, time
sys.path.insert(0, "."); sys.path.insert(0, "..")
import reintersect_curved as RC, lemma0_check_run as R
names = sys.argv[1:] or ["sloppy cylinder g=0.01", "sloppy cylinder g=0.05", "sloppy pipe g=0.01", "sloppy box g=0.01",
                         "sloppy wedge 30deg g=0.01", "cylinder", "box"]
for n in names:
    t = time.time()
    r = RC.check(R.PARTS[n](), n)
    print({k: r[k] for k in r if k not in ("unreached",)}, f"{time.time()-t:.0f}s", flush=True)
