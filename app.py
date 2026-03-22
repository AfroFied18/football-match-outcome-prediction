import streamlit as st
import pickle
import pandas as pd

# Page config
st.set_page_config(page_title="Football Match Predictor", layout="centered")

# Load model and mapping
model = pickle.load(open("model.pkl", "rb"))
team_dict = pickle.load(open("team_dict.pkl", "rb"))

# Convert mapping
name_to_id = {v: k for k, v in team_dict.items()}
team_names = list(name_to_id.keys())

# UI
st.title("⚽ Football Match Outcome Predictor")
st.markdown("### Select teams to predict match result")

home_team_name = st.selectbox("🏠 Select Home Team", team_names)
away_team_name = st.selectbox("✈️ Select Away Team", team_names)

# Convert names to IDs
home_id = name_to_id[home_team_name]
away_id = name_to_id[away_team_name]

# Prediction
if st.button("🔮 Predict Match Result"):

    # Create input dataframe
    input_data = pd.DataFrame(
        [[home_id, away_id]],
        columns=['home_team_api_id', 'away_team_api_id']
    )

    st.write("### 🔢 Input Data")
    st.write(input_data)

    # Predict
    prediction = model.predict(input_data)
    probabilities = model.predict_proba(input_data)

    st.write("### 📊 Prediction Probabilities")

    # Assuming: 0 = Away Win, 1 = Home Win, 2 = Draw
    st.write(f"🏠 Home Win: {probabilities[0][1]*100:.2f}%")
    st.write(f"✈️ Away Win: {probabilities[0][0]*100:.2f}%")
    st.write(f"🤝 Draw: {probabilities[0][2]*100:.2f}%")

    st.write("---")

    # Final result
    if prediction[0] == 1:
        st.success(f"🏆 {home_team_name} is likely to WIN!")
    elif prediction[0] == 0:
        st.success(f"🏆 {away_team_name} is likely to WIN!")
    else:
        st.info("🤝 Match is likely to be a DRAW!")
