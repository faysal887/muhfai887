import uvicorn
import logging
from fastapi import FastAPI, HTTPException
import fasttext
from pydantic import BaseModel
from datetime import datetime
from hydra import initialize, compose
from pydantic import BaseModel, Field


app = FastAPI()

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s \n'
logging.basicConfig(filename='app.log', filemode='w', format=log_format)


class TEXT(BaseModel):
    text: str
    text: str = Field(..., min_length=1, max_length=1024)


@app.on_event("startup")
def load_model():
    global model
    path=get_config()['model']['path']
    model = fasttext.load_model(path)


def get_config():
    with initialize(config_path="conf"):
        cfg = compose(config_name="config.yaml")
        return cfg
    

def predict_fasttext(text):
    pred = model.predict(text.text, k=1)
    conf = round(pred[1][0],2)
    label = pred[0][0].replace('__label__', '')

    return label, conf


@app.post("/classify/")
async def classify(text: TEXT):
    try:
        conf_threshold = get_config()['threshold']['default']

        label, conf= predict_fasttext(text)

        if conf < conf_threshold:
            return {'label': 'undefined', 'conf': conf}
        else:
            return {'label': label, 'conf': conf}
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        logging.error(error_msg)
        raise HTTPException(status_code=500, detail='server side error')
