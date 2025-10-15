#!/usr/bin/env python3
import json, argparse, os, datetime, sys

DATA_FILE = "notes.json"

def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_notes(notes):
    with open(DATA_FILE, "w") as f:
        json.dump(notes, f, indent=2)

def list_notes(label="all"):
    notes = load_notes()
    for n in notes:
        if label != "all" and n["label"] != label:
            continue
        print(f"{n['created'][:10]} [{n['label']}] {n['text']}")

def add_note(text, label):
    #how to prevent duplicates in getting added
    notes = load_notes()
    for n in notes:
        if n["text"] == text and n["label"] == label:
            #update print statement based on modified logic
            print("Duplicate note found. Updating timestamp.")
            #if duplicate found, update the timestamp
            n["created"] = datetime.datetime.utcnow().isoformat()
            save_notes(notes)
            return
    notes.append(
        {
            "text": text,
            "label": label,
            "created": datetime.datetime.utcnow().isoformat(),
        }
    )
    save_notes(notes)
    print(notes)

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")

    list_cmd = sub.add_parser("list")
    # --label will be added by learner
    list_cmd.add_argument("--label", choices=["all", "work", "personal"], default="all")


    add_cmd = sub.add_parser("add")
    add_cmd.add_argument("note")
    add_cmd.add_argument("label", choices=["work", "personal"])

    args = parser.parse_args()

    if args.command == "list":
        # Learner will extend here
        list_notes(args.label)
    elif args.command == "add":
        add_note(args.note, args.label)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()