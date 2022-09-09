from flask import Flask,render_template, url_for
import psycopg2
from minio import Minio
import val

app = Flask(__name__)

@app.route('/')
def hello_world():
    db = None
    paths_for_actions = []
    table = []
    try:
        # client = Minio(
        #     val.MINIO_ENDPOINT_URL,
        #     access_key=val.MINIO_ACCESS_KEY,
        #     secret_key=val.MINIO_SECRET_KEY,
        #     secure=False
        # )
        # def get_file_to_s3(object_name, file_path):
        #     found = client.bucket_exists(val.MINIO_BUCKET)
        #     assert found == True
        #     client.fget_object(val.MINIO_BUCKET, object_name, file_path)

        db = psycopg2.connect(
            host=val.pg_host,
            port=val.pg_port,
            user=val.pg_user,
            password=val.pg_password,
            database=val.pd_database)
        cursor = db.cursor()
        cursor.execute("""select id_action, name, time, clip_path from events join action_types on action_types.id = events.id_action;""")
        table = cursor.fetchall()
        paths_for_actions = [i[3] for i in table]
        # for i in paths_for_actions:
        #     get_file_to_s3(i,i)

        cursor.close()
        db.close()
    except:
        print("эрор")
    return render_template('index.html', massiv=paths_for_actions, table=table)

if __name__ == '__main__':
    app.run()