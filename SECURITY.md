# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please do the following:

1. **Do NOT** open a public issue
2. Email the maintainer directly at: [your-email@example.com]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We aim to respond to security reports within 48 hours and will keep you informed about the progress.

## Security Best Practices

When using this project:

- Keep dependencies up to date
- Use virtual environments for isolation
- Run the Flask app behind a production WSGI server (not the development server)
- Validate all user inputs
- Use HTTPS in production deployments

Thank you for helping keep H2O secure!
