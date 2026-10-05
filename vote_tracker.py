import csv
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
import xml.etree.ElementTree as ET

# start with a smal set of historical House votes
YEAR = 2026
VOTE_NUMBERS = [10, 11, 12, 13, 14]

# save the CSV
OUTPUT_FILE = Path(__file__).parent / "house_votes.csv"

def get_vote(year, vote_number):
    """Download one official vote record and extract useful fields."""
    xml_url = (
        f"https://clerk.house.gov/evs/{year}/"
        f"roll{vote_number:03d}.xml"
    )
    source_url = f"https://clerk.house.gov/Votes/{year}{vote_number}"

    with urlopen(xml_url, timeout=20) as response:
        root = ET.fromstring(response.read())

    metadata = root.find("vote-metadata")
    if metadata is None:
        raise ValueError("Vote metadata is missing.")

    def text(tag):
        return metadata.findtext(tag, default="").strip()

    totals = metadata.find("vote-totals/totals-by-vote")
    if totals is None:
        raise ValueError("Vote totals are missing.")

    def count(tag):
        value = totals.findtext(tag)
        if value is None:
            raise ValueError(f"Missing total: {tag}")
        return int(value)

    return {
        "year": year,
        "roll_call": vote_number,
        "date": text("action-date"),
        "bill_number": text("legis-num"),
        "description": text("vote-desc"),
        "vote_question": text("vote-question"),
        "result": text("vote-result"),
        "yea": count("yea-total"),
        "nay": count("nay-total"),
        "present": count("present-total"),
        "not_voting": count("not-voting-total"),
        "source_url": source_url,
    }

def main():
    votes = []

    for number in VOTE_NUMBERS:
        try:
            vote = get_vote(YEAR, number)
        except (URLError, TimeoutError, ET.ParseError, ValueError) as error:
            print(f"Could not retrieve vote {number}: {error}")
            continue

        votes.append(vote)
        print(
            f"Roll call {number} | {vote['date']} | "
            f"{vote['bill_number']}\n"
            f"  {vote['description']}\n"
            f"  Question: {vote['vote_question']}\n"
            f"  Result: {vote['result']} | "
            f"Yea: {vote['yea']} | Nay: {vote['nay']}\n"
        )

    if not votes:
        print("No votes retrieved. No CSV was written.")
        return

    keyword = input(
        "Filter by keyword, or press Enter for all votes: "
    ).strip().lower()

    if keyword:
        votes = [
            vote for vote in votes
            if keyword in (
                vote["bill_number"] + " "
                + vote["description"] + " "
                + vote["vote_question"]
            ).lower()
        ]

    if not votes:
        print("No votes matched. No CSV was written.")
        return

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(votes[0].keys()))
        writer.writeheader()
        writer.writerows(votes)

    print(f"Saved {len(votes)} of {len(VOTE_NUMBERS)} votes "
    f"to {OUTPUT_FILE.name}"
    )

if __name__ == "__main__":
    main()