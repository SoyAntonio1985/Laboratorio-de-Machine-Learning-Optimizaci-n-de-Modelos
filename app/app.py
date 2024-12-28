import pickle
import json
from flask import Flask, request
import pandas as pd


FEATURES = pickle.load(open("churn/models/features.pk", "rb"))

model = pickle.load(open("churn/models/model.pk", "rb"))
column_equivalence = pickle.load(open("churn/models/column_equivalence.pk", "rb"))

# create the Flask app
app = Flask(__name__)

def convert_numerical(features):
    # Usar pandas para manejar transformaciones masivamente
    try:
        converted_features = [
            column_equivalence[i][feat] if i in column_equivalence else pd.to_numeric(feat, errors='coerce') 
            for i, feat in enumerate(features)
        ]
        # Reemplazar valores NaN resultantes de errores de conversión por 0
        return pd.Series(converted_features).fillna(0).tolist()
    except Exception as e:
        raise ValueError(f"Error en la conversión de características: {e}")


@app.route('/query', methods=['GET', 'POST'])
def query_example():
    if request.method == 'GET':
        # Respuesta clara para solicitudes GET
        return "Por favor, utiliza POST para realizar una consulta con los datos necesarios.", 405
    elif request.method == 'POST':
        try:
            data = request.get_json()  # Obtiene los datos en formato JSON
            features = convert_numerical(data['features'])
            response = {
                'response': [int(x) for x in model.predict([features])]
            }
            return json.dumps(response)
        except Exception as e:
            return json.dumps({'error': str(e)}), 400

if __name__ == '__main__':
    # run app in debug mode on port 3001
    app.run(debug=True, port=3001)