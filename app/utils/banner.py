from pathlib import Path


def print_banner():
    banner_path = Path("app/assets/ascii-art.txt")

    with open(banner_path, "r", encoding="utf-8") as file:
        print(file.read())

    print("🚀 MarketFabric runtime ready.")