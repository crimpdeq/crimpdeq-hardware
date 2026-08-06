import pcbnew, sys

def load_map(path):
    b=pcbnew.LoadBoard(path)
    # (ref, padname) -> set of netnames seen (should be 1)
    padnet={}
    net_to_pads={}
    for f in b.GetFootprints():
        ref=f.GetReference()
        for p in f.Pads():
            key=(ref, p.GetPadName())
            net=p.GetNetname()
            padnet.setdefault(key,set()).add(net)
    # reduce: each key -> single net (or flag multi)
    keynet={}
    for k,v in padnet.items():
        keynet[k]= sorted(v)[0] if len(v)==1 else "MULTI:"+"|".join(sorted(v))
    # build net -> frozenset of keys, treating unconnected/empty as singleton
    from collections import defaultdict
    groups=defaultdict(set)
    for k,net in keynet.items():
        if net=="" or net.startswith("unconnected-") or net.startswith("MULTI:"):
            groups[("SINGLE",)+k].add(k)   # singleton
        else:
            groups[net].add(k)
    partition=set(frozenset(v) for v in groups.values())
    return keynet, partition

pathA=sys.argv[1]; pathB=sys.argv[2]
labelA=sys.argv[3] if len(sys.argv)>3 else "A"
labelB=sys.argv[4] if len(sys.argv)>4 else "B"
kA,pA=load_map(pathA)
kB,pB=load_map(pathB)

print(f"=== {labelA}  vs  {labelB} ===")
print(f"{labelA}: {len(kA)} named pads, {len(pA)} nets(partition classes)")
print(f"{labelB}: {len(kB)} named pads, {len(pB)} nets(partition classes)")

# 1) same pad keys?
onlyA=set(kA)-set(kB); onlyB=set(kB)-set(kA)
print(f"pad keys only in {labelA}: {len(onlyA)}  only in {labelB}: {len(onlyB)}")
for k in sorted(onlyA)[:10]: print("   only A:",k)
for k in sorted(onlyB)[:10]: print("   only B:",k)

# 2) net-name match on common keys
common=set(kA)&set(kB)
namediff=[(k,kA[k],kB[k]) for k in common if kA[k]!=kB[k]]
print(f"net-NAME mismatches on common pads: {len(namediff)}")
for d in namediff[:20]: print("   ",d)

# 3) partition (connectivity) equivalence, ignoring net names
print(f"partition (connectivity) IDENTICAL ignoring names: {pA==pB}")
if pA!=pB:
    onlyPA=pA-pB; onlyPB=pB-pA
    print(f"  net-classes only in {labelA}: {len(onlyPA)}; only in {labelB}: {len(onlyPB)}")
    for s in list(onlyPA)[:8]: print("   A-only net class:", sorted(s))
    for s in list(onlyPB)[:8]: print("   B-only net class:", sorted(s))

if onlyA or onlyB or namediff or pA != pB:
    raise SystemExit(1)
