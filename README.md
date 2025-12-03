# IMMO ELIZA - Model Deployment

## 🚀 Project Mission

The real estate company Immo Eliza is happy with our regression model and current work up to now.

They would like us to create an API so their web developers can access the predictions whenever they need to. 
They also want to have a small web application for the non-technical employees and possibly their clients to use.
The API and the web application should be intertwined but separate.

My focus for this project will be the small web application.

## 🧾 Approach
1. Created GitHub repository named `immo-eliza-deployment`
2. Created a requirements.txt to store dependencies
3. Created an `api` folder to contain all code and files for the API
4. Added our trained model artifact `xgboost_model.pkl`
5. Created an `app.py` file that would house the FastAPI if I get that far
6. (Not yet created `Dockerfile` to create Docker image for the API)
7. Created a `predict.py` file that will contain the code used to predict
8. Created a `streamlit` folder to store related application files
9. 
10. 

## ⚙️ Installation

1. Clone the repository:

```
git clone https://github.com/kristinnuyens/immo-eliza-deployment.git
```

2. Create and activate a virtual environment (optional):

```
python3 -m venv venv source venv/bin/activate
```

3. Install dependencies: 

```
pip install -r requirements.txt
```

## 🌳 Repo Structure
```
.
├── api/
│   ├── app.py
│   ├── best_xgb_model_top20.pkl
│   ├── predict.py
│   └── ...
├── notebooks/
│   ├── 01_predict.ipynb
│   ├── ....ipynb
│   └── ....ipynb
├── streamlit/
│   ├── ...
│   ├── ....ipynb
│   └── ....ipynb
├── .gitignore
├── README.md
└── requirements.txt
```




++++++++
INSTRUCTIONS:
## Architecture
You will set up:
- GitHub repository including your model artifacts
    - Option 1: Your streamlit code, and Streamlit Community Cloud account to deploy your frontend web application
    - Option 2: the FastAPI code, the API Dockerfile, and a Render account to deploy your backend API
    - Option 3: Combine the two. The below diagram summarizes the whole architecture.

### API
For every API use case, the first thing to decide _(for each route)_, is the **input** and the **output** you want.
You want to get your data in **JSON format** and return the data in the same format. Your Python code will have to handle the conversion from and to JSON, and to other output formats as needed.
Below is an example of how you could structure your input and output. Use this as a starting point, but you will have to change this according to your model and the data input it requires.

#### Input
An example input looks like:
```json
{
  "data": {
    "LivingArea": int,
    "TypeOfProperty": ["apartment" | "house" | "land" | "office"| "garage"],
    "Bedrooms": int,
    "PostalCode": int,
    "SurfaceOfGood": Optional[int],
    "Garden": Optional[bool],
    "GardenArea": Optional[int],
    "SwimmingPool": Optional[bool],
    "Furnished": Optional[bool],
    "Openfire": Optional[bool],
    "Terrace": Optional[bool],
    "NumberOfFacades": Optional[int],
    "ConstructionYear": Optional[int],
    "StateOfBuilding": Optional["to be done up" | "to restore" | "to renovate"],
    "Kitchen": Optional(["not installed" | "usa not installed" | "installed"])
  }
}
```
**Again, you will need to modify the input based on the data input required in your model!**
Do not forget to specify which parameters are required and which ones are optional (and set a default value for those).

#### Output
Your output should look like:
```json
{
  "prediction": Optional[float],
  "status_code": Optional[int]
}
```
You need to provide an error if something went wrong. For more information, check the [FastAPI documentation](https://fastapi.tiangolo.com/tutorial/handling-errors/) and [this list of common status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).

## Steps
### Project preparation
Note: This project structure is based on Option 3, but can be adapted for Option 1 & 2.
- Create a `api` folder that will contain all the code and files for your API
  - Add your trained model artifacts (pick a model with good performance, a reliable `predict.py` script, but also best < 100 MB - you may want to consider to retrain your model if you made it too complex)
  - Add a `predict.py` file that will contain the code used to predict
  - Add a `app.py` file that will house the FastAPI
  - Add a `Dockerfile` to create a Docker image for your API
- Create a `streamlit` folder that will contain all the code for your Streamlit application
- Create a `requirements.txt` to store your dependencies

### Prediction

In the previous project, you made a machine learning model to predict the price of a property. You stored its artifacts for both the preprocessing steps and the model.

The `predict.py` script will contain all the code to load your artifacts, preprocess your data, and generate a prediction.

The script should contain a `predict()` function that takes data for a single property (or possibly multiple properties) as an input and returns a price as output. The function should be a regular Python function, not a CLI tool.

Feel free to break down the `predict()` function into smaller functions. It would make sense to at least also have a `preprocess()` function that takes care of the preprocessing of the data.

### Option 1: Create your API

In your `app.py` file, create an API with FastAPI that contains two endpoints (also called routes):
- A route at `/` that accepts:
  - `GET` requests and returns `"alive"` if the server is up and running
- A route at `/predict` that accepts:
  - `POST` requests that receives the data of a property in JSON format and returns a prediction in JSON format

The function attached to your `/predict` endpoint should deal with all the input features provided as a JSON, preprocess them, pass them through your `predict()` function, and then return the prediction again as a JSON.

You are very lucky, because FastAPI [autogenerates documentation](https://fastapi.tiangolo.com/features/#automatic-docs) for you about the available routes and the inputs and outputs!

### 1.1 Create a Dockerfile for your API

To deploy your API, you will use Docker. Docker is a tool that allows you to package your application and its dependencies into a single image that can be run on any machine.

The Dockerfile is a text file that contains all the commands to build an image and then run it as a container. Create a Dockerfile that runs your `app.py` file with Python.

### Deploy your Docker image on `render.com`

The hosting provider [Render](https://render.com/) allows you to build your Docker container on their server and send requests to it. Engineers will see Docker in more detail later on. But for now the only thing needed is a [Dockerfile](https://docs.docker.com/reference/dockerfile/). You can see how to create it for an FastAPI [here](https://fastapi.tiangolo.com/deployment/docker/#dockerfile).

There is a free plan that should be enough, but you need to be careful to remove the unnecessary dependencies in your Docker image. Hopefully you don't have a too large model, otherwise, back to the drawing table.

If you have an issue or need more information, the [Render documentation](https://render.com/docs/docker) is well made!

### Option 2: Create a Streamlit application

Create a small web application using Streamlit that will allow non-technical people to use your API.

As seen in the architecture diagram, the Streamlit application will send requests to your API and display the results in a visual interface.

To help get you started, you can check this [tutorial](https://medium.com/codex/streamlit-fastapi-%EF%B8%8F-the-ingredients-you-need-for-your-next-data-science-recipe-ffbeb5f76a92). [This](https://30days.streamlit.app/) is also a great resource to get started with Streamlit.

### 2.1 Deploy your application on Streamlit Community Cloud

Time to show the world your Streamlit app! To do so, check out these [instructions](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app).


### Option 3: Combine the two

I would suggest having an MVP first before attempting this one! In practice, you usually go for Option 1 or Option 2. However, you can think of this as having an option for developers and an option for users. 


### Presentation
Again we will do a show and tell of a few projects during debrief! You will show directly your deployed solution and give a brief demo. 

## Deliverables

1. Publish the up-to-date source code on your GitHub repository with all folders and files required as described above.




++++++++
ML README:


## 📊 Summary of Results
Metrics:

| Model             | RMSE (EUR) | MAE (EUR) | R²    | CV_R2_mean | CV_R2_std | overfit_gap |
| ----------------- | ---------- | --------- | ----- | ---------- | --------- | ----------- |
| Linear Regression |    364 671 |   161 831 | 0.324 |            |           |             |
| Random Forest     |     90 687 |    29 742 | 0.958 |      0.694 |    0.0358 |       0.265 |
| XGBoost           |    158 835 |    78 998 | 0.872 |      0.686 |    0.0429 |       0.186 |
| Tuned XGBoost     |    162 544 |    84 012 | 0.866 |      0.670 |    0.0338 |       0.195 |

* Linear Regression underperforms: the housing data is not linear and contains strong interactions and non-linear relationships
* Random Forest was the strongest performer with the lowest error and the highest R², but there is a very high training fit and much lower CV performance → strong overfitting
* XGBoost performed well but requires more tuning as it still overfits

Both RF and XGB models need hyperparameter tuning to reduce overfitting.

Looking into finetuning we found that RF did not really improve, so continued with XGBoost, and have our current best model stored as best_xgb_model_top20.pkl. Metrics are added in the table above.


## 🧑‍💻 Contributors

Solo project:

* Kristin Nuyens

## ⏰ Timeline

4 working days