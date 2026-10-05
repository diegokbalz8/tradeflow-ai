from pathlib import Path
# You might need to run: pip install pypdf pymupdf4llm
import pymupdf4llm 


def extract_and_convert_pdf(input_pdf_path, output_md_path, start_page=41, end_page=115):
    """
    Extracts specific pages from a PDF and converts them directly to Markdown.
    """
    print(f"Reading {input_pdf_path}...")
    
    # pymupdf4llm uses 0-based indexing. 
    # Page 1 is index 0, page 115 is index 114.
    page_range = range(start_page - 1, end_page)
    
    # Convert directly to Markdown text
    md_text = pymupdf4llm.to_markdown(input_pdf_path, pages=page_range)
    
    # Ensure the output directory exists
    output_path = Path(output_md_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save the markdown file
    output_path.write_text(md_text, encoding="utf-8")
    print(f"🎉 Success! Markdown saved to: {output_md_path}")


# THIS IS WHAT RUNS WHEN YOU EXECUTE THE FILE
if __name__ == "__main__":
    # Put your 700-page PDF in your project folder, or provide its full path here:
    source_pdf = r"C:\Users\d_cab\OneDrive\Documents\Aduanas\Manual_de_Procedimientos_Aduaneros2021_Febrero2021.pdf"
    
    # Where you want the final markdown file to go
    destination_md = "knowledge_base/document.md"
    
    # Call the function with your parameters
    extract_and_convert_pdf(source_pdf, destination_md, start_page=41, end_page=115)

