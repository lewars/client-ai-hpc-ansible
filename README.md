# Slurm Cluster Deployment

This project provides Ansible automation for deploying and managing a Slurm cluster with Enroot container support. The deployment supports mixed environments with RHEL 9 controller nodes and Ubuntu compute nodes.

## Architecture

- **Controller Nodes**: RHEL 9
- **Compute Nodes**: Ubuntu 22.04
- **Submit Nodes**: Mixed distribution support

## Prerequisites

- Ansible 2.9 or higher
- Task (taskfile) installed
- RHEL 9 nodes for controllers
- Ubuntu 22.04 nodes for compute
- SSH access to all nodes
- Sudo privileges on target nodes

## Directory Structure

```
hpc-cluster/
├── inventory/          # Environment inventories
│   ├── lab
│   ├── dev
│   └── prod
├── group_vars/        # Group variables
├── roles/            # Ansible roles
│   ├── slurm/       # Slurm configuration
│   └── enroot/      # Enroot configuration
├── playbook.yml     # Main playbook
└── ansible.cfg      # Ansible configuration
```

## Quick Start

1. Install dependencies:
   ```bash
   task install-deps
   ```

2. Configure inventory:
   - Edit `inventory/lab` for your environment
   - Update group_vars as needed

3. Deploy lab environment:
   ```bash
   task lab
   ```

## Available Tasks

- `task lab` - Deploy to lab environment
- `task dev` - Deploy to development environment
- `task prod` - Deploy to production environment
- `task deploy-controllers` - Deploy only Slurm controllers
- `task deploy-compute` - Deploy only compute nodes
- `task healthcheck` - Run cluster health checks

## Environment Configuration

Configure different environments in their respective inventory files:
- `inventory/lab` - Testing environment
- `inventory/dev` - Development environment
- `inventory/prod` - Production environment

## Security Notes

- Munge key must be consistent across all nodes
- SSL certificates required for production
- Proper firewall configuration needed
- SELinux/AppArmor considerations

## Testing

Run validation:
```bash
task test
```

## Maintenance

- Backup configuration: `task backup`
- Update packages: `task update`
- Generate new Munge key: `task generate-munge`

## Support

- Issue tracker: [Project Issues](https://github.com/lewars/ai-factory-hpc-cluster/issues)
- Documentation: See `docs/` directory

## License

MIT License - See LICENSE file for details
