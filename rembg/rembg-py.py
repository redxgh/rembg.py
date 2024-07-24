import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from requests_toolbelt.multipart.encoder import MultipartEncoderMonitor
from tempfile import NamedTemporaryFile
import base64
import mimetypes

def rembg(api_key, input_image, on_upload_progress=None, on_download_progress=None, return_mask=False, return_base64=False):
    """
    Removes the background from an image using the rembg.com API.

    Args:
        api_key (str): The API key for rembg.com.
        input_image (str|bytes|dict): The input image, can be a file path, bytes, or a dict with a base64 property.
        on_upload_progress (callable, optional): A callback function to handle upload progress events. Defaults to None.
        on_download_progress (callable, optional): A callback function to handle download progress events. Defaults to None.
        return_mask (bool, optional): Whether to return a mask instead of the image. Defaults to False.
        return_base64 (bool, optional): Whether to return the output image as a Base64 string. Defaults to False.

    Returns:
        dict: If return_base64 is True, returns a dictionary with the base64Image property containing the Base64 string of the output image.
              If return_base64 is False, returns a dictionary with the outputImagePath property containing the path to the output image file,
              and the cleanup function to delete the temporary file.

    Raises:
        Exception: If the API key is not provided or if the request fails.
    """
    if not api_key:
        raise Exception('⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️: API key not provided, trials will be very limited.')

    url = "https://api.rembg.com/rmbg"
    API_KEY_HEADER = "x-api-key"

    # Create multipart/form-data payload
    fields = {}
    
    if isinstance(input_image, str):
        # Input is a file path
        mime_type, _ = mimetypes.guess_type(input_image)
        if not mime_type:
            mime_type = 'application/octet-stream'
        with open(input_image, 'rb') as f:
            fields['image'] = (f.name, f, mime_type)
    elif isinstance(input_image, bytes):
        # Input is bytes
        fields['image'] = ('image.png', input_image, 'image/png')
    elif isinstance(input_image, dict) and 'base64' in input_image:
        # Input is a base64 string
        base64_data = input_image['base64']
        if base64_data.startswith('data:'):
            base64_data = base64_data.split(',')[1]
        buffer = base64.b64decode(base64_data)
        fields['image'] = ('image.png', buffer, 'image/png')
    else:
        raise Exception('Invalid input type. Must be a file path, bytes, or a dict with a base64 property.')

    if return_mask:
        fields['mask'] = 'true'
        
    m = MultipartEncoder(fields=fields)

    def create_monitor_callback(encoder, callback):
        def monitor_callback(monitor):
            if callback:
                callback(monitor.bytes_read, encoder.len)
        return monitor_callback

    monitor = MultipartEncoderMonitor(m, create_monitor_callback(m, on_upload_progress))

    headers = {
        API_KEY_HEADER: api_key,
        'Content-Type': monitor.content_type
    }

    # Make the API request
    try:
        response = requests.post(url, headers=headers, data=monitor, stream=True)
        response.raise_for_status()  # Raise an HTTPError on bad status

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        content = bytearray()
        
        for chunk in response.iter_content(chunk_size=4096):
            content.extend(chunk)
            downloaded_size += len(chunk)
            if on_download_progress:
                on_download_progress(downloaded_size, total_size)

        if return_base64:
            # Return a base64 string if return_base64 is True
            base64_image = f"data:image/png;base64,{base64.b64encode(content).decode('utf-8')}"
            return {'base64Image': base64_image}
        else:
            # Write the response content to a temporary file
            output_image = NamedTemporaryFile(delete=False, prefix='rembg-', suffix='.png')
            output_image.write(content)
            output_image.close()
            return {'outputImagePath': output_image.name, 'cleanup': lambda: os.remove(output_image.name)}

    except requests.exceptions.HTTPError as e:
        # Specific handling for HTTP errors
        raise Exception(f"❌ HTTPError: {e.response.status_code} {e.response.text}")
    except requests.exceptions.RequestException as e:
        # General handling for request errors
        raise Exception(f"❌ RequestException: {str(e)}")
    except Exception as e:
        # General handling for any other exceptions
        raise Exception(f"❌ Exception: {str(e)}")

# Example usage:
def upload_progress(bytes_read, total_bytes):
    print(f"Upload progress: {bytes_read}/{total_bytes} bytes")

def download_progress(bytes_read, total_bytes):
    print(f"Download progress: {bytes_read}/{total_bytes} bytes")

result = rembg(
    api_key='Your_API_Key',  # Change to your API key
    input_image='Your_Image_Path',  # Change to your image path
    on_upload_progress=upload_progress, 
    on_download_progress=download_progress, 
    return_base64=False, # Set to True to return the output image as a Base64 string
    return_mask=True # Set to True to return the mask instead of the image
)