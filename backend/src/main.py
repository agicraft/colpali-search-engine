from contextlib import asynccontextmanager
import logging
import os
from fastapi import FastAPI

from .rag.rag_service import RagService
from .colpali.colpali_service import ColpaliService
from .classifier.default_doc_processor import DefaultDocProcessor

from .classifier.classifier_service import (
    CLASSIFIER_SERVICE_NAME,
    DOC_INDEXER_SERVICE_NAME,
    RAG_SERVICE_NAME,
    DOC_PROCESSOR_SERVICE_NAME,
    ClassifierService,
)
from .classifier import classifier_router, classifier_models

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "WARNING").upper())

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):

    # classifier_models.create_all_tables()

    yield {
        CLASSIFIER_SERVICE_NAME: ClassifierService(),
        DOC_PROCESSOR_SERVICE_NAME: DefaultDocProcessor(),
        DOC_INDEXER_SERVICE_NAME: ColpaliService(),
        RAG_SERVICE_NAME: RagService(),
    }


app = FastAPI(lifespan=lifespan, root_path=os.environ["API_BASE_URI"])

app.include_router(classifier_router.router)


@app.get("/")
def version():
    return {"version": "1.0.0"}
