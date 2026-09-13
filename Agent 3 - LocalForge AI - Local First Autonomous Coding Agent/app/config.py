import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = Path(os.getenv("SCA_WORKSPACE", str(ROOT / "workspace"))).resolve()
DB_PATH = Path(os.getenv("SCA_DB", str(ROOT / ".sca" / "state.db"))).resolve()
HOST = os.getenv("SCA_HOST", "127.0.0.1")
PORT = int(os.getenv("SCA_PORT", "8000"))
MAX_ITERATIONS = int(os.getenv("SCA_MAX_ITERATIONS", "30"))
COMMAND_TIMEOUT = int(os.getenv("SCA_COMMAND_TIMEOUT", "180"))
AUTO_PUSH = os.getenv("SCA_AUTO_PUSH", "false").lower() == "true"
REQUIRE_CLEAN_GATES = os.getenv("SCA_REQUIRE_CLEAN_GATES", "true").lower() == "true"
USE_DOCKER_SANDBOX = os.getenv("SCA_USE_DOCKER", "false").lower() == "true"
SANDBOX_IMAGE = os.getenv("SCA_SANDBOX_IMAGE", "sovereign-code-agent-sandbox:latest")
