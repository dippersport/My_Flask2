import os
import requests
import time
import concurrent.futures
import asyncio
import aiohttp

def download_image_sync(url, start_time):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    content_type = response.headers.get('Content-Type')
    
    # Проверка, является ли содержимое изображением
    if content_type and content_type.startswith('image'):
        extension = content_type.split('/')[-1]
        filename = f'sync_{url.replace("https://", "").replace(".", "_").replace("/", "")}.{extension}'
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

async def download_image_async(session, url, start_time):
    async with session.get(url) as response:
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        
        # Проверка, является ли содержимое изображением
        if content_type and content_type.startswith('image'):
            extension = content_type.split('/')[-1]
            filename = f'async_{url.replace("https://", "").replace(".", "_").replace("/", "")}.{extension}'
            content = await response.read()
            with open(filename, "wb") as f:
                f.write(content)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")

async def download_all_images_async(urls, start_time):
    async with aiohttp.ClientSession() as session:
        tasks = [download_image_async(session, url, start_time) for url in urls]
        await asyncio.gather(*tasks)

def main():
    urls = [
        'https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png',
        'https://www.python.org/static/img/python-logo.png',
        'https://jpeg.org/jpeg/'  
    ]
    start_time = time.time()

    # Синхронный подход
    for url in urls:
        download_image_sync(url, start_time)

    # Многопоточный подход
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_image_sync, url, start_time) for url in urls]
        concurrent.futures.wait(futures)

    # Многопроцессорный подход
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(download_image_sync, url, start_time) for url in urls]
        concurrent.futures.wait(futures)

    # Асинхронный подход
    asyncio.run(download_all_images_async(urls, start_time))

if __name__ == "__main__":
    main()





