import io
from typing import Tuple, Optional
from PIL import Image
import streamlit as st


class ImageProcessor:
    SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'webp']
    MAX_FILE_SIZE_MB = 10
    MAX_RESOLUTION = (2048, 2048)
    
    @classmethod
    def validate_image(cls, uploaded_file) -> Tuple[bool, str]:
        if uploaded_file is None:
            return False, "No file uploaded"
        
        if uploaded_file.size > cls.MAX_FILE_SIZE_MB * 1024 * 1024:
            return False, f"File size exceeds {cls.MAX_FILE_SIZE_MB}MB limit"
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in cls.SUPPORTED_FORMATS:
            return False, f"Unsupported format. Supported: {', '.join(cls.SUPPORTED_FORMATS)}"
        
        return True, "Valid image"
    
    @classmethod
    def process_image(cls, uploaded_file) -> Tuple[Optional[bytes], Optional[str]]:
        try:
            is_valid, message = cls.validate_image(uploaded_file)
            if not is_valid:
                st.error(message)
                return None, None
            
            image_bytes = uploaded_file.getvalue()
            
            with Image.open(io.BytesIO(image_bytes)) as img:
                if img.mode == 'RGBA':
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                if img.size[0] > cls.MAX_RESOLUTION[0] or img.size[1] > cls.MAX_RESOLUTION[1]:
                    img.thumbnail(cls.MAX_RESOLUTION, Image.Resampling.LANCZOS)
                
                output_buffer = io.BytesIO()
                img.save(output_buffer, format='JPEG', quality=85, optimize=True)
                processed_bytes = output_buffer.getvalue()
            
            return processed_bytes, 'jpeg'
            
        except Exception as e:
            st.error(f"Error processing image: {str(e)}")
            return None, None
    
    @classmethod
    def get_image_info(cls, uploaded_file) -> dict:
        try:
            with Image.open(uploaded_file) as img:
                return {
                    'filename': uploaded_file.name,
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'file_size_kb': round(uploaded_file.size / 1024, 2)
                }
        except Exception:
            return {'error': 'Could not read image information'}