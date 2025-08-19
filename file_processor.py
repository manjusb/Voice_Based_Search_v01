import fitz  # PyMuPDF
from PIL import Image
import io

# Try to import Google Cloud Vision, but handle gracefully if not available
try:
    from google.cloud import vision
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    print("Warning: Google Cloud Vision not available. Image OCR functionality will be limited.")

class FileProcessor:
    def __init__(self):
        if VISION_AVAILABLE:
            self.vision_client = vision.ImageAnnotatorClient()
        else:
            self.vision_client = None

    def process_file(self, file_path):
        """
        Processes the uploaded file (PDF or JPEG) and extracts text.
        """
        if file_path.lower().endswith('.pdf'):
            return self._process_pdf(file_path)
        elif file_path.lower().endswith(('.jpeg', '.jpg')):
            return self._process_image(file_path)
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or JPEG file.")

    def _process_pdf(self, file_path):
        """
        Extracts text from a PDF file.
        """
        try:
            doc = fitz.open(file_path)
            text = ""
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text += page.get_text()
            doc.close()
            print(f"[DEBUG] Extracted PDF text length: {len(text)}")
            print(f"[DEBUG] Extracted PDF text preview: {text[:200]}")
            return text
        except Exception as e:
            raise Exception(f"Error processing PDF file: {e}")

    def _process_image(self, file_path):
        """
        Performs OCR on an image file to extract text.
        """
        if not VISION_AVAILABLE:
            raise Exception("Google Cloud Vision is not available. Please install google-cloud-vision package for image OCR functionality.")
        
        try:
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image)
            texts = response.text_annotations

            if texts:
                return texts[0].description
            else:
                return ""
        except Exception as e:
            raise Exception(f"Error processing image file: {e}")

if __name__ == '__main__':
    # Example usage (for testing)
    # Create a dummy file for testing
    with open("dummy.txt", "w") as f:
        f.write("This is a test.")

    processor = FileProcessor()
    try:
        # To test, you would replace "dummy.txt" with a real PDF or JPEG file.
        # text = processor.process_file('path_to_your_file.pdf')
        # print(text)
        print("FileProcessor class created. Ready for use with PDF and JPEG files.")
    except Exception as e:
        print(f"An error occurred: {e}")