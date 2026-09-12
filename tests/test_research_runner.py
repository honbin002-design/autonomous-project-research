import os
import shutil
import tempfile
import unittest
from src.research_runner import (
    parse_steps,
    update_step_status,
    log_research_execution,
    append_finding,
    run_step
)

SAMPLE_CHECKPOINT = """# Autonomous Research Checkpoint

## 3. 研究路徑與狀態矩陣 (Roadmap & Status Matrix)

| Step ID | 研究任務 / 假設驗證 | 狀態 | 完成日期 | 備註 |
|:---|:---|:---|:---|:---|
| Step 1 | 建立 README.md 與 CHECKPOINT.md 基礎結構 | Completed | 2025-09-12 | 系統基石建立完成 |
| Step 2 | 實現核心研究執行腳本 `src/research_runner.py` | Pending | - | 負責 checkpoint 解析與執行日誌紀錄 |

---

## 4. 研究發現與紀錄 (Findings & Findings Record)
### [2025-09-12] 系統啟動紀錄
- 完成自主研究系統架構規劃。

---
"""

class TestResearchRunner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.checkpoint_path = os.path.join(self.test_dir, "CHECKPOINT.md")
        self.logs_dir = os.path.join(self.test_dir, "research_logs")
        with open(self.checkpoint_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_CHECKPOINT)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_parse_steps(self):
        steps = parse_steps(SAMPLE_CHECKPOINT)
        self.assertEqual(len(steps), 2)
        self.assertEqual(steps[0]["step_id"], "Step 1")
        self.assertEqual(steps[0]["status"], "Completed")
        self.assertEqual(steps[1]["step_id"], "Step 2")
        self.assertEqual(steps[1]["status"], "Pending")

    def test_update_step_status(self):
        updated = update_step_status(SAMPLE_CHECKPOINT, "Step 2", "Completed", date_str="2025-09-12", note="Done")
        steps = parse_steps(updated)
        self.assertEqual(steps[1]["status"], "Completed")
        self.assertEqual(steps[1]["date"], "2025-09-12")
        self.assertEqual(steps[1]["note"], "Done")

    def test_log_research_execution(self):
        log_path = log_research_execution("Step 2", "Test log details", logs_dir=self.logs_dir)
        self.assertTrue(os.path.exists(log_path))
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("Step 2", content)
            self.assertIn("Test log details", content)

    def test_append_finding(self):
        updated = append_finding(SAMPLE_CHECKPOINT, "Test Finding Title", "Test Finding Desc")
        self.assertIn("Test Finding Title", updated)
        self.assertIn("Test Finding Desc", updated)

    def test_run_step(self):
        res = run_step(2, filepath=self.checkpoint_path, logs_dir=self.logs_dir)
        self.assertTrue(res)
        with open(self.checkpoint_path, "r", encoding="utf-8") as f:
            content = f.read()
        steps = parse_steps(content)
        self.assertEqual(steps[1]["status"], "Completed")
        self.assertIn("Step 2 執行完畢", content)

if __name__ == "__main__":
    unittest.main()
