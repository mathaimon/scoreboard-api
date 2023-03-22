from flask import Flask
import os
from supabase import create_client, Client


supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_ANON_KEY")
    )

def get_points():
    """
    Get the point details from the database and calculate the overall points of each team
    Retuns a dicionary of association and scores
    Example => {
        scam : 0,
        mace : 0,
        element : 0,
    }
    """
    scores_list = {
        "scam" : 0,
        "mace" : 0,
        "element" : 0,
    }
    response = supabase.table('contests').select("*").eq('is_complete', True).execute()
    for contest in response.data:
        if (contest["first_place_grp"]is not None and contest["first_place_grp"]!=""):
            scores_list[contest["first_place_grp"]] += contest["first_place_point"]
        if (contest["second_place_grp"]is not None and contest["second_place_grp"]!=""):
            scores_list[contest["second_place_grp"]] += contest["second_place_point"]
        if (contest["third_place_grp"]is not None and contest["third_place_grp"]!=""):
            scores_list[contest["third_place_grp"]] += contest["third_place_point"]

    return scores_list
 

app = Flask(__name__)

@app.route('/')
def home():
    return {
        "message": "Welcome to the Planke Scoreboard API"
    }

@app.route('/scores')
def scores():
    return get_points()

@app.route('/combined')
def combined_scores():
    score = get_points()
    # Leading "1" is to convert the numbers with leading zeroes to integers
    return {
        "scores" : int("1" + str(score['scam']).zfill(3)
        +str(score['element']).zfill(3)+str(score['mace']).zfill(3))
    }
