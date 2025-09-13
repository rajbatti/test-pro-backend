from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException
from bson import ObjectId
from app.models import TestModel, ResultModel, QuestionModel, TestPaperModel, TestModelDTO
from app.db import tests_collection, results_collection, questions_collection
from app.services import questions_service

async def create_test(name, time_limit_minutes, is_practice, file,user):
    question_ids= await questions_service.get_questions_from_docx(file)
    test_dict={
        "name": name,
        "questions": question_ids,
        "time_limit_minutes": time_limit_minutes,
        "is_practice": is_practice,
        "author": user.email
    }
    result = await tests_collection.insert_one(test_dict)
    new_test = await tests_collection.find_one({"_id": result.inserted_id})
    return new_test

async def get_tests(user) -> List[TestModelDTO]:
    result_list = await results_collection.find({"user_id": ObjectId(user.id)}).to_list(length=None)
    test_list = await tests_collection.find({}).to_list(length=None)

    for test in test_list:
        for result in result_list:
            if test["_id"] == result["test_id"]:
                test["is_completed"] = True
                test["score"] = result["score"]
                test["completedAt"] = result["end_time"]
        if "is_completed" not in test:
            test["is_completed"] = False
    print(test_list)
    return test_list

async def get_test_by_id(test_id: str,user):
    if not ObjectId.is_valid(test_id):
        raise HTTPException(status_code=400, detail="Invalid test ID")
    result = await results_collection.find_one({"user_id":ObjectId(user.id),"test_id": ObjectId(test_id)})


    test = await tests_collection.find_one({"_id": ObjectId(test_id)})
    if test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    questions = await get_questions(test["questions"])
    test["questions"] = questions
    if result is not None:
        result=ResultModel(**result)
        return {"test": test, "result": result}
    else:
        return {"test": test, "result": None}


async def submit_test(test_id: str, answers: list, user: dict):
    # Validate test ID
    if not ObjectId.is_valid(test_id):
        raise ValueError("Invalid test ID")

    # Fetch the test
    test_doc = await tests_collection.find_one({"_id": ObjectId(test_id)})
    if not test_doc:
        raise ValueError("Test not found")

    test = TestModel(**test_doc)
    total_questions = len(test.questions)

    # Count correct answers
    correct_answers_count = 0
    for i, question_id in enumerate(test.questions):
        question_doc = await questions_collection.find_one({"_id": ObjectId(question_id)})
        if question_doc:
            correct_option = question_doc.get("correct_option")
            if i < len(answers) and answers[i] == correct_option:
                correct_answers_count += 1

    questions_attempted = len([a for a in answers if a.strip() != ""])
    score_percent = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0

    # Prepare result document
    result_dict = {
        "user_id": ObjectId(user.id),
        "test_id": ObjectId(test_id),
        "start_time": datetime.now(),  # Can be tracked from actual test start
        "end_time": datetime.now(),
        "answers": answers,
        "completed": True,
        "total_questions": total_questions,
        "questions_attempted": questions_attempted,
        "correct_answers": correct_answers_count,
        "score": score_percent
    }

    # Insert into DB
    inserted = await results_collection.insert_one(result_dict)
    stored_result = await results_collection.find_one({"_id": inserted.inserted_id})

    return "Result submited Sucessfully"

async def get_questions(question_ids):
    questions = []
    for question_id in question_ids:
        q=await questions_collection.find_one({"_id":question_id})
        questions.append(QuestionModel(**q))
    return questions

