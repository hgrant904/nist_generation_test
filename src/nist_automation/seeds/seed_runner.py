"""Seed runner for loading NIST taxonomy and questionnaire data into the database."""

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.crud_service import CRUDService
from .nist_csf_data import (
    NIST_CSF_FAMILIES,
    NIST_CSF_CONTROLS,
    NIST_IMPLEMENTATION_TIERS,
    SAMPLE_QUESTIONS,
)
from ..models.question import QuestionType


class SeedRunner:

    def __init__(self, db: Session):
        self.db = db
        self.service = CRUDService(db)
        self.family_map: Dict[str, int] = {}
        self.control_map: Dict[str, int] = {}

    def seed_control_families(self) -> None:
        print("Seeding control families...")
        for family_data in NIST_CSF_FAMILIES:
            family = self.service.create_control_family(**family_data)
            self.family_map[family.code] = family.id
            print(f"  Created family: {family.code} - {family.name}")
        print(f"✓ Seeded {len(NIST_CSF_FAMILIES)} control families\n")

    def seed_controls(self) -> None:
        print("Seeding controls...")
        for control_data in NIST_CSF_CONTROLS:
            family_code = control_data.pop("family_code")
            family_id = self.family_map.get(family_code)
            if not family_id:
                print(f"  Warning: Family {family_code} not found, skipping control")
                continue

            control = self.service.create_control(family_id=family_id, **control_data)
            self.control_map[control.code] = control.id
            print(f"  Created control: {control.code} - {control.name}")
        print(f"✓ Seeded {len(NIST_CSF_CONTROLS)} controls\n")

    def seed_implementation_tiers(self) -> None:
        print("Seeding implementation tiers...")
        for tier_data in NIST_IMPLEMENTATION_TIERS:
            tier = self.service.create_implementation_tier(**tier_data)
            print(f"  Created tier {tier.tier_level}: {tier.name}")
        print(f"✓ Seeded {len(NIST_IMPLEMENTATION_TIERS)} implementation tiers\n")

    def seed_questions(self) -> None:
        print("Seeding sample questions...")
        for question_data in SAMPLE_QUESTIONS:
            control_code = question_data.pop("control_code")
            control_id = self.control_map.get(control_code)
            if not control_id:
                print(f"  Warning: Control {control_code} not found, skipping question")
                continue

            options_data = question_data.pop("options", None)

            question_type_str = question_data["question_type"]
            question_data["question_type"] = QuestionType[question_type_str]

            question = self.service.create_question(control_id=control_id, **question_data)
            print(f"  Created question for {control_code}: {question.question_text[:60]}...")

            if options_data:
                for option_data in options_data:
                    option = self.service.create_option(question_id=question.id, **option_data)
                    print(f"    Added option: {option.option_text}")

        print(f"✓ Seeded {len(SAMPLE_QUESTIONS)} sample questions\n")

    def run_all(self) -> None:
        print("\n" + "=" * 70)
        print("NIST CSF Data Seeding Process")
        print("=" * 70 + "\n")

        try:
            self.seed_control_families()
            self.seed_controls()
            self.seed_implementation_tiers()
            self.seed_questions()

            print("=" * 70)
            print("✓ All seed data loaded successfully!")
            print("=" * 70 + "\n")

        except Exception as e:
            print(f"\n✗ Error during seeding: {str(e)}")
            self.db.rollback()
            raise


def run_seeds() -> None:
    db = SessionLocal()
    try:
        runner = SeedRunner(db)
        runner.run_all()
    finally:
        db.close()


if __name__ == "__main__":
    run_seeds()
