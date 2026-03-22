import streamlit as st
import pickle
import pandas as pd

# Load model
model = pickle.load(open("model.pkl", "rb"))
team_dict = pickle.load(open("team_dict.pkl", "rb"))

# Convert mapping
name_to_id = {v: k for k, v in team_dict.items()}
team_names = list(name_to_id.keys())

# UI
st.title("⚽ Football Match Predictor")
st.markdown("### Select teams to predict match result")

home_team_name = st.selectbox("Select Home Team", team_names)
away_team_name = st.selectbox("Select Away Team", team_names)

# Convert names to IDs
home_id = name_to_id[home_team_name]
away_id = name_to_id[away_team_name]

# Prediction
if st.button("Predict Match Result"):

    input_data = pd.DataFrame([[home_id, away_id]], columns=['home_team_api_id', 'away_team_api_id'])

    st.write("Input Data:", input_data)

    prediction = model.predict(input_data)

    if prediction[0] == 1:
        st.success(f"{home_team_name} Wins!")
    elif prediction[0] == 0:
        st.success(f"{away_team_name} Wins!")
    else:
        st.info("Match Draw!")