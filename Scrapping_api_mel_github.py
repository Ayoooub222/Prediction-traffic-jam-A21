import requests
import pandas as pd
from datetime import datetime
import time
import os    

#1. CONFIGURATION
API_KEY = "your api"

FICHIER_CSV = "your path"

POINTS_A_SURVEILLER = [
    {
        "nom": "Point A_1 - Vrai Point Inser1 vers D ", 
        "lat": 50.431664, 
        "lon": 2.931068
    },
    {
        "nom": "Point A_2 - Inser1 vers L  (Corrigé)", 
        "lat": 50.43177, 
        "lon": 2.931005
    },
    {
        "nom": "Point B_1 - Mid_Inser1-2 vers D", 
        "lat": 50.432193, 
        "lon": 2.937499
    },
    {
        "nom": "Point C_1 _ Inser 2 vers D", 
        "lat": 50.430505, 
        "lon": 2.9621
    },
    {
        "nom": "Point D_1 _ Sortie1 _ vers D", 
        "lat": 50.428886, 
        "lon": 2.979063
    },
    {
        "nom": "Point E_1 _ Insertion- vers L", 
        "lat": 50.423737, 
        "lon": 3.022513
    },
    {
        "nom": "Point F_1 _ Radar _ Douai", 
        "lat": 50.424005, 
        "lon": 3.020059
    },
    {
        "nom": "Point G_1 _ Sortie Final _  vers D", 
        "lat": 50.388299, 
        "lon":  3.128845
    }
    
]

# L'adresse de l'API TomTom
BASE_URL = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

def verifier_bouchons():
    lignes_a_sauvegarder = []
    
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🛰️ Scan de l'A21 en cours...")
    
    for point in POINTS_A_SURVEILLER:
        # On prépare l'adresse pour ce point précis
        url = f"{BASE_URL}?key={API_KEY}&point={point['lat']},{point['lon']}&unit=KMPH"
        
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                flow = data['flowSegmentData']
                
                # --- Récupération des données ---
                vitesse_reelle = flow['currentSpeed']
                vitesse_habituelle = flow['freeFlowSpeed']
                temps_trajet_actuel = flow['currentTravelTime']
                temps_trajet_habituel = flow['freeFlowTravelTime']
                
                # Calcul du retard (bouchon)
                perte_de_temps = temps_trajet_actuel - temps_trajet_habituel
                
                # On décide arbitrairement si c'est bouché 
                if perte_de_temps < 60:
                    etat = "🟢 FLUIDE"
                    niveau_bouchon = 0
                elif 60 < perte_de_temps < 120:
                    etat = "🟠 DENSE"
                    niveau_bouchon = 1
                else:
                    etat = "🔴 SATURÉ"
                    niveau_bouchon = 2
                
                print(f"   📍 {point['nom']}")
                print(f"      ↳ Vitesse : {vitesse_reelle} km/h (Ref: {vitesse_habituelle} km/h)")
                print(f"      ↳ État : {etat} (Perte: {perte_de_temps} sec)")
                
                # On stocke les infos pour le fichier CSV
                lignes_a_sauvegarder.append({
                    "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "nom_point": point['nom'],
                    "latitude": point['lat'],
                    "longitude": point['lon'],
                    "vitesse_reelle": vitesse_reelle,
                    "vitesse_habituelle": vitesse_habituelle,
                    "bouchon_seconds": perte_de_temps,
                    "niveau traffic": niveau_bouchon
                })
                
            else:
                print(f"   ❌ Erreur API sur {point['nom']} : Code {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Erreur technique sur {point['nom']}: {e}")

    #3. SAUVEGARDE DANS LE FICHIER 
    if lignes_a_sauvegarder:
        df = pd.DataFrame(lignes_a_sauvegarder)
        
        #Si le fichier n'existe pas encore, on le crée avec les titres
        if not os.path.isfile(FICHIER_CSV):
            df.to_csv(FICHIER_CSV, index=False, sep=';')
            print("   💾 Fichier créé et données sauvegardées.")
        # Sinon, on ajoute à la suite (mode 'append')
        else:
            df.to_csv(FICHIER_CSV, mode='a', header=False, index=False, sep=';')
            print("   💾 Données ajoutées à l'historique.")

#4. LA BOUCLE INFINIE 
print("--- 🏁 Démarrage du moniteur A21 ---")
print("Appuyez sur 'Ctrl + C' pour arrêter proprement.")

try:
    while True:
        verifier_bouchons()
        print("💤 Pause de 5 minutes...")
        time.sleep(300)

except KeyboardInterrupt:
    print("\n🛑 Arrêt demandé. Les données sont bien au chaud dans le CSV !")  