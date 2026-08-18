# Image boundary

This directory will contain the reproducible live-image configuration after the
desktop session and recovery behavior are stable. It intentionally contains no
script that repartitions disks or modifies a bootloader.

Planned output: a signed UEFI-capable live ISO that supports trial mode and a
standard guided dual-boot installer. Image work begins only after the runtime,
session startup, updates, rollback, and recovery criteria are testable.
