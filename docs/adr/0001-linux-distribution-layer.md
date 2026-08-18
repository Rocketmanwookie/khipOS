# ADR 0001: Build on Linux

Status: Accepted — 2026-08-18

## Decision

Build KHIP OS as a distribution and desktop layer on the Linux kernel, initially
targeting an Ubuntu-family base. Develop it first as an application that can be
run and tested without repartitioning a machine.

## Rationale

Creating a kernel would delay all differentiating work and sacrifice mature
drivers, security maintenance, installers, filesystems, and dual-boot support.
The agent runtime, permission model, and shell are the actual product.

## Consequences

The early prototype is not itself bootable. A pinned live-image configuration
will package the validated desktop session during Milestone 5. Windows remains
untouched until the user deliberately installs the image beside it.
