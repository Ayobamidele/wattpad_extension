import httpx
import os
from services.storage import fetch_filebin_storage
import asyncio

FILEBIN_UPLOAD_URL = asyncio.run(fetch_filebin_storage())
 # Base URL for Filebin API

async def download_image(image_url):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to download image. Status code: {response.status_code}")

async def upload_to_filebin(image_data):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            FILEBIN_UPLOAD_URL,
            files={'file': ('image.jpg', image_data, 'image/jpeg')}
        )
        if response.status_code == 200:
            # Extract the filebin URL from the response
            return response.text.strip()
        else:
            raise Exception(f"Failed to upload image to Filebin. Status code: {response.status_code}")

async def handler(event, context):
    image_url = event.get('queryStringParameters', {}).get('image_url')
    if not image_url:
        return {
            'statusCode': 400,
            'body': 'Missing image_url parameter'
        }

    try:
        image_data = await download_image(image_url)
        filebin_url = await upload_to_filebin(image_data)
        return {
            'statusCode': 200,
            'body': filebin_url
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }

# Wrapper to handle the asynchronous function in an environment that expects synchronous functions
def run_handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(handler(event, context))
