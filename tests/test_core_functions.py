import unittest
import sys
from pathlib import Path

# Add src directory to path
src_path = Path(__file__).parent.parent / 'src'
sys.path.insert(0, str(src_path))

from agent_logic.core_functions import AgentCore

class TestAgentCore(unittest.TestCase):
    def test_run(self):
        agent = AgentCore()
        self.assertIsNone(agent.run())

if __name__ == '__main__':
    unittest.main()
