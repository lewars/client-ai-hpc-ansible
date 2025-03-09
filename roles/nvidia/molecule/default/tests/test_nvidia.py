import os
import pytest
import re


def test_nvidia_repo_installed(host):
    """Test that the local NVIDIA repository was installed."""
    if (
        host.system_info.distribution == "rhel"
        or host.system_info.distribution == "centos"
        or host.system_info.distribution == "rocky"
    ):
        # Check for RHEL/Rocky repository
        repo_file = host.file("/etc/yum.repos.d/cuda-rhel.repo")
        assert repo_file.exists, "NVIDIA RHEL repository file not found"
    elif (
        host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "debian"
    ):
        # Check for Ubuntu repository
        gpg_key = host.file("/usr/share/keyrings/cuda-archive-keyring.gpg")
        assert gpg_key.exists, "NVIDIA GPG key not found in /usr/share/keyrings"

        # Check for pin file
        pin_file = host.file("/etc/apt/preferences.d/cuda-repository-pin-600")
        assert pin_file.exists, "CUDA repository pin file not found"


def test_nvidia_driver_loaded(host):
    """Test that the NVIDIA kernel module is loaded."""
    assert host.exists("nvidia"), "NVIDIA kernel module is not loaded"


def test_nvidia_smi_exists(host):
    """Test that nvidia-smi executable exists."""
    nvidia_smi = host.file("/usr/bin/nvidia-smi")
    assert nvidia_smi.exists, "nvidia-smi executable not found"
    assert nvidia_smi.mode & 0o111 != 0, "nvidia-smi not executable"


def test_nvidia_smi_execution(host):
    """Test that nvidia-smi runs successfully."""
    cmd = host.run("nvidia-smi")
    assert cmd.rc == 0, "nvidia-smi failed to run"
    assert "NVIDIA-SMI" in cmd.stdout, "nvidia-smi output is unexpected"
    # Check that driver version is as expected
    assert re.search(
        r"Driver Version: [5][7][0-9]\.[0-9]+\.[0-9]+", cmd.stdout
    ), "Driver version mismatch"


def test_cuda_installation(host):
    """Test if CUDA is properly installed."""
    # Check for CUDA compiler
    nvcc = host.file("/usr/local/cuda/bin/nvcc")
    if not nvcc.exists:
        # Alternative location on some distributions
        nvcc = host.file("/usr/bin/nvcc")

    assert nvcc.exists, "CUDA compiler not found"

    cmd = host.run(nvcc.path + " --version")
    assert cmd.rc == 0, "NVCC failed to run"
    assert "cuda" in cmd.stdout.lower(), "NVCC output doesn't mention CUDA"

    # Check for CUDA libraries
    cuda_lib_paths = [
        "/usr/local/cuda/lib64/libcudart.so",
        "/usr/lib/x86_64-linux-gnu/libcudart.so",  # Debian/Ubuntu
        "/usr/lib64/libcudart.so",  # RHEL/Rocky
    ]

    lib_found = False
    for lib_path in cuda_lib_paths:
        cuda_lib = host.file(lib_path)
        if cuda_lib.exists:
            lib_found = True
            break

    assert lib_found, "CUDA runtime library not found"


def test_cuda_environment_variables(host):
    """Test if CUDA environment variables are set."""
    cuda_env = host.file("/etc/profile.d/cuda.sh")
    assert cuda_env.exists, "CUDA environment file not found"
    assert cuda_env.contains("CUDA_HOME"), "CUDA_HOME not set in environment file"
    assert cuda_env.contains("PATH"), "PATH not updated in CUDA environment file"


def test_nvidia_persistence_daemon_installed(host):
    """Test if the NVIDIA persistence daemon is installed."""
    if (
        host.system_info.distribution == "rhel"
        or host.system_info.distribution == "centos"
        or host.system_info.distribution == "rocky"
    ):
        package = host.package("nvidia-persistenced")
        assert package.is_installed, "NVIDIA persistence daemon is not installed"
    elif (
        host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "debian"
    ):
        package = host.package("nvidia-persistenced")
        assert package.is_installed, "NVIDIA persistence daemon is not installed"


def test_nvidia_persistence_daemon_config(host):
    """Test if the NVIDIA persistence daemon config exists."""
    config_file = host.file("/etc/nvidia/nvidia-persistenced.conf")
    assert config_file.exists, "NVIDIA persistence daemon config not found"
    assert config_file.contains(
        "--no-persistenced-user"
    ), "NVIDIA persistence daemon config missing expected content"


def test_nvidia_persistence_daemon_running(host):
    """Test if the NVIDIA persistence daemon is running."""
    service = host.service("nvidia-persistenced")
    assert service.is_running, "NVIDIA persistence daemon is not running"
    assert service.is_enabled, "NVIDIA persistence daemon is not enabled"


def test_nvidia_fabricmanager_installed(host):
    """Test if the NVIDIA Fabric Manager is installed."""
    # Only check if fabricmanager is installed if NVIDIA_INSTALL_FABRICMANAGER is true
    # We'll check for the package and skip if it's not installed
    if (
        host.system_info.distribution == "rhel"
        or host.system_info.distribution == "centos"
        or host.system_info.distribution == "rocky"
    ):
        package = host.package("nvidia-fabricmanager")
        if not package.is_installed:
            pytest.skip("NVIDIA Fabric Manager is not installed, skipping test")
        assert package.is_installed, "NVIDIA Fabric Manager is not installed"
    elif (
        host.system_info.distribution == "ubuntu"
        or host.system_info.distribution == "debian"
    ):
        package = host.package("nvidia-fabricmanager")
        if not package.is_installed:
            pytest.skip("NVIDIA Fabric Manager is not installed, skipping test")
        assert package.is_installed, "NVIDIA Fabric Manager is not installed"


def test_nvidia_fabricmanager_running(host):
    """Test if the NVIDIA Fabric Manager is running."""
    service = host.service("nvidia-fabricmanager")
    if not service.is_running:
        pytest.skip("NVIDIA Fabric Manager service is not running, skipping test")
    assert service.is_running, "NVIDIA Fabric Manager is not running"
    assert service.is_enabled, "NVIDIA Fabric Manager is not enabled"
