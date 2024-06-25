def check_pod_status():
    try:
        # Construct the kubectl command
        command = [
            'kubectl', 'get', 'pods', '--all-namespaces',
            '-o', 'custom-columns=NAME:.metadata.name,NAMESPACE:.metadata.namespace,STATUS:.status.phase,READY:.status.containerStatuses[*].ready'
        ]

        # Run the kubectl command and capture output and errors
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            alert = False
            body = "Pod status alert:\n\n"
            body += f"{'POD NAME':<30}{'NAMESPACE':<20}{'STATUS':<15}{'READY':<10}\n"
            body += "-" * 75 + "\n"

            lines = result.stdout.strip().split('\n')
            headers = lines[0].split()  # Get the headers to know the indices
            for line in lines[1:]:
                columns = line.split()
                pod_name = columns[headers.index('NAME')]
                pod_namespace = columns[headers.index('NAMESPACE')]
                pod_status = columns[headers.index('STATUS')]
                ready_status = columns[headers.index('READY')]

                # Check if the pod is in the desired state
                if not ((pod_status == "Running" and ready_status == "True") or (pod_status == "Succeeded")):
                    alert = True
                    body += f"{pod_name:<30}{pod_namespace:<20}{pod_status:<15}{ready_status:<10}\n"

            if alert:
                send_email("Kubernetes Pod Alert", body)
            else:
                print("All pods are in the desired state.")
        else:
            # Print error message and stderr if command failed
            print(f"Error running kubectl command: {result.stderr}")
    
    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl command: {e}")
        print("Command stderr:")
        print(e.stderr)
