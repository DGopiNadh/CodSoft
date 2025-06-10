from transformers import pipeline
from PIL import Image
import os

from transformers.utils import logging as hf_logging
hf_logging.set_verbosity_error()

def setup_captioning_model(model_name: str = "Salesforce/blip-image-captioning-base"):
    """Initialize a fast image captioning model."""
    captioner = pipeline(
        "image-to-text",
        model=model_name,
        device=-1  
    )
    return captioner

def load_image(image_path: str) -> Image.Image:
    """Load and convert image to RGB."""
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")
    return Image.open(image_path).convert("RGB")

def generate_caption(captioner, img: Image.Image, max_new_tokens: int = 12, temperature: float = 0.9) -> str:
    """Generate caption for an image."""
    result = captioner(
        img,
        generate_kwargs={
            "max_new_tokens": max_new_tokens,
            "temperature": temperature
        }
    )[0]['generated_text']
    return result.strip()

def caption_images(image_paths: list, max_new_tokens: int = 12, temperature: float = 0.9) -> list:
    """Generate captions for a list of image paths."""
    captioner = setup_captioning_model()
    results = []
    
    for path in image_paths:
        try:
            img = load_image(path)
            caption = generate_caption(captioner, img, max_new_tokens, temperature)
            results.append({"image_path": path, "caption": caption})
        except Exception as e:
            results.append({"image_path": path, "caption": f"Error: {str(e)}"})
    
    return results

if __name__ == "__main__":
    image_paths = [
        r"D:\Intern\ImageCaption\Img1.webp", 
        r"D:\Intern\ImageCaption\Img2.webp"
    ]
    
    captions = caption_images(
        image_paths=image_paths,
        max_new_tokens=12,
        temperature=0.9
    )
    
    print("\nImage Captioning Results:\n")
    for i, result in enumerate(captions):
        print(f"Image - {i + 1} ")
        print(f"Caption: {result['caption']}\n")
