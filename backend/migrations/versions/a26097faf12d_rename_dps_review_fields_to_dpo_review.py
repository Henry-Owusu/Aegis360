"""rename dps review fields to dpo review

Revision ID: a26097faf12d
Revises: e95708740909
Create Date: 2026-08-27 13:08:55.599867

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "a26097faf12d"
down_revision = "e95708740909"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dps_review_decision',
            'dpo_review_decision',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dps_review_comment',
            'dpo_review_comment',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dps_reviewed_by',
            'dpo_reviewed_by',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dps_reviewed_at',
            'dpo_reviewed_at',
            'COLUMN'
    """)


def downgrade():
    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dpo_review_decision',
            'dps_review_decision',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dpo_review_comment',
            'dps_review_comment',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dpo_reviewed_by',
            'dps_reviewed_by',
            'COLUMN'
    """)

    op.execute("""
        EXEC sp_rename
            'dbo.dpia_assessments.dpo_reviewed_at',
            'dps_reviewed_at',
            'COLUMN'
    """)