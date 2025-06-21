import pickle 
import pandas  as pd

MODEL_VERSION='1.0.0'

# Load model
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)



def predict_output(user_input: dict):

    df = pd.DataFrame([user_input])
    
    output=model.predict(df)[0]
    
    return output