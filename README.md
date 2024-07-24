# [www.rembg.com](https://www.rembg.com) API wrapper for Python

<img src="https://github.com/Remove-Background-ai/rembg.js/blob/main/media/background-remove-preview.png" width="400px"  />

A simple, FREE AI background removal tool for **Python**. Currently, this is **THE ONLY FREE** library available for personal usage from API. Check out our website at www.rembg.com for more details.

## Requirements

Get your **FREE** API Key from https://www.rembg.com/api-usage.
Note: you can still use the API without a key, but it is very limited.

## Installation

```bash
pip install rembg
```

## Library

input_image can be one of these: str (file path) | bytes (Buffer) | dict (with a base64 key).
Usage Example
Basic Usage

```python
import os
from rembg import rembg
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# API_KEY will be loaded from the .env file

API_KEY = os.getenv('API_KEY')

# Log upload and download progress

def on_upload_progress(bytes_read, total_bytes):
    print(f"Upload progress: {bytes_read}/{total_bytes} bytes")

def on_download_progress(bytes_read, total_bytes):
    print(f"Download progress: {bytes_read}/{total_bytes} bytes")

result = rembg(
    api_key=API_KEY,
    input_image_path='./input.png',
    on_upload_progress=on_upload_progress,
    on_download_progress=on_download_progress
)
print(f"✅🎉 Background removed and saved under path={result['outputImagePath']}")

# Call cleanup to remove the temporary file if needed

# result['cleanup']()
```

## Base64 Return Type Example

If you wish to return a Base64 string instead of a temporary file path, you can use the return_base64 parameter:

```python
import os
from rembg import rembg
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# API_KEY will be loaded from the .env file

API_KEY = os.getenv('API_KEY')

# Log upload and download progress

def on_upload_progress(bytes_read, total_bytes):
    print(f"Upload progress: {bytes_read}/{total_bytes} bytes")

def on_download_progress(bytes_read, total_bytes):
    print(f"Download progress: {bytes_read}/{total_bytes} bytes")

result = rembg(
    api_key=API_KEY,
    input_image_path='./input.png',
    on_upload_progress=on_upload_progress,
    on_download_progress=on_download_progress,
    return_base64=True
)
print(f"✅🎉 Background removed: {result['base64Image']}")
```

## Input Image as Base64 or Buffer

Since version 1.1.8, the rembg function can accept an input image as a Buffer or Base64 object. Below is a quick demonstration:

```python
import os
from rembg import rembg
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

base64_input = 'data:image/png;base64,/9j/4AAQSkZJRgABAQEASABIAAD/.....etc'

# API_KEY will be loaded from the .env file

API_KEY = os.getenv('API_KEY')

# Log upload and download progress

def on_upload_progress(bytes_read, total_bytes):
    print(f"Upload progress: {bytes_read}/{total_bytes} bytes")

def on_download_progress(bytes_read, total_bytes):
    print(f"Download progress: {bytes_read}/{total_bytes} bytes")

result = rembg(
    api_key=API_KEY,
    input_image_path={'base64': base64_input}, # or simply an image Buffer
    on_upload_progress=on_upload_progress,
    on_download_progress=on_download_progress,
    return_base64=True
)
print(f"✅🎉 Background removed: {result['base64Image']}")
```

## Usage of return_mask Flag

The library provides an option to return a mask of the image instead of the processed image. This is controlled by the return_mask parameter. When set to true, the function returns a mask. By default (if omitted), this parameter is set to false.

```python
import os
from rembg import rembg
from dotenv import load_dotenv

# Load environment variables from .env file

load_dotenv()

# API_KEY will be loaded from the .env file

API_KEY = os.getenv('API_KEY')

# Log upload and download progress

def on_upload_progress(bytes_read, total_bytes):
    print(f"Upload progress: {bytes_read}/{total_bytes} bytes")

def on_download_progress(bytes_read, total_bytes):
    print(f"Download progress: {bytes_read}/{total_bytes} bytes")

result = rembg(
    api_key=API_KEY,
    input_image_path='./input.jpg',
    on_upload_progress=on_upload_progress,
    on_download_progress=on_download_progress,
    return_mask=True, # <----- Set to true to get the mask of the image
    return_base64=True # Set to true to receive the result as a Base64 string
)
print(f"✅🎉 Mask retrieved: {result['base64Image']}")
```

# Generated Mask

This image demonstrates the result of the mask generation process. The mask typically highlights the main subject of the image with the background removed or made transparent.

<img src="https://github.com/Remove-Background-ai/rembg.js/blob/main/media/generated_mask.png" width="400px"  />

This is very useful to work with Stable Diffusion for a perfect area of inpainting, for example.
