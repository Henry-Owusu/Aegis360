from app.modules.dpia.models import assessment
from flask import Blueprint, jsonify, request, g

from app.extensions.database import db

from app.modules.authentication.middleware.auth import require_auth

from app.modules.authorization.decorators import require_permission

from app.modules.dpia.models import (
    DPIAAssessment,
    DPIAScreening,
)



dpia_bp = Blueprint(
    "dpia",
    __name__,
    url_prefix="/api/dpia",
)


# ============================================================
# CREATE DPIA ASSESSMENT - BASIC DATA
# ============================================================

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
        "dps_review"
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