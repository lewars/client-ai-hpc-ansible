# Mock NVIDIA Repository Packages

This directory contains mock files that simulate the NVIDIA repository packages during Molecule testing.

In a real environment, you would have the actual .rpm and .deb files here:
- `nvidia-driver-local-repo-rhel9-570.124.06-1.0-1.x86_64.rpm`
- `nvidia-driver-local-repo-ubuntu2404-570.124.06_1.0-1_amd64.deb`

These mock files allow the Ansible role tests to run without actually installing NVIDIA drivers.
