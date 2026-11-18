import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)
        self.fixture = json.loads((ROOT / 'data/workbench.json').read_text())
        self.save()

    def save(self):
        (self.root / 'workbench.json').write_text(json.dumps(self.fixture))

    def run_action(self, action, key=None, succeeds=True):
        args = [sys.executable, '-m', 'app', action, '--data', str(self.root),
                '--ledger', str(self.root / 'receipts.sqlite3')]
        if key is not None:
            args.extend(['--key', key])
        proc = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=5)
        if succeeds:
            self.assertEqual(proc.returncode, 0, proc.stderr)
            return json.loads(proc.stdout)
        self.assertEqual(proc.returncode, 2, proc.stderr)
        return proc.stderr

    def test_late_refund_differs_from_closed_statement(self):
        issued = self.run_action('settle')
        self.assertEqual(issued['fee_cents'], 1310)
        self.fixture['refunds'].append({'id': 'f2', 'sale': 's1', 'day': '2026-06-22', 'cents': 1000})
        self.save()
        self.assertEqual(self.run_action('turnover')['s1'], 2000)
        self.assertEqual(self.run_action('receipts'), issued)
        self.fixture['events'][0]['state'] = 'cancelled'
        self.save()
        self.assertIn('未实际举办', self.run_action('settle', succeeds=False))
