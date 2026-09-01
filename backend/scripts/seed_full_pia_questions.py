from app import create_app
from app.extensions.database import db
from app.modules.dpia.models.question import DPIAQuestion


QUESTIONS = [

    # ============================================================
    # PART 1
    # ============================================================

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.1",
        "question_text": (
            "What is your ‘good reason’ or legal ground for this processing activity? "
            "There may be different reasons for different parts of the processing, "
            "select all that apply."
        ),
        "guidance": (
            "If you are unsure, leave blank and discuss with the Data Protection team "
            "or your local legal team."
        ),
        "answer_type": "multi_choice",
        "options": [
            "The data subject has provided their consent",
            "The processing is necessary for the performance of a contract with the data subject or to take steps prior to entering into a contract",
            "The processing is necessary to comply with an Organisation legal obligation",
            "The processing is necessary to protect the vital interests of the data subject",
            "The processing is in the public interest",
            "We are pursuing legitimate business interests of Organisation",
        ],
        "required": True,
        "display_order": 1,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.2",
        "question_text": (
            "Please provide an explanation of your choice in the box provided."
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 2,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.3",
        "question_text": (
            "If you are processing any sensitive personal data, you must have an "
            "extra good reason/legal basis. Please select which of the following applies."
        ),
        "guidance": (
            "If your processing does not sit comfortably within one of these categories, "
            "it is likely to be illegal and this could place Organisation at huge risk. "
            "Seek advice from your local legal team immediately."
        ),
        "answer_type": "multi_choice",
        "options": [
            "The data subject has provided their explicit consent",
            "The processing is necessary in order to comply with employment law",
            "The processing is necessary to protect the vital interests of the data subject or another person, where the data subject is physically or legally incapable of providing their consent",
            "The data subject has deliberately placed the data in the public domain",
            "The processing is necessary as part of a legal case",
            "The processing is conducted ONLY for scientific research or statistical purposes",
            "The processing is in the public interest and is necessary to ensure high standards of quality and safety of health care, medicinal products or medical devices",
        ],
        "required": False,
        "display_order": 3,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.4",
        "question_text": (
            "Please also provide an explanation of your choice in the box provided."
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 4,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.5",
        "question_text": (
            "How are you telling data subjects about the processing you intend to do "
            "with their personal data? Are you providing a Fair Processing Notice "
            "at the point of collection?"
        ),
        "guidance": (
            "Data subjects must be fully informed about the processing of their data; "
            "they need to be made aware of the purpose of the processing, how long "
            "their data will be kept, who will be handling it, where it will be "
            "stored/shared, any third parties with access, and who to contact with concerns."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 5,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.6",
        "question_text": (
            "If you have selected consent or explicit consent as your answer to "
            "the questions above, what will you do if it is refused or withdrawn?"
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 6,
    },

    {
        "section": 1,
        "section_title": "Are you processing personal data fairly and lawfully?",
        "question_number": "1.7",
        "question_text": (
            "Is your project subject to any other legal or regulatory duties? "
            "Have you any concerns that there may be any conflict with data "
            "protection/privacy law?"
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 7,
    },

    # ============================================================
    # PART 2
    # ============================================================

    {
        "section": 2,
        "section_title": "For what specific reason are you processing this personal data?",
        "question_number": "2.1",
        "question_text": (
            "Are you collecting new personal data for the first time as part of "
            "this project, or using personal data already in Organisation’s possession?"
        ),
        "guidance": None,
        "answer_type": "single_choice",
        "options": [
            "Collecting new personal data",
            "Using personal data already held by Organisation",
            "Both",
        ],
        "required": True,
        "display_order": 8,
    },

    {
        "section": 2,
        "section_title": "For what specific reason are you processing this personal data?",
        "question_number": "2.2",
        "question_text": (
            "If you selected ‘Using data already held by Organisation’, is the purpose "
            "compatible with the original purpose for which it was collected and would "
            "the data subjects concerned expect this type of processing?"
        ),
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": False,
        "display_order": 9,
    },

    {
        "section": 2,
        "section_title": "For what specific reason are you processing this personal data?",
        "question_number": "2.3",
        "question_text": (
            "For what specific purpose are you collecting and processing personal data?"
        ),
        "guidance": (
            "Personal data must only be processed for a specified purpose, and this "
            "must be defined upfront before the personal data is collected."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 10,
    },

    {
        "section": 2,
        "section_title": "For what specific reason are you processing this personal data?",
        "question_number": "2.4",
        "question_text": (
            "Have you described this specific purpose in your notice to the data subjects?"
        ),
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 11,
    },

    {
        "section": 2,
        "section_title": "For what specific reason are you processing this personal data?",
        "question_number": "2.5",
        "question_text": (
            "Have you considered any wider purposes for which this data might be used "
            "in the future, or shared with other departments for related purposes?"
        ),
        "guidance": (
            "This scope/purpose cannot be expanded at a later date unless the data "
            "subjects concerned are notified."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 12,
    },

    # ============================================================
    # PART 3
    # ============================================================

    {
        "section": 3,
        "section_title": "Are you collecting the correct data as required for your project? Minimality (Section 19)",
        "question_number": "3.1",
        "question_text": (
            "Have you identified all of the actual fields containing personal data "
            "you will be processing? List these fields in the box to the right or "
            "attach a document if this outlines these clearly."
        ),
        "guidance": (
            "For example, if you selected Employment details in screening questions, "
            "you may enter fields such as previous job, job dates, reason for leaving, "
            "line manager, job title etc."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 13,
    },

    {
        "section": 3,
        "section_title": "Are you collecting the correct data as required for your project? Minimality (Section 19)",
        "question_number": "3.2",
        "question_text": (
            "Are there any of these fields which you could delete without compromising "
            "your needs? Could some be anonymised or pseudonymised?"
        ),
        "guidance": (
            "If you would like to discuss options for anonymising data, please discuss "
            "with your IS competency center, or with the Data Protection Team."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 14,
    },

    {
        "section": 3,
        "section_title": "Are you collecting the correct data as required for your project? Minimality (Section 19)",
        "question_number": "3.3",
        "question_text": (
            "Do you need to collect ALL fields in ALL cases? If not, do you have "
            "processes in place to only collect the minimum fields necessary in a specific case?"
        ),
        "guidance": "For example, only collect one medium of contact according to the consumer’s preference.",
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 15,
    },

    {
        "section": 3,
        "section_title": "Are you collecting the correct data as required for your project? Minimality (Section 19)",
        "question_number": "3.4",
        "question_text": (
            "Are you satisfied that all fields you are processing are fully relevant "
            "to your specified purpose as identified in section 2?"
        ),
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 16,
    },

    # ============================================================
    # PART 4
    # ============================================================

    {
        "section": 4,
        "section_title": "How will you be ensuring the personal data is accurate? Quality of Information (Section 26)",
        "question_number": "4.1",
        "question_text": (
            "Does the system you are using to store and manage the data allow you "
            "to make amendments to correct any inaccuracies? If you cannot actually "
            "delete or overwrite data, is there a facility to allow you to mark it as inaccurate?"
        ),
        "guidance": (
            "A data controller who processes personal data shall ensure that the data "
            "is complete, accurate, up to date and not misleading having regard to the "
            "purpose for the collection or processing of the personal data."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 17,
    },

    {
        "section": 4,
        "section_title": "How will you be ensuring the personal data is accurate? Quality of Information (Section 26)",
        "question_number": "4.2",
        "question_text": (
            "How will you be making sure that the personal data remains accurate "
            "and up to date throughout its use by Organisation?"
        ),
        "guidance": (
            "For example, do you have a business process to check for accuracy, "
            "or will it be the data subjects' responsibility to amend their own data?"
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 18,
    },

    {
        "section": 4,
        "section_title": "How will you be ensuring the personal data is accurate? Quality of Information (Section 26)",
        "question_number": "4.3",
        "question_text": (
            "If you are obtaining the personal data from a 3rd party or another "
            "department, how will you be ensuring that it is accurate and up to date? "
            "Are you able to demonstrate the original source of the data and related consent where relevant?"
        ),
        "guidance": (
            "For example, will you check when it was collected, last updated or confirmed, "
            "and will you check how its quality was ensured in the first place?"
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 19,
    },

    # ============================================================
    # PART 5
    # ============================================================

    {
        "section": 5,
        "section_title": "For how long will you need to keep this personal data and when/how will it be deleted? Retention of Records (Section 24)",
        "question_number": "5.1",
        "question_text": (
            "What retention period are you applying to the personal data? Why do "
            "you need to hold the data for this long?"
        ),
        "guidance": (
            "The questionnaire specifies a retention period of 7 YEARS. "
            "Personal data should only be held for the period necessary to fulfil "
            "the specified purpose."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 20,
    },

    {
        "section": 5,
        "section_title": "For how long will you need to keep this personal data and when/how will it be deleted? Retention of Records (Section 24)",
        "question_number": "5.2",
        "question_text": (
            "Is this retention period in line with the Organisation or Agency's "
            "Document Management and File Maintenance Policy & Retention Schedule?"
        ),
        "guidance": "Please refer to the applicable policy and retention schedule and check the Organisation retention period for this type of record.",
        "answer_type": "yes_no",
        "options": ["Yes", "No", "To be reviewed"],
        "required": True,
        "display_order": 21,
    },

    {
        "section": 5,
        "section_title": "For how long will you need to keep this personal data and when/how will it be deleted? Retention of Records (Section 24)",
        "question_number": "5.3",
        "question_text": (
            "Does the system allow you to delete data, both on an ad-hoc basis and "
            "subject to controlled retention periods? How are you ensuring data held "
            "electronically is destroyed after the specified retention period?"
        ),
        "guidance": (
            "Ensure deletion of records is available, while applying strict restrictions "
            "around who is able to delete records and what footprint remains afterwards."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 22,
    },

    {
        "section": 5,
        "section_title": "For how long will you need to keep this personal data and when/how will it be deleted? Retention of Records (Section 24)",
        "question_number": "5.4",
        "question_text": (
            "How are you ensuring any data held in physical form is destroyed after "
            "the specified retention period, including data held in archive?"
        ),
        "guidance": (
            "Consider whether you have a process for alerting the data custodian when "
            "a retention period has been reached, or whether someone manually checks "
            "archived files periodically."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 23,
    },

    {
        "section": 5,
        "section_title": "For how long will you need to keep this personal data and when/how will it be deleted? Retention of Records (Section 24)",
        "question_number": "5.5",
        "question_text": (
            "If you are relying on a 3rd party to apply retention/destruction on "
            "behalf of Organisation, what guarantees will you be given that the data "
            "has been destroyed securely?"
        ),
        "guidance": (
            "For example, a third party may provide a certificate confirming secure destruction."
        ),
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 24,
    },

    # ============================================================
    # PART 6
    # ============================================================

    {
        "section": 6,
        "section_title": "How are you ensuring that the rights of the data subjects are respected?",
        "question_number": "6.1",
        "question_text": (
            "Have you considered that data subjects may have the right to ask us "
            "for a copy of all of the personal data we hold about them? How would "
            "you deal with such a request?"
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 25,
    },

    {
        "section": 6,
        "section_title": "How are you ensuring that the rights of the data subjects are respected?",
        "question_number": "6.2",
        "question_text": (
            "Does the system storing the personal data allow you to readily extract "
            "all data held about a single data subject in order to fulfil such a request?"
        ),
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 26,
    },

    {
        "section": 6,
        "section_title": "How are you ensuring that the rights of the data subjects are respected?",
        "question_number": "6.3",
        "question_text": (
            "Does the system make any automated decisions which might affect data subjects? "
            "If so, will there be a process in place to allow human intervention? "
            "Please describe this in detail."
        ),
        "guidance": (
            "Examples include analysis or prediction of performance, economic profile, "
            "health, preferences, interests, reliability, behaviour, location or movement."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 27,
    },

    # ============================================================
    # PART 7
    # ============================================================

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.1",
        "question_text": (
            "Does your system allow you to allocate role-based access to the data "
            "on a need-to-know basis? Have you defined the roles and access permission groups? "
            "Please outline details here."
        ),
        "guidance": (
            "Consider whether all users need the same level of access. Good practice "
            "is to create separate permissions groups with different rights such as "
            "read, write, edit and delete depending on the user's role."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 28,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.2",
        "question_text": (
            "How will you ensure access controls and privileges are regularly reviewed, "
            "refreshed and revoked in line with joiners, leavers and transfers?"
        ),
        "guidance": (
            "Depending on the number of users, consider regular reviews or feeds from "
            "HR covering joiners, leavers and transfers."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 29,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.3",
        "question_text": (
            "Will users with access to the personal data be provided with training "
            "before being granted access which ensures they understand their obligations "
            "for protecting the security of the data?"
        ),
        "guidance": (
            "Consider employees and third-party users. Training should cover data "
            "protection responsibilities, system training and key areas of data protection risk."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 30,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.4",
        "question_text": (
            "Have you completed the Information Security Assessment under PMV3?"
        ),
        "guidance": (
            "Speak to your local IS competency center if you are unsure about this."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No", "Not applicable", "Unsure"],
        "required": True,
        "display_order": 31,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.5",
        "question_text": (
            "Will there be a need/ability to extract/export data from the system "
            "e.g. in a report format such as .xls, .csv, .doc or email message? "
            "If data will be exported in this manner, how will its ongoing security be assured?"
        ),
        "guidance": (
            "If ongoing security cannot be guaranteed, identify the risk and propose "
            "any mitigations you can employ."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 32,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.6",
        "question_text": (
            "Does the system allow you to trace any amendments made to records as "
            "an electronic audit trail, or does it simply record that changes have been made?"
        ),
        "guidance": (
            "It is important to trace who accessed data, when they accessed it and "
            "what changes were made so that inappropriate activity can be investigated."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 33,
    },

    {
        "section": 7,
        "section_title": "What security measures are you putting in place to protect the personal data?",
        "question_number": "7.7",
        "question_text": (
            "Will users be able to access the personal data from outside the Organisation network?"
        ),
        "guidance": (
            "Consider whether users need to be on an Organisation laptop or VPN, "
            "or whether they can access the system from personal computers or public locations."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 34,
    },

    # ============================================================
    # PART 8
    # ============================================================

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.1",
        "question_text": (
            "Have you documented this processing activity in the form of an Organisation PII map?"
        ),
        "guidance": (
            "If not, please contact the Organisation DP Specialist to complete one."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 35,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.2",
        "question_text": (
            "Will personal data be shared with or transferred to any 3rd parties?"
        ),
        "guidance": None,
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 36,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.3",
        "question_text": (
            "If you answered Yes, please outline the roles of all such 3rd parties here."
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 37,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.4",
        "question_text": (
            "Have you conducted due diligence on the 3rd party to ensure they provide "
            "an adequate level of protection for personal data? Have you completed the "
            "Organisation Supplier Assessment Questionnaire, and an Information Security audit as part of PMV3?"
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 38,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.5",
        "question_text": (
            "Please select the countries in which the 3rd parties are located, including "
            "any data centres, back up, DR and support desks."
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 39,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.6",
        "question_text": (
            "Where you have identified any personal data processing in other countries, "
            "how are you ensuring these countries offer adequate protection?"
        ),
        "guidance": (
            "Please consult with your local legal team to answer this question. "
            "This is a technical legal question and must be answered in conjunction "
            "with legal or the Data Protection Team."
        ),
        "answer_type": "text",
        "options": None,
        "required": False,
        "display_order": 40,
    },

    {
        "section": 8,
        "section_title": "Will you be sharing the personal data with any third parties or transferring across borders to other countries?",
        "question_number": "8.7",
        "question_text": (
            "Has your legal team been involved in drafting/reviewing/negotiating any "
            "contract with 3rd parties/suppliers? Please attach a copy of any contract "
            "to this PIA for review."
        ),
        "guidance": (
            "All contracts should have obtained appropriate legal involvement and signoff. "
            "If this has not happened, consult your local legal representatives before any contract is signed."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No", "Not applicable"],
        "required": False,
        "display_order": 41,
    },

    # ============================================================
    # PART 9
    # ============================================================

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.1",
        "question_text": (
            "Are you intending to use any of the personal data collected for the "
            "purposes of sending any marketing messages electronically by phone, SMS, "
            "email or via an automated calling system?"
        ),
        "guidance": (
            "If you answer No to this question, you may ignore the remainder of Part 9."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No"],
        "required": True,
        "display_order": 42,
    },

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.2",
        "question_text": (
            "How are you informing recipients about their rights in relation to our "
            "direct marketing communications? Please describe both the mechanism "
            "you are using and the information you are providing."
        ),
        "guidance": (
            "Examples of mechanisms include notice on website, automated phone message or email auto-reply."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 43,
        "conditional_logic": {
            "question_number": "9.1",
            "operator": "equals",
            "value": "Yes",
        },
    },

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.3",
        "question_text": (
            "How can you demonstrate that data subjects have consented to receive marketing communications?"
        ),
        "guidance": (
            "The website or application should have the built-in capability to record "
            "consents, date/time-stamp them and relate them to copies of the exact notices presented."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 44,
        "conditional_logic": {
            "question_number": "9.1",
            "operator": "equals",
            "value": "Yes",
        },
    },

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.4",
        "question_text": (
            "What type of consent mechanism are you relying on? Please describe."
        ),
        "guidance": (
            "For example, an opt-in tick box where the data subject actively provides consent, "
            "rather than a pre-ticked box requiring the data subject to untick it."
        ),
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 45,
        "conditional_logic": {
            "question_number": "9.1",
            "operator": "equals",
            "value": "Yes",
        },
    },

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.5",
        "question_text": (
            "Do your Direct Marketing email communications provide unsubscribe "
            "links/instructions? What is the process for managing withdrawal of consent?"
        ),
        "guidance": None,
        "answer_type": "text",
        "options": None,
        "required": True,
        "display_order": 46,
        "conditional_logic": {
            "question_number": "9.1",
            "operator": "equals",
            "value": "Yes",
        },
    },

    {
        "section": 9,
        "section_title": "Will you be using personal data for the purposes of marketing?",
        "question_number": "9.6",
        "question_text": (
            "If you are collecting personal data and consent via an Organisation "
            "website, are you using StarterKit and Organisationid?"
        ),
        "guidance": (
            "Please consult with your local IS or digital teams for help with this."
        ),
        "answer_type": "yes_no",
        "options": ["Yes", "No", "Not applicable"],
        "required": False,
        "display_order": 47,
        "conditional_logic": {
            "question_number": "9.1",
            "operator": "equals",
            "value": "Yes",
        },
    },
]


def seed_questions():
    created = 0
    updated = 0

    for q in QUESTIONS:
        existing_question = DPIAQuestion.query.filter_by(
            section="full_pia",
            question_number=q["question_number"]
        ).first()

        if existing_question:
            existing_question.question_text = q["question_text"]
            existing_question.guidance = q.get("guidance")
            existing_question.answer_type = q["answer_type"]
            existing_question.options = q.get("options")
            existing_question.required = q.get("required", True)
            existing_question.conditional_logic = q.get("conditional_logic")
            existing_question.display_order = q["display_order"]
            updated += 1
        else:
            new_question = DPIAQuestion(
                section="full_pia",
                section_title=q["section_title"],
                question_number=q["question_number"],
                question_text=q["question_text"],
                guidance=q.get("guidance"),
                answer_type=q["answer_type"],
                options=q.get("options"),
                required=q.get("required", True),
                conditional_logic=q.get("conditional_logic"),
                display_order=q["display_order"]
            )
            db.session.add(new_question)
            created += 1

    db.session.commit()

    print("Full PIA question seed completed successfully.")
    print(f"Questions created: {created}")
    print(f"Questions updated: {updated}")
    print(f"Total questions: {DPIAQuestion.query.count()}")


def main():
    app = create_app()

    with app.app_context():
        seed_questions()


if __name__ == "__main__":
    main()