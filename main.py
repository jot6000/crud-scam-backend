from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient

client = MongoClient()

db = client["scam"]
collection = db["scam-analytics"]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class cords(BaseModel):
    x: int
    y: int

class scamData(BaseModel):
    name: str
    xAxisName: str
    yAxisName: str
    dataPoints: List[cords]

@app.get('/')
def status():
    return {'status':'running'}

@app.get('/scamdata')
def getData():
    """Get all of our graphs"""
    graphs = collection.find()
    responsgraphs = []
    for graph in graphs:
        responsgraphs.append(scamData(**graph))
    return responsgraphs

@app.post('/scamdata')
def addData(data:scamData):
    """Add a new graph"""
    result = collection.insert_one(data.dict())
    return{"insertion":result.acknowledged}