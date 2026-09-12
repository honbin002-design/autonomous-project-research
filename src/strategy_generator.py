import os
import re
import sys

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.research_runner import load_checkpoint, parse_steps

def generate_next_hypothesis_and_step(checkpoint_path="CHECKPOINT.md"):
    content = load_checkpoint(checkpoint_path)
    steps = parse_steps(content)
    next_step_num = len(steps) + 1

    # Analyze completed tasks and propose next research phase step
    next_step_id = f"Step {next_step_num}"
    next_task = "評估與優化自主策略生成器之長程對齊與錯誤回饋機制"

    return {
        "step_id": next_step_id,
        "task": next_task,
        "status": "Pending",
        "date": "-",
        "note": "由自主策略生成器自動產生"
    }

def add_step_to_checkpoint(new_step, checkpoint_path="CHECKPOINT.md"):
    content = load_checkpoint(checkpoint_path)
    steps = parse_steps(content)

    # Check if step already exists
    if any(s["step_id"].lower() == new_step["step_id"].lower() for s in steps):
        return False, "Step already exists"

    table_row = f"| {new_step['step_id']} | {new_step['task']} | {new_step['status']} | {new_step['date']} | {new_step['note']} |\n"

    pattern = r"(\|\s*Step\s+\d+\s*\|.*?\|\n)(?!\s*\|\s*Step)"
    matches = list(re.finditer(pattern, content))
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        updated_content = content[:insert_pos] + table_row + content[insert_pos:]
    else:
        # Fallback append to matrix table section
        section_hdr = "## 3. 研究路徑與狀態矩陣 (Roadmap & Status Matrix)"
        if section_hdr in content:
            parts = content.split(section_hdr)
            updated_content = parts[0] + section_hdr + parts[1] + table_row
        else:
            updated_content = content + "\n" + table_row

    with open(checkpoint_path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    return True, updated_content

if __name__ == "__main__":
    next_step = generate_next_hypothesis_and_step()
    success, msg = add_step_to_checkpoint(next_step)
    if success:
        print(f"Successfully added {next_step['step_id']}: {next_step['task']}")
    else:
        print(f"Failed to add step: {msg}")
