import os
import json

def to_geojson():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(BASE_DIR + '/secrets/secrets.json') as f:
        SECRETS = json.load(f)

    PORT = 25432
    HOST = 'localhost'
    DB_NAME = 'c19persons'
    DB_PASS = SECRETS['DB_PASSWORD']
    if os.getenv('SETTINGS_MODE') == 'prod':
        PORT = 5432
        DB_NAME = 'c19cases'
    elif os.getenv('GCR_INSTACE'):
        PORT = 5432
        DB_NAME = 'c19cases'
        HOST = '/cloudsql/ethereal-yen-274604:us-central1:c19persons'
    ogr2ogr_command = f'ogr2ogr -f GeoJSON \
                          c19persons.json \
                          "PG:host={HOST} dbname={DB_NAME} user=juan password={DB_PASS} port={PORT}" \
                          -sql "select * from c19map_person";'
    # connection = r"host=localhost dbname=c19persons user=juan password=caramba port=25432"
    # schema = "GeoJSON"
    # target_shp = r"c19persons.json"
    # command = r'ogr2ogr -f "GeoJSON" %s PG:"%s" -sql "select * from c19map_person";' % (connection, target_shp)
    print(ogr2ogr_command)
    os.system(ogr2ogr_command,)

def update_mapbox():
    command = 'mapbox --access-token sk.eyJ1IjoianVhbnNvbGFuYSIsImEiOiJjazkza25ubWkwM2J5M2dxaHExeG56YTJ6In0.v28PPnMoaghNV3-ol01E3A upload juansolana.c19persons-tiles c19persons.json'
    print(command)
    os.system(command, )

# to_geojson()

