import os
import shutil
import tempfile
import unittest
from src.research_runner import parse_steps
from src.strategy_generator import generate_next_hypothesis_and_step, add_step_to_checkpoint

SAMPLE_CHECKPOINT = """# Autonomous Research Checkpoint

## 3. 研究路徑與狀態矩陣 (Roadmap & Status Matrix)

| Step ID | 研究任務 / 假設驗證 | 狀態 | 完成日期 | 備註 |
|:---|:---|:---|:---|:---|
| Step 1 | 建立 README.md 與 CHECKPOINT.md 基礎結構 | Completed | 2025-09-12 | 系統基石建立完成 |
| Step 2 | 實現核心研究執行腳本 `src/research_runner.py` | Completed | 2026-09-12 | 自動執行完成 |

---
"""

class TestStrategyGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.checkpoint_path = os.path.join(self.test_dir, "CHECKPOINT.md")
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CHECKPOINT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_generate_next_hypothesis_and_step(self):
        next_step = generate_next_hypothesis_and_step(self.checkpoint_path)
        self.assertEqual(next_step["step_id"], "Step 3")
        self.assertEqual(next_step["status"], "Pending")

    def test_add_step_to_checkpoint(self):
        next_step = generate_next_hypothesis_and_step(self.checkpoint_path)
        success, _ = add_step_to_checkpoint(next_step, self.checkpoint_path)
        self.assertTrue(success)

        with open(self.checkpoint_path, "r", encoding="utf-8") as f:
            content = f.read()

        steps = parse_steps(content)
        self.assertEqual(len(steps), 3)
        self.assertEqual(steps[2]["step_id"], "Step 3")

    def test_add_duplicate_step(self):
        next_step = generate_next_hypothesis_and_step(self.checkpoint_path)
        add_step_to_checkpoint(next_step, self.checkpoint_path)
        success, msg = add_step_to_checkpoint(next_step, self.checkpoint_path)
        self.assertFalse(success)
        self.assertEqual(msg, "Step already exists")

if __name__ == "__main__":
    unittest.main()
