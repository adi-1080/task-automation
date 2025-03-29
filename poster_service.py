import google.generativeai as genai
import requests
import cloudinary
import cloudinary.uploader
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Configure APIs
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-1.5-flash')

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def build_prompt_from_questions(request_data: dict) -> str:
    """Convert user answers into a detailed prompt"""
    base_template = f"""
    Design a vibrant poster with these characteristics:
    - Theme: {request_data['theme']['name']}
    - Description: {request_data['theme'].get('description', '')}
    - Style: {request_data['style']}
    - Colors: {', '.join(request_data['color_palette'])}
    - Elements: {', '.join(request_data['elements'])}
    - Mood: {request_data['mood']}
    - Text Placement: {request_data['text_placement']}
    """
    
    if request_data.get('additional_notes'):
        base_template += f"\nAdditional Notes: {request_data['additional_notes']}"
    
    return base_template.strip()

def enhance_prompt(basic_prompt: str) -> str:
    """Use Gemini to improve the prompt"""
    enhancement_instructions = """
    Improve this image generation prompt with:
    1. More vivid visual details
    2. Specific artistic style suggestions
    3. Clear composition guidance
    4. Ample space for text overlay
    5. Keep under 2000 characters
    """
    
    try:
        response = gemini_model.generate_content(
            f"{enhancement_instructions}\n\nOriginal Prompt: {basic_prompt}"
        )
        return response.text
    except Exception:
        return basic_prompt  # Fallback to original

def generate_images(prompt: str, num_variations: int = 3) -> list:
    """Generate multiple image variations using Stability AI"""
    API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
    headers = {
        "Authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
        "Accept": "image/png"
    }
    
    images = []
    for i in range(num_variations):
        body = {
            "text_prompts": [{"text": prompt, "weight": 1}],
            "cfg_scale": 7 + i,  # Vary creativity
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
            "seed": 1000 + i  # Different seeds for variations
        }
        
        response = requests.post(API_URL, headers=headers, json=body)
        response.raise_for_status()
        images.append(BytesIO(response.content))
    
    return images

def upload_to_cloudinary(image_bytes: BytesIO) -> dict:
    """Upload image to Cloudinary"""
    image_bytes.seek(0)
    return cloudinary.uploader.upload(
        image_bytes,
        folder="poster_generator",
        transformation=[
            {"width": 1024, "height": 1024, "crop": "limit"},
            {"quality": "auto:best"}
        ]
    )

def generate_posters(request_data: dict) -> dict:
    """Full pipeline from questions to final posters"""
    # Step 1: Build basic prompt from user answers
    basic_prompt = build_prompt_from_questions(request_data)
    
    # Step 2: Enhance prompt with Gemini
    enhanced_prompt = enhance_prompt(basic_prompt)
    
    # Step 3: Generate images
    image_files = generate_images(enhanced_prompt)
    
    # Step 4: Upload to Cloudinary
    uploaded = []
    for img in image_files:
        result = upload_to_cloudinary(img)
        uploaded.append({
            "url": result['secure_url'],
            "public_id": result['public_id'],
            "width": result['width'],
            "height": result['height'],
            "format": result['format']
        })
    
    return {
        "original_prompt": basic_prompt,
        "enhanced_prompt": enhanced_prompt,
        "variations": uploaded
    }