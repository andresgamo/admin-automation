from typing import List, Dict, Tuple, Union
from services.onboarding.models import NewHire, Buddy


def create_pairs(rows: List[Dict]) -> List[Tuple[NewHire, Buddy]]:
    """
    Iterate over each row and, for rows where the "country" equals "colombia",
    create a tuple containing a NewHire and a Buddy.
    """
    pairs = []
    for row in rows:
        if row.get("country", "") != "colombia":
            continue

        new_hire = NewHire(
            name=row["nh_name"],
            newhire_id=row["nh_id"],
            gl_email=row["nh_gl_email"],
            personal_email=row["nh_personal_email"],
            address=row["nh_address"],
            city=row["nh_city"],
            phone=row["nh_phone"],
            size=row["nh_size"],
            onboarding=row["nh_onboarding"].replace(" ", "_"),
            client=row["nh_client"],
        )
        buddy = Buddy(
            name=row["bp_name"],
            address=row["bp_address"],
            phone=row["bp_phone"],
            support=row["bp_onboarding"].replace(" ", "_"),
        )
        pairs.append((new_hire, buddy))
    return pairs


def categorize_pairs(pairs: List[Tuple[NewHire, Buddy]]) -> Tuple[List, List]:
    """
    Splits (NewHire, Buddy) pairs into buddy_program and onsite_lunch groups.
    """
    buddy_program = []
    onsite_lunch = []
    laptop_delivery = []
    for nh, bd in pairs:
        match (nh.onboarding, bd.support):
            case ("remote", _):
                buddy_program.extend([nh, bd])
                laptop_delivery.append(nh)
            case ("on_site", "remote"):
                buddy_program.extend([nh, bd])
                onsite_lunch.append(nh)
            case _:
                onsite_lunch.extend([nh, bd])
    return buddy_program, onsite_lunch, laptop_delivery


def unpairing_buddy_program(
    buddy_program: List[Union[NewHire, Buddy]],
) -> Tuple[List[NewHire], List[Buddy]]:
    """
    Given a flat list of NewHire and Buddy objects, returns two lists:
    1) all the NewHires
    2) all the Buddies
    """
    new_hires: List[NewHire] = []
    buddies: List[Buddy] = []

    for person in buddy_program:
        match person:
            case NewHire():
                new_hires.append(person)
            case Buddy():
                buddies.append(person)
            case _:
                # optionally log or raise if you expect only those two types
                pass

    return new_hires, buddies
