
# Security policy

patool is essentially a convenience wrapper script and calls other archive
programs to handle archive files.

Due to the design of those archive programs, patool might do the following:

1. patool might extract files outside the current or given
   extraction directory. It does its best to avoid this, eg. by
   using `tar --force-local` or similar options. But there are
   several archive programs that do not have such options and might
   write outside the extraction directory.

2. Archive programs that are called from patool might have
   vulnerabilities. These are outside the scope of patool.

These are not considered vulnerabilities in patool. If you think
patool's behaviour in these areas can be hardened or improved,
please file an issue for a new feature.

If you handle untrusted archives with patool and want reduce the
risk of the above points, you should use a hardened and sandboxed
environment.

## Reporting a vulnerability

Please do not report security vulnerabilities as public GitHub issues.

To report a vulnerability, use one of the GitHub Private Vulnerability Reporting
for this repository at [https://github.com/wummel/patool/security/advisories/new].
