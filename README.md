# IMMO ELIZA - Model Deployment

## 🚀 Project Mission
The real estate company Immo Eliza is happy with our regression model and current work up to now.

They would like us to create an API so their web developers can access the predictions whenever they need to. 
They also want to have a small web application for the non-technical employees and possibly their clients to use.
The API and the web application should be intertwined but separate.

My focus for this project will be the web application.

## 🧾 Approach
1. Created a GitHub repository named `immo-eliza-deployment`
2. Created a `requirements.txt` to store dependencies
3. Created a `src` folder to store the scripts for the preprocessing and the model that were created in the previous project
4. Created an `api` folder to contain files for the API (currently only used for `predict.py`)
5. Created a `models` folder and added the `preprocessor.pkl` and trained `model.pkl`
6. Created a `predict.py` script containing the code to load aretefacts, preprocess the data and generate a prediction; this script contains a python function taking in data for a single property and returning a price prediction as output
7. Created a `streamlit` folder to store related application files; created several draft versions of the `app_vX.X.py` scripts to continue finetuning. First final version `app_v1.0.py` was used for deployment to the Streamlit Community Cloud

## 📘 Streamlit Application — Deliverable

This project contains a fully deployed **Streamlit web application** that predicts Belgian property prices based on user-provided inputs. The app is designed as a lightweight, interactive tool that demonstrates a full end-to-end machine learning workflow, from preprocessing to prediction.

### 🔍 Features

* User-friendly interface built with Streamlit
* Real-time property price prediction
* Clean form layout with required fields and dynamic inputs
* Deployed and shareable through a public Streamlit URL

### 🚀 Deployment

The application is deployed and accessible here:

👉 **Live app:** *[add your Streamlit deployment link]*

The deployment automatically rebuilds when the repository is updated

## ⚙️ Installation & Local Setup

To run the app locally:

```bash
# 1. Clone the repository
git clone https://github.com/kristinnuyens/immo-eliza-deployment.git

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Streamlit
streamlit run streamlit/app_v1.0.py
```

## 🌳 Repo Structure
```text
immo-eliza-deployment
├── api/
│   └── predict.py
├── models/
│   ├── model.pkl
│   └── preprocessor.pkl
├── src/
│   ├── Immo_Eliza_Logo.png
│   ├── preprocess_module.py
│   └── setup_model.py
├── streamlit/
│   ├── app_v0.0.py
│   ├── ....py
│   ├── ....py
│   ├── ....py
│   └── app_v1.0.py
├── README.md
└── requirements.txt
```

## 🧑‍💻 Contributors

Solo project:

* Kristin Nuyens

## ⏰ Timeline

3 working days