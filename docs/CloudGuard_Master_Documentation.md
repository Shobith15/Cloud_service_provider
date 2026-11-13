# CloudGuard — Master Project Documentation
## Source of truth for the final hackathon report

**Project title:** CloudGuard — Cloud Service Provider  
**Project category:** Linux System Administration / Cloud Infrastructure Administration  
**Project environment:** EndeavourOS host + Ubuntu Server/Desktop virtual machine in Oracle VirtualBox  
**Documentation purpose:** This file is the central content and implementation reference for preparing the final project report. It is intended to be read together with the actual project source files, configuration files, screenshots and the supplied reference report.

---

## 1. Instructions for the report-generation agent

Treat this document as the primary narrative source for the CloudGuard implementation. Inspect the complete workspace before writing the report.

### 1.1 Required workspace inspection

Inspect the following, when present:

- `README.md`
- `docs/` and all Markdown files inside it
- `scripts/dashboard/` and its Python, HTML, CSS, JavaScript and requirements files
- `CloudGuard_Evidence/screenshots/`
- `CloudGuard_Evidence/command_outputs/`
- `CloudGuard_Evidence/test_results/`
- Any project configuration, shell scripts, service definitions, logs or other implementation files included in the workspace
- The reference report PDF supplied separately in the workspace

Use the real files to verify implementation details. If this master file and an actual configuration file disagree, inspect the implementation and flag the discrepancy rather than silently inventing a resolution.

### 1.2 Accuracy rules

1. Describe the project that was actually implemented. Do not turn proposed or future features into completed features.
2. Do not invent command output, screenshots, test results, configuration contents, benchmark values, performance figures, security certifications or successful executions.
3. Do not claim that CloudGuard is a public production cloud platform. It is a locally demonstrated cloud-service-provider-style environment hosted in VirtualBox.
4. Do not describe the two customer websites as publicly accessible. Their hostnames resolve on the EndeavourOS host through `/etc/hosts`, and the VM is reached over a VirtualBox host-only network.
5. Do not claim TLS/HTTPS was configured. The demonstrated customer sites use HTTP on port 80.
6. Do not claim a database, payment system, customer self-service portal, automated provisioning API, container orchestration or public cloud integration was implemented unless the actual workspace contains evidence for it.
7. Commands may be included as implementation examples when supported by the project history or actual scripts/configuration. Clearly distinguish command examples from captured terminal output.
8. Use screenshots only as evidence of what they visibly show. A screenshot of the dashboard does not prove every backend operation.
9. The restore test was performed successfully during implementation, but no dedicated restore-test screenshot was captured in the evidence set described below. Report the test as an implementation-history result, and do not imply that a screenshot exists for it.
10. The `command_outputs/` folder may be empty. Do not fabricate `.txt` files or claim raw command transcripts were saved if they were not.
11. The user has captured eight screenshots. Preserve their filenames and use them in the relevant report sections.
12. If the reference PDF is not present in the workspace, ask for it or use a conventional academic report structure. Do not claim to have followed a reference document that was not inspected.

### 1.3 Expected report approach

Use the reference PDF for presentation structure, order, page layout and academic conventions, while using CloudGuard's own verified implementation for technical content. The final report should explain the project chronologically and technically, not merely describe the screenshots.

Where appropriate, include:
- Cover/title page
- Certificate/declaration/acknowledgement only if required by the reference or institution; do not invent signatures, names, designations or approval details
- Abstract
- Table of contents
- Introduction and problem statement
- Objectives and scope
- Requirements and tools
- System architecture and network topology
- Implementation methodology, in chronological stages
- Configuration and code explanations
- Security design
- Backup, recovery and monitoring
- Dashboard implementation
- Testing and validation
- Results and discussion
- Limitations and future enhancements
- Conclusion
- References
- Appendices for selected commands/configuration excerpts if useful

Create clear diagrams from the real architecture. A diagram may be newly drawn, but it must accurately represent the described topology and must not imply a public network or features that were not implemented.

---

## 2. Project overview

### 2.1 Project summary

CloudGuard is a small-scale cloud-service-provider simulation implemented as a Linux server environment. It demonstrates how a service provider can host multiple customer websites on one Linux server while separating customer storage, Linux accounts and directory permissions. It also includes storage management through LVM, web hosting through Nginx, restricted network access through UFW, SSH hardening, scheduled backups, monitoring scripts and a read-only Flask-based administration dashboard.

The project is implemented on an Ubuntu virtual machine running in Oracle VirtualBox. The EndeavourOS laptop acts as the host and administration workstation. SSH is used by the host to administer the Ubuntu VM. A host-only network provides controlled communication between the host and VM.

The project is intended as a practical Linux system-administration demonstration, not as a commercial or production-ready public cloud platform.

### 2.2 Problem statement

A small hosting provider needs to host more than one customer on a shared Linux server without allowing one customer to access another customer's files. The provider also needs to allocate storage, publish each customer's website, restrict administrative access, maintain backups, monitor system health and provide an overview of the server's status.

CloudGuard demonstrates a compact implementation of these requirements using standard Linux administration tools and services.

### 2.3 Objectives

The main objectives are to:

- Build and administer an Ubuntu-based Linux server in a virtualized environment.
- Establish secure SSH administration from the EndeavourOS host.
- Configure separate customer Linux accounts and directory permissions.
- Allocate a dedicated data disk to customer and backup storage using LVM.
- Host two independent customer websites using Nginx virtual hosts.
- Restrict inbound network access using UFW.
- Harden SSH by disabling root and password-based login.
- Automate customer-data backups and apply backup retention.
- Test restoration of a deleted test file from a backup.
- Schedule system monitoring and backup tasks using cron.
- Build a read-only web dashboard for viewing server, storage, service, customer and backup information.

### 2.4 Scope

**Implemented scope**

- One Ubuntu VM serving as the CloudGuard server.
- Two simulated customers: `client1` and `client2`.
- Separate customer Linux accounts and storage mount points.
- LVM-based storage on a dedicated virtual data disk.
- Two Nginx-hosted static customer websites.
- Host-only network access from the EndeavourOS host.
- UFW rules for SSH, HTTP and the dashboard.
- SSH public-key authentication and hardening.
- Timestamped backups with a seven-backup retention limit.
- A manual recovery test.
- Periodic monitoring and backup cron jobs.
- A Flask/Gunicorn read-only dashboard protected by basic authentication.

**Outside the implemented scope**

- Public Internet hosting or deployment to a commercial cloud provider.
- HTTPS/TLS certificates.
- Real customer registration, billing or payment processing.
- A customer-facing control panel or self-service provisioning API.
- Database-backed dynamic websites.
- High availability, clustering or multi-server failover.
- Container orchestration.
- Enterprise identity management.
- Production disaster-recovery infrastructure.

---

## 3. Environment and tools

### 3.1 Host system

- Host operating system: EndeavourOS.
- Desktop environment: KDE Plasma.
- Virtualization software: Oracle VirtualBox.
- Host role: administration workstation, SSH client and browser used to access the dashboard and customer websites.
- Host-side SSH shortcut: `cloudguard`.

The project was developed on the user's laptop. Do not include personal device serial numbers, account identifiers or unrelated personal information in the report.

### 3.2 Virtual machine

- VM name: `CloudGuard-Server`.
- Guest operating system: Ubuntu 26.04.1 LTS Desktop installation.
- Hostname: `cloudguard-server`.
- Administrative Linux account: `cloudadmin`.
- Kernel recorded during implementation: `7.0.0-43-generic`.
- Architecture: x86_64.
- VM memory: approximately 4 GiB allocated (approximately 3.3 GiB visible to the guest).
- Root/system virtual disk: `/dev/sda`, 25 GB.
- Dedicated data virtual disk: `/dev/sdb`, 25 GiB.

**Important storage safety distinction:** `/dev/sda` is the operating-system disk. The LVM configuration was created on the separate `/dev/sdb` data disk. Do not describe or imply that the root disk was repartitioned for customer storage.

### 3.3 Main software and utilities

The implementation uses:

- Ubuntu Linux
- Oracle VirtualBox
- OpenSSH server/client
- `curl`, `wget`, `git`, `vim`, `nano`, `htop`
- `net-tools`, `dnsutils`
- `rsync`
- `lvm2`
- UFW
- Nginx
- Python 3 and a Python virtual environment
- Flask
- Gunicorn
- psutil
- systemd
- cron

Use the actual installed requirements file and service files in the workspace to verify exact versions if version numbers are needed. Do not invent versions.

---

## 4. Network architecture

### 4.1 VirtualBox network configuration

The Ubuntu VM has two virtual network adapters:

| Adapter | VirtualBox mode | Guest interface | Guest IPv4 | Purpose |
|---|---|---|---|---|
| Adapter 1 | NAT | `enp0s3` | `10.0.2.15/24` | Outbound network access for package installation and updates |
| Adapter 2 | Host-only | `enp0s8` | `192.168.56.103/24` | Private communication between EndeavourOS host and CloudGuard VM |

The host-only network is associated with the VirtualBox host-only network `vboxnet0`. The server's host-only address is `192.168.56.103`.

There is no bridged adapter configured for this project. Do not describe the VM as directly exposed to a physical LAN or the public Internet.

### 4.2 SSH administration path

The EndeavourOS host administers the Ubuntu VM using SSH over the host-only network.

Host-side SSH configuration uses the alias:

```sshconfig
Host cloudguard
    HostName 192.168.56.103
    User cloudadmin
    IdentityFile ~/.ssh/cloudguard_ed25519
    IdentitiesOnly yes
```

The host generated an Ed25519 key pair. The private key remains on the EndeavourOS host. The public key was installed for the `cloudadmin` account on Ubuntu. Key-based login was tested successfully.

Typical host-side connection:

```bash
ssh cloudguard
```

The SSH configuration is an administration convenience; it does not mean the Ubuntu VM has a second physical host. The two systems are the EndeavourOS host and the Ubuntu guest VM.

### 4.3 Hostname resolution for the customer websites

The EndeavourOS host `/etc/hosts` file contains:

```text
192.168.56.103 client1.cloudguard.local
192.168.56.103 client2.cloudguard.local
```

This allows the host browser and `curl` to resolve both customer hostnames to the Ubuntu VM. These names are local demonstration hostnames, not public DNS records.

### 4.4 Network flow

The intended architecture is:

1. EndeavourOS host reaches the Ubuntu VM through the VirtualBox host-only network.
2. SSH administration uses TCP port 22 on the host-only interface.
3. Customer website requests use HTTP port 80 on the host-only interface.
4. Dashboard requests use TCP port 5000 on the host-only interface.
5. The VM's NAT interface provides outbound access; it is not the customer-facing interface in the demonstrated host-only setup.

Create an accurate architecture/network diagram showing the EndeavourOS host, VirtualBox, Ubuntu CloudGuard VM, both virtual NICs, the host-only subnet, the SSH path, the two website hostnames, the dashboard and the customer/storage services.

---

## 5. Implementation methodology — chronological account

The final report should give a coherent account of the work from initial environment preparation through dashboard validation. The stages below describe the implementation sequence and the reason for each stage.

### 5.1 Virtual machine preparation

An Ubuntu VM was installed in VirtualBox and prepared as the CloudGuard server. The VM was given a recognizable hostname and the `cloudadmin` administration account was used for server configuration.

The VM was configured with a system disk and a separate 25 GiB data disk. This separation allowed the operating system to remain on `/dev/sda` while customer and backup storage was built on `/dev/sdb`.

A VirtualBox snapshot named `Ubuntu-Base-SSH-Ready` was taken after the initial SSH setup and reboot, before the later package-update and service configuration stages. This provided a recovery point for the VM during development.

The guest timezone was set to `Asia/Kolkata`, and time synchronization was checked.

### 5.2 Package installation and preparation

The Ubuntu environment was prepared with the administration, storage, networking and web-server tools required by the project. These included SSH, Nginx, UFW, LVM utilities, rsync, Python tooling and diagnostic utilities.

The report should explain the role of these tools rather than merely listing package names.

### 5.3 SSH key-based administration

SSH was configured so the EndeavourOS host could administer the Ubuntu guest without repeatedly entering an account password.

The host generated an Ed25519 key pair. The private key remained on the host, while the public key was authorized for the Ubuntu `cloudadmin` account. An SSH client alias named `cloudguard` was configured on the host.

The connection was tested from the EndeavourOS terminal. An initial unsuccessful attempt involved an incorrect/missing identity-file path from within the VM; this was corrected by using the host-side key and correct SSH client configuration. The final host-to-VM key-based connection succeeded.

Do not portray the initial failed attempt as the final configuration. If discussing troubleshooting, explain that the client key path and the machine from which SSH was invoked were corrected.

### 5.4 Dedicated data disk and LVM

The separate 25 GiB `/dev/sdb` disk was used for customer and backup storage. The OS disk `/dev/sda` was left untouched.

The data disk was partitioned with a GPT partition table and one partition configured for LVM. The physical volume and volume group were created, followed by three logical volumes.

The resulting storage plan is:

| Logical volume | Size | Intended use | Mount point |
|---|---:|---|---|
| `client1_lv` | 8 GiB | Client 1 files and website | `/srv/client1` |
| `client2_lv` | 8 GiB | Client 2 files and website | `/srv/client2` |
| `backup_lv` | 4 GiB | Backup storage | `/srv/backups` |
| Unallocated VG space | Approximately 5 GiB | Future capacity within the volume group | Not mounted |

The volume group is named `cloudguard_vg`. The physical volume is on `/dev/sdb1`.

The logical volumes were formatted with ext4 and mounted at the paths shown above. UUID-based entries were added to `/etc/fstab`, and `mount -a` was used to validate the mount configuration.

The report should explain the LVM hierarchy:

- Physical disk: `/dev/sdb`
- LVM partition: `/dev/sdb1`
- Physical volume (PV): `/dev/sdb1`
- Volume group (VG): `cloudguard_vg`
- Logical volumes (LVs): `client1_lv`, `client2_lv`, `backup_lv`
- Filesystems: ext4
- Mount points: `/srv/client1`, `/srv/client2`, `/srv/backups`

The final evidence screenshot `02_lvm_storage_configuration.png` shows the disk, PV, VG and LV configuration.

### 5.5 Customer accounts and directory isolation

Two separate Linux customer accounts were created:

- `client1`
- `client2`

Their files are kept under separate mount points:

- `/srv/client1`
- `/srv/client2`

Each customer has a public web directory:

- `/srv/client1/public`
- `/srv/client2/public`

The directory ownership and permissions were configured to isolate the customers while allowing the Nginx worker account to read website content.

Recorded directory ownership/mode:

```text
/srv/client1          client1:www-data   drwxr-s---
/srv/client1/public   client1:www-data   drwxr-s---
/srv/client2          client2:www-data   drwxr-s---
/srv/client2/public   client2:www-data   drwxr-s---
```

The setgid bit on the directories supports group inheritance for newly created content. The `www-data` group is used so Nginx can read the customer website files. Website index files were configured as `root:www-data` with mode `644`, while parent directories restrict traversal.

Customer isolation was tested using commands equivalent to:

```bash
sudo -u client1 ls /srv/client1/public
sudo -u client1 ls /srv/client2/public

sudo -u client2 ls /srv/client2/public
sudo -u client2 ls /srv/client1/public
```

Each customer could list their own public directory, while attempts to list the other customer's directory returned `Permission denied`. This is an important validation result and should be explained in the report.

The evidence screenshot `03_customer_account_isolation.png` captures the account identities, directory permissions and access-denied tests.

### 5.6 Nginx virtual hosts and customer websites

Nginx was installed, enabled and configured to host two separate static customer websites on the same Ubuntu server.

The site configuration files are:

- `/etc/nginx/sites-available/client1`
- `/etc/nginx/sites-available/client2`

The corresponding enabled site links are under `/etc/nginx/sites-enabled/`. The default site was removed from the active configuration.

The virtual hosts use these hostnames and document roots:

| Customer | Hostname | Document root | Customer identifier |
|---|---|---|---|
| Client 1 | `client1.cloudguard.local` | `/srv/client1/public` | `CG-001` |
| Client 2 | `client2.cloudguard.local` | `/srv/client2/public` | `CG-002` |

Both sites listen on HTTP port 80. The configuration uses `try_files` for request handling. The customer pages are separate HTML files and display their respective customer identity.

The host `/etc/hosts` entries map both names to `192.168.56.103`. From the EndeavourOS host, `curl` requests to both hostnames returned the correct separate HTML pages.

The report should explain how Nginx selects the appropriate server block based on the requested hostname and serves content from the corresponding customer document root.

Evidence:
- `04_customer_websites.png` — terminal output from `curl` showing both customer websites and their distinct identifiers.

### 5.7 UFW firewall configuration

UFW was configured as the host firewall.

The default policies are:

- Incoming traffic: deny
- Outgoing traffic: allow

Inbound allow rules were added for TCP ports:

- `22` — SSH administration
- `80` — customer HTTP websites
- `5000` — CloudGuard dashboard

These rules are restricted to the host-only interface `enp0s8` and source subnet `192.168.56.0/24`. The project therefore demonstrates interface- and source-restricted access rather than opening the services to every network.

The firewall is active. The report should explain why the rules are limited to the host-only network and why the NAT interface is not used as the administrative/customer ingress path.

No HTTPS/443 rule or TLS deployment was implemented.

### 5.8 SSH hardening

SSH was hardened through:

`/etc/ssh/sshd_config.d/99-cloudguard.conf`

The effective configuration includes:

```text
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
```

The SSH configuration was syntax-checked using `sshd -t`, and the effective settings were inspected using `sshd -T`. The SSH service was reloaded after the configuration change, and a new host-to-VM key-based connection was successful.

Explain the security purpose of each setting:
- Public-key authentication is enabled.
- Password authentication is disabled.
- Keyboard-interactive authentication is disabled.
- Direct root login is disabled.

Do not state that all SSH access is disabled. The `cloudadmin` account can still connect using the authorized SSH key.

Evidence:
- `05_firewall_and_ssh_security.png` — UFW status and effective SSH settings.

### 5.9 Automated backup system

A backup script was created at:

`/usr/local/sbin/cloudguard-backup.sh`

The script uses Bash strict-mode options (`set -Eeuo pipefail`), creates a timestamped backup directory under `/srv/backups/cloudguard`, and uses `rsync -a` to copy the contents of both customer storage trees:

- `/srv/client1/`
- `/srv/client2/`

The script logs the start and completion of backup operations to:

`/var/log/cloudguard-backup.log`

If either rsync operation fails, the script records an error and exits unsuccessfully. The script also implements a retention policy that keeps up to seven timestamped backup directories and removes older backup directories beyond that limit.

The backup script is executable and is run with root privileges through its scheduled cron entry.

The backup directory is protected. The dashboard has a restricted reader group (`cloudguard-backup-readers`) that allows the dashboard to list backup names and modification times without granting general read access to the backup contents.

A daily backup job is configured in:

`/etc/cron.d/cloudguard-backup`

Schedule:

```cron
0 2 * * * root /usr/local/sbin/cloudguard-backup.sh
```

This schedules the backup at 02:00 server-local time. The guest timezone was configured as `Asia/Kolkata`.

Several timestamped backups were successfully created during implementation. Examples observed on 11 November 2026 include:

- `2026-11-11_09-21-45`
- `2026-11-11_08-44-48`
- `2026-11-11_03-07-53`

Treat these as observed examples, not as a complete backup inventory. The backup log and actual snapshot directories should be inspected if the report needs current values.

### 5.10 Recovery validation

A manual recovery test was performed during implementation:

1. A temporary test file named `recovery-test.txt` was created under `/srv/client1/public`.
2. The backup script was run so the test file was included in a timestamped backup.
3. The live test file was deleted.
4. The file was restored from the corresponding backup.
5. The restored content and metadata were checked.
6. The temporary test file was removed after validation.

The recovery test succeeded. The temporary test file is not intended to remain in the live customer website directory.

Important evidence qualification: the successful recovery test is recorded in the project implementation history, but the eight named screenshots do not include a dedicated screenshot of the restore procedure. Do not label the backup-log screenshot as a direct screenshot of the restore test.

### 5.11 Monitoring script and scheduled monitoring

A monitoring script was created at:

`/usr/local/sbin/cloudguard-monitor.sh`

The script collects and logs system health information, including:

- System uptime
- Load information
- Memory usage
- Disk usage
- LVM volume-group and logical-volume information
- Nginx service status
- SSH service status

The monitoring log is:

`/var/log/cloudguard-monitor.log`

The script uses warning thresholds of 80% for memory and disk usage. It is executable and runs with root privileges through cron.

The monitoring schedule is configured in:

`/etc/cron.d/cloudguard-monitor`

Schedule:

```cron
0 * * * * root /usr/local/sbin/cloudguard-monitor.sh >/dev/null 2>&1
```

This schedules the monitoring script hourly. The cron service is enabled and running. The monitoring log showed a successful execution during implementation, including uptime, memory, disk, LVM and service status information.

Evidence:
- `07_monitoring_and_cron.png` — monitoring log and both cron schedules.

### 5.12 CloudGuard administration dashboard

A read-only web dashboard named CloudGuard was developed using Flask, Gunicorn, HTML, CSS and JavaScript. It provides a consolidated view of the server and the simulated hosting environment.

#### Dashboard source files

The host-side project source directory is:

`scripts/dashboard/`

It contains:

- `app.py`
- `requirements.txt`
- `templates/index.html`
- `static/style.css`
- `static/dashboard.js`

The deployed application is under:

`/opt/cloudguard-dashboard/`

A Python virtual environment is used for application dependencies. The implementation used Flask, Gunicorn and psutil.

#### Dashboard account and authentication

The dashboard runs under a dedicated Linux service account:

- Account: `cloudguard-dashboard`
- Login shell: non-interactive (`nologin`)
- No sudo privileges
- Supplementary groups: `www-data` and `cloudguard-backup-readers`

The dashboard is protected by HTTP basic authentication. Credentials are stored in the root-only environment file:

`/etc/cloudguard-dashboard.env`

The file is mode `600`. Do not include the actual password, password hash or other secret values in the report.

The application is designed as a read-only monitoring interface. It does not provide arbitrary shell execution.

#### Dashboard endpoints and data

The application includes routes:

- `/` — dashboard interface
- `/api/overview` — dashboard overview data
- `/health` — health endpoint

The application uses psutil for CPU, memory and uptime information. It also displays disk usage, customer website readiness, storage/LVM information, backup history and service status.

The storage view was adjusted to use unprivileged `lsblk` output rather than privileged `vgs`/`lvs` commands. This avoids granting the dashboard broad administrative privileges merely to display storage information.

The dashboard displays the dedicated data disk and logical-volume mount information, including:

- `sdb` — 25 GiB data disk
- `client1_lv` — 8 GiB mounted at `/srv/client1`
- `client2_lv` — 8 GiB mounted at `/srv/client2`
- `backup_lv` — 4 GiB mounted at `/srv/backups`

It also displays CPU and memory information, uptime, disk usage, service health for Nginx/SSH/cron, customer readiness and recent backup entries. The dashboard refreshes automatically at a 15-second interval.

#### Gunicorn and systemd

The dashboard is served using Gunicorn through a systemd unit:

`/etc/systemd/system/cloudguard-dashboard.service`

The service runs as `cloudguard-dashboard`, uses the application virtual environment, reads the protected environment file and binds to:

`192.168.56.103:5000`

The systemd service includes hardening directives:

```ini
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
```

The service was enabled and running during validation.

The dashboard is accessible from the host through:

`http://192.168.56.103:5000`

The UFW rule for port 5000 is limited to the host-only interface and host-only subnet. Basic authentication was tested: an unauthenticated API request returned HTTP 401, while an authenticated request returned dashboard JSON data.

Evidence:
- `01_cloudguard_dashboard.png` — complete dashboard view.
- `08_dashboard_service_hardening.png` — dashboard service account, service state and systemd hardening properties.

---

## 6. Security design

The report should describe security as multiple layers rather than one feature.

### 6.1 Network isolation

- VirtualBox host-only networking provides a private host-to-guest path.
- The guest also has a NAT adapter for outbound access.
- UFW restricts inbound SSH, HTTP and dashboard traffic to the host-only interface and subnet.
- No bridged network or public-facing exposure was configured.

### 6.2 Administrative access

- SSH public-key authentication is enabled.
- SSH password and keyboard-interactive authentication are disabled.
- Root login over SSH is disabled.
- The private Ed25519 key remains on the host.

### 6.3 Customer separation

- Each customer has a separate Linux account.
- Each customer has a separate storage mount point and website document root.
- Directory ownership and mode bits prevent one customer from traversing the other customer's directory.
- Nginx receives read access through the `www-data` group.

### 6.4 Dashboard privilege separation

- The dashboard uses a dedicated non-login service account.
- The account has no sudo privileges.
- The application is read-only.
- Backup visibility is limited through a dedicated reader group.
- Credentials are stored in a root-only environment file.
- systemd hardening directives restrict the service process.
- The dashboard binds to the host-only IP rather than all network interfaces.

### 6.5 Backup protection

- Backups are stored separately from the customer web roots on the dedicated backup logical volume.
- The backup script runs with the privileges required to read customer data.
- Backup directories are protected.
- The dashboard is allowed limited listing/metadata access, not general backup-content access.

Avoid overstating the security model. This is a learning/demo implementation. It has not undergone a formal penetration test or independent security audit.

---

## 7. Testing and validation

The report should present tests as functional validation of the implemented environment. Use a test matrix such as the following and retain the distinction between a test performed during implementation and a screenshot captured for the report.

| ID | Area | Validation performed | Observed result |
|---|---|---|---|
| T01 | SSH administration | Connected from EndeavourOS host to Ubuntu VM using the configured `cloudguard` SSH alias and Ed25519 key | Successful |
| T02 | LVM | Inspected `/dev/sdb`, PV, VG and logical volumes | Dedicated 25 GiB data disk and three logical volumes observed |
| T03 | Customer isolation | Ran directory-listing tests as `client1` and `client2` | Own directory accessible; other customer's directory returned `Permission denied` |
| T04 | Website hosting | Requested both customer hostnames from the host using `curl` | Both separate HTML websites returned with their respective customer IDs |
| T05 | Firewall | Inspected UFW status and rules | Firewall active; inbound access restricted to the host-only subnet for required ports |
| T06 | SSH hardening | Inspected effective SSH daemon configuration | Root/password/keyboard-interactive login disabled; public-key authentication enabled |
| T07 | Backup | Ran backup process and inspected log and timestamped backup directories | Backup completion logged and timestamped snapshots created |
| T08 | Recovery | Deleted a temporary test file after backup, restored it from the backup and checked the restored file | Successful recovery; temporary test file then removed |
| T09 | Monitoring | Inspected monitoring log and cron schedules | Monitoring records present; hourly monitoring and daily backup schedules configured |
| T10 | Dashboard | Opened dashboard and checked its data; tested unauthenticated and authenticated API access | Dashboard displayed system information; unauthenticated request returned 401 and authenticated request returned data |
| T11 | Dashboard service | Inspected service account, systemd service state and hardening properties | Dedicated service account and systemd hardening settings present |

The table is a summary of tests described in the implementation history. Before finalizing, inspect the current workspace and evidence screenshots to ensure no later change invalidated a result. Do not create fake terminal transcripts.

### 7.1 Evidence screenshot inventory

The user saved the following eight screenshots in:

`CloudGuard_Evidence/screenshots/`

| Filename | What it demonstrates | Suggested report placement |
|---|---|---|
| `01_cloudguard_dashboard.png` | Dashboard overview, system metrics, storage, service status, customer status and backup history | Dashboard implementation and results |
| `02_lvm_storage_configuration.png` | Dedicated data disk, PV, VG and logical volumes | Storage/LVM implementation |
| `03_customer_account_isolation.png` | Customer accounts, directory ownership/permissions and cross-customer access-denied checks | Customer management and access control |
| `04_customer_websites.png` | `curl` output for both customer websites and their identifiers | Nginx/web hosting |
| `05_firewall_and_ssh_security.png` | UFW status/rules and effective SSH security settings | Network security and SSH hardening |
| `06_backup_history_and_logs.png` | Backup script log and timestamped backup directories | Backup implementation |
| `07_monitoring_and_cron.png` | Monitoring log and monitoring/backup cron entries | Monitoring and automation |
| `08_dashboard_service_hardening.png` | Dashboard account, service state and systemd hardening settings | Dashboard deployment/security |

Use the actual images from the workspace. Do not replace them with generated mock terminal screenshots.

### 7.2 Supporting evidence folders

The user created:

```text
CloudGuard_Evidence/
├── screenshots/
├── command_outputs/
└── test_results/
```

The eight screenshots are the captured evidence set. `command_outputs/` may be empty because separate raw `.txt` transcripts were not collected. The test matrix in this master document can be used as the starting point for a test-results document, but do not claim that a separate test-results file already exists unless one is actually present.

---

## 8. Results and discussion

CloudGuard demonstrates a working, small-scale multi-customer hosting environment on a single Ubuntu server.

The principal outcomes are:

1. The Ubuntu VM can be administered remotely from the EndeavourOS host using SSH public-key authentication.
2. A separate 25 GiB virtual data disk is managed through LVM, with dedicated logical volumes for two customers and backups.
3. The two customer accounts have separate storage areas and tested directory-level isolation.
4. Nginx serves two different customer websites using hostname-based virtual hosting.
5. UFW limits the required inbound services to the VirtualBox host-only network.
6. SSH configuration removes password-based and direct root login.
7. A timestamped backup script records results and applies a seven-backup retention policy.
8. A manual file recovery test was completed successfully.
9. Cron schedules monitoring hourly and backups daily.
10. A read-only Flask/Gunicorn dashboard provides a consolidated view of the server and hosting environment, with basic authentication and systemd service hardening.

The dashboard acts as an administrative visibility layer over the underlying Linux services. It does not replace the native Linux administration tools; it summarizes selected information for easier monitoring.

The implementation shows how standard Linux facilities can be combined to simulate important functions of a basic hosting provider.

---

## 9. Limitations

The final report should honestly identify the following limitations:

- The system runs inside one VirtualBox VM and is not a production cloud platform.
- The customer websites are reachable through local host-only networking and local host-file mappings, not public DNS.
- The websites use HTTP; TLS/HTTPS was not configured.
- Only two simulated customers are configured.
- The websites are static HTML pages.
- There is no customer billing, payment, registration or self-service portal.
- There is no database-backed application or dynamic customer content management.
- There is no multi-node high availability or automatic failover.
- Backup storage is on a logical volume within the same VM and virtual disk group; this is not equivalent to off-site disaster recovery.
- Monitoring is based on scripts and cron, not a full enterprise monitoring/alerting platform.
- The dashboard is read-only and provides a limited set of operational metrics.
- No formal third-party security audit or penetration test was performed.

---

## 10. Future enhancements

Potential future improvements, clearly labelled as future work, include:

- Configure TLS/HTTPS with a suitable certificate authority for an appropriate deployment environment.
- Add a customer provisioning workflow to create accounts, storage volumes and Nginx virtual hosts consistently.
- Add a database-backed customer inventory.
- Add a customer self-service portal with role-based access controls.
- Move backups to a separate host or remote object-storage service.
- Add backup integrity verification and scheduled restore drills.
- Add alerting for resource thresholds and failed services.
- Add richer monitoring and historical metrics.
- Add automated configuration management and deployment.
- Introduce a multi-server architecture with redundancy and failover.
- Add audit logging and stronger centralized authentication.
- Deploy the design to a cloud provider as a separate future project.

Do not describe these enhancements as completed implementation.

---

## 11. Suggested report chapter structure

Adapt this structure to the supplied reference report PDF rather than forcing it if the reference uses a different academic format.

1. Title page
2. Certificate/declaration, if institutionally required
3. Acknowledgement, if required
4. Abstract
5. Table of contents
6. List of figures and tables
7. Introduction
   - Background
   - Problem statement
   - Motivation
8. Objectives and scope
9. System requirements and tools
10. System architecture
    - Host and VM environment
    - VirtualBox network topology
    - Storage architecture
    - Service architecture
11. Implementation
    - VM setup and package preparation
    - SSH key-based administration
    - LVM storage configuration
    - Customer accounts and permissions
    - Nginx virtual hosting
    - UFW and SSH hardening
    - Backup and recovery
    - Monitoring and cron
    - Flask dashboard
12. Security design
13. Testing and validation
14. Results and discussion
15. Limitations
16. Future enhancements
17. Conclusion
18. References
19. Appendices
    - Selected command examples
    - Selected configuration excerpts
    - Additional screenshots, if useful

The reference report should determine the expected front matter, page style, headings, spacing, figure captions, table style and citation format. Do not invent institutional details.

---

## 12. Figure and table guidance

Use captions that explain the purpose of each figure. Suggested captions:

- **Figure 1:** CloudGuard system architecture.
- **Figure 2:** VirtualBox network configuration and host-only communication.
- **Figure 3:** LVM storage layout on the dedicated data disk.
- **Figure 4:** Customer account separation and directory permissions.
- **Figure 5:** Nginx virtual hosting for Client 1 and Client 2.
- **Figure 6:** UFW firewall and SSH hardening configuration.
- **Figure 7:** Timestamped backup history and backup log.
- **Figure 8:** Monitoring records and cron scheduling.
- **Figure 9:** CloudGuard administration dashboard.
- **Figure 10:** Dashboard service account and systemd hardening.

Only use the screenshots that actually exist for the corresponding figures. Architecture and workflow diagrams may be generated from the verified description in this document.

Potential tables:

- Host and guest system specifications.
- Virtual network interface configuration.
- LVM allocation.
- Customer account and directory layout.
- Service/port/network access matrix.
- Backup and monitoring schedules.
- Test case matrix.
- Limitations and future enhancements.

---

## 13. Important paths and implementation inventory

### 13.1 Host-side project location

Original project directory:

`/home/shobith/alliance/linux_ad/hackathon/`

Evidence directory:

`/home/shobith/alliance/linux_ad/hackathon/CloudGuard_Evidence/`

Expected report workspace is a duplicate of the project directory. Keep the original project unchanged.

### 13.2 Host-side dashboard source

```text
scripts/dashboard/
├── app.py
├── requirements.txt
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── dashboard.js
```

### 13.3 Important guest paths

| Purpose | Path |
|---|---|
| Client 1 storage | `/srv/client1` |
| Client 1 website | `/srv/client1/public` |
| Client 2 storage | `/srv/client2` |
| Client 2 website | `/srv/client2/public` |
| Backup mount | `/srv/backups` |
| Timestamped backup root | `/srv/backups/cloudguard` |
| Backup script | `/usr/local/sbin/cloudguard-backup.sh` |
| Backup log | `/var/log/cloudguard-backup.log` |
| Monitoring script | `/usr/local/sbin/cloudguard-monitor.sh` |
| Monitoring log | `/var/log/cloudguard-monitor.log` |
| Nginx Client 1 site | `/etc/nginx/sites-available/client1` |
| Nginx Client 2 site | `/etc/nginx/sites-available/client2` |
| SSH hardening drop-in | `/etc/ssh/sshd_config.d/99-cloudguard.conf` |
| Dashboard deployment | `/opt/cloudguard-dashboard/` |
| Dashboard environment file | `/etc/cloudguard-dashboard.env` |
| Dashboard systemd unit | `/etc/systemd/system/cloudguard-dashboard.service` |
| Backup cron | `/etc/cron.d/cloudguard-backup` |
| Monitoring cron | `/etc/cron.d/cloudguard-monitor` |

### 13.4 Key service and port summary

| Service | Port / schedule | Access or purpose |
|---|---|---|
| SSH | TCP 22 | Host-only network; key-based administration |
| Nginx | TCP 80 | Host-only network; two customer websites |
| Flask/Gunicorn dashboard | TCP 5000 | Host-only network; basic-authenticated dashboard |
| Monitoring cron | Every hour at minute 0 | Runs monitoring script as root |
| Backup cron | Daily at 02:00 | Runs backup script as root |

---

## 14. Final quality-control checklist for the report

Before considering the report complete, verify:

- [ ] The report title and project name are consistent: **CloudGuard — Cloud Service Provider**.
- [ ] The report follows the supplied reference PDF's structure and formatting where applicable.
- [ ] The implementation is explained from environment setup through final dashboard.
- [ ] SSH administration is explained as a connection from the EndeavourOS host to the Ubuntu VM over the host-only network.
- [ ] The dedicated data disk is correctly identified as `/dev/sdb`; the OS disk `/dev/sda` is not described as the LVM data disk.
- [ ] LVM sizes and mount points are accurate.
- [ ] Customer account isolation is explained with the actual permission model and test.
- [ ] Both Nginx virtual hosts and local hostname resolution are explained.
- [ ] UFW rules are described as restricted to `enp0s8` and `192.168.56.0/24`.
- [ ] SSH hardening settings are accurately represented.
- [ ] Backup retention is described as keeping up to seven timestamped backups.
- [ ] The recovery test is described accurately without inventing a screenshot.
- [ ] Monitoring and backup cron schedules are correct.
- [ ] Dashboard authentication, service account and systemd hardening are covered.
- [ ] All eight screenshots are placed in relevant sections with figure numbers and captions.
- [ ] No screenshot is fabricated or materially altered to appear as terminal evidence.
- [ ] No credentials, password hashes, private keys or other secrets appear in the report.
- [ ] Future enhancements are not presented as completed features.
- [ ] Limitations are stated honestly.
- [ ] References are real and relevant; do not invent books, papers, URLs or access dates.
- [ ] Any certificate, declaration, acknowledgement or approval page contains only institutionally verified details.
- [ ] The final report is saved inside the duplicate report workspace, leaving the original project unchanged.

---

## 15. Source-of-truth note

This master file records the CloudGuard implementation as described during the project work and is intended to guide report preparation. The actual source code, shell scripts, configuration files and captured evidence in the workspace should be used for final verification.

Where a detail cannot be confirmed from the workspace or project history, mark it for clarification rather than guessing. The final report should be technically complete, academically presented and faithful to what was actually built.
