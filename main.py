import re
from PIL import Image
from pdf2image import convert_from_path
import pytesseract
from ebooklib import epub

# Function to detect if a line is a section header
def is_section_header(line):
    # Define patterns for matching headers based on the provided structure
    patterns = [
        r'^绪论$',  # Preface
        r'^第[一-九]章$',  # Chapter titles, e.g., "第一章"
        r'^第[一二三四五六七八九十百千0-9]+节$',  # Section titles, e.g., "第一节"
        r'^余论$',  # Postscript
    ]
    
    for pattern in patterns:
        if re.match(pattern, line.strip()):
            return True
    return False

def pdf_to_epub_with_structure(pdf_path, epub_name):
    images = convert_from_path(pdf_path)
    text_parts = []
    current_chapter = None
    current_section = None
    chapters = []

    for i, image in enumerate(images):
        print(f"Processing page {i + 1}")
        text = pytesseract.image_to_string(image, lang='chi_sim')  # Use 'eng' for English
        
        lines = text.split('\n')
        for line in lines:
            stripped_line = line.strip()
            if is_section_header(stripped_line):
                # If it's a new chapter or section, create a new entry
                if '章' in stripped_line:
                    current_chapter = stripped_line
                    current_section = None
                else:
                    current_section = stripped_line
                chapters.append({
                    'chapter': current_chapter,
                    'section': current_section,
                    'content': ''
                })
            elif chapters:  # Add content only if we have a chapter/section
                chapters[-1]['content'] += line + '\n'

    # Create EPUB book
    book = epub.EpubBook()
    book.set_identifier('id12345678')
    book.set_title('Structured Converted Book')
    book.set_language('zh')
    book.add_author('Author Name')

    toc = []
    spine = ['nav']

    # Create chapters from the structured text
    for item in chapters:
        c = epub.EpubHtml(title=f"{item['chapter']} - {item['section']}", file_name=f"{item['chapter']}_{item['section']}.xhtml", lang='zh')
        c.content = f"<h1>{item['chapter']}</h1><h2>{item['section']}</h2><p>{item['content']}</p>"
        book.add_item(c)
        
        # Build TOC and spine
        toc_entry = (epub.Link(f"{item['chapter']}_{item['section']}.xhtml", f"{item['chapter']} - {item['section']}", f"{item['chapter']}_{item['section']}"))
        toc.append(toc_entry)
        spine.append(c)

    # Define Table Of Contents
    book.toc = tuple(toc)

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Set spine order
    book.spine = spine

    # Write to the file
    epub.write_epub(epub_name, book, {})

# Call function with your PDF path and desired EPUB name
pdf_to_epub_with_structure('example.pdf', 'output_structured.epub')