# Security Policy

## Supported Versions

Security fixes are provided for the latest released version of `patool` and the current `main` branch.

Older releases are not actively supported unless the maintainer explicitly decides to backport a fix. Users are encouraged to upgrade to the latest release before reporting or reproducing a security issue.

| Version | Supported |
| ------- | --------- |
| Latest release | Yes |
| `main` branch | Yes |
| Older releases | No |

## Reporting a Vulnerability

Please do not report security vulnerabilities as public GitHub issues.

To report a vulnerability, use one of the following private channels:

1. GitHub Private Vulnerability Reporting for this repository, if it is enabled.
2. Email the maintainer at `bastian.kleineidam@web.de`.

If you use email, please include `patool security report` in the subject line.

## What to Include

A good report should include:

- affected `patool` version or commit;
- operating system and Python version;
- archive format involved, if applicable;
- minimal proof of concept archive or reproduction steps;
- expected behavior and actual behavior;
- security impact;
- whether the issue affects the CLI, the Python API, or both.

Reports involving archive extraction should clearly mention whether the issue can cause one of the following:

- writing files outside the requested output directory;
- overwriting existing files unexpectedly;
- following unsafe symlinks or hardlinks;
- executing unintended commands;
- leaking file contents or sensitive paths;
- denial of service through excessive CPU, memory, disk usage, or recursion.

## Disclosure Process

The maintainer will try to acknowledge the report and investigate it as soon as reasonably possible.

Please allow time for the issue to be confirmed, fixed, tested, and released before publishing details publicly. Coordinated disclosure is appreciated.

After a fix is available, the maintainer may publish a security advisory or release notes describing the issue and the affected versions.

## Public Issues

Non-security bugs can be reported in the public issue tracker.

If you are unsure whether a bug has security impact, report it privately first.
