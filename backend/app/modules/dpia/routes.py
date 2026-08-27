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
    DPIAScreening,
    DPIAFullPIA,
    DPIAFullPIAResponse,
    DPIAFullPIAQuestion,
)



dpia_bp = Blueprint(
    "dpia",
    __name__,
    url_prefix="/api/dpia",
)


# CREATE DPIA ASSESSMENT - BASIC DATA

@dpia_bp.post("/assessments")
@require_auth
@require_permission("assessment.create")
def create_assessment():

    data = request.get_json() or {}

    required_fields = [
        "project_manager",
        "title",
        "nature_of_change",
    ]

    missing_fields = [
        field
        for field in required_fields
        if not data.get(field)
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields,
        }), 400

    if not isinstance(data["nature_of_change"], list):
        return jsonify({
            "error": "nature_of_change must be an array"
        }), 400

    if len(data["nature_of_change"]) == 0:
        return jsonify({
            "error": "At least one nature_of_change option is required"
        }), 400

    assessment = DPIAAssessment(
        project_manager=data["project_manager"],
        department_function_agency=
            data.get("department_function_agency"),
        area_ministry=
            data.get("area_ministry"),
        region=
            data.get("region"),
        title=data["title"],
        nature_of_change=
            data["nature_of_change"],
        other_nature_of_change=
            data.get("other_nature_of_change"),
        description=
            data.get("description"),
        implementation_timescales=
            data.get("implementation_timescales"),
        status="draft",
        created_by=g.current_user.id,
    )

    db.session.add(assessment)
    db.session.commit()

    return jsonify({
        "message": "DPIA assessment created successfully",
        "assessment": {
            "id": assessment.id,
            "project_manager": assessment.project_manager,
            "department_function_agency":
                assessment.department_function_agency,
            "area_ministry":
                assessment.area_ministry,
            "region":
                assessment.region,
            "title":
                assessment.title,
            "nature_of_change":
                assessment.nature_of_change,
            "other_nature_of_change":
                assessment.other_nature_of_change,
            "description":
                assessment.description,
            "implementation_timescales":
                assessment.implementation_timescales,
            "status":
                assessment.status,
            "created_by":
                assessment.created_by,
            "created_at":
                assessment.created_at.isoformat(),
            "updated_at":
                assessment.updated_at.isoformat(),
        }
    }), 201


# ============================================================
# GET DPIA ASSESSMENT
# ============================================================

@dpia_bp.get("/assessments/<assessment_id>")
@require_auth
@require_permission("assessment.view")
def get_assessment(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    return jsonify({
        "assessment": {
            "id": assessment.id,
            "project_manager":
                assessment.project_manager,
            "department_function_agency":
                assessment.department_function_agency,
            "area_ministry":
                assessment.area_ministry,
            "region":
                assessment.region,
            "title":
                assessment.title,
            "nature_of_change":
                assessment.nature_of_change,
            "other_nature_of_change":
                assessment.other_nature_of_change,
            "description":
                assessment.description,
            "implementation_timescales":
                assessment.implementation_timescales,
            "status":
                assessment.status,
            "created_by":
                assessment.created_by,
            "created_at":
                assessment.created_at.isoformat(),
            "updated_at":
                assessment.updated_at.isoformat(),
        }
    }), 200



# ============================================================
# UPDATE DPIA ASSESSMENT - BASIC DATA
# ============================================================

@dpia_bp.put("/assessments/<assessment_id>")
@require_auth
@require_permission("assessment.edit")
def update_assessment(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "draft":
        return jsonify({
            "error": "Basic Data can no longer be edited",
            "status": assessment.status
        }), 409

    data = request.get_json() or {}

    fields = [
        "project_manager",
        "department_function_agency",
        "area_ministry",
        "region",
        "title",
        "nature_of_change",
        "other_nature_of_change",
        "description",
        "implementation_timescales",
    ]

    for field in fields:

        if field not in data:
            continue

        if field == "nature_of_change":

            if not isinstance(data[field], list):
                return jsonify({
                    "error": "nature_of_change must be an array"
                }), 400

            if len(data[field]) == 0:
                return jsonify({
                    "error":
                        "At least one nature_of_change option is required"
                }), 400

        setattr(assessment, field, data[field])

    if not assessment.project_manager:
        return jsonify({
            "error": "Project Manager/Lead is required"
        }), 400

    if not assessment.title:
        return jsonify({
            "error": "Change/Project Title is required"
        }), 400

    if not assessment.nature_of_change:
        return jsonify({
            "error": "At least one nature of change option is required"
        }), 400

    db.session.commit()

    return jsonify({
        "message": "DPIA Basic Data updated successfully",
        "assessment_id": assessment.id,
        "status": assessment.status,
    }), 200




# ============================================================
# SUBMIT BASIC DATA
# ============================================================

@dpia_bp.post("/assessments/<assessment_id>/submit")
@require_auth
@require_permission("assessment.edit")
def submit_basic_data(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "draft":
        return jsonify({
            "error": "Assessment is no longer in the Basic Data stage",
            "status": assessment.status
        }), 409

    if not assessment.project_manager:
        return jsonify({
            "error": "Project Manager/Lead is required"
        }), 400

    if not assessment.title:
        return jsonify({
            "error": "Change/Project Title is required"
        }), 400

    if not assessment.nature_of_change:
        return jsonify({
            "error": "Nature of Change/Project is required"
        }), 400

    if (
        "other" in assessment.nature_of_change
        and not assessment.other_nature_of_change
    ):
        return jsonify({
            "error":
                "Please specify the Other nature of change/project"
        }), 400

    assessment.status = "screening"

    db.session.commit()

    return jsonify({
        "message": "Basic Data submitted successfully",
        "assessment_id": assessment.id,
        "next_stage": "screening",
        "status": assessment.status,
    }), 200

# ============================================================
# GET SCREENING
# ============================================================

@dpia_bp.get("/<assessment_id>/screening")
@require_auth
@require_permission("assessment.view")
def get_screening(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    screening = assessment.screening

    if not screening:
        return jsonify({
            "assessment_id": assessment.id,
            "screening": None
        }), 200

    return jsonify({
        "assessment_id": assessment.id,
        "screening": {
            "id": screening.id,
            "involves_personal_data": screening.involves_personal_data,

            "personal_data_subject_types":
                screening.personal_data_subject_types,

            "personal_data_categories":
                screening.personal_data_categories,

            "sensitive_personal_data_categories":
                screening.sensitive_personal_data_categories,

            "other_personal_data":
                screening.other_personal_data,

            "data_subject_locations":
                screening.data_subject_locations,

            "data_subject_specific_countries":
                screening.data_subject_specific_countries,

            "approximate_users_with_access":
                screening.approximate_users_with_access,

            "approximate_records_per_year":
                screening.approximate_records_per_year,

            "system_use_locations":
                screening.system_use_locations,

            "system_use_specific_countries":
                screening.system_use_specific_countries,

            "system_hosting_locations":
                screening.system_hosting_locations,

            "system_hosting_specific_countries":
                screening.system_hosting_specific_countries,

            "system_host":
                screening.system_host,

            "system_support_types":
                screening.system_support_types,

            "support_locations":
                screening.support_locations,

            "support_specific_countries":
                screening.support_specific_countries,

            "third_party_access":
                screening.third_party_access,

            "third_party_access_explanation":
                screening.third_party_access_explanation,

            "risk_tier":
                screening.risk_tier,

            "full_pia_required":
                screening.full_pia_required,

            "created_at":
                screening.created_at.isoformat(),

            "updated_at":
                screening.updated_at.isoformat(),
        }
    }), 200


# ============================================================
# CREATE SCREENING
# ============================================================

@dpia_bp.post("/<assessment_id>/screening")
@require_auth
@require_permission("assessment.edit")
def create_screening(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "screening":
        return jsonify({
            "error": "Assessment is not ready for screening",
            "status": assessment.status
        }), 409

    if assessment.screening:
        return jsonify({
            "error": "Screening already exists"
        }), 409

    data = request.get_json() or {}

    screening = DPIAScreening(
        assessment_id=assessment.id,

        involves_personal_data=
            data.get("involves_personal_data"),

        personal_data_subject_types=
            data.get("personal_data_subject_types"),

        personal_data_categories=
            data.get("personal_data_categories"),

        sensitive_personal_data_categories=
            data.get("sensitive_personal_data_categories"),

        other_personal_data=
            data.get("other_personal_data"),

        data_subject_locations=
            data.get("data_subject_locations"),

        data_subject_specific_countries=
            data.get("data_subject_specific_countries"),

        approximate_users_with_access=
            data.get("approximate_users_with_access"),

        approximate_records_per_year=
            data.get("approximate_records_per_year"),

        system_use_locations=
            data.get("system_use_locations"),

        system_use_specific_countries=
            data.get("system_use_specific_countries"),

        system_hosting_locations=
            data.get("system_hosting_locations"),

        system_hosting_specific_countries=
            data.get("system_hosting_specific_countries"),

        system_host=
            data.get("system_host"),

        system_support_types=
            data.get("system_support_types"),

        support_locations=
            data.get("support_locations"),

        support_specific_countries=
            data.get("support_specific_countries"),

        third_party_access=
            data.get("third_party_access"),

        third_party_access_explanation=
            data.get("third_party_access_explanation"),

        full_pia_required=
            data.get("full_pia_required"),
    )

    db.session.add(screening)
    db.session.commit()

    return jsonify({
        "message": "Screening created successfully",
        "assessment_id": assessment.id,
        "screening_id": screening.id,
    }), 201


# ============================================================
# UPDATE SCREENING
# ============================================================

@dpia_bp.put("/<assessment_id>/screening")
@require_auth
@require_permission("assessment.edit")
def update_screening(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    screening = assessment.screening

    if not screening:
        return jsonify({
            "error": "Screening not found"
        }), 404

    if assessment.status != "screening":
        return jsonify({
            "error": "Screening can no longer be edited",
            "status": assessment.status
        }), 409

    data = request.get_json() or {}

    fields = [
        "involves_personal_data",
        "personal_data_subject_types",
        "personal_data_categories",
        "sensitive_personal_data_categories",
        "other_personal_data",
        "data_subject_locations",
        "data_subject_specific_countries",
        "approximate_users_with_access",
        "approximate_records_per_year",
        "system_use_locations",
        "system_use_specific_countries",
        "system_hosting_locations",
        "system_hosting_specific_countries",
        "system_host",
        "system_support_types",
        "support_locations",
        "support_specific_countries",
        "third_party_access",
        "third_party_access_explanation",
        "full_pia_required",
    ]

    for field in fields:
        if field in data:
            setattr(screening, field, data[field])

    db.session.commit()

    return jsonify({
        "message": "Screening updated successfully",
        "assessment_id": assessment.id,
        "screening_id": screening.id,
    }), 200


# ============================================================
# SUBMIT SCREENING
# ============================================================

@dpia_bp.post("/<assessment_id>/screening/submit")
@require_auth
@require_permission("assessment.edit")
def submit_screening(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    screening = assessment.screening

    if not screening:
        return jsonify({
            "error": "Screening must be completed before submission"
        }), 400

    if assessment.status != "screening":
        return jsonify({
            "error": "Assessment is no longer in the screening stage",
            "status": assessment.status
        }), 409

    if screening.full_pia_required is None:
        return jsonify({
            "error": "Please specify whether a Full PIA is required"
        }), 400

    assessment.status = (
        "dpo_review"
        if screening.full_pia_required
        else "completed"
    )

    db.session.commit()

    return jsonify({
        "message": "Screening submitted successfully",
        "assessment_id": assessment.id,
        "full_pia_required": screening.full_pia_required,
        "next_status": assessment.status,
    }), 200



# ============================================================
# GET DPS REVIEW
# ============================================================

@dpia_bp.get("/assessments/<assessment_id>/dpo-review")
@require_auth
@require_permission("assessment.view")
def get_dpo_review(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    return jsonify({
        "assessment_id": assessment.id,
        "status": assessment.status,
        "dpo_review": {
            "decision": assessment.dpo_review_decision,
            "comment": assessment.dpo_review_comment,
            "reviewed_by": assessment.dpo_reviewed_by,
            "reviewed_at": (
                assessment.dpo_reviewed_at.isoformat()
                if assessment.dpo_reviewed_at
                else None
            ),
        }
    }), 200


# ============================================================
# SUBMIT DPO REVIEW
# ============================================================

@dpia_bp.post("/assessments/<assessment_id>/dpo-review")
@require_auth
@require_permission("assessment.approve")
@require_role("DPO")
def submit_dpo_review(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    # DPO can only review assessments waiting for DPO review
    if assessment.status != "dpo_review":
        return jsonify({
            "error": "Assessment is not awaiting DPO review",
            "status": assessment.status
        }), 409

    data = request.get_json() or {}

    decision = data.get("decision")
    comment = data.get("comment")

    # Validate decision
    if decision not in ["approved", "rejected"]:
        return jsonify({
            "error": "Invalid decision",
            "message": "Decision must be 'approved' or 'rejected'"
        }), 400

    # Rejection must include a reason
    if decision == "rejected" and not comment:
        return jsonify({
            "error": "Comment is required when rejecting an assessment"
        }), 400

    # Current authenticated user
    reviewer = g.current_user

    assessment.dpo_review_decision = decision
    assessment.dpo_review_comment = comment
    assessment.dpo_reviewed_by = reviewer.id
    assessment.dpo_reviewed_at = datetime.now(timezone.utc)

    # Move assessment through the workflow
    if decision == "approved":
        assessment.status = "full_pia"
    else:
        assessment.status = "draft"

    db.session.commit()

    return jsonify({
        "message": "DPO review submitted successfully",
        "assessment_id": assessment.id,
        "decision": decision,
        "status": assessment.status,
        "reviewed_by": reviewer.id,
        "reviewed_at": assessment.dpo_reviewed_at.isoformat(),
    }), 200



# ============================================================
# GET FULL PIA
# ============================================================

@dpia_bp.get("/<assessment_id>/full-pia")
@require_auth
@require_permission("assessment.view")
def get_full_pia(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status not in ["full_pia", "completed"]:
        return jsonify({
            "error": "Assessment is not in the Full PIA stage",
            "status": assessment.status
        }), 409

    full_pia = assessment.full_pia

    questions = (
        DPIAFullPIAQuestion.query
        .filter_by(is_active=True)
        .order_by(
            DPIAFullPIAQuestion.display_order.asc()
        )
        .all()
    )

    responses = {}

    if full_pia:
        for response in full_pia.responses:
            responses[response.question_id] = {
                "id": response.id,
                "answer": response.answer,
                "answered_by": response.answered_by,
                "answered_at": (
                    response.answered_at.isoformat()
                    if response.answered_at
                    else None
                ),
            }

    return jsonify({
        "assessment_id": assessment.id,
        "status": assessment.status,
        "full_pia": (
            {
                "id": full_pia.id,
                "status": full_pia.status,
                "started_at": full_pia.started_at.isoformat(),
                "submitted_at": (
                    full_pia.submitted_at.isoformat()
                    if full_pia.submitted_at
                    else None
                ),
            }
            if full_pia
            else None
        ),
        "questions": [
            {
                "id": question.id,
                "section": question.section,
                "section_title": question.section_title,
                "question_number": question.question_number,
                "question_text": question.question_text,
                "guidance": question.guidance,
                "answer_type": question.answer_type,
                "options": question.options,
                "required": question.required,
                "display_order": question.display_order,
                "conditional_logic": question.conditional_logic,
                "answer": (
                    responses[question.id]["answer"]
                    if question.id in responses
                    else None
                ),
                "response_id": (
                    responses[question.id]["id"]
                    if question.id in responses
                    else None
                ),
            }
            for question in questions
        ],
    }), 200


# ============================================================
# CREATE FULL PIA
# ============================================================

@dpia_bp.post("/<assessment_id>/full-pia")
@require_auth
@require_permission("assessment.edit")
def create_full_pia(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "full_pia":
        return jsonify({
            "error": "Assessment is not ready for Full PIA",
            "status": assessment.status
        }), 409

    if assessment.full_pia:
        return jsonify({
            "error": "Full PIA already exists",
            "full_pia_id": assessment.full_pia.id
        }), 409

    full_pia = DPIAFullPIA(
        assessment_id=assessment.id,
        status="draft"
    )

    db.session.add(full_pia)
    db.session.commit()

    return jsonify({
        "message": "Full PIA created successfully",
        "assessment_id": assessment.id,
        "full_pia_id": full_pia.id,
        "status": full_pia.status,
        "started_at": full_pia.started_at.isoformat(),
    }), 201


# ============================================================
# SAVE FULL PIA RESPONSES
# ============================================================

@dpia_bp.put("/<assessment_id>/full-pia/responses")
@require_auth
@require_permission("assessment.edit")
def save_full_pia_responses(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "full_pia":
        return jsonify({
            "error": "Full PIA is not available for editing",
            "status": assessment.status
        }), 409

    full_pia = assessment.full_pia

    if not full_pia:
        return jsonify({
            "error": "Full PIA has not been created"
        }), 404

    if full_pia.status != "draft":
        return jsonify({
            "error": "Full PIA can no longer be edited",
            "status": full_pia.status
        }), 409

    data = request.get_json() or {}

    responses = data.get("responses")

    if not isinstance(responses, list):
        return jsonify({
            "error": "responses must be an array"
        }), 400

    question_ids = {
        question.id
        for question in DPIAFullPIAQuestion.query.filter_by(
            is_active=True
        ).all()
    }

    saved = []

    for item in responses:

        question_id = item.get("question_id")
        answer = item.get("answer")

        if not question_id:
            return jsonify({
                "error": "Each response must include question_id"
            }), 400

        if question_id not in question_ids:
            return jsonify({
                "error": "Invalid question_id",
                "question_id": question_id
            }), 400

        response = DPIAFullPIAResponse.query.filter_by(
            full_pia_id=full_pia.id,
            question_id=question_id
        ).first()

        if not response:
            response = DPIAFullPIAResponse(
                full_pia_id=full_pia.id,
                question_id=question_id
            )
            db.session.add(response)

        response.answer = answer
        response.answered_by = g.current_user.id
        response.answered_at = datetime.now(timezone.utc)

        saved.append(question_id)

    db.session.commit()

    return jsonify({
        "message": "Full PIA responses saved successfully",
        "assessment_id": assessment.id,
        "full_pia_id": full_pia.id,
        "saved_questions": saved,
        "saved_count": len(saved),
    }), 200


# ============================================================
# SUBMIT FULL PIA
# ============================================================

@dpia_bp.post("/<assessment_id>/full-pia/submit")
@require_auth
@require_permission("assessment.edit")
def submit_full_pia(assessment_id):

    assessment = DPIAAssessment.query.get(assessment_id)

    if not assessment:
        return jsonify({
            "error": "Assessment not found"
        }), 404

    if assessment.status != "full_pia":
        return jsonify({
            "error": "Assessment is not in the Full PIA stage",
            "status": assessment.status
        }), 409

    full_pia = assessment.full_pia

    if not full_pia:
        return jsonify({
            "error": "Full PIA has not been created"
        }), 404

    if full_pia.status != "draft":
        return jsonify({
            "error": "Full PIA has already been submitted",
            "status": full_pia.status
        }), 409

    questions = (
        DPIAFullPIAQuestion.query
        .filter_by(is_active=True)
        .order_by(
            DPIAFullPIAQuestion.display_order.asc()
        )
        .all()
    )

    responses = {
        response.question_id: response
        for response in full_pia.responses
    }

    missing_questions = []

    for question in questions:

        # No response exists
        if question.id not in responses:
            if question.required:
                missing_questions.append({
                    "question_number": question.question_number,
                    "question_id": question.id,
                    "reason": "Required question has not been answered"
                })

            continue

        response = responses[question.id]

        # Empty answer
        if (
            question.required
            and (
                response.answer is None
                or response.answer == ""
                or response.answer == []
            )
        ):
            missing_questions.append({
                "question_number": question.question_number,
                "question_id": question.id,
                "reason": "Required question has not been answered"
            })

    if missing_questions:
        return jsonify({
            "error": "Full PIA cannot be submitted",
            "message": "Please answer all required questions",
            "missing_questions": missing_questions,
        }), 400

    full_pia.status = "submitted"
    full_pia.submitted_at = datetime.now(timezone.utc)

    assessment.status = "completed"

    db.session.commit()

    return jsonify({
        "message": "Full PIA submitted successfully",
        "assessment_id": assessment.id,
        "full_pia_id": full_pia.id,
        "full_pia_status": full_pia.status,
        "assessment_status": assessment.status,
        "submitted_at": full_pia.submitted_at.isoformat(),
    }), 200
