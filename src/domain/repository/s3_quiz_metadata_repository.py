import boto3
from typing import List

from domain.quiz_data import QuizData
from domain.repository.base_quiz_metadata_repository import BaseQuizMetadataRepository
from settings import settings


class S3QuizMetadataRepository(BaseQuizMetadataRepository):
    def __init__(self):
        self._bucket_name = settings.bucket_name
        self._s3_client = boto3.client('s3')
        self._s3_resource = boto3.resource('s3')

    def read_quizes(self) -> List[QuizData]:
        quizes: List[QuizData] = []
        quiz_bucket = self._s3_resource.Bucket(self._bucket_name)

        for bucket_object in quiz_bucket.objects.all():
            quiz_file_data = self._s3_client.get_object(
                Bucket=bucket_object.bucket_name, Key=bucket_object.key)
            quiz_json = quiz_file_data["Body"].read()
            quiz_data: QuizData = QuizData.from_json(quiz_json)
            quizes.append(quiz_data)
        return quizes


if __name__ == "__main__":
    repo = S3QuizMetadataRepository()
    print(repo.read_quizes())
