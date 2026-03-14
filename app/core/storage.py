"""Google Cloud Storage service for file uploads."""
from google.cloud import storage
from fastapi import UploadFile
from app.core.config import settings


class StorageService:
    """Wraps Google Cloud Storage operations for uploading and deleting files."""

    def __init__(self):
        self._client = storage.Client()
        self._bucket = self._client.bucket(settings.GCS_BUCKET_NAME)

    def upload_file(self, file: UploadFile, destination: str) -> str:
        """Upload a file to GCS and return its public URL.

        Args:
            file: The FastAPI UploadFile object.
            destination: The blob path inside the bucket (e.g. 'projects/proj-1/img.png').

        Returns:
            The public URL of the uploaded file.
        """
        blob = self._bucket.blob(destination)
        blob.upload_from_file(
            file.file,
            content_type=file.content_type or "application/octet-stream",
        )
        return f"https://storage.googleapis.com/{settings.GCS_BUCKET_NAME}/{destination}"

    def delete_file(self, destination: str) -> None:
        """Delete a file from GCS. Silently ignores if the file doesn't exist.

        Args:
            destination: The blob path inside the bucket.
        """
        blob = self._bucket.blob(destination)
        try:
            blob.delete()
        except Exception:
            # File may not exist; ignore
            pass


# Singleton instance
storage_service = StorageService()
