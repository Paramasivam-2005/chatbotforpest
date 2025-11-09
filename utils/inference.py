from PIL import Image
import os, json, hashlib, numpy as np

with open(os.path.join(os.path.dirname(__file__), "actions.json")) as f:
    ACTIONS = json.load(f)

LABELS = ["Aphid", "Stem Borer", "Whitefly", "Thrips", "Armyworm", "Pod Borer"]

def _image_hash_bytes(image_file):
    try:
        data = image_file.read()
        image_file.seek(0)
    except Exception:
        with open(image_file, "rb") as f:
            data = f.read()
    h = hashlib.sha256(data).digest()
    return h

def _seed_from_hash(h):
    return int.from_bytes(h[:4], "big")

def get_action_for_pest(pest_name):
    return ACTIONS.get(pest_name, "No action found. Consult local agricultural expert.")

def identify_pest(image_file, top_k=3):
    h = _image_hash_bytes(image_file)
    seed = _seed_from_hash(h)
    rng = np.random.default_rng(seed)
    probs = rng.random(len(LABELS))
    probs = probs / probs.sum()
    top_idx = np.argsort(probs)[::-1][:top_k]
    result = {LABELS[i]: float(probs[i]) for i in range(len(LABELS))}
    top_pest = LABELS[int(top_idx[0])]
    action = get_action_for_pest(top_pest)
    try:
        image_file.seek(0)
    except Exception:
        pass
    return top_pest, result, action
