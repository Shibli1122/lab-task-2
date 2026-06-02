/**
 * Backend Tier - Node.js + Express
 * REST API that communicates with the Python DB service
 */

const express = require("express");
const cors = require("cors");
const { execSync } = require("child_process");
const path = require("path");

const app = express();
const PORT = 5000;

app.use(cors());
app.use(express.json());

// Helper: call Python DB service
function callPython(script) {
  try {
    const result = execSync(`python3 ${path.join(__dirname, "../database/db_service.py")} ${script}`, {
      encoding: "utf8",
    });
    return null; // used for init only
  } catch (e) {
    return e.message;
  }
}

// ─── ROUTES ────────────────────────────────────────────────────────────────────

// Health check
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", tier: "backend", timestamp: new Date().toISOString() });
});

// GET all projects (calls Python inline via child process)
app.get("/api/projects", (req, res) => {
  try {
    const result = execSync(
      `python3 -c "
import sys; sys.path.insert(0, '${path.join(__dirname, '../database')}')
from db_service import get_all_projects
import json
data = get_all_projects()
for p in data:
    import json as j
    try: p['tech_stack'] = j.loads(p['tech_stack'])
    except: pass
print(json.dumps(data))
"`,
      { encoding: "utf8" }
    );
    res.json(JSON.parse(result.trim()));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// GET all skills
app.get("/api/skills", (req, res) => {
  try {
    const result = execSync(
      `python3 -c "
import sys; sys.path.insert(0, '${path.join(__dirname, '../database')}')
from db_service import get_all_skills
import json
print(json.dumps(get_all_skills()))
"`,
      { encoding: "utf8" }
    );
    res.json(JSON.parse(result.trim()));
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// POST contact message
app.post("/api/contact", (req, res) => {
  const { name, email, message } = req.body;
  if (!name || !email || !message) {
    return res.status(400).json({ error: "All fields required." });
  }
  try {
    const result = execSync(
      `python3 -c "
import sys; sys.path.insert(0, '${path.join(__dirname, '../database')}')
from db_service import save_message
import json
print(json.dumps(save_message('${name.replace(/'/g, "\\'")}', '${email}', '${message.replace(/'/g, "\\'")}' )))
"`,
      { encoding: "utf8" }
    );
    res.json({ success: true, ...JSON.parse(result.trim()) });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ─── START ──────────────────────────────────────────────────────────────────────
app.listen(PORT, () => {
  console.log(`🚀 Backend running on http://localhost:${PORT}`);
});

module.exports = app;
