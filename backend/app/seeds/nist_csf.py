from __future__ import annotations

import asyncio
from typing import Any
from uuid import UUID

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import get_settings
from app.models.nist import NistCategory, NistFunction, NistQuestion, NistSubcategory

load_dotenv()

NIST_CSF_DATA = [
    {
        "code": "ID",
        "name": "Identify",
        "description": "Develop the organizational understanding to manage cybersecurity risk.",
        "categories": [
            {
                "code": "ID.AM",
                "name": "Asset Management",
                "description": "The data, personnel, devices, systems, and facilities are identified and managed consistent with their relative importance to organizational objectives and the organization’s risk strategy.",
                "subcategories": [
                    {
                        "code": "ID.AM-1",
                        "description": "Physical devices and systems within the organization are inventoried.",
                        "questions": [
                            {
                                "code": "ID.AM-1.Q1",
                                "prompt": "Do you maintain an up-to-date inventory of physical devices across the organization?",
                                "guidance": "Consider servers, workstations, mobile devices, and any specialized operational technology equipment.",
                            },
                            {
                                "code": "ID.AM-1.Q2",
                                "prompt": "How frequently is your asset inventory reviewed and reconciled?",
                                "guidance": "Describe the cadence for asset audits and the stakeholders involved in keeping inventories accurate.",
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "code": "PR",
        "name": "Protect",
        "description": "Develop and implement appropriate safeguards to ensure delivery of critical services.",
        "categories": [
            {
                "code": "PR.AC",
                "name": "Identity Management, Authentication and Access Control",
                "description": "Access to physical and logical assets is limited to authorized users, processes, or devices, and to authorized activities and transactions.",
                "subcategories": [
                    {
                        "code": "PR.AC-1",
                        "description": "Identities and credentials are managed for authorized devices and users.",
                        "questions": [
                            {
                                "code": "PR.AC-1.Q1",
                                "prompt": "How are user and device identities provisioned and deprovisioned within your environment?",
                                "guidance": "Outline any automated workflows or manual approval steps that exist.",
                            },
                            {
                                "code": "PR.AC-1.Q2",
                                "prompt": "What multi-factor authentication mechanisms are enforced for privileged access?",
                                "guidance": "Include details on conditional access rules or exceptions.",
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "code": "DE",
        "name": "Detect",
        "description": "Develop and implement appropriate activities to identify the occurrence of a cybersecurity event.",
        "categories": [
            {
                "code": "DE.AE",
                "name": "Anomalies and Events",
                "description": "Anomalous activity is detected and the potential impact of events is understood.",
                "subcategories": [
                    {
                        "code": "DE.AE-1",
                        "description": "A baseline of network operations and expected data flows for users and systems is established and managed.",
                        "questions": [
                            {
                                "code": "DE.AE-1.Q1",
                                "prompt": "Do you maintain baseline network activity profiles to aid in detecting anomalies?",
                                "guidance": "Highlight any tooling used for network or user behavior analytics.",
                            },
                            {
                                "code": "DE.AE-1.Q2",
                                "prompt": "Describe how anomalies are triaged and escalated for investigation.",
                                "guidance": "Explain the integration between monitoring systems and response playbooks.",
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "code": "RS",
        "name": "Respond",
        "description": "Develop and implement appropriate activities to take action regarding a detected cybersecurity event.",
        "categories": [
            {
                "code": "RS.RP",
                "name": "Response Planning",
                "description": "Response processes and procedures are executed and maintained, to ensure timely response to detected cybersecurity events.",
                "subcategories": [
                    {
                        "code": "RS.RP-1",
                        "description": "Response plan is executed during or after an incident.",
                        "questions": [
                            {
                                "code": "RS.RP-1.Q1",
                                "prompt": "When was your incident response plan last tested in a tabletop or live exercise?",
                                "guidance": "Include scope, frequency, and the teams that participated.",
                            },
                            {
                                "code": "RS.RP-1.Q2",
                                "prompt": "How are lessons learned from incidents incorporated back into response playbooks?",
                                "guidance": "Share examples of recent improvements based on post-incident reviews.",
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "code": "RC",
        "name": "Recover",
        "description": "Develop and implement appropriate activities to maintain plans for resilience and to restore any capabilities or services that were impaired due to a cybersecurity incident.",
        "categories": [
            {
                "code": "RC.RP",
                "name": "Recovery Planning",
                "description": "Recovery processes and procedures are executed and maintained to ensure timely restoration of systems or assets affected by cybersecurity events.",
                "subcategories": [
                    {
                        "code": "RC.RP-1",
                        "description": "Recovery plan is executed during or after a cybersecurity incident.",
                        "questions": [
                            {
                                "code": "RC.RP-1.Q1",
                                "prompt": "What strategies are in place to prioritize system restoration following an incident?",
                                "guidance": "Detail decision criteria for sequencing recoveries and communication practices.",
                            },
                            {
                                "code": "RC.RP-1.Q2",
                                "prompt": "Explain how recovery exercises validate backup integrity and recovery time objectives.",
                                "guidance": "Include tooling or automation leveraged to validate recoverability.",
                            },
                        ],
                    }
                ],
            }
        ],
    },
]


async def upsert_function(session: AsyncSession, data: dict[str, Any]) -> NistFunction:
    result = await session.execute(select(NistFunction).where(NistFunction.code == data["code"]))
    function = result.scalar_one_or_none()

    if function is None:
        function = NistFunction(code=data["code"], name=data["name"], description=data.get("description"))
        session.add(function)
        await session.flush()
    else:
        function.name = data["name"]
        function.description = data.get("description")

    return function


async def upsert_category(
    session: AsyncSession, function_id: UUID, data: dict[str, Any]
) -> NistCategory:
    result = await session.execute(select(NistCategory).where(NistCategory.code == data["code"]))
    category = result.scalar_one_or_none()

    if category is None:
        category = NistCategory(
            function_id=function_id,
            code=data["code"],
            name=data["name"],
            description=data.get("description"),
        )
        session.add(category)
        await session.flush()
    else:
        category.function_id = function_id
        category.name = data["name"]
        category.description = data.get("description")

    return category


async def upsert_subcategory(
    session: AsyncSession, category_id: UUID, data: dict[str, Any]
) -> NistSubcategory:
    result = await session.execute(
        select(NistSubcategory).where(NistSubcategory.code == data["code"])
    )
    subcategory = result.scalar_one_or_none()

    if subcategory is None:
        subcategory = NistSubcategory(
            category_id=category_id,
            code=data["code"],
            description=data["description"],
        )
        session.add(subcategory)
        await session.flush()
    else:
        subcategory.category_id = category_id
        subcategory.description = data["description"]

    return subcategory


async def upsert_question(
    session: AsyncSession,
    subcategory_id: UUID,
    data: dict[str, Any],
    order_index: int,
) -> NistQuestion:
    result = await session.execute(select(NistQuestion).where(NistQuestion.code == data["code"]))
    question = result.scalar_one_or_none()

    if question is None:
        question = NistQuestion(
            subcategory_id=subcategory_id,
            code=data["code"],
            prompt=data["prompt"],
            guidance=data.get("guidance"),
            order_index=order_index,
        )
        session.add(question)
    else:
        question.subcategory_id = subcategory_id
        question.prompt = data["prompt"]
        question.guidance = data.get("guidance")
        question.order_index = order_index

    return question


async def seed(session: AsyncSession) -> None:
    order_counter = 1

    for function_data in NIST_CSF_DATA:
        function = await upsert_function(session, function_data)

        for category_data in function_data.get("categories", []):
            category = await upsert_category(session, function.id, category_data)

            for subcategory_data in category_data.get("subcategories", []):
                subcategory = await upsert_subcategory(session, category.id, subcategory_data)

                for question_data in subcategory_data.get("questions", []):
                    await upsert_question(session, subcategory.id, question_data, order_counter)
                    order_counter += 1

    await session.commit()


async def main() -> None:
    settings = get_settings()
    engine = create_async_engine(settings.database_url, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with session_factory() as session:
        await seed(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
