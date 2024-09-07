import keras
import pickle
import pandas as pd
import columns
import numpy as np
from sklearn.preprocessing import StandardScaler
import category_encoders as ce

'''
['Age', 'Sex', 'Ethnicity_0', 'Ethnicity_1', 'Ethnicity_2', 'Ethnicity_3', 'Height', 'Weight', 'Systolic BP', 'Diastolic BP', 'eGFR', 'MCV', 'CHOL', 'TRIG', 'HDL', 'LDL', 'Hypercholesterolaemia', 'Cerebrovascular disease', 'Asthma', 'Heart Failure', 'atrial fibrillation', 'Obesity', 'Prev MI', 'SEVERE AS?', 'Age_real', 'Height_real', 'Weight_real', 'Systolic BP_real', 'Diastolic BP_real', 'eGFR_real', 'MCV_real', 'CHOL_real', 'TRIG_real', 'HDL_real', 'LDL_real']
'''
def predict(age, sex, ethnicity, height, weight, sbp, dbp, egfr, mcv, chol, trig, hdl, ldl, hcl, cvd, asthma, hf, af, ob, mi):
    model = keras.models.load_model("resources/model.keras")
    with open("resources/standardscaler.pkl", "rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    with open("resources/category_encoder.pkl", "rb") as encoder_file:
        encoder = pickle.load(encoder_file)

    data = {
        'Age': [age],
        'Sex': [sex],
        'Ethnicity': [ethnicity],
        'Height': [height],
        'Weight': [weight],
        'Systolic BP': [sbp],
        'Diastolic BP': [dbp],
        'eGFR': [egfr],
        'MCV': [mcv],
        'CHOL': [chol],
        'TRIG': [trig],
        'HDL': [hdl],
        'LDL': [ldl],
        'Hypercholesterolaemia': [hcl],
        'Cerebrovascular disease': [cvd],
        'Asthma': [asthma],
        'Heart Failure': [hf],
        'Atrial Fibrillation': [af],
        'Obesity': [ob],
        'Prev MI': [mi],
        'SEVERE AS?': [np.NaN]
    }
    data = pd.DataFrame(data)

    num_cols = list(columns.nums)

    for col in num_cols:
        col_name = col + "_real"
        data[col_name] = 1.0
        data.loc[data[col] == 0, col_name] = 0.0

    data[num_cols] = data[num_cols].replace({0: np.NaN})
    data[num_cols] = scaler.transform(data[num_cols])
    data[num_cols] = data[num_cols].fillna(0)

    data = encoder.transform(data)
    data = data.drop(columns = ["SEVERE AS?"])

    data = data.astype('float32')

    prediction = model.predict(data)
    return int(prediction[0] > 0.5)

