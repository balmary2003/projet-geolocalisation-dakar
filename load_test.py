import requests
import time
from concurrent.futures import ThreadPoolExecutor

URL = "https://projet-geolocalisation-dakar.onrender.com/tracking/restaurants_data/"
NB_REQUETES = 20
NB_SIMULTANEES = 5

def faire_requete(i):
    debut = time.time()
    try:
        r = requests.get(URL, timeout=15)
        duree = (time.time() - debut) * 1000
        return {"num": i, "status": r.status_code, "duree_ms": round(duree, 1)}
    except Exception as e:
        return {"num": i, "status": "ERREUR", "duree_ms": None, "erreur": str(e)}

print(f"Envoi de {NB_REQUETES} requêtes, {NB_SIMULTANEES} en simultané...")

resultats = []
with ThreadPoolExecutor(max_workers=NB_SIMULTANEES) as executor:
    resultats = list(executor.map(faire_requete, range(NB_REQUETES)))

reussies = [r for r in resultats if r["status"] == 200]
echouees = [r for r in resultats if r["status"] != 200]

print(f"\n--- RÉSULTATS ---")
print(f"Requêtes réussies : {len(reussies)}/{NB_REQUETES}")
print(f"Requêtes échouées : {len(echouees)}")

if reussies:
    durees = [r["duree_ms"] for r in reussies]
    print(f"Temps de réponse min : {min(durees)} ms")
    print(f"Temps de réponse max : {max(durees)} ms")
    print(f"Temps de réponse moyen : {round(sum(durees)/len(durees), 1)} ms")

if echouees:
    print("\nDétail des échecs :")
    for e in echouees:
        print(e)