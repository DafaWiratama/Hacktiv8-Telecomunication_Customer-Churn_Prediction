import pickle
import pandas as pd
import json
from flask import Flask, request, Response
from includes import ChurnModel

app = Flask(__name__)

categories = pickle.load(open('models/categories.pkl', 'rb'))
model = ChurnModel('models')


@app.route('/v1/inference', methods=['GET'])
def route_inference():
    try:
        input_frame = pd.DataFrame([request.args.to_dict()])
        input_frame['SeniorCitizen'] = input_frame['SeniorCitizen'].astype(int)
        probability = int(model(input_frame).numpy()[0, 0] * 100)
        return Response(
            json.dumps({'probability': probability, 'status': 200}),
            status=200, mimetype='application/json'
        )

    except Exception as e:
        return Response(
            json.dumps({'message': 'Oops Something went wrong please try again letter', 'status': 500}),
            status=500, mimetype='application/json'
        )


@app.route('/v1/batch_inference', methods=['POST'])
def route_batch_inference():
    try:
        file = request.files['file']
        input_frame = pd.read_csv(file)
        input_frame['SeniorCitizen'] = input_frame['SeniorCitizen'].astype(int)
        probability = model(input_frame).numpy()[:, 0] * 100
        return Response(
            json.dumps({'probabilities': [int(x) for x in probability], 'status': 200}),
            status=200, mimetype='application/json'
        )
    except Exception as e:
        return Response(
            json.dumps({'message': 'Oops Something went wrong please try again letter', 'status': 500}),
            status=500, mimetype='application/json'
        )


@app.route('/v1/options', methods=['GET'])
def route_options():
    return Response(
        json.dumps({'categories': categories, 'status': 200}),
        status=200, mimetype='application/json'
    )


# app.run(host='10.10.10.13', port=5000, debug=True)