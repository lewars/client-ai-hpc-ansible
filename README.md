# AI/HPC Infrastructure Deployment

This project provides Ansible automation for deploying and managing infrastructure components for AI and HPC workloads, specifically focusing on NVIDIA GPU drivers, Enroot containers, and Pyxis integration with Slurm.

## Components

- **NVIDIA Drivers**: Automated installation and configuration of NVIDIA GPU drivers, CUDA toolkit, and related components
- **Enroot**: Container runtime for unprivileged containers in HPC environments
- **Pyxis**: Slurm plugin for container execution via Enroot

## Architecture Support

- **RHEL/Rocky Linux 9**: Controllers and submit nodes
- **Ubuntu 22.04/24.04**: Compute nodes
- **Mixed Environment**: Full support for heterogeneous clusters

## Prerequisites

- Ansible 2.14 or higher
- Python 3.12+
- Task (taskfile) installed for workflow automation
- SSH access to all nodes
- Sudo privileges on target nodes

## Directory Structure

```
ai-hpc-ansible/
├── inventory/          # Environment inventories
│   ├── lab             # Lab environment inventory
│   ├── dev             # Development inventory
│   └── prod            # Production inventory
├── roles/              # Ansible roles
│   ├── nvidia/         # NVIDIA driver configuration
│   ├── enroot/         # Enroot container runtime
│   └── pyxis/          # Pyxis Slurm plugin
├── playbooks/          # Ansible playbooks
└── Taskfile.yml        # Task automation
```

## Quick Start

1. Install dependencies:
   ```bash
   task install-deps
   ```

2. Configure inventory:
   - Edit `inventory/lab` for your environment
   - Update group_vars as needed

3. Deploy NVIDIA drivers, Enroot, and Pyxis to lab environment:
   ```bash
   task deploy-lab
   ```

## NVIDIA Configuration

The NVIDIA role handles driver installation, CUDA toolkit setup, and additional components:

- NVIDIA drivers (version 570.124.06 by default)
- CUDA toolkit 12.8
- Persistence daemon for consistent GPU state
- Fabric Manager for systems with NVLink/NVSwitch

Configuration options are available in `roles/nvidia/defaults/main.yml`.

## Enroot and Pyxis Setup

Enroot provides unprivileged container functionality, while Pyxis integrates it with Slurm:

- Container image importing and conversion
- Unprivileged execution
- GPU passthrough
- Integration with Slurm workload manager

## Testing

Individual role testing is available via Molecule:

```bash
task test:role ROLE=nvidia
task test:role ROLE=enroot
task test:role ROLE=pyxis
```

To test all roles at once:

```bash
task test:all
```

## Environment Configuration

Configure different environments in their respective inventory files:
- `inventory/lab` - Testing environment
- `inventory/dev` - Development environment
- `inventory/prod` - Production environment

## Support

- Issue tracker: [Project Issues](https://github.com/lewars/ai-hpc-ansible/issues)

## License

MIT License
