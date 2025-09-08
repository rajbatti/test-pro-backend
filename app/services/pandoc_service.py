import pypandoc
import os
import app.services.aiservice as aiservice
import base64
import re

def docx_to_html(file_path: str, media_dir: str = "media") -> str:
    """
    Convert DOCX file to HTML string using pandoc inside Docker.
    - Preserves math equations with MathJax
    - Extracts images into a 'media/' folder
    - Keeps <img src="media/..."> references in HTML
    """
    os.makedirs(media_dir, exist_ok=True)

    output = pypandoc.convert_file(
        file_path,
        to="html",
        format="docx",
        extra_args=[
            "--standalone",
            "--mathjax",
            f"--extract-media={media_dir}"
        ]
    )

    output=aiservice.call_gemini_extract_mcqs(str(output.strip()))
    return output