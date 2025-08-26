import joblib
import streamlit as st
import json


@st.cache_resource
def load_model(model_path):
    model = joblib.load(model_path)
    return model

@st.cache_data
def load_classes(classes_path):
    with open(classes_path, 'r') as file:
        classes = json.load(file)
    return classes


@st.cache_data
def predict_salary(_model, input_data):
    prediction = _model.predict(input_data)
    return prediction

@st.cache_data
def predict_class(_model, input_data):
    prediction = _model.predict(input_data)[0]
    return prediction
