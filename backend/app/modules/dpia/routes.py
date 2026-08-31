from flask import Blueprint, jsonify, request, g
from datetime import datetime, timezone

from app.extensions.database import db

from app.modules.authentication.middleware.auth import require_auth
from app.modules.authorization.decorators import (
    require_permission,
    require_role,
)

from app.modules.dpia.models import (
    DPIAAssessment,
    DPIAFullPIA,
    DPIAQuestion,
    DPIAResponse,
)

dpia_bp = Blueprint(
    "dpia",
    __name__,
    url_prefix="/api/dpia",
)


# ============================================================
# ASSESSMENTS
# ============================================================

@dpia_bp.get("/assessments")
@require_auth
@require_permission("assessment.view")
def list_assessments():
    status_filter = request.args.get("status")
    query = DPIAAssessment.query

    if status_filter:
        statuses = [s.strip() for s in status_filter.split(",")]
        query = query.filter(DPIAAssessment.status.in_(statuses))

    assessments = query.order_by(DPIAAssessment.created_at.desc()).all()

    return jsonify({
        "assessments": [
            {
                "id": a.id,
                "title": a.title,
                "project_manager": a.project_manager,
                "status": a.status,
                "created_at": a.created_at.isoformat(),
            } for a in assessments
        ]
    }), 200


@dpia_bp.post("/assessments")
@require_auth
@require_permission("assessment.create")
def create_assessment():
    data = request.get_json() or {}
    
    title = data.get("title")
    pm = data.get("project_manager")
    
    if not title or not pm:
        return jsonify({"error": "Title and Project Manager are required"}), 400

    assessment = DPIAAssessment(
        title=title,
        project_manager=pm,
        status="Draft",
        created_by=g.current_user.id
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({"message": "Assessment created", "id": assessment.id}), 201


@dpia_bp.get("/assessments/<assessment_id>")
@require_auth
@require_permission("assessment.view")
def get_assessment(assessment_id):
    assessment = DPIAAssessment.query.get(assessment_id)
    if not assessment:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
        "id": assessment.id,
        "title": assessment.title,
        "project_manager": assessment.project_manager,
        "status": assessment.status,
        "created_by": assessment.created_by,
        "created_at": assessment.created_at.isoformat(),
        "updated_at": assessment.updated_at.isoformat()
    }), 200


@dpia_bp.post("/assessments/<assessment_id>/submit")
@require_auth
@require_permission("assessment.create")
def submit_assessment(assessment_id):
    assessment = DPIAAssessment.query.get(assessment_id)
    if not assessment:
        return jsonify({"error": "Not found"}), 404
        
    assessment.status = "Submitted"
    db.session.commit()
    return jsonify({"message": "Assessment submitted", "status": assessment.status}), 200


# ============================================================
# QUESTIONS
# ============================================================

@dpia_bp.get("/questions")
@require_auth
def get_questions():
    section = request.args.get("section")
    
    query = DPIAQuestion.query.filter_by(is_active=True)
    if section:
        query = query.filter_by(section=section)
        
    questions = query.order_by(DPIAQuestion.display_order.asc()).all()
    
    return jsonify({
        "questions": [
            {
                "id": q.id,
                "section": q.section,
                "section_title": q.section_title,
                "question_number": q.question_number,
                "question_text": q.question_text,
                "guidance": q.guidance,
                "answer_type": q.answer_type,
                "options": q.options,
                "required": q.required,
                "display_order": q.display_order
            } for q in questions
        ]
    }), 200


@dpia_bp.post("/questions")
@require_auth
@require_role("DPO")
def create_question():
    data = request.get_json() or {}
    
    required_fields = ["section", "section_title", "question_number", "question_text", "answer_type"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400
            
    q = DPIAQuestion(
        section=data["section"],
        section_title=data["section_title"],
        question_number=data["question_number"],
        question_text=data["question_text"],
        guidance=data.get("guidance"),
        answer_type=data["answer_type"],
        options=data.get("options"),
        required=data.get("required", True),
        display_order=data.get("display_order", 0)
    )
    
    db.session.add(q)
    db.session.commit()
    
    return jsonify({"message": "Question created", "id": q.id}), 201

@dpia_bp.put("/questions/<int:question_id>")
@require_auth
@require_role("DPO")
def update_question(question_id):
    q = DPIAQuestion.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404
        
    data = request.get_json() or {}
    
    # Update fields if provided
    if "section" in data: q.section = data["section"]
    if "section_title" in data: q.section_title = data["section_title"]
    if "question_number" in data: q.question_number = data["question_number"]
    if "question_text" in data: q.question_text = data["question_text"]
    if "guidance" in data: q.guidance = data["guidance"]
    if "answer_type" in data: q.answer_type = data["answer_type"]
    if "options" in data: q.options = data["options"]
    if "required" in data: q.required = data["required"]
    if "display_order" in data: q.display_order = data["display_order"]
    if "is_active" in data: q.is_active = data["is_active"]
    
    db.session.commit()
    return jsonify({"message": "Question updated"}), 200

@dpia_bp.delete("/questions/<int:question_id>")
@require_auth
@require_role("DPO")
def delete_question(question_id):
    q = DPIAQuestion.query.get(question_id)
    if not q:
        return jsonify({"error": "Question not found"}), 404
        
    # Soft delete
    q.is_active = False
    db.session.commit()
    return jsonify({"message": "Question deleted"}), 200


# ============================================================
# RESPONSES
# ============================================================

@dpia_bp.get("/assessments/<assessment_id>/responses")
@require_auth
def get_responses(assessment_id):
    section = request.args.get("section")
    
    query = DPIAResponse.query.filter_by(assessment_id=assessment_id)
    if section:
        query = query.join(DPIAQuestion).filter(DPIAQuestion.section == section)
        
    responses = query.all()
    
    return jsonify({
        "responses": {
            r.question_id: r.answer for r in responses
        }
    }), 200


@dpia_bp.put("/assessments/<assessment_id>/responses")
@require_auth
def save_responses(assessment_id):
    data = request.get_json() or {}
    responses_dict = data.get("responses", {})
    
    for q_id, answer in responses_dict.items():
        resp = DPIAResponse.query.filter_by(assessment_id=assessment_id, question_id=q_id).first()
        if resp:
            resp.answer = answer
            resp.answered_by = g.current_user.id
            resp.answered_at = datetime.now(timezone.utc)
        else:
            resp = DPIAResponse(
                assessment_id=assessment_id,
                question_id=q_id,
                answer=answer,
                answered_by=g.current_user.id,
                answered_at=datetime.now(timezone.utc)
            )
            db.session.add(resp)
            
    db.session.commit()
    return jsonify({"message": "Responses saved"}), 200
