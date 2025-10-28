# Security Policy for pyfiles_db

## Supported Versions

We actively maintain security for the latest release of **pyfiles_db**. Older versions may not receive security updates. Please use the latest stable version whenever possible.

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. Do **not** open a public issue with sensitive details.
2. Send an email to the repository admins: anton1programmist@gmail.com

Include:
- A detailed description of the vulnerability
- Steps to reproduce
- Environment details (OS, Python version, pyfiles_db version)
- Any suggested mitigation (if known)

3. We will acknowledge your report within 48 hours and provide an estimated timeline for a fix.

## Security Guidelines for Contributors

- Always validate and sanitize inputs when modifying the database API.
- Avoid writing code that allows arbitrary file system access outside the database path.
- Ensure tests cover security-critical paths.
- Follow Python security best practices (PEP 458, PEP 501, etc.).
- Use dependency checks when adding new packages with Poetry:

```bash
poetry show --tree
poetry audit
```

## Emergency Contact

If you find a severe vulnerability requiring immediate attention, contact the repository administrators via email and GitHub direct message.

## Disclosure Policy

We follow responsible disclosure principles:

- You will be credited in release notes or security advisory once the issue is resolved.
- Avoid public disclosure until a patch is available.
