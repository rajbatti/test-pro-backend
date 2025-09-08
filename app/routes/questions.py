from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services import pandoc_service, extractor_service
from app.db import questions_collection
from app.models import QuestionModel
from app.schemas import QuestionCreate, QuestionUpdate
from bson import ObjectId
import json
import os
import base64
import re
import tempfile
router = APIRouter()



def image_embedding(output):
    media_dir = "media"
    img_tags = re.findall(r'<img\s+[^>]*src="([^"]+)"', output)

    for img_src in img_tags:
        if img_src.startswith(media_dir + "/"):
            img_path = img_src
            full_img_path = os.path.join(os.getcwd(), img_path)

            if os.path.exists(full_img_path):
                with open(full_img_path, "rb") as img_file:
                    img_data = img_file.read()
                    encoded_string = base64.b64encode(img_data).decode('utf-8')
                    ext = os.path.splitext(img_path)[1].lower()
                    if ext == '.png':
                        mime = 'image/png'
                    elif ext in ['.jpg', '.jpeg']:
                        mime = 'image/jpeg'
                    elif ext == '.gif':
                        mime = 'image/gif'
                    else:
                        mime = 'application/octet-stream'

                    data_uri = f"data:{mime};base64,{encoded_string}"
                    output = output.replace(f'src="{img_src}"', f'src="{data_uri}"')
    return output

def add_image_embbedings(q):
    q["question"] = image_embedding(q["question"])
    l=[]
    for o in q["options"]:
        l.append(image_embedding(o))
    q["options"] = l
    return q


@router.post("/convert")
async def convert_docx(file: UploadFile = File(...)):
    """Upload DOCX, convert to HTML, extract questions, store in MongoDB"""
    print("request recieved")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        output_text = pandoc_service.docx_to_html(tmp_path)
        pattern = r'\[.*\]'
        match = re.search(pattern, output_text, re.DOTALL)
        # Now attempt to parse the JSON
        print(match.group(0))
        try:
            parsed_json = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON: {e}")

        inserted_ids = []
        print(parsed_json)
        for q in parsed_json:
            q=add_image_embbedings(q)
            result = await questions_collection.insert_one(q)
            inserted_ids.append(str(result.inserted_id))

        return {"inserted_ids": inserted_ids}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/questions")
async def get_questions():
    docs = questions_collection.find()
    return [QuestionModel(**doc) async for doc in docs]


@router.get("/questions/{id}")
async def get_question(id: str):
    doc = await questions_collection.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Question not found")
    return QuestionModel(**doc)


@router.put("/questions/{id}")
async def update_question(id: str, body: QuestionUpdate):
    update_data = {k: v for k, v in body.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await questions_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question updated"}


@router.delete("/questions/{id}")
async def delete_question(id: str):
    result = await questions_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted"}
