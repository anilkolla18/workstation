# Linux Notes

# Register RHEL with developer version

```
sudo subscription-manager register --username anil79.kolla --password Tony0518
```


# update Yum
   
   ```
   yum update
   ```

# Install apt using yum

In Red Hat Enterprise Linux (RHEL) and its derivatives, the default package manager is yum (or dnf in more recent versions). apt is not the standard package manager for RHEL, but it is available through the Extra Packages for Enterprise Linux (EPEL) repository. You can use yum to install apt if you have the EPEL repository enabled. Here's how you can do it:

Enable the EPEL Repository (if not already enabled):

First, you need to enable the EPEL repository on your RHEL system. EPEL provides additional packages, including apt. Run the following command to enable EPEL:

```
sudo yum install epel-release
```

Install apt with yum:
After enabling the EPEL repository, you can install apt using yum:

```
sudo yum install apt
```
Use apt Commands:
You should now be able to use apt commands on your RHEL system, similar to how you use them on Debian-based distributions. For example:

```
sudo apt update
sudo apt install package-name
```

Keep in mind that while you can install and use apt on RHEL using EPEL, it's not the recommended or standard approach. dnf or yum is the preferred way to manage packages on RHEL and its derivatives. Using apt alongside the native package manager can lead to potential issues and package conflicts, so use it with caution and only when necessary.



# To enable sudo for your user ID on RHEL, add your user ID to the wheel group:
1. Become root by running su
2. Run
   ```
   usermod -aG wheel your_user_id
   ```
4. Log out and back in again


# How to change your hostname in Linux
1. Run hostname command to find current hostname


