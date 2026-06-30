import pdfplumber
import os
import json
import re


def clean_text(text):

    # Remove long slash separators
    text = re.sub(r'/{3,}', ' ', text)

    # Remove multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)

    # Remove isolated page numbers
    text = re.sub(r'^\d+\s*$', '', text)

    return text.strip()

DATA_FOLDER = "data"

all_pages = []

for file in os.listdir(DATA_FOLDER):

    if file.endswith(".pdf"):

        pdf_path = os.path.join(DATA_FOLDER, file)

        print(f"Processing: {file}")

        with pdfplumber.open(pdf_path) as pdf:

            print(f"Pages: {len(pdf.pages)}")

            for page_num, page in enumerate(pdf.pages):

                text = page.extract_text()

                if text:

                    text = clean_text(text)

                    if len(text.split()) >= 30:

                        all_pages.append({
                            "source": file,
                            "page": page_num + 1,
                            "text": text
                        })

print("\nExtraction Complete")
print("Total Records:", len(all_pages))

with open(
    "all_pages.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_pages,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Saved to all_pages.json")