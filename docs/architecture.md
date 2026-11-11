# CloudGuard — System Architecture

## 1. Architecture Overview

CloudGuard uses an Ubuntu virtual machine to simulate a small hosting provider.

The EndeavourOS laptop acts as the administration host. VirtualBox provides NAT connectivity for outbound network access and a host-only network for private administration and website access.

## 2. Network Architecture

| Interface | Network | Address | Purpose |
|---|---|---|---|
| enp0s3 | NAT | 10.0.2.15 | Outbound connectivity |
| enp0s8 | Host-only | 192.168.56.103 | Private host communication |

The host-only network uses the 192.168.56.0/24 subnet.

The host machine resolves the local customer domains through its /etc/hosts configuration:

- 192.168.56.103 client1.cloudguard.local
- 192.168.56.103 client2.cloudguard.local

These are local demonstration domains, not publicly registered DNS domains.

## 3. Storage Architecture

The operating system uses /dev/sda.

A separate 25 GB data disk, /dev/sdb, contains:

- GPT partition table.
- LVM physical volume: /dev/sdb1.
- Volume group: cloudguard_vg.
- Logical volumes: client1_lv, client2_lv, backup_lv.

Each logical volume uses the ext4 filesystem.

| Mount Point | Logical Volume | Size |
|---|---|---:|
| /srv/client1 | client1_lv | 8 GB |
| /srv/client2 | client2_lv | 8 GB |
| /srv/backups | backup_lv | 4 GB |

Persistent mounting is configured using filesystem UUID entries in /etc/fstab.

## 4. Customer Architecture

Two separate Linux accounts are used:

- client1
- client2

Their website directories are:

- /srv/client1/public
- /srv/client2/public

Directory ownership and group permissions restrict cross-customer filesystem access.

The Nginx worker group is www-data, allowing web server access to the hosted content.

## 5. Web Hosting Architecture

Nginx provides two name-based virtual hosts:

| Domain | Document Root |
|---|---|
| client1.cloudguard.local | /srv/client1/public |
| client2.cloudguard.local | /srv/client2/public |

Configuration files:

- /etc/nginx/sites-available/client1
- /etc/nginx/sites-available/client2

Enabled configurations are linked in /etc/nginx/sites-enabled/.

## 6. Security Architecture

- SSH listens for administration connections.
- Public-key authentication is enabled.
- Password authentication is disabled.
- Direct root SSH login is disabled.
- UFW denies incoming traffic by default.
- SSH port 22 and HTTP port 80 are permitted on enp0s8 only, from 192.168.56.0/24.

## 7. Backup and Monitoring Architecture

Backup script:
- /usr/local/sbin/cloudguard-backup.sh

Backup destination:
- /srv/backups/cloudguard/

Monitoring script:
- /usr/local/sbin/cloudguard-monitor.sh

Log files:
- /var/log/cloudguard-backup.log
- /var/log/cloudguard-monitor.log

Cron configuration:
- /etc/cron.d/cloudguard-backup
- /etc/cron.d/cloudguard-monitor

## 8. Planned Dashboard Architecture

The planned dashboard will use Python Flask for its backend and HTML, CSS, and JavaScript for its interface.

It will retrieve actual server metrics, customer information, storage information, service health, and backup history.

The dashboard has not yet been implemented.
