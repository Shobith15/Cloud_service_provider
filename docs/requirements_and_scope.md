# CloudGuard — Requirements and Scope

## Functional Requirements

1. Provide a Linux-based hosting server.
2. Support multiple customer accounts.
3. Separate customer storage using LVM.
4. Restrict access between customer directories.
5. Host multiple websites using Nginx virtual hosts.
6. Support secure remote administration.
7. Restrict incoming network access through a firewall.
8. Automate customer data backups.
9. Retain a bounded number of backups.
10. Monitor system resources and important services.
11. Provide an administrative dashboard.

## Non-Functional Requirements

- Maintainability through scripts and configuration files.
- Separation of customer data.
- Restricted administrative access.
- Persistent storage configuration.
- Automated recurring tasks.
- Verifiable test results.
- Clear technical documentation.

## Implemented Scope

The current implementation supports two simulated customers on one Ubuntu virtual machine.

It provides storage separation, filesystem permission controls, Nginx virtual hosting, SSH security, firewall restrictions, backup and monitoring automation.

## Pending Scope

The administrative dashboard and its integration with live server information remain pending.

## Out of Scope

- Public cloud provisioning.
- Multi-region infrastructure.
- Automatic VM/container provisioning.
- Public customer registration.
- Billing and payment processing.
- Production-grade high availability.
- Publicly accessible customer DNS and TLS deployment.
