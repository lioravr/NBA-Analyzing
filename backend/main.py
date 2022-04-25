from fastapi import FastAPI
import uvicorn
from nba_Api import *


app = FastAPI()


@app.get("/load_data/selectyear={selected_year}selectstat={selected_stat}")
async def ttt(selected_year:int,selected_stat:str):
    return load_data(selected_year,selected_stat).to_json()



@app.get('/get_player_data/season={season}&category={category}')
async def nnnn(season:int, category:str):
    return get_players_data(season,category).to_json()
    

if __name__ == "__main__":
   uvicorn.run("main:app", host="0.0.0.0", port=8000, debug=True)

