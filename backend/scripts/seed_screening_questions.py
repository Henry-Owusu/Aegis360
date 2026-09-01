from app import create_app
from app.extensions.database import db
from app.modules.dpia.models.question import DPIAQuestion

QUESTIONS = [
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S1",
        "question_text": "Does the project or concept involve the use of any personal data?",
        "guidance": '"personal data" means data about an individual who can be identified, (a) from the data, or (b) from the data or other information in the possession of, or likely to come into the possession of the data controller; Examples: name, address, photo, access card number, mobile phone, email address, etc.',
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 1,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S2",
        "question_text": "Please select the categories of personal data and sensitive personal data which will be processed about each type of data subject:",
        "guidance": '"Special personal data" means personal data which consists of information that relates to (a) the race, colour, ethnic or tribal origin of the data subject; (b) the political opinion of the data subject; (c) the religious beliefs or other beliefs of a similar nature, of the data subject; (d) the physical, medical, mental health or mental condition or DNA of the data subject; (e) the sexual orientation of the data subject; (f) the commission or alleged commission of an offence by the individual; or (g) proceedings for an offence committed or alleged to have been committed by the individual, the disposal of such proceedings or the sentence of any court in the proceedings.',
        "answer_type": "matrix",
        "options": {
            "rows": [
                "Personal Data: Basic details, e.g. name, email",
                "Personal Data: Home address",
                "Personal Data: Marketing preferences",
                "Personal Data: Age/Date of Birth",
                "Personal Data: Family details (e.g. next of kin, relationships)",
                "Personal Data: Education",
                "Personal Data: Financial information inc. bank account details",
                "Personal Data: Employment details",
                "Personal Data: Online identifiers (e.g. IP addresses, cookie identifiers, RFI tags)",
                "Sensitive Personal Data: Race or colour, ethnic or tribal origin",
                "Sensitive Personal Data: Political opinion / Trade union membership",
                "Sensitive Personal Data: Religious beliefs / beliefs of a similar nature",
                "Sensitive Personal Data: Health or medical (physical or emotional) / mental condition data",
                "Sensitive Personal Data: Sexual life/orientation",
                "Sensitive Personal Data: Data relating to criminal offences",
                "Sensitive Personal Data: Passport/ Social security / Tax Identification numbers",
                "Sensitive Personal Data: Genetic data or biometric data",
                "Other: (please specify below)"
            ],
            "columns": ["Employee", "Consumer/Member of the public", "Customer", "Other"]
        },
        "required": True,
        "display_order": 2,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S3",
        "question_text": "Where are the data subjects located? You may select multiple areas.",
        "guidance": None,
        "answer_type": "multi_choice",
        "options": ["Ghana", "Europe", "Asia (exc. India)", "USA", "Asia Pacific", "West Africa", "Other African Country", "Other Locations"],
        "required": True,
        "display_order": 3,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S4",
        "question_text": "Please outline the specific countries (where known):",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 4,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S5",
        "question_text": "Approximately how many users will have access to the personal data?",
        "guidance": "This figure should include users, application support, helpdesk, call centres, specialists & consultants. Anyone who has access to the personal information for either business use or support of a system used to process the data. (Both permanent employees and contractors)",
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 5,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S6",
        "question_text": "Approximately how many records will be collected per year?",
        "guidance": "If the application holds a very small number of records, then the potential exposure is not as great as if it held records of all Organisation's employees globally",
        "answer_type": "single_choice",
        "options": ["10 or less records", "11 - 100 records", "101 - 1000", "1000+"],
        "required": True,
        "display_order": 6,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S7",
        "question_text": "Which location(s) will USE the system?",
        "guidance": None,
        "answer_type": "multi_choice",
        "options": ["Ghana", "Europe", "USA", "Asia Pacific", "West Africa", "Other African Country", "Other Locations"],
        "required": True,
        "display_order": 7,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S8",
        "question_text": "Please outline the specific countries (where known):",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 8,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S9",
        "question_text": "Where will the system be HOSTED?",
        "guidance": None,
        "answer_type": "multi_choice",
        "options": ["Ghana", "Europe", "USA & Canada", "Asia Pacific", "West Africa", "Other African Country", "Other Locations"],
        "required": True,
        "display_order": 9,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S10",
        "question_text": "Please outline the specific countries (where known):",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 10,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S11",
        "question_text": "Who will HOST the system?",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 11,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S12",
        "question_text": "Who will SUPPORT the system?",
        "guidance": "You may select multiple options as most apps will have multi-line support arrangements in place",
        "answer_type": "multi_choice",
        "options": ["Internal Team", "3rd Party Support", "Government Department", "Other Please"],
        "required": True,
        "display_order": 12,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S13",
        "question_text": "Where are support located?",
        "guidance": None,
        "answer_type": "multi_choice",
        "options": ["Europe", "Ghana", "Australasia", "India", "Asia (exc. India)", "South America", "Africa"],
        "required": True,
        "display_order": 13,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S14",
        "question_text": "Please outline the specific countries (where known):",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 14,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S15",
        "question_text": "Will any of the personal information be located in 3rd party premises or accessed by a 3rd party other than for hosting/support?",
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 15,
    },
    {
        "section": "screening",
        "section_title": "Screening Matrix",
        "question_number": "S16",
        "question_text": "If yes, please explain.",
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 16,
    }
]

def seed_questions():
    created = 0
    updated = 0

    for q in QUESTIONS:
        existing_question = DPIAQuestion.query.filter_by(
            section=q["section"],
            question_number=q["question_number"]
        ).first()

        if existing_question:
            existing_question.question_text = q["question_text"]
            existing_question.guidance = q.get("guidance")
            existing_question.answer_type = q["answer_type"]
            existing_question.options = q.get("options")
            existing_question.required = q.get("required", True)
            existing_question.display_order = q["display_order"]
            updated += 1
        else:
            new_question = DPIAQuestion(
                section=q["section"],
                section_title=q["section_title"],
                question_number=q["question_number"],
                question_text=q["question_text"],
                guidance=q.get("guidance"),
                answer_type=q["answer_type"],
                options=q.get("options"),
                required=q.get("required", True),
                display_order=q["display_order"]
            )
            db.session.add(new_question)
            created += 1

    db.session.commit()

    print("Screening matrix question seed completed successfully.")
    print(f"Questions created: {created}")
    print(f"Questions updated: {updated}")
    print(f"Total screening questions: {DPIAQuestion.query.filter_by(section='screening').count()}")


def main():
    app = create_app()
    with app.app_context():
        seed_questions()


if __name__ == "__main__":
    main()
