from fastapi import APIRouter
from backend.app.services.scheme_collector import get_all_schemes

router = APIRouter(
    prefix="/schemes",
    tags=["Government Schemes"]
)


@router.get("/")
def get_all_schemes_api():

    schemes = get_all_schemes()

    return {
        "status": "success",
        "count": len(schemes),
        "schemes": schemes
    }


@router.post("/match")
def match_schemes(profile: dict):

    schemes = get_all_schemes()

    matched_schemes = []

    business_type = profile.get(
        "businessType", ""
    ).lower().strip()

    location = profile.get(
        "location", ""
    ).lower().strip()

    gender = profile.get(
        "gender", ""
    ).lower().strip()

    category = profile.get(
        "category", ""
    ).lower().strip()

    business_stage = profile.get(
        "businessStage", ""
    ).lower().strip()


    for scheme in schemes:

        score = 0

        target_groups = " ".join(
            scheme.get("target_groups", [])
        ).lower()

        description = scheme.get(
            "description", ""
        ).lower()

        scheme_text = (
            target_groups
            + " "
            + description
        )


        # -------------------------
        # GENDER MATCH
        # -------------------------

        if gender == "female":

            if "women" in scheme_text:
                score += 4


        # -------------------------
        # CATEGORY MATCH
        # -------------------------

        if category == "sc":

            if "sc" in scheme_text:
                score += 4

        elif category == "st":

            if "st" in scheme_text:
                score += 4

        elif category == "obc":

            if "obc" in scheme_text:
                score += 4

        elif category == "minority":

            if "minority" in scheme_text:
                score += 4


        # -------------------------
        # BUSINESS TYPE MATCH
        # -------------------------

        if business_type:

            if business_type == "technology":

                if (
                    "startup" in scheme_text
                    or "technology" in scheme_text
                ):
                    score += 3

            elif business_type in scheme_text:

                score += 3

            elif business_type == "services":

                if (
                    "business" in scheme_text
                    or "enterprise" in scheme_text
                ):
                    score += 1

            elif business_type == "trading":

                if (
                    "business" in scheme_text
                    or "micro" in scheme_text
                ):
                    score += 1


        # -------------------------
        # BUSINESS STAGE MATCH
        # -------------------------

        if business_stage == "idea":

            if (
                "entrepreneur" in scheme_text
                or "startup" in scheme_text
            ):
                score += 3


        elif business_stage == "new":

            if (
                "new entrepreneur" in scheme_text
                or "new entrepreneurs" in scheme_text
                or "startup" in scheme_text
            ):
                score += 3


        elif business_stage == "existing":

            if (
                "micro" in scheme_text
                or "small" in scheme_text
                or "business" in scheme_text
            ):
                score += 2


        elif business_stage == "expansion":

            if (
                "expansion" in scheme_text
                or "existing" in scheme_text
                or "business" in scheme_text
            ):
                score += 2


        # -------------------------
        # LOCATION MATCH
        # -------------------------

        scheme_location = str(
            scheme.get("location", "")
        ).lower()

        if location:

            if (
                location in scheme_location
                or "all india" in scheme_location
            ):
                score += 2


        # -------------------------
        # GENERAL ENTREPRENEUR MATCH
        # -------------------------

        if "entrepreneur" in scheme_text:

            score += 1


        # -------------------------
        # ADD MATCHED SCHEME
        # -------------------------

        if score > 0:

            matched_scheme = scheme.copy()

            matched_scheme["match_score"] = score

            matched_schemes.append(
                matched_scheme
            )


    # Highest score first

    matched_schemes.sort(
        key=lambda x: x["match_score"],
        reverse=True
    )


    return {
        "status": "success",
        "count": len(matched_schemes),
        "schemes": matched_schemes
    }