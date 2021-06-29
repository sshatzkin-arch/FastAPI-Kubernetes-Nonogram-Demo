import numpy as np
from fastapi import FastAPI
from nonogram import Nonogram

app = FastAPI()


@app.get("/")
async def root():
  return {"message": "Hello World"}


@app.get("/nonogram/{rows}/{cols}/")
async def read_item(rows: int, cols: int):
  test_puzz = Nonogram(rows, cols)
  print(test_puzz.solution)
  return {"clues": test_puzz.clues, "solution": test_puzz.solution.tolist()}
    

