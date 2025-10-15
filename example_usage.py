"""Example usage of the NIST Automation system."""

from src.nist_automation.database import SessionLocal
from src.nist_automation.services import CRUDService
from src.nist_automation.models.assessment import AssessmentStatus


def main():
    print("\n" + "=" * 70)
    print("NIST Automation System - Example Usage")
    print("=" * 70 + "\n")

    db = SessionLocal()
    service = CRUDService(db)

    try:
        print("1. Fetching Control Families...")
        families = service.get_control_families(framework="NIST_CSF")
        print(f"   Found {len(families)} control families:")
        for family in families[:3]:
            print(f"   - {family.code}: {family.name}")
        if len(families) > 3:
            print(f"   ... and {len(families) - 3} more\n")

        print("2. Fetching Controls for first family...")
        if families:
            controls = service.get_controls(family_id=families[0].id)
            print(f"   Found {len(controls)} controls in {families[0].code}:")
            for control in controls[:3]:
                print(f"   - {control.code}: {control.name}")
            if len(controls) > 3:
                print(f"   ... and {len(controls) - 3} more\n")

            print("3. Fetching Implementation Tiers...")
            tiers = service.get_implementation_tiers()
            print(f"   Found {len(tiers)} implementation tiers:")
            for tier in tiers:
                print(f"   - Tier {tier.tier_level}: {tier.name}")
            print()

            print("4. Creating a sample assessment...")
            assessment = service.create_assessment(
                name="Example Security Assessment",
                description="Demonstration assessment using NIST CSF 2.0",
                framework="NIST_CSF",
                framework_version="2.0",
                status=AssessmentStatus.DRAFT,
                organization_name="Demo Organization",
                assessor_name="Demo User",
            )
            print(f"   Created assessment: {assessment.name} (ID: {assessment.id})")
            print(f"   Status: {assessment.status.value}\n")

            print("5. Fetching questions for a control...")
            if controls:
                questions = service.get_questions(control_id=controls[0].id)
                print(f"   Found {len(questions)} questions for {controls[0].code}:")
                for question in questions:
                    print(f"   - Type: {question.question_type.value}")
                    print(f"     Text: {question.question_text[:80]}...")
                    options = service.get_options(question_id=question.id)
                    if options:
                        print(f"     Options: {len(options)}")
                print()

            print("6. Statistics:")
            print(f"   - Total Control Families: {len(families)}")
            print(f"   - Total Controls: {sum(len(service.get_controls(f.id)) for f in families)}")
            print(f"   - Total Assessments: {len(service.get_assessments())}")
            print()

        print("=" * 70)
        print("✓ Example completed successfully!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}\n")
        import traceback

        traceback.print_exc()

    finally:
        db.close()


if __name__ == "__main__":
    main()
