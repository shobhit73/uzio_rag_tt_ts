import os
from docx import Document
from docx.document import Document as _Document
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from docx.table import _Cell, Table, _Row
from docx.text.paragraph import Paragraph
import pandas as pd
from PIL import Image
import io

# Configuration
DOCS_DIR = "."
OUTPUT_DIR = "processed_data"
IMAGES_DIR = os.path.join(OUTPUT_DIR, "images")
TEXT_OUTPUT = os.path.join(OUTPUT_DIR, "text_content.json")

os.makedirs(IMAGES_DIR, exist_ok=True)

def iter_block_items(parent):
    """
    Iterate through the document element by element (paragraphs and tables).
    """
    if isinstance(parent, _Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    elif isinstance(parent, _Row):
        parent_elm = parent._tr
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

def extract_images_from_doc(doc, doc_name):
    """
    Extracts images from the document and saves them.
    Returns a dictionary mapping image_hash/id to filename.
    """
    image_map = {}
    for i, rel in enumerate(doc.part.rels.values()):
        if "image" in rel.target_ref:
            try:
                img_data = rel.target_part.blob
                # Generate unique filename
                filename = f"{doc_name}_img_{i}.png"
                filepath = os.path.join(IMAGES_DIR, filename)
                
                with open(filepath, "wb") as f:
                    f.write(img_data)
                
                # In a real rigorous extraction, we'd map the relationship ID (rId) to the position in text.
                # structure. For now, we are bulk extracting context.
                # To map securely, we need to inspect xml.
                # For this efficiently-minded version, we'll store all images and let Gemini caption them.
                image_map[rel.rId] = filename
            except Exception as e:
                print(f"Failed to extract image {i} from {doc_name}: {e}")
    return image_map

def process_docx(file_path):
    doc_name = os.path.splitext(os.path.basename(file_path))[0].replace(" ", "_")
    doc = Document(file_path)
    
    # 1. Extract all images first to handle relationships
    # Note: python-docx makes it hard to get exact image position without low-level XML parsing.
    # To keep this "efficient" and simpler, we will extract all images as "Figures" for the document 
    # and treat them as separate chunks that need captioning.
    print(f"Extracting images from {doc_name}...")
    extract_images_from_doc(doc, doc_name)
    
    # 2. Extract Text
    content = []
    print(f"Extracting text from {doc_name}...")
    
    for block in iter_block_items(doc):
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                content.append({
                    "source": doc_name,
                    "type": "text",
                    "content": text
                })
        elif isinstance(block, Table):
            # Convert table to string/markdown
            table_data = []
            for row in block.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(" | ".join(row_data))
            table_text = "\n".join(table_data)
            if table_text.strip():
                content.append({
                    "source": doc_name,
                    "type": "table",
                    "content": table_text
                })
    
    # Add image references to data (listing them as chunks to be processed)
    # We re-scan the directory for images belonging to this doc
    images = [f for f in os.listdir(IMAGES_DIR) if f.startswith(doc_name)]
    for img in images:
        content.append({
            "source": doc_name,
            "type": "image",
            "content": f"Image File: {img}",
            "image_path": os.path.join(IMAGES_DIR, img)
        })
        
    return content

def main():
    files = [
        "UZIO Overview (Master).docx",
        "UZIO Scheduling.docx",
        "UZIO Time Tracking.docx"
    ]
    
    all_data = []
    
    for f in files:
        if os.path.exists(f):
            data = process_docx(f)
            all_data.extend(data)
        else:
            print(f"File not found: {f}")
            
    # Save to JSON
    import json
    with open(TEXT_OUTPUT, "w") as f:
        json.dump(all_data, f, indent=2)
    
    print(f"Extraction complete. Data saved to {TEXT_OUTPUT}")
    print(f"Total chunks: {len(all_data)}")

if __name__ == "__main__":
    main()
