def _get_size_spec(device, size_gb):
    size_kb = int(size_gb * 1024.0 * 1024.0)
    disk_spec = _edit_existing_hard_disk_helper(disk=device, size_kb=size_kb) if device.capacityInKB < size_kb else None
    return disk_spec