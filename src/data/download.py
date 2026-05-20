import kagglehub
import shutil
from pathlib import Path

RAW_DIR = Path("data/raw")
DATASET = "emmarex/plantdisease"


def download():
    if any(RAW_DIR.iterdir()) if RAW_DIR.exists() else False:
        print("Data already exists — skipping download.")
        return

    print("Downloading PlantVillage dataset...")
    cache_path = Path(kagglehub.dataset_download(DATASET))
    
    image_root = _find_image_root(cache_path)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    for class_dir in image_root.iterdir():
        if class_dir.is_dir():
            dest = RAW_DIR / class_dir.name
            if not dest.exists():
                shutil.copytree(class_dir, dest)
    
    print(f"Done — data saved to {RAW_DIR}")


def _find_image_root(path: Path) -> Path:
    current = path
    for _ in range(6):
        children = [c for c in current.iterdir() if c.is_dir()]
        for child in children:
            if any(p.suffix.lower() in {".jpg", ".jpeg"} 
                   for p in child.iterdir() if p.is_file()):
                return current
        color = next((c for c in children 
                      if c.name.lower() == "color"), None)
        current = color if color is not None else children[0]
    return current


if __name__ == "__main__":
    download()