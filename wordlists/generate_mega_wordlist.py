import itertools
import os

BASE = [
    "api", "dev", "prod", "stage", "static", "cdn", "files", "backup", "admin",
    "auth", "login", "private", "public", "internal", "secure", "db", "cache",
    "node", "cluster", "app", "service"
]

REGIONS = [
    "us", "us-east", "us-west", "eu", "sa", "br", "latam", "apac", "asia", "jp", "au"
]

VERSIONS = [f"v{i}" for i in range(1, 20)]
NUM = [str(i) for i in range(0, 200)]

output = "mega_wordlist.txt"

with open(output, "w", encoding="utf-8") as f:
    # Base direta
    for b in BASE:
        f.write(b + "\n")

    # Combinações base + números
    for b, n in itertools.product(BASE, NUM):
        f.write(f"{b}{n}\n")

    # Combinações base + region
    for b, r in itertools.product(BASE, REGIONS):
        f.write(f"{b}-{r}\n")

    # Combos base + versão
    for b, v in itertools.product(BASE, VERSIONS):
        f.write(f"{b}-{v}\n")

    # Combos base + region + versão
    for b, r, v in itertools.product(BASE, REGIONS, VERSIONS):
        f.write(f"{b}-{r}-{v}\n")

print("Gerado mega_wordlist.txt com milhões de entradas.")
