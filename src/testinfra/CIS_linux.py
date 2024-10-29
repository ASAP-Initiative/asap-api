import typing

def _mount_partition_exists(host, partition: str) -> bool:
    cmd = host.run(f"mount |grep -E '\s{partition}\s'")
    return (cmd.stdout != '')

def _mount_partition_option_enabled(host, partition: str, option: str) -> bool:
    cmd = host.run(f"mount | grep -E '\s{partition}\s' | grep {option}")
    return (cmd.stdout != '')


def test_1_1_1_1_cramfs_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.1', 
        'title': 'Ensure mounting of cramfs filesystems is disabled'
    }    
    cmd = host.run('lsmod | grep cramfs')
    assert cmd.stdout == ''

def test_1_1_1_2_freexvfs_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.2', 
        'title': 'Ensure mounting of freexvfs filesystems is disabled'
    }
    cmd = host.run('lsmod | grep freexvfs')
    assert cmd.stdout == ''

def test_1_1_1_3_jffs2_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.3', 
        'title': 'Ensure mounting of jffs2 filesystems is disabled'
    }
    cmd = host.run('lsmod | grep jffs2')
    assert cmd.stdout == ''

def test_1_1_1_4_hfs_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.4', 
        'title': 'Ensure mounting of hfs filesystems is disabled'
    }
    cmd = host.run('lsmod | grep hfs')
    assert cmd.stdout == ''

def test_1_1_1_5_hfsplus_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.5', 
        'title': 'Ensure mounting of hfsplus filesystems is disabled'
    }
    cmd = host.run('lsmod | grep hfsplus')
    assert cmd.stdout == ''

def test_1_1_1_6_squashfs_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.6', 
        'title': 'Ensure mounting of squashfs filesystems is disabled'
    }
    cmd = host.run('lsmod | grep squashfs')
    assert cmd.stdout == ''

def test_1_1_1_7_udf_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.7', 
        'title': 'Ensure mounting of udf filesystems is disabled'
    }
    cmd = host.run('lsmod | grep udf')
    assert cmd.stdout == ''

def test_1_1_1_8_vfat_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.1.8', 
        'title': 'Ensure mounting of FAT filesystems is disabled'
    }
    cmd = host.run('lsmod | grep vfat')
    assert cmd.stdout == ''

def test_1_1_2_tmp_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.2', 
        'title': 'Ensure /tmp is configured'
    }
    assert _mount_partition_exists(host, '/tmp'), json_metadata['CIS']['title']

def test_1_1_3_nodev_option_on_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.3', 
        'title': 'Ensure nodev option set on /tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/tmp', 'nodev'), json_metadata['CIS']['title']

def test_1_1_4_nosuid_option_on_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.4', 
        'title': 'Ensure nosuid option set on /tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/tmp', 'nosuid'), json_metadata['CIS']['title']

def test_1_1_5_noexec_option_on_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.5', 
        'title': 'Ensure noexec option set on /tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/tmp', 'noexec'), json_metadata['CIS']['title']

def test_1_1_6_var_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.6', 
        'title': 'Ensure separate partition exists for /var'
    }
    assert _mount_partition_exists(host, '/var'), json_metadata['CIS']['title']

def test_1_1_7_var_tmp_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.6', 
        'title': 'Ensure separate partition exists for /var/tmp'
    }
    assert _mount_partition_exists(host, '/var/tmp'), json_metadata['CIS']['title']

def test_1_1_8_nodev_option_on_var_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.8', 
        'title': 'Ensure nodev option set on /var/tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/var/tmp', 'nodev'), json_metadata['CIS']['title']

def test_1_1_9_nosuid_option_on_var_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.9', 
        'title': 'Ensure nosuid option set on /var/tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/var/tmp', 'nosuid'), json_metadata['CIS']['title']

def test_1_1_10_noexec_option_on_var_tmp(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.10', 
        'title': 'Ensure noexec option set on /var/tmp partition'
    }
    assert _mount_partition_option_enabled(host, '/var/tmp', 'noexec'), json_metadata['CIS']['title']

def test_1_1_11_var_log_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.11', 
        'title': 'Ensure separate partition exists for /var/log'
    }
    assert _mount_partition_exists(host, '/var/log'), json_metadata['CIS']['title']

def test_1_1_12_var_log_audit_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.12', 
        'title': 'Ensure separate partition exists for /var/log/audit'
    }
    assert _mount_partition_exists(host, '/var/log/audit'), json_metadata['CIS']['title']

def test_1_1_13_home_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.13', 
        'title': 'Ensure separate partition exists for /home'
    }
    assert _mount_partition_exists(host, '/home'), json_metadata['CIS']['title']

def test_1_1_14_nodev_option_on_home(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.14', 
        'title': 'Ensure nodev option set on /home partition'
    }
    assert _mount_partition_option_enabled(host, '/home', 'nodev'), json_metadata['CIS']['title']


def test_1_1_15_nodev_option_on_dev_shm(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.15', 
        'title': 'Ensure nodev option set on /dev/shm partition'
    }
    assert _mount_partition_option_enabled(host, '/dev/shm', 'nodev'), json_metadata['CIS']['title']

def test_1_1_16_nosuid_option_on_dev_shm(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.16', 
        'title': 'Ensure nosuid option set on /dev/shm partition'
    }
    assert _mount_partition_option_enabled(host, '/dev/shm', 'nosuid'), json_metadata['CIS']['title']

def test_1_1_17_noexec_option_on_dev_shm(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.17', 
        'title': 'Ensure noexec option set on /dev/shm partition'
    }
    assert _mount_partition_option_enabled(host, '/dev/shm', 'noexec'), json_metadata['CIS']['title']

def test_1_1_18_nodev_option_on_removable_media(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.18', 
        'title': 'Ensure nodev option set on removable media'
    }
    # TODO

def test_1_1_19_nosuid_option_on_removable_media(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.19', 
        'title': 'Ensure nosuid option set on removable media'
    }
    # TODO

def test_1_1_20_noexec_option_on_removable_media(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.20', 
        'title': 'Ensure noexec option set on removable media'
    }
    # TODO

def test_1_1_21_sticky_bit_on_all_world_writable_directories(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.21', 
        'title': 'Ensure sticky bit is set on all world-writable directories'
    }
    # TODO

def test_1_1_22_disable_automounting(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.22', 
        'title': 'Disable automounting'
    }
    # TODO

def test_1_1_23_disable_usb_storage(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.1.23', 
        'title': 'Disable USB storage'
    }
    # TODO

def test_1_2_2_gpg_keys_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.2.2', 
        'title': 'Ensure GPG keys are configured'
    }
    # TODO


###
### 1.3 Filesystem Integrity Checking
###

def test_1_3_1_ensure_aide_installed(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.3.1', 
        'title': 'Ensure AIDE is installed'
    }
    assert host.package('aide').is_installed, json_metadata['CIS']['title'] 

def test_1_3_2_ensure_filesystem_integrity_regularly_checked(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.3.2', 
        'title': 'Ensure filesystem integrity is regularly checked'
    }
    # TODO


###
### 1.4 Secure Boot Settings
###

def test_1_4_1_permissions_on_bootloader_configured(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.4.1', 
        'title': 'Ensure permissions on bootloader config are configured'
    }
    # TODO

def test_1_4_2_bootloader_password_is_set(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.4.2', 
        'title': 'Ensure bootloader password is set'
    }
    # TODO

def test_1_4_3_authentication_required_for_single_user_mode(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.4.3', 
        'title': 'Ensure authentication required for single user mode'
    }
    # TODO

def test_1_4_4_interactive_boot_not_enabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.4.4', 
        'title': 'Ensure interactive boot is not enabled'
    }
    # TODO


###
### 1.5 Additional Process Hardening
###

def test_1_5_1_core_dumps_restricted(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.5.1', 
        'title': 'Ensure core dumps are restricted'
    }
    # TODO

def test_1_5_2_xd_nx_support_enabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.5.2', 
        'title': 'Ensure XD/NX support is enabled'
    }
    # TODO

def test_1_5_3_aslr_enabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.5.3', 
        'title': 'Ensure address space layout randomization (ASLR) is enabled'
    }
    # TODO

def test_1_5_4_prelink_disabled(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.5.4', 
        'title': 'Ensure prelink is disabled'
    }
    # TODO


###
### 1.6 Mandatory Access Control
###

def test_1_6_1_1_selinux_or_apparmor_installed(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.6.1.1', 
        'title': 'Ensure SELinux or AppArmor are installed'
    }
    # TODO

def test_1_6_2_1_selinux_not_disabled_in_bootloader_configuration(host, json_metadata):
    json_metadata['CIS'] = { 
        'id': '1.6.2.1', 
        'title': ' Ensure SELinux is not disabled in bootloader configuration'
    }
    # TODO