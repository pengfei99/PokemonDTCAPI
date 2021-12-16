import warnings
from typing import List
import os
import joblib
import mlflow
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

pokemon_app = FastAPI()


class Pokemon(BaseModel):
    hp: int
    attack: int
    defence: int
    special_attack: int
    special_defense: int
    speed: int


@pokemon_app.get("/pokemon-type")
def get_pokemon_type(hp: int, attack: int, defence: int, special_attack: int, special_defense: int, speed: int):
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    df.loc[0] = pd.Series({'hp': hp, 'attack': attack, 'defence': defence, 'special_attack': special_attack,
                           'special_defense': special_defense, 'speed': speed})
    model = get_model("../models/model2.pkl")
    res = bool(model.predict(df)[0])
    return {"is_legendary": res}


@pokemon_app.post("/pokemon-type")
def post_pokemon_type(pokemon: Pokemon):
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    df.loc[0] = pd.Series({'hp': pokemon.hp, 'attack': pokemon.attack, 'defence': pokemon.defence,
                           'special_attack': pokemon.special_attack,
                           'special_defense': pokemon.special_defense, 'speed': pokemon.speed})
    model = get_model("/api/models/model2.pkl")
    res = bool(model.predict(df)[0])
    return {"is_legendary": res}


@pokemon_app.post("/pokemon-types")
def get_pokemon_types(pokemons: List[Pokemon]):
    i = 0
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    for pokemon in pokemons:
        df.loc[i] = pd.Series({'hp': pokemon.hp, 'attack': pokemon.attack, 'defence': pokemon.defence,
                               'special_attack': pokemon.special_attack,
                               'special_defense': pokemon.special_defense, 'speed': pokemon.speed})
        i += 1
    model = get_model("../models/model2.pkl")
    results = []
    for r in model.predict(df):
        results.append(bool(r))
    return {"is_legendary": results}


def get_model():
    # if model_path starts with a mlflow model path, use mlflow pyfunc to get the model
    # mlflow model must have blow formats:
    # - f"models:/{model_name}/{stage}"
    # note env needs to contain "MLFLOW_MODEL_NAME" and MLFLOW_MODEL_STAGE
    model_path: str=None
    model_name: str=os.getenv("MLFLOW_MODEL_NAME")
    model_stage: str=os.getenv("MLFLOW_MODEL_STAGE")
    if model_name and model_stage:
        model_path=f"models:/{model_name}/{stage}"
    else:
        model_path="/api/models/model2.pkl"
    if model_path.startswith("models"):
        model = mlflow.pyfunc.load_model(
            model_uri=model_path
        )
    # if it's a local fs path, use joblib to get the model
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            model = joblib.load(open(model_path, 'rb'))
    return model
