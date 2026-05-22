import subprocess
import os


def detect_language(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    languages = {
        ".py":   "python",
        ".js":   "javascript",
        ".ts":   "typescript",
        ".java": "java",
        ".php":  "php",
        ".cs":   "csharp"
    }
    return languages.get(ext, "unknown")


def run_flake8(filepath):
    result = subprocess.run(
        ["flake8", filepath],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    return output if output else "No flake8 issues found."


def run_radon(filepath):
    result = subprocess.run(
        ["radon", "cc", filepath, "-s", "-a"],
        capture_output=True,
        text=True
    )
    output = result.stdout.strip()
    return output if output else "No complexity issues found."


def run_eslint(filepath):
    # Use eslint.cmd on Windows
    eslint_cmd = "eslint.cmd" if os.name == "nt" else "eslint"
    result = subprocess.run(
        [eslint_cmd, filepath, "--format", "compact"],
        capture_output=True,
        text=True
    )


def run_tools(filepath):
    language = detect_language(filepath)
    print(f"🌐 Detected language: {language}")

    if language == "python":
        print("🔍 Running flake8...")
        linter = run_flake8(filepath)
        print("📊 Running radon...")
        complexity = run_radon(filepath)

    elif language in ("javascript", "typescript"):
        print("🔍 Running ESLint...")
        linter = run_eslint(filepath)
        complexity = "ESLint handles complexity for JS/TS."

    else:
        print(f"ℹ️ No static analysis tools for {language} — using LLM only.")
        linter = f"No static analysis tool configured for {language}."
        complexity = "N/A"

    return language, linter, complexity