import joblib
import pandas as pd
from fastapi import FastAPI
import os 
from enum import Enum

app = FastAPI()

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir , "regressor.pkl")
colonne_path = os.path.join(current_dir , "regressor_colonne.pkl")

model = joblib.load(model_path)
model_colonne = joblib.load(colonne_path)

liste_points = [i.replace("nom_point_" , "") for i in model_colonne if i.startswith("nom_point_")]

if not liste_points: 
    liste_points = ["Aucun point trouvé"]
PointEnum = Enum("PointEnum" , {name : name for name in liste_points})

VITESSE_REF_PAR_HEURE = {
    0: 107.0, 1: 107.0, 2: 107.0, 3: 107.0, 4: 107.0, 5: 107.0, 
    6: 106.9, 7: 94.0, 8: 89.6, 9: 103.4, 10: 106.8, 11: 107.0, 
    12: 106.2, 13: 106.4, 14: 106.7, 15: 105.5, 16: 97.2, 17: 89.7, 
    18: 99.5, 19: 105.2, 20: 103.8, 21: 107.0, 22: 107.0, 23: 107.0
}

@app.get("/")
def home ():
    return{"Message : API de prediction trafic active"}



@app.get("/predict")
def predict(jour: int, heure: int, nom_point : PointEnum ,vitesse_precedente: float = None, est_ferie: int= 0):
    if vitesse_precedente is None:
        vitesse_precedente = VITESSE_REF_PAR_HEURE.get(heure, 107.0)

    nom_point_str = nom_point.value
    col_point = f"nom_point_{nom_point_str}"

    input_data = pd.DataFrame({
        'Holiday_code': [est_ferie], 
        'Shift_code': [heure],
        'Week_code': [jour],
        'latitude': [50.35],       
        'longitude': [3.10],      
        'vitesse_precedente': [vitesse_precedente],
        'nom_point': [col_point]
    })

    df_model = pd.DataFrame(0 , index=[0], columns=model_colonne)

    df_model['Holiday_code'] = est_ferie
    df_model['Shift_code'] = heure
    df_model['Week_code'] = jour
    df_model['latitude'] = 50.35
    df_model['longitude'] = 3.10
    df_model['vitesse_precedente'] = vitesse_precedente
    
    if col_point in df_model.columns:
        df_model[col_point] = 1

    prediction = model.predict(df_model)[0]
    
    return {
        "point": nom_point_str,
        "heure": heure,
        "vitesse_reference_utilisée": vitesse_precedente,
        "traffic_estime": prediction
    }