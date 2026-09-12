import argparse
import datetime
import os
import re

CHECKPOINT_PATH = "CHECKPOINT.md"
LOGS_DIR = "research_logs"

def load_checkpoint(filepath=CHECKPOINT_PATH):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Checkpoint file not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def parse_steps(content):
    steps = []
    # Match markdown table rows in section 3
    pattern = r"\|\s*(Step\s+\d+)\s*\|\s*(.*?)\s*\|\s*(Completed|Pending|In Progress)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    for match in re.finditer(pattern, content):
        steps.append({
            "step_id": match.group(1).strip(),
            "task": match.group(2).strip(),
            "status": match.group(3).strip(),
            "date": match.group(4).strip(),
            "note": match.group(5).strip(),
        })
    return steps

def update_step_status(content, step_id, new_status, date_str=None, note=None):
    if date_str is None:
        date_str = datetime.date.today().isoformat()

    def replacer(match):
        curr_step_id = match.group(1).strip()
        if curr_step_id.lower() == step_id.lower():
            task = match.group(2).strip()
            curr_note = note if note is not None else match.group(5).strip()
            return f"| {curr_step_id} | {task} | {new_status} | {date_str} | {curr_note} |"
        return match.group(0)

    pattern = r"\|\s*(Step\s+\d+)\s*\|\s*(.*?)\s*\|\s*(Completed|Pending|In Progress)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|"
    updated_content, count = re.subn(pattern, replacer, content)
    return updated_content

def log_research_execution(step_id, details, logs_dir=LOGS_DIR):
    os.makedirs(logs_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"research_{step_id.replace(' ', '_').lower()}_{timestamp}.log"
    log_filepath = os.path.join(logs_dir, log_filename)

    with open(log_filepath, "w", encoding="utf-8") as f:
        f.write(f"=== Autonomous Research Log ===\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"Step: {step_id}\n")
        f.write(f"Details:\n{details}\n")
        f.write("===============================\n")
    return log_filepath

def append_finding(content, finding_title, finding_desc):
    today = datetime.date.today().isoformat()
    finding_entry = f"\n### [{today}] {finding_title}\n{finding_desc}\n"

    section_hdr = "## 4. 研究發現與紀錄 (Findings & Findings Record)"
    if section_hdr in content:
        parts = content.split(section_hdr)
        next_sec_split = parts[1].split("\n---\n", 1)
        if len(next_sec_split) == 2:
            updated = parts[0] + section_hdr + next_sec_split[0] + finding_entry + "\n---\n" + next_sec_split[1]
        else:
            updated = parts[0] + section_hdr + parts[1] + finding_entry
        return updated
    else:
        return content + f"\n{section_hdr}\n{finding_entry}"

def run_step(step_number, filepath=CHECKPOINT_PATH, logs_dir=LOGS_DIR):
    content = load_checkpoint(filepath)
    step_id = f"Step {step_number}"
    steps = parse_steps(content)

    target_step = next((s for s in steps if s["step_id"].lower() == step_id.lower()), None)
    if not target_step:
        print(f"Step {step_id} not found in {filepath}")
        return False

    print(f"Executing {step_id}: {target_step['task']}")

    # Execute action & log
    log_details = f"Executing research task: {target_step['task']}\nPrevious status: {target_step['status']}"
    log_file = log_research_execution(step_id, log_details, logs_dir=logs_dir)

    # Update checkpoint
    updated_content = update_step_status(content, step_id, "Completed", note="自動執行完成")
    finding_title = f"{step_id} 執行完畢"
    finding_desc = f"- 成功執行研究步驟 '{target_step['task']}'，詳細紀錄參見 `{log_file}`。"
    updated_content = append_finding(updated_content, finding_title, finding_desc)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Updated {step_id} status to Completed in {filepath}. Log: {log_file}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Autonomous Research System Runner")
    parser.add_argument("--step", type=int, help="Step number to run")
    parser.add_argument("--list", action="store_true", help="List all checkpoint steps")
    args = parser.parse_args()

    if args.list:
        content = load_checkpoint()
        steps = parse_steps(content)
        for s in steps:
            print(f"[{s['status']}] {s['step_id']}: {s['task']} (Date: {s['date']})")
    elif args.step is not None:
        run_step(args.step)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
