import mimetypes

from app.core.config import settings
from supabase import AsyncClient, create_async_client


async def get_supabase_client() -> AsyncClient:
    return await create_async_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def upload_file_to_supabase(file_content: bytes, file_name: str) -> str:
    supabase = await get_supabase_client()
    bucket_name = settings.SUPABASE_BUCKET

    # Guess content type
    content_type, _ = mimetypes.guess_type(file_name)
    if not content_type:
        content_type = "application/octet-stream"

    # Upload file
    await supabase.storage.from_(bucket_name).upload(
        path=file_name, file=file_content, file_options={"content-type": content_type}
    )

    # Create signed URL (valid for 1 hour)
    response = await supabase.storage.from_(bucket_name).create_signed_url(
        file_name, expires_in=3600
    )

    return response
