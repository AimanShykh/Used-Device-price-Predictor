import pickle
import json
import numpy as np
import os

__brands = None
__data_columns = None
__model = None

def get_estimated_price(brand, os, screen_size, rear_camera_mp, front_camera_mp, internal_memory, ram, battery, weight, device_age, price_drop, has_4g, has_5g):
    if __model is None:
        print("Error: Model is not loaded!")
        return None

    try:
        brand_index = __data_columns.index(brand.lower()) if brand.lower() in __data_columns else -1
        os_index = __data_columns.index(os.lower()) if os.lower() in __data_columns else -1
    except:
        brand_index = -1
        os_index = -1

    # Initialize feature array
    x = np.zeros(len(__data_columns))

    # Assign numerical values
    feature_values = {
        "screen_size": screen_size,
        "rear_camera_mp": rear_camera_mp,
        "front_camera_mp": front_camera_mp,
        "internal_memory": internal_memory,
        "ram": ram,
        "battery": battery,
        "weight": weight,
        "device_age": device_age,
        "price_drop": price_drop,
        "4g_yes": has_4g,
        "5g_yes": has_5g
    }

    for feature, value in feature_values.items():
        if feature in __data_columns:
            x[__data_columns.index(feature)] = value

    # Set categorical values
    if brand_index >= 0:
        x[brand_index] = 1
    if os_index >= 0:
        x[os_index] = 1

    print("Feature vector:", x)  # Debugging line

    try:
        prediction = __model.predict([x])[0]
        print("Predicted price:", prediction)
        return round(prediction)
    except Exception as e:
        print("Prediction error:", e)
        return None

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __brands
    global __model

    columns_path = './server/artifacts/columns.json'
    model_path = './server/artifacts/test_set.pkl'

    if not os.path.exists(columns_path):
        print("Error: columns.json file not found in", os.getcwd())
        return
    if not os.path.exists(model_path):
        print("Error: test_set.pkl file not found in", os.getcwd())
        return

    try:
        with open(columns_path, 'r') as f:
            __data_columns = json.load(f)['data_columns']
            print("Loaded Columns:", __data_columns)

        __brands = [col for col in __data_columns if col.startswith("device_brand_")]

        # Load model
        with open(model_path, 'rb') as f:
            loaded_data = pickle.load(f)

        # If the loaded data is a tuple, extract the first element (the model)
        if isinstance(loaded_data, tuple):
            __model = loaded_data[0]  # Extract the trained model
        else:
            __model = loaded_data

        print("Model loaded successfully!")
        print("Model type:", type(__model))

        if not hasattr(__model, "predict"):
            print("Error: Loaded object is not a valid model with a predict() method.")
            __model = None

    except Exception as e:
        print(f"Error loading artifacts: {e}")
        __model = None

    print("loading saved artifacts...done")

    print("Identified Brands:", __brands)

def get_brands_names():
    return __brands

def get_data_columns():
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    import pickle

    try:
        with open('./server/artifacts/test_set.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Model loaded successfully!")
        print(type(model))  # Should be a sklearn model like LinearRegression, RandomForest, etc.
    except Exception as e:
        print("Error loading model:", e)



    # Test the function with sample inputs
    print(get_estimated_price(
        brand='device_brand_nokia',
        os='Android',  
        screen_size=17.3,
        rear_camera_mp=0.3,
        front_camera_mp=24,
        internal_memory=64,
        ram=6,
        battery=4500,
        weight=220,
        device_age=5,
        price_drop=0.7,
        has_4g=True,
        has_5g=False
    ))

    
    

