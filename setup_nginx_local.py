import paramiko
import time

def setup_nginx_local_instance(instance_ip, key_path):
    try:
        # Connect to local instance via SSH
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname="localhost", username="root", key_filename="/c/Users/debsu/.ssh/id_rsa24")

        # Update and install Nginx
        update_command = "sudo apt update"
        install_nginx_command = "sudo apt install -y nginx"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(update_command)
        print(f"Output of '{update_command}':")
        print(ssh_stdout.read().decode())
        print(ssh_stderr.read().decode())

        time.sleep(1)  # Wait for a moment before running the next command

        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(install_nginx_command)
        print(f"Output of '{install_nginx_command}':")
        print(ssh_stdout.read().decode())
        print(ssh_stderr.read().decode())

        # Configure Nginx (example configuration)
        nginx_config = """
        server {
            listen 80;
            html Server;

            root C:\JUL-13_CI_CD;
            index index.html;

            location / {
                try_files $uri $uri/ =404;
            }
        }
        """
        nginx_config_file = "/etc/nginx/sites-available/default"
        
        # Upload nginx config file
        ftp_client = ssh_client.open_sftp()
        nginx_config_file_remote = ftp_client.file(nginx_config_file, "w")
        nginx_config_file_remote.write(nginx_config)
        nginx_config_file_remote.close()
        ftp_client.close()

        # Restart Nginx
        restart_nginx_command = "sudo systemctl restart nginx"
        ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(restart_nginx_command)
        print(f"Output of '{restart_nginx_command}':")
        print(ssh_stdout.read().decode())
        print(ssh_stderr.read().decode())

        print("Nginx setup completed on local instance.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if ssh_client:
            ssh_client.close()

if __name__ == "__main__":
    instance_ip = "your_local_instance_ip"  # Replace with your local instance's IP address
    key_path = "/path/to/your/key.pem"      # Replace with path to your SSH private key

    setup_nginx_local_instance(instance_ip, key_path)
