import os
import requests
from unittest import mock
import pytest
from rembg.rembg import rembg  # Adjust the import to your actual module

# Define your tests here
@pytest.fixture(autouse=True)
def setup_mocks():
    with mock.patch('tempfile.NamedTemporaryFile', mock.MagicMock()) as mock_tmp, \
         mock.patch('os.remove', mock.MagicMock()):
        mock_tmp.return_value.__enter__.return_value.name = 'path/to/output.png'
        yield

def test_rembg_api_key_not_provided():
    with pytest.raises(Exception, match='⚠️⚠️⚠️ WARNING ⚠️⚠️⚠️: API key not provided, trials will be very limited.'):
        rembg(api_key='', input_image='path/to/image.png')

def test_rembg_return_base64():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'image data']
        result = rembg(api_key='your-api-key', input_image='path/to/image.png', return_base64=True)
        assert result == {'base64Image': 'data:image/png;base64,aW1hZ2UgZGF0YQ=='}
        assert mock_post.called

def test_rembg_return_output_image_path():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'image data']
        result = rembg(api_key='your-api-key', input_image='path/to/image.png', return_base64=False)
        assert result == {'outputImagePath': 'path/to/output.png', 'cleanup': mock.ANY}
        assert mock_post.called

def test_rembg_request_fails():
    with mock.patch('requests.post') as mock_post:
        mock_post.side_effect = requests.RequestException('Request failed')
        with pytest.raises(Exception, match='❌ RequestException: Request failed'):
            rembg(api_key='your-api-key', input_image='path/to/image.png')

def test_rembg_server_error():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 500
        mock_post.return_value.text = 'Internal Server Error'
        with pytest.raises(Exception, match='❌ HTTPError: 500 Internal Server Error'):
            rembg(api_key='your-api-key', input_image='path/to/image.png')

def test_rembg_no_response():
    with mock.patch('requests.post') as mock_post:
        mock_post.side_effect = requests.RequestException()
        with pytest.raises(Exception, match='❌ RequestException'):
            rembg(api_key='your-api-key', input_image='path/to/image.png')

def test_rembg_api_key_header():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'image data']
        rembg(api_key='your-api-key', input_image='path/to/image.png')
        assert mock_post.call_args[1]['headers']['x-api-key'] == 'your-api-key'

def test_rembg_return_mask():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'image data']
        rembg(api_key='your-api-key', input_image='path/to/image.png', return_mask=True, return_base64=False)
        assert any('mask' in call.kwargs['data'].fields for call in mock_post.mock_calls)

def test_rembg_handle_buffer_input():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'processed image data']
        input_buffer = b'input image data'
        result = rembg(api_key='your-api-key', input_image=input_buffer)
        assert result == {'outputImagePath': 'path/to/output.png', 'cleanup': mock.ANY}
        assert mock_post.called

def test_rembg_handle_base64_input():
    with mock.patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.iter_content = lambda chunk_size: [b'processed image data']
        base64_input = {'base64': 'aW5wdXQgaW1hZ2UgZGF0YQ=='}
        result = rembg(api_key='your-api-key', input_image=base64_input)
        assert result == {'outputImagePath': 'path/to/output.png', 'cleanup': mock.ANY}
        assert mock_post.called

def test_rembg_invalid_input_type():
    with pytest.raises(Exception, match='Invalid input type. Must be a file path, bytes, or a dict with a base64 property.'):
        rembg(api_key='your-api-key', input_image=123)
