# Imports necessary for validation
from PIL import Image
import io
import os
import mimetypes

# Define accepted safe formats
ALLOWED_IMAGE_MIME_TYPES = {
    'image/jpeg', 
    'image/png', 
    'image/webp' # Added webp as modern standard support
}

def process_uploaded_file(file_data, original_filename):
    """
    Handles file validation and processing. 
    :param file_data: File bytes (from uploaded stream).
    :param original_filename: Name provided by the client.
    :return: Processed image data or raises an exception on failure.
    """
    # --- START FIX IMPLEMENTATION ---
    
    # 1. Basic Content/MIME Type Validation
    try:
        # Use mimetypes for initial check, though this is not foolproof
        mime_type, _ = mimetypes.guess_type(original_filename)

        if mime_type is None or mime_type.startswith('text/') or mime_type.startswith('application/'):
             raise ValueError("Unsupported file type based on MIME inspection.")
        
    except Exception as e:
        # Catch all initial metadata failures
        print(f"Initial validation failed: {e}")
        return None

    # 2. Robust Structural Validation (Image Check)
    if mime_type in ALLOWED_IMAGE_MIME_TYPES:
        try:
            image_stream = io.BytesIO(file_data)
            img = Image.open(image_stream)
            
            # Check if the image can be loaded and scaled, which validates integrity
            img.verify() 
            img.close() # Important to release resources
            
            return img
        except Exception as e:
            # Catch exceptions specific to Pillow (e.g., invalid header/format)
            raise ValueError(f"File content is not a verifiable image structure: {str(e)}")

    # 3. General Fallback Rejection
    raise ValueError("Unsupported or unsafe file format detected.")
    
    # --- END FIX IMPLEMENTATION ---


def upload_file_handler(uploaded_file):
    """Endpoint handler using the validated processing logic."""
    if not uploaded_file:
        return {"success": False, "error": "No file provided."}

    file_bytes = uploaded_file.read() # Read content into bytes for processing
    filename = uploaded_file.filename or 'unknown'
    
    try:
        processed_image = process_uploaded_file(file_bytes, filename)
        if processed_image:
            # Logic to proceed with image resizing/saving...
            return {"success": True, "message": f"File {filename} successfully validated and processed."}
    except ValueError as e:
        # Report specific validation failure to the user
        print(f"Validation Failure for {filename}: {e}")
        return {"success": False, "error": str(e)}
