import os, sys
import certifi
import pymongo
from dotenv import load_dotenv
import pandas as pd
import numpy as np

from fastapi import FastAPI,File,UploadFile,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME

# ✅ Load environment variables
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")
print("MongoDB URL:", mongo_db_url)
load_dotenv()


# ✅ MongoDB Connection
ca = certifi.where()
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# ----------- FAST API APPLICATION ------------------
# ✅ FastAPI App
app = FastAPI()


# ✅ Jinja2 template setup
templates = Jinja2Templates(directory="./templates")

# ✅ Correct CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ------ Home page -------
# ✅ Root: Redirect to /docs
# @app.get("/docs", tags=['authentication'])
# async def index():
#     return RedirectResponse(url="/docs")

# ✅ Root Route - Show Home Page
@app.get("/", response_class=HTMLResponse, tags=['Home'])
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ----------TRAIN MODEL -------
# ✅ Train Endpoint
@app.get("/train", tags=['training'])
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return JSONResponse(content={"message": "Training is successful ✅"}, status_code=200)
    except Exception as e:
        logging.error(f"Training failed: {e}")
        raise NetworkSecurityException(e,sys)
    
# ---------- PREDICT TEST DATA ------
# ✅ Predict Endpoint


# @app.get("/predict")
# async def predict_route(request:Request, file:UploadFile = File(...)):
#     try:
#         df= pd.read_csv(file.file)
#         preprocessor = load_object('final_models/preprocessor.pkl')
#         final_model = load_object('final_modles/model.pkl')

#         network_model = NetworkModel(preprocessor = preprocessor, model = final_model)
#         print(df.iloc[0])
#         y_pred = network_model.predict(df)
#         print(y_pred)
#         df['predicted-column'] = y_pred
#         print(df['predicted_column'])
#         table_html = df.tohtml(classess= 'table striped')
#         df.to_csv('prediction_output/output.csv', index=False)

#         return templates.TemplateResponse('table_html', {'request':request, 'table':table_html})
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)

@app.get("/predict", response_class=HTMLResponse, tags=["prediction"])
async def predict_form(request: Request):
    # Serve the upload form
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse, tags=["prediction"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        # Load model & preprocessor
        preprocessor = load_object('final_models/preprocessor.pkl')
        final_model = load_object('final_models/model.pkl')

        # Predict
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_label'] = y_pred

        # Save and render
        df.to_csv('prediction_output/output.csv', index=False)
        table_html = df.to_html(classes='table table-striped', index=False)

        return templates.TemplateResponse("table.html", {
            "request": request,
            "table": table_html
        })

    except Exception as e:
        raise NetworkSecurityException(e, sys)
# ------ RUN APP CODE -------
# ✅ Run the App
if __name__=="__main__":
    app_run(app, host="localhost", port=8000)