# CloudGuard — Implementation Log

This document records the implementation stages and verified outcomes.

## Stage 1 — Virtual Machine Preparation

- Created the CloudGuard-Server virtual machine.
- Installed Ubuntu 26.04.1 LTS Desktop.
- Configured NAT and host-only networking.
- Configured hostname cloudguard-server.
- Created the cloudadmin administration account.
- Configured SSH public-key authentication from EndeavourOS.

## Stage 2 — System Preparation

- Updated Ubuntu packages.
- Installed administration utilities including curl, wget, git, vim, nano, htop, net-tools, rsync, lvm2, and ufw.
- Enabled and verified SSH service.

## Stage 3 — LVM Storage

- Inspected the dedicated /dev/sdb disk before partitioning.
- Created GPT partition and LVM partition.
- Created physical volume /dev/sdb1.
- Created volume group cloudguard_vg.
- Created client1_lv (8 GB).
- Created client2_lv (8 GB).
- Created backup_lv (4 GB).
- Formatted logical volumes with ext4.
- Configured persistent mounts using UUID entries in /etc/fstab.
- Verified the mounted filesystems.

## Stage 4 — Customer Isolation

- Configured separate client1 and client2 Linux accounts.
- Created separate customer website directories.
- Configured directory ownership and permissions.
- Verified that client1 cannot list client2's protected directory and vice versa.
- Configured www-data group access for Nginx.

## Stage 5 — Nginx Virtual Hosting

- Installed and enabled Nginx.
- Created separate virtual host configurations.
- Configured client1.cloudguard.local.
- Configured client2.cloudguard.local.
- Removed the default enabled site.
- Validated Nginx configuration using nginx -t.
- Tested both websites using curl from the EndeavourOS host.
- Confirmed that each domain returned its respective customer page.

## Stage 6 — SSH Security

- Inspected effective SSH daemon configuration.
- Created /etc/ssh/sshd_config.d/99-cloudguard.conf.
- Enabled public-key authentication.
- Disabled password authentication.
- Disabled keyboard-interactive authentication.
- Disabled direct root SSH login.
- Validated configuration using sshd -t.
- Reloaded SSH and verified a new key-based connection from the host.

## Stage 7 — Firewall

- Configured default-deny incoming policy.
- Allowed outgoing traffic.
- Allowed TCP port 22 on enp0s8 from 192.168.56.0/24.
- Allowed TCP port 80 on enp0s8 from 192.168.56.0/24.
- Enabled UFW.
- Verified SSH and both customer websites remained accessible from the host.

## Stage 8 — Automated Backups

- Created /srv/backups/cloudguard.
- Created cloudguard-backup.sh using Bash and rsync.
- Configured timestamped backup directories.
- Executed manual backups successfully.
- Created daily 02:00 cron schedule.
- Configured server timezone as Asia/Kolkata.
- Tested recovery by backing up a temporary file, deleting it, and restoring it.
- Added retention logic to keep up to seven newest timestamped backup directories.
- Validated script syntax using bash -n.
- Executed and verified a backup after adding retention.

## Stage 9 — Monitoring

- Created cloudguard-monitor.sh.
- Added uptime, CPU load, memory, disk, LVM, and service checks.
- Configured warning threshold of 80% for memory and monitored filesystems.
- Created hourly cron schedule.
- Verified cron execution through the monitoring log.

## Stage 10 — Final Infrastructure Verification

Verified:
- Ubuntu hostname and OS.
- Dedicated data disk and LVM volumes.
- Customer and backup mount points through lsblk.
- SSH, Nginx, and cron service status.
- UFW firewall rules.
- Effective SSH security settings.

## Stage 11 — Project Documentation

- Created master project directory and documentation structure.
- Started README, architecture, and implementation records.

## Pending Stages

- Develop Flask dashboard.
- Integrate actual server metrics and management information.
- Perform integrated dashboard testing.
- Capture final screenshots and command evidence.
- Complete report and demonstration guide.
