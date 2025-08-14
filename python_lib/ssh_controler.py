import os,sys,paramiko

class SSHController:
    def __init__(self, hostname, port=22, username=None, password=None, key_filename=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_filename = key_filename
        self.client = None
        
        self.validate()
    
    def validate(self):
        if self.username is None: raise ValueError("Username must be provided for SSH connection.")
        if self.password is None and self.key_filename is None: raise ValueError("Either password or key_filename must be provided for SSH connection.")

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.key_filename is not None: self.client.connect(self.hostname, port=self.port, username=self.username, key_filename=self.key_filename)
            else: self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            print(f"Connected to {self.hostname} as {self.username}")
        except Exception as e:
            print(f"Failed to connect to {self.hostname}: {e}")
        
    def execute_command(self, command):
        try:
            print(f"Executing command: '{command}'")
            stdin, stdout, stderr = ssh_client.exec_command(command)

            # Read output
            print("\n--- STDOUT ---")
            for line in stdout:print(line.strip())

            # Read error output
            print("\n--- STDERR ---")
            error_output = stderr.read().decode().strip()
            print(error_output)

            # Get the exit status of the command
            exit_status = stdout.channel.recv_exit_status()
            print(f"\nCommand exited with status: {exit_status}")
        except paramiko.SSHException as ssh_exc: print(f"SSH error: {ssh_exc}")
        except Exception as e: print(f"An unexpected error occurred: {e}")