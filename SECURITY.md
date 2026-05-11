# Security Policy

## Reporting a Vulnerability

If you discover a security issue (e.g., API key leakage vectors, prompt injection), please report it via [GitHub Security Advisories](https://github.com/20kiki/deepseek-eyes/security/advisories/new).

**Do not open a public issue.**

## Scope

This tool processes image files and sends them to Alibaba Cloud Bailian's API. The `DASHSCOPE_API_KEY` is read from the environment — never hardcoded in the script.
