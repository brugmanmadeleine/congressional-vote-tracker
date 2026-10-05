# Congressional Vote Tracker

A Python tool that retrieves selected U.S. House vote records,
filters them by keyword, and exports them to a CSV.

## How to Run

Run `python vote_tracker.py` in the terminal.
Enter a keyword to filter the results, or press Enter for all votes.

## Data Source

Official vote records from the Office of the Clerk,
U.S. House of Representatives.

## Intended User

Political reporters and researchers who need to organize congressional vote records without manually copying information from individual pages.

## Validation

I ran the tool on 2026 House roll calls 10-14 and confirmed that it exported all five records. I also tested the keyword "gridlock," which returned only roll calls 10 and 11. I checked the date, result, vote totals, and source link for roll call 10 against trhe official record.

## Limitations

- Retrieves selected roll call numbers rather than finding new votes automatically.
- Covers House votes only.
- Keyword searches use vote descriptions, bill numbers, and vote questions.
- Results should be checked against the linked official records.