from flask import Flask, request, jsonify
import util  

app = Flask(__name__)

@app.route('/get_brand_names', methods=['GET'])
def get_brand_names():
    response = jsonify({
        'brands': util.get_brands_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/predict_device_price', methods=['GET', 'POST'])
def predict_device_price():
    try:
        # Extracting form data
        brand = request.form['brand']
        os = request.form['os']
        screen_size = float(request.form['screen_size'])
        rear_camera_mp = float(request.form['rear_camera_mp'])
        front_camera_mp = float(request.form['front_camera_mp'])
        internal_memory = int(request.form['internal_memory'])
        ram = int(request.form['ram'])
        battery = int(request.form['battery'])
        weight = float(request.form['weight'])
        new_price = int(request.form['normalized_new_price'])
        device_age = int(request.form['device_age'])
       
        has_4g = bool(request.form['has_4g'])
        has_5g = bool(request.form['has_5g'])

     
        estimated_price = util.get_estimated_price(
            brand, os, screen_size, rear_camera_mp ,front_camera_mp, internal_memory, 
            ram, battery, weight,device_age,new_price, has_4g, has_5g
        )

       
        response = jsonify({
            'estimated_price': estimated_price
        })
    except Exception as e:
        response = jsonify({
            'error': str(e)
        })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask Server For Device Price Prediction...")
    util.load_saved_artifacts() 
    app.run(debug=True)
