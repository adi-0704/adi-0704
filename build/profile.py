"""Every personal fact the SVGs render. Edit here, re-run build.py."""

PROFILE = {
    "name": "ADITYA TYAGI",
    "name_display": "Aditya Tyagi",
    "github": "adi-0704",
    "github_url": "https://github.com/adi-0704",
    "role_primary": "AI Automation Developer",
    "location": "Remote / India",
    "company": None,  # GitHub company field is empty
    "pitch": "I build LLM-powered agents and automations that actually run in production.",
    "pitch_short": "Ship agents, not demos.",
    "greeting": "whoami",
    "roles": [
        "AI Automation Developer",
        "AI Agent Engineer",
        "LLM Application Developer",
        "Workflow Automation (n8n)",
    ],
    "interests": [
        {
            "title": "Open-source AI tooling",
            "body": "Following and building on new agent frameworks — LangGraph, n8n, MCP.",
        },
        {
            "title": "Building side projects",
            "body": "32 public repositories in sixteen months. Most start as a problem worth solving.",
        },
        {
            "title": "Automating boring things",
            "body": "Outreach dashboards, scrapers and schedulers that remove the manual step.",
        },
    ],
    "capabilities": [
        ("Multi-agent pipelines", "LangGraph orchestration, tool use, structured output"),
        ("RAG systems", "Retrieval, grounding and evaluation over private documents"),
        ("Workflow automation", "n8n, schedulers and API glue that runs unattended"),
        ("LLM product work", "Prompt design, scoring rubrics and reasoning you can audit"),
    ],
    # Verified against the GitHub REST API on the date below. Nothing here is invented.
    "stats_asof": "07 NOV 2026",
    "stats": [
        ("PUBLIC REPOS", "32"),
        ("TOP LANGUAGE", "PYTHON"),
        ("ON GITHUB SINCE", "JUL 2025"),
    ],
    "lang_mix": [
        ("Python", 10),
        ("TypeScript", 9),
        ("JavaScript", 5),
        ("HTML", 2),
    ],
    "projects": [
        {
            "name": "Loqo-Script-AI",
            "url": "https://github.com/adi-0704/Loqo-Script-AI",
            "lang": "TypeScript",
            "desc": "Multi-agent LangGraph + Gemini pipeline that turns raw news URLs into "
                    "structured TV broadcast screenplays with dynamic visual prompting.",
            "icon": "langchain",
        },
        {
            "name": "ats-system",
            "url": "https://github.com/adi-0704/ats-system",
            "lang": "Python",
            "desc": "AI-powered ATS that scores resumes against job descriptions and returns "
                    "strengths, weaknesses and hiring insights from LLM reasoning.",
            "icon": "openai",
        },
        {
            "name": "RAG-Solar-Assistant",
            "url": "https://github.com/adi-0704/RAG-Solar-Assistant",
            "lang": "Python",
            "desc": "Retrieval-augmented assistant answering solar-domain questions grounded "
                    "in a private document corpus.",
            "icon": "python",
        },
        {
            "name": "collabhive-site",
            "url": "https://github.com/adi-0704/collabhive-site",
            "lang": "Python",
            "desc": "CollabHive — creator-first influencer marketing platform, shipped as a "
                    "static site on GitHub Pages.",
            "icon": "vercel",
        },
    ],
    "stack_groups": [
        ("LANGUAGES", ["python", "typescript", "javascript"]),
        ("AI / LLM", ["openai", "googlegemini", "langchain", "n8n"]),
        ("DATA & INFRA", ["fastapi", "postgresql", "docker", "supabase"]),
    ],
    "orbits": [
        ["python", "typescript", "javascript", "nodedotjs", "react"],
        ["openai", "googlegemini", "langchain", "n8n"],
        ["fastapi", "postgresql", "docker", "supabase", "git"],
    ],
    # Only platforms with a confirmed URL are rendered. Add yours and re-run.
    "socials": [
        {"platform": "github", "label": "GitHub", "handle": "@adi-0704",
         "url": "https://github.com/adi-0704"},
        {"platform": "linkedin", "label": "LinkedIn", "handle": "adityatyagi-ai",
         "url": "https://www.linkedin.com/in/adityatyagi-ai"},
    ],
}

ICON_LABELS = {
    "python": "Python",
    "typescript": "TypeScript",
    "javascript": "JavaScript",
    "nodedotjs": "Node.js",
    "react": "React",
    "openai": "OpenAI",
    "googlegemini": "Gemini",
    "langchain": "LangChain",
    "n8n": "n8n",
    "fastapi": "FastAPI",
    "postgresql": "Postgres",
    "docker": "Docker",
    "supabase": "Supabase",
    "git": "Git",
    "github": "GitHub",
    "vercel": "Vercel",
    "linkedin": "LinkedIn",
    "pandas": "pandas",
    "streamlit": "Streamlit",
    "selenium": "Selenium",
}
