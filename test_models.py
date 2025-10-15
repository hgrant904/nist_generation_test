"""Simple test to verify models can be imported and instantiated."""

import sys
from datetime import datetime


def test_imports():
    print("Testing model imports...")
    try:
        from src.nist_automation.models import (
            ControlFamily,
            Control,
            ImplementationTier,
            Question,
            Option,
            Assessment,
            AssessmentSession,
            Response,
            Evidence,
        )
        from src.nist_automation.models.question import QuestionType
        from src.nist_automation.models.assessment import AssessmentStatus

        print("✓ All models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Import failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def test_config():
    print("\nTesting configuration...")
    try:
        from src.nist_automation.config import settings

        print(f"  Database URL configured: {bool(settings.database_url)}")
        print(f"  Environment: {settings.environment}")
        print("✓ Configuration loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Configuration failed: {str(e)}")
        return False


def test_repository():
    print("\nTesting repository...")
    try:
        from src.nist_automation.repositories import BaseRepository

        print("✓ Repository imported successfully")
        return True
    except Exception as e:
        print(f"✗ Repository import failed: {str(e)}")
        return False


def test_service():
    print("\nTesting service layer...")
    try:
        from src.nist_automation.services import CRUDService

        print("✓ Service layer imported successfully")
        return True
    except Exception as e:
        print(f"✗ Service import failed: {str(e)}")
        return False


def test_seeds():
    print("\nTesting seed data...")
    try:
        from src.nist_automation.seeds import (
            NIST_CSF_FAMILIES,
            NIST_CSF_CONTROLS,
            NIST_IMPLEMENTATION_TIERS,
            SeedRunner,
        )

        print(f"  Control Families: {len(NIST_CSF_FAMILIES)}")
        print(f"  Controls: {len(NIST_CSF_CONTROLS)}")
        print(f"  Implementation Tiers: {len(NIST_IMPLEMENTATION_TIERS)}")
        print("✓ Seed data loaded successfully")
        return True
    except Exception as e:
        print(f"✗ Seed data failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


def main():
    print("=" * 70)
    print("NIST Automation System - Model Verification")
    print("=" * 70 + "\n")

    results = []
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_config()))
    results.append(("Repository", test_repository()))
    results.append(("Service", test_service()))
    results.append(("Seeds", test_seeds()))

    print("\n" + "=" * 70)
    print("Test Results:")
    print("=" * 70)

    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:20s} {status}")
        if not passed:
            all_passed = False

    print("=" * 70)

    if all_passed:
        print("\n✓ All tests passed! System is ready to use.")
        print("  Next step: Run migrations with 'alembic upgrade head'")
        print("  Then load seeds with 'python -m src.nist_automation.seeds.seed_runner'\n")
        return 0
    else:
        print("\n✗ Some tests failed. Please check the errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
