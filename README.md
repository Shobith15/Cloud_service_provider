
# CloudGuard — Linux-Based Cloud Service Provider

**Hackathon-SEE | B.Tech Information Technology**

CloudGuard is a Linux-based cloud service provider prototype that demonstrates how a service provider can provision customer environments, manage storage, monitor server health, automate backups, and provide customer-facing services through a web portal.

The project combines Linux system administration, server security, automation, web technologies, and centralized monitoring into a single working demonstration.

---

## 1. Project Overview

CloudGuard provides two separate interfaces:

- **Administrator Dashboard:** Centralized monitoring and management of the cloud server, customer environments, storage, services, backups, and support tickets.
- **Customer Portal:** Separate customer-facing websites for Client 1 and Client 2, with service information, account-related demo information, and support request submission.

The infrastructure runs on an Ubuntu Server virtual machine, administered remotely from an EndeavourOS host.

## 2. Architecture

```text
                  EndeavourOS Host
                         |
                  VirtualBox Network
                         |
                Ubuntu CloudGuard VM
                  192.168.56.103
                         |
          +--------------+--------------+
          |              |              |
        Nginx       Flask Dashboard   Flask Portal
       Port 80       Port 5000        Port 5001
          |              |              |
     +----+----+         |         +----+----+
     |         |         |         |         |
  Client 1  Client 2  Admin UI   Portal API
     |         |         |         |
     +----+----+         |         |
          |              |         |
     Customer         Monitoring  SQLite
     Websites          and        Database
                       Support
                       Management
```

### Main Components

| Component | Purpose |
|---|---|
| Ubuntu Server | Main cloud infrastructure |
| Nginx | Web server and reverse proxy |
| Flask | Dashboard and customer portal applications |
| Gunicorn | Application server |
| SQLite | Customer support ticket storage |
| LVM | Logical storage management |
| UFW | Firewall management |
| SSH | Secure remote administration |
| rsync | Automated backup operations |
| cron | Scheduled tasks |
| systemd | Service management |

## 3. Administrator Dashboard

The CloudGuard administrator dashboard provides centralized visibility into the server environment.

Features include:

- System information and resource monitoring.
- CPU, memory, and disk utilization.
- Customer environment status.
- Storage and logical volume information.
- Running system services.
- Backup status and history.
- Customer support ticket management.
- Automatic dashboard refresh every 15 seconds.

**Dashboard URL:**

`http://192.168.56.103:5000`

## 4. Customer Portal

CloudGuard provides separate customer-facing websites.

### Client 1

`http://client1.cloudguard.local`

### Client 2

`http://client2.cloudguard.local`

Each customer has a separate website environment and customer-specific portal identity.

The Nginx virtual hosts route requests to the appropriate customer environment and forward API requests to the internal Flask portal application.

### Customer Portal Features

- Customer-specific service information.
- Demo account and billing information.
- Support request submission.
- Customer-specific API routing.

## 5. Support Ticket Management

The support ticket system connects the customer portal with the administrator dashboard.

Workflow:

1. A customer submits a support request through their portal.
2. The Flask portal API validates and stores the request.
3. The ticket is saved in an SQLite database.
4. The administrator retrieves tickets through the dashboard.
5. The administrator can update ticket status.
6. Customers' requests can be tracked through the support workflow.

Supported ticket statuses:

- Open
- In Progress
- Resolved

Internal support management endpoints are protected using an administrator bearer token and restricted to loopback communication.

## 6. Linux Infrastructure and Administration

The project demonstrates practical Linux server administration, including:

- Linux user and group management.
- Customer-specific directory permissions.
- Logical Volume Manager (LVM) configuration.
- Separate logical storage volumes for customers and backups.
- SSH configuration hardening.
- UFW firewall configuration.
- Nginx virtual host configuration.
- systemd service creation and management.
- Scheduled backup and monitoring tasks.
- Server health monitoring.

### Storage Allocation

| Logical Volume | Allocated Storage |
|---|---:|
| Client 1 | 8 GB |
| Client 2 | 8 GB |
| Backups | 4 GB |

## 7. Backup and Automation

CloudGuard implements automated backup operations using `rsync` and cron.

The backup system includes:

- Scheduled daily backups.
- Retention of the latest seven backup sets.
- Separate backup storage.
- Scheduled monitoring operations.

These operations demonstrate basic data protection and routine server maintenance.

## 8. Security Implementation

Security is addressed at both infrastructure and application levels.

Implemented measures include:

- SSH hardening for remote administration.
- UFW firewall rules.
- Linux user and group permission separation.
- Customer-specific directory access.
- Nginx virtual host separation.
- Trusted customer identity headers configured by Nginx.
- Internal portal API restricted to loopback communication.
- Bearer-token protection for administrator support endpoints.
- Environment-based storage of sensitive configuration.
- Dedicated system service accounts.
- systemd service hardening.

**Security limitation:** The current customer portal is a demonstration prototype. It does not implement full customer login/password authentication or real payment processing. Customer separation is demonstrated through Nginx virtual hosts and trusted server-side routing.

## 9. Technology Stack

| Technology | Usage |
|---|---|
| EndeavourOS | Host operating system |
| Ubuntu Server | Cloud server environment |
| VirtualBox | Virtualization |
| Linux | Server administration |
| Nginx | Web serving and reverse proxy |
| Python | Backend programming |
| Flask | Web applications and APIs |
| Gunicorn | WSGI application server |
| SQLite | Support ticket database |
| HTML5 | Frontend structure |
| CSS3 | Frontend styling |
| JavaScript | Frontend interactions |
| LVM | Storage management |
| UFW | Firewall |
| SSH | Remote administration |
| rsync | Backup operations |
| cron | Task scheduling |
| systemd | Service management |
| Git and GitHub | Version control |

## 10. Repository Structure

```text
Cloud_service_provider/
│
├── docs/
│   ├── architecture.md
│   ├── implementation_log.md
│   ├── requirements_and_scope.md
│   ├── CloudGuard_Master_Documentation.md
│   ├── Cloud_Service_Provider_Hackathon_SEE_Report.pdf
│   └── generate_presentation.py
│
├── scripts/
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── templates/
│   │   │   └── index.html
│   │   └── static/
│   │       ├── dashboard.js
│   │       └── style.css
│   │
│   └── portal/
│       ├── portal_app.py
│       ├── requirements.txt
│       ├── index.html
│       ├── client1.html
│       ├── client2.html
│       ├── portal.css
│       └── portal.js
│
└── README.md
```

*The repository may contain additional documentation and supporting files.*

## 11. Running the Demonstration

The project is designed to run using an Ubuntu Server virtual machine hosted through VirtualBox.

### Prerequisites

- EndeavourOS or another Linux host.
- Oracle VirtualBox.
- Ubuntu Server.
- Python 3.
- Nginx.
- Git.
- Administrative privileges on the Ubuntu VM.

### Accessing the Applications

Once the infrastructure and services are configured:

| Application | Address |
|---|---|
| Administrator Dashboard | `http://192.168.56.103:5000` |
| Client 1 Portal | `http://client1.cloudguard.local` |
| Client 2 Portal | `http://client2.cloudguard.local` |

The two customer hostnames must resolve to the CloudGuard VM's IP address on the host machine.

The project documentation contains additional implementation details, configuration information, and demonstration guidance.

## 12. Testing and Validation

The project includes practical validation of:

- Linux user and group configuration.
- Customer directory permissions.
- Logical volume allocation.
- SSH access and hardening.
- Firewall configuration.
- Nginx customer virtual host routing.
- Dashboard application availability.
- Customer portal API availability.
- Customer identity separation.
- Support ticket submission and storage.
- Administrator support ticket retrieval and status updates.
- Backup and monitoring services.

The dashboard and customer portal were deployed and tested on the Ubuntu Server VM.

## 13. Limitations and Future Scope

CloudGuard is an academic prototype and can be extended with:

- Full customer authentication and role-based access control.
- Real payment gateway integration.
- Dynamic customer provisioning.
- Automated resource allocation.
- Cloud API integration.
- Container-based customer isolation.
- Centralized logging and alerting.
- Advanced monitoring and reporting.
- HTTPS with valid domain certificates.
- More comprehensive backup restoration and disaster recovery.

## 14. Project Documentation

Additional project materials are available in the `docs/` directory:

- **Master Documentation:** `docs/CloudGuard_Master_Documentation.md`
- **Hackathon-SEE Project Report:** `docs/Cloud_Service_Provider_Hackathon_SEE_Report.pdf`
- **Architecture Documentation:** `docs/architecture.md`
- **Implementation Log:** `docs/implementation_log.md`
- **Requirements and Scope:** `docs/requirements_and_scope.md`

## 15. Contributors

Developed as a team project for the B.Tech Information Technology Hackathon-SEE.

---

**CloudGuard — Secure Infrastructure. Managed Services. Centralized Control.**
