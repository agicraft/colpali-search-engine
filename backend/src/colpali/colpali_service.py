import logging
from typing import Any, List

from PIL import Image
from qdrant_client.conversions.common_types import Points
from qdrant_client.http.exceptions import ApiException
from qdrant_client.http.models.models import UpdateStatus
from ..utils.images import pil_to_bytes

from .colpali_client import ColpaliClient
from ..classifier.classifier_service import DocIndexer
from ..classifier.classifier_models import Document

from qdrant_client import QdrantClient
from qdrant_client.http import models
import os

logger = logging.getLogger(__name__)

COLLECTION_NAME = "colpali"
BATCH_SIZE = int(os.environ["COLPALI_BATCH_SIZE"])

SEARCH_TIMEOUT = 60
SEARCH_LIMIT = 10


class ColpaliService(DocIndexer):
    def __init__(self) -> None:
        super().__init__()
        self.qdrant = QdrantClient(host=os.environ["VECTOR_DB_HOST"], port=6333)
        self.colpali = ColpaliClient(base_url=os.environ["COLPALI_BASE_URL"])
        self.__init_collection()

    def interpret(self, query: str, image: bytes) -> bytes:
        return self.colpali.interpret(query=query, image=image)

    def query(self, query: str) -> List[int]:
        multivector_query = self.colpali.process_queries([query])[0]

        search_result = self.qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=multivector_query,
            limit=SEARCH_LIMIT,
            timeout=SEARCH_TIMEOUT,
        )

        return [int(point.id) for point in search_result.points]

    def delete(self, doc: Document):
        chunk_ids: List[models.ExtendedPointId] = [chunk.id for chunk in doc.chunks]
        if not chunk_ids:
            return
        self.qdrant.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.PointIdsList(
                points=chunk_ids,
            ),
        )

    def index(self, doc: Document):

        chunks = doc.chunks

        for i in range(0, len(chunks), BATCH_SIZE):
            chunks_batch = chunks[i : i + BATCH_SIZE]
            image_chunk_ids: List[int] = []
            images: List[bytes] = []
            for chunk in chunks_batch:
                image_chunk_ids.append(chunk.id)
                images.append(chunk.image)

            image_embeddings = self.colpali.process_images(images)

            # prepare points for Qdrant
            points = []
            for j, multivector in enumerate(image_embeddings):
                chunk_id = image_chunk_ids[j]
                points.append(
                    models.PointStruct(
                        id=chunk_id,
                        vector=multivector,  # This is now a list of vectors
                        payload={},
                    )
                )

            self.__qdrant_upsert(points)

    def __init_collection(self):
        if self.qdrant.collection_exists(COLLECTION_NAME):
            logger.info(f"Found QDrant {COLLECTION_NAME=}")
            return

        vector_size = self.__detect_vector_size()

        logger.info(f"Creating QDrant collection {COLLECTION_NAME=} {vector_size=}")
        self.qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            # store the payload on disk
            on_disk_payload=True,
            # it can be useful to swith this off when doing a bulk upload
            # and then manually trigger the indexing once the upload is done
            optimizers_config=models.OptimizersConfigDiff(indexing_threshold=100),
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
                multivector_config=models.MultiVectorConfig(
                    comparator=models.MultiVectorComparator.MAX_SIM
                ),
                quantization_config=models.ScalarQuantization(
                    scalar=models.ScalarQuantizationConfig(
                        type=models.ScalarType.INT8,
                        quantile=0.99,
                        always_ram=True,
                    ),
                ),
            ),
        )

    def __detect_vector_size(self):
        sample_image = Image.new(mode="RGB", size=(64, 64))
        sample_embedding = self.colpali.process_images([pil_to_bytes(sample_image)])
        return len(sample_embedding[0][0])

    def __qdrant_upsert(self, points: Points):
        for n in range(3):
            try:
                res = self.qdrant.upsert(
                    collection_name=COLLECTION_NAME,
                    points=points,
                    wait=True,
                )
                if res.status != UpdateStatus.COMPLETED:
                    raise RuntimeError("Qdrant operation not completed")
                else:
                    return
            except ApiException:
                logger.exception(f"Attempt {n=} failed")
        raise RuntimeError("Request to Qdrant failed in all attempts")
