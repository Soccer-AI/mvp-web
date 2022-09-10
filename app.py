import os
from dotenv import load_dotenv

import psycopg2
from minio import Minio

from flask import Flask,render_template, url_for

load_dotenv()

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

app = Flask(__name__)

@app.route('/')
def main():
    db = None
    paths_for_actions = []
    table = []
    try:
        db = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            database=POSTGRES_DB
        )
        cursor = db.cursor()
        cursor.execute("""select events.id-3, name, time, clip_path,id_action 
                          from events 
                          join action_types on action_types.id = events.id_action;""")
        table = cursor.fetchall()
        cursor.close()
        db.close()
        paths_for_actions = [i[3] for i in table]
    except:
        print("Error")
    return render_template('index.html', massiv=paths_for_actions, table=table)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)