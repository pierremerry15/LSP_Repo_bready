#will automatically generation a CSV file contaning a visual question/VQA
# questions for ship images. It reads filenames and creates both yes/no
# and open-ended questions per image, then saves them into a CSV file.

from __future__ import annotations
import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Iterable

#default config 
# Default list of 8 countries used for "Is this ship from ___?" questions
DEFAULT_COUNTRIES: List[str] = [
    "United States", "China", "Russia", "Japan",
    "South Korea", "United Kingdom", "France", "Germany",
]

# 4 general yes/no questions
GENERAL_YN_QUESTIONS: List[str] = [
    "Is this a ship?",
    "Is this a military vessel?",
    "Is the ship at sea?",
    "Is this a top-down view?",
]

# 6 open-ended questions about ship type
TYPE_OPEN_QUESTIONS: List[str] = [
    "What type of ship is shown?",
    "Which class does this vessel likely belong to?",
    "Identify the general category of this ship.",
    "What is the ship's primary mission or role?",
    "Name the ship category (e.g., tanker, destroyer, carrier).",
    "Describe the ship type based on visible features.",
]

#question data class  

# A simple structure to hold question info for each image
@dataclass
class QuestionRow:
    image_name: str
    question: str
    answer_type: str
    category: str
    country: str = ""
    notes: str = ""
    author: str = ""
    course: str = ""
    semester: str = ""

#here are the helper functions 
# Converts a comma-separated string of countries into a list
def parse_countries(raw: str | None) -> List[str]:
    if not raw:
        return DEFAULT_COUNTRIES.copy()
    return [c.strip() for c in raw.split(",") if c.strip()]

# Extracts a likely model/class name from a filename
# Example: "DDG-51_Arleigh_Burke.png" -> "Arleigh Burke"
def infer_model_from_filename(filename: str) -> str:
    stem = Path(filename).stem
    chunks = re.split(r"[ _-]+", stem)
    tokens = [t for t in chunks if not t.isdigit() and len(t) > 2]

    # Common hull codes to remove
    hull_codes = {
        "DDG", "FFG", "CG", "CVN", "LHD", "LHA", "DD", "BB",
        "SSN", "SSK", "SSBN", "LCS", "DDH", "DDX", "CV", "CVF", "CVL", "CVS"
    }

    filtered = [t for t in tokens if t.upper() not in hull_codes]
    hint = " ".join(filtered) if filtered else " ".join(tokens)
    hint = re.sub(r"\s+", " ", hint).strip().title()
    return hint if hint else stem

# Collects image file paths from the directory (recursive optional)
def gather_images(root: Path, exts: Tuple[str, ...], recursive: bool) -> List[Path]:
    if recursive:
        return sorted([p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in exts])
    return sorted([p for p in root.iterdir() if p.is_file() and p.suffix.lower() in exts])

# Builds a list of questions for one image
def build_questions_for_image(
    fname: str,
    countries: List[str],
    author: str = "",
    course: str = "",
    semester: str = "",
) -> List[QuestionRow]:
    rows: List[QuestionRow] = []

    # THis adds 4 general yes/no questions
    for q in GENERAL_YN_QUESTIONS:
        rows.append(QuestionRow(fname, q, "yes/no", "general", author=author, course=course, semester=semester))

    # this add 6 open-ended type questions
    for q in TYPE_OPEN_QUESTIONS:
        rows.append(QuestionRow(fname, q, "open-ended", "type", author=author, course=course, semester=semester))

    # this adds 1 model question inferred from filename
    model_hint = infer_model_from_filename(fname)
    rows.append(QuestionRow(
        fname,
        f"Is this ship a {model_hint}?",
        "yes/no",
        "model",
        notes="inferred_from_filename",
        author=author,
        course=course,
        semester=semester
    ))

    # Add 8 yes/no questions for each country
    for c in countries:
        rows.append(QuestionRow(
            fname,
            f"Is this ship from {c}?",
            "yes/no",
            "country",
            country=c,
            author=author,
            course=course,
            semester=semester
        ))

    return rows

# Writes all generated questions to a CSV file
def write_csv(rows: Iterable[QuestionRow], out_path: Path) -> None:
    fieldnames = [
        "image_name", "question", "answer_type", "category",
        "country", "notes", "author", "course", "semester"
    ]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  # write column headers
        for r in rows:
            writer.writerow(r.__dict__)  # convert dataclass to dictionary and write each row

# --------------------------- MAIN FUNCTION -------------------------- #

def main() -> None:
    # Setup command-line arguments
    parser = argparse.ArgumentParser(description="Generate a VQA question CSV for ship images.")
    parser.add_argument("--input_dir", required=True, help="Path to folder containing images.")
    parser.add_argument("--output_csv", default="vqa_questions.csv", help="Output CSV file name.")
    parser.add_argument("--extensions", default=".png,.jpg,.jpeg", help="Image types to include.")
    parser.add_argument("--countries", default=",".join(DEFAULT_COUNTRIES), help="Comma-separated list of countries.")
    parser.add_argument("--recursive", action="store_true", help="Search subfolders for images.")
    parser.add_argument("--author", default="Kyle Pierre", help="Your name.")
    parser.add_argument("--course", default="CSCI 370", help="Course name or code.")
    parser.add_argument("--semester", default="Fall 2025", help="Semester or term.")

    args = parser.parse_args()

    # Convert and check folder
    input_path = Path(args.input_dir)
    if not input_path.exists():
        raise SystemExit(f"[Error] Input directory not found: {input_path}")

    # Normalize extensions into a tuple
    exts = tuple(e.strip().lower() for e in args.extensions.split(",") if e.strip().startswith("."))
    if not exts:
        raise SystemExit("[Error] No valid file extensions provided.")

    # Parse countries and find image files
    countries = parse_countries(args.countries)
    images = gather_images(input_path, exts, args.recursive)
    if not images:
        raise SystemExit(f"[Error] No images found in {input_path}")

    # Generate all questions for all images
    all_rows: List[QuestionRow] = []
    for img in images:
        all_rows.extend(
            build_questions_for_image(
                img.name, countries, author=args.author, course=args.course, semester=args.semester
            )
        )

    # Write all results to CSV
    out_path = Path(args.output_csv)
    write_csv(all_rows, out_path)

    # Display success message
    print(f"[OK] Wrote {len(all_rows)} questions for {len(images)} images → {out_path.resolve()}")
    print("Tip: Open the CSV in Excel or Google Sheets to review sample questions.")

# Run the script
if __name__ == "__main__":
    main()
