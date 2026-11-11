# CloudGuard – Cloud Service Provider

**Category:** Hackathon-SEE  
**Project Type:** Linux System Administration / Cloud Infrastructure  
**Platform:** Ubuntu Server 26.04.1 LTS

## 1. Project Overview

CloudGuard is a Linux-based cloud service provider prototype designed to demonstrate how a service provider can host and manage multiple customer websites on a single Linux server.

The project implements isolated customer accounts, dedicated storage volumes, web hosting, automated backups, server monitoring, firewall protection, and a web-based administration dashboard.

## 2. Project Objectives

- Configure a Linux server to act as a basic cloud hosting platform.
- Provide separate hosting environments for multiple customers.
- Implement storage allocation using Logical Volume Management (LVM).
- Configure web hosting using Nginx virtual hosts.
- Secure customer data through Linux permissions and account isolation.
- Automate backups and server monitoring.
- Develop a web dashboard for infrastructure visibility.

## 3. Technology Stack

| Component | Technology |
|---|---|
| Operating System | Ubuntu Server 26.04.1 LTS |
| Virtualization | Oracle VirtualBox |
| Storage Management | LVM |
| Web Server | Nginx |
| Backend Dashboard | Python Flask |
| Application Server | Gunicorn |
| Firewall | UFW |
| Remote Administration | OpenSSH |
| Backup | rsync |
| Automation | Cron and Bash |
| Service Management | systemd |

## 4. Infrastructure Configuration

The project uses an Ubuntu Server virtual machine hosted through VirtualBox.

| Component | Configuration |
|---|---|
| Server Hostname | cloudguard-server |
| Server Administrator | cloudadmin |
| Server IP | 192.168.56.103 |
| Network | Host-only |
| Customer 1 | client1 |
| Customer 2 | client2 |

The server hosts two separate customer environments:

- `client1.cloudguard.local`
- `client2.cloudguard.local`

## 5. Storage Management

Logical Volume Management is used to allocate dedicated storage for customer environments and backups.

| Logical Volume | Allocated Storage |
|---|---:|
| Client 1 | 8 GB |
| Client 2 | 8 GB |
| Backups | 4 GB |

The dedicated data disk has a capacity of approximately 25 GB.

LVM provides flexible storage allocation and makes it easier to manage customer storage independently.

## 6. Customer Isolation and Web Hosting

Separate Linux customer accounts and directory structures are configured for the hosted environments.

Nginx virtual hosts serve the individual customer websites.

Linux ownership and permission settings restrict unauthorized access between customer environments.

## 7. Security Implementation

The following security measures are implemented:

- UFW firewall configuration.
- SSH security hardening.
- Separate customer Linux accounts.
- Restricted directory permissions.
- Isolated customer website directories.
- Dedicated dashboard service account.
- Dashboard authentication.
- systemd service hardening.
- Read-only infrastructure monitoring.

## 8. Backup and Monitoring

Automated backup and monitoring functionality is configured on the server.

The backup system uses rsync to copy customer website data into dedicated backup storage.

The backup process retains a limited number of recent backups to manage storage usage.

Scheduled tasks are configured through cron.

A monitoring script collects server information and supports periodic infrastructure checks.

A backup restoration test was also performed to validate the recovery process.

## 9. CloudGuard Administration Dashboard

A Flask-based administration dashboard provides a centralized interface for viewing server information.

The dashboard includes:

- Infrastructure overview.
- Customer hosting information.
- Storage utilization.
- Backup history.
- Service status.
- Monitoring information.

Gunicorn is used to serve the Flask application, with systemd managing the dashboard service.

## 10. Project Evidence

Screenshots documenting the implementation and testing are available in:

`CloudGuard_Evidence/screenshots/`

The evidence includes:

- Dashboard overview.
- Storage and LVM configuration.
- Customer account isolation.
- Hosted customer websites.
- Firewall and SSH security.
- Backup history and logs.
- Monitoring and cron configuration.
- Dashboard service hardening.

## 11. Project Limitations

This implementation is a locally hosted cloud service provider prototype.

It does not currently include:

- Public cloud deployment.
- Public DNS configuration.
- Public HTTPS hosting.
- High availability or automatic failover.
- Customer billing and payment processing.
- A production-scale customer management database.

## 12. Future Scope

Possible improvements include:

- Public cloud deployment.
- Domain registration and DNS integration.
- HTTPS certificates.
- Customer self-service portal.
- Resource usage quotas.
- Billing and subscription management.
- High availability and load balancing.
- Database-backed customer management.

## 13. Conclusion

CloudGuard demonstrates the fundamental components of a Linux-based cloud hosting environment.

The project combines Linux administration, storage management, web hosting, access isolation, security hardening, automated backups, monitoring, and dashboard development into a working prototype.

It provides practical exposure to the infrastructure and administrative concepts involved in operating a basic cloud service provider.
