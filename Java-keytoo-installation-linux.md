# Java-keytoo-installation-linux

Download JDK on Another Machine:
On a machine with internet access, visit the official OpenJDK website or an alternative source, and download the JDK package that you want. Make sure to select the appropriate version for your system architecture.

Example using wget:

```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```
Transfer the Package to the RHEL 8 Machine:
Transfer the downloaded JDK package to the RHEL 8 machine using methods like SCP, USB drive, or any other means.

Extract the JDK Package:
On the RHEL 8 machine, navigate to the directory where you transferred the JDK package and extract its contents:

```
tar -xvf openjdk-11.0.2_linux-x64_bin.tar.gz
```
Move the Extracted Directory:
Move the extracted directory to a location where you want to store the JDK. For example:

```
sudo mv jdk-11.0.2 /opt/
```

Set Environment Variables:
You may want to set the JAVA_HOME environment variable to point to the JDK installation and update the PATH variable accordingly. Add the following lines to your shell profile file (e.g., .bashrc, .zshrc):

```
export JAVA_HOME=/opt/jdk-11.0.2
export PATH=$JAVA_HOME/bin:$PATH
```
Then, run ```source ~/.bashrc``` (or source ~/.zshrc depending on your shell) to apply the changes.

Verify Installation:
Verify that Java and keytool are installed:

```
java -version
keytool -version
```
These commands should display information about the installed Java version and keytool.

By following these steps, you can install the JDK and keytool on your RHEL 8 machine without the need for an internet connection during the installation process.
