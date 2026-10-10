import os, hashlib, json, sys

ROOT = r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction"
ext = r"C:\Users\vyasn\OneDrive\Desktop\Disease_prediction\data\external"
IMG_EXT = {".jpg",".jpeg",".png",".bmp",".webp",".gif",".tif",".tiff"}

def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()

def scan_leaf(base):
    res={}
    for dp,dn,fn in os.walk(base):
        imgs=[os.path.join(dp,f) for f in fn if os.path.splitext(f)[1].lower() in IMG_EXT]
        if imgs:
            shas=set(sha256(p) for p in imgs)
            res[os.path.relpath(dp,base)]={"files":len(imgs),"unique":len(shas)}
    return res

which=sys.argv[1]
targets = {
  "cauliflower_fruit": os.path.join(ext,"Cauliflower Dataset","cauliflower_fruit"),
  "cauliflower_leaves": os.path.join(ext,"Cauliflower Dataset","cauliflower_leaves"),
  "pepperbell": os.path.join(ext,"Pepper Bell Leaf Disease","pepperbell_leaves"),
  "end_to_end_test": os.path.join(ext,"end_to_end_test"),
}
base=targets[which]
res=scan_leaf(base)
with open(os.path.join(ROOT,"reports",f"_ext_{which}.json"),"w") as f:
    json.dump(res,f,indent=1)
for rel,c in sorted(res.items()):
    print(f"  {rel}: files={c['files']} unique={c['unique']}")
print("done",which)
