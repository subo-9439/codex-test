"""FastAPI service for Korean legal questions.

This module is a demo and its responses should not be taken as official legal advice.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import json
import os
from transformers import pipeline

BASE_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(BASE_DIR, '..', 'data', 'legal_cases.jsonl')
MODEL_DIR = os.path.join(BASE_DIR, '..', 'model')

app = FastAPI(title="Korean Legal QA")

class Question(BaseModel):
    query: str

# Load model - use fine-tuned model if available
if os.path.exists(MODEL_DIR):
    qa_pipeline = pipeline('text-generation', model=MODEL_DIR)
else:
    qa_pipeline = pipeline('text-generation', model='skt/kogpt2-base-v2')

# Load case data
cases = []
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    for line in f:
        cases.append(json.loads(line))


def retrieve_cases(query: str, top_k: int = 1) -> List[dict]:
    # naive retrieval based on keyword overlap
    scored = []
    for case in cases:
        score = sum(1 for word in query.split() if word in case['text'])
        scored.append((score, case))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [case for _, case in scored[:top_k]]


@app.post('/ask')
def ask(question: Question):
    related_cases = retrieve_cases(question.query)
    if not related_cases:
        raise HTTPException(status_code=404, detail='No relevant case found')
    context = related_cases[0]['text']
    answer = qa_pipeline(question.query + '\n' + context, max_length=100)[0]['generated_text']
    return {
        'answer': answer,
        'source': related_cases[0]['citation']
    }
