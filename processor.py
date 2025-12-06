import os
import json
import time
from llama_index.llms.gemini import Gemini
from llama_index.core.schema import ImageDocument
from PIL import Image
from dotenv import load_dotenv

# Load API Key
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

# Configuration
INPUT_FILE = "processed_data/text_content.json"
OUTPUT_FILE = "processed_data/enriched_content.json"

# Initialize Gemini 2.0 Flash (Cutting Edge, available)
llm = Gemini(model="models/gemini-2.0-flash-001", api_key=GOOGLE_API_KEY)

def generate_image_description(image_path):
    """
    Generates a detailed description for an image using Gemini Vision.
    """
    try:
        # LlamaIndex Gemini wrapper supports passing images
        # We construct a prompt for the multimodal model
        print(f"Generating description for {image_path}...")
        
        # Simple retry logic
        for attempt in range(3):
            try:
                # Using the complete function with image_documents might be needed depending on the version, 
                # but Gemini.complete normally takes text. 
                # Let's use the lower level completion or the specialized complete method if available.
                # Actually, LlamaIndex Gemini `complete` handles images in the `image_documents` arg.
                
                resp = llm.complete(
                    prompt="Describe this image in detail. If it is a chart, extract the data points. If it is text, transcribe it. If it is a diagram, explain the flow.",
                    image_documents=[ImageDocument(image_path=image_path)]
                )
                return resp.text
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {e}")
                time.sleep(2)
        return "Error generating description."
        
    except Exception as e:
        print(f"Failed to describe image {image_path}: {e}")
        return "Error processing image."

def generate_synthetic_questions(text_content):
    """
    Generates synthetic questions based on the text content.
    """
    try:
        prompt = f"""
        Read the following text and generate 3 potential questions a user might ask that can be answered by this text.
        Format the output as a simple list of questions string.
        
        Text:
        {text_content[:4000]} # Truncate to avoid context limit if somehow massive, though chunks should be small.
        """
        resp = llm.complete(prompt)
        return resp.text
    except Exception as e:
        print(f"Failed to generate questions: {e}")
        return ""

def process_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Input file {INPUT_FILE} not found. Run extractor.py first.")
        return

    with open(INPUT_FILE, "r") as f:
        data = json.load(f)
    
    enriched_data = []
    
    print(f"Processing {len(data)} items...")
    
    for i, item in enumerate(data):
        print(f"Processing item {i+1}/{len(data)}")
        new_item = item.copy()
        
        # 1. Image Captioning
        if item["type"] == "image":
            img_path = item.get("image_path")
            if img_path and os.path.exists(img_path):
                description = generate_image_description(img_path)
                new_item["image_description"] = description
                # We replace the "content" with the description for the text-index
                new_item["content"] = f"[IMAGE DESCRIPTION] {description}\n[ORIGINAL FILE] {item['content']}"
            else:
                new_item["content"] = "[MISSING IMAGE]"
        
        # 2. Synthetic Questions
        # We only do this if the content is substantial enough (> 100 chars) ensures meaningful questions
        content_text = new_item.get("content", "")
        if len(content_text) > 100 and item["type"] == "text":
             # Optimization: Only generate questions for "text" type (not table/image handled elsewhere)
             # To save time/cost, we can also sample or just do all. Let's do all substantial text.
             questions = generate_synthetic_questions(content_text)
             new_item["generated_questions"] = questions
        
        enriched_data.append(new_item)
        
        # Save checkpoint every 50 items
        if (i + 1) % 50 == 0:
            print(f"Saving checkpoint at {i+1}...")
            with open(OUTPUT_FILE, "w") as f:
                json.dump(enriched_data, f, indent=2)
        
        # Rate limiting
        time.sleep(0.5)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(enriched_data, f, indent=2)
    
    print(f"Enrichment complete. Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_data()
