import subprocess

def command_run(commands):
    # First parse the commands into a list
    commands_list = commands_parser(commands)
    
    all_outputs = []
    
    # Run each command separately
    for cmd in commands_list:
        if cmd.strip():  # Skip empty commands
            result = subprocess.run(
                cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            # Collect the output
            all_outputs.append(f"Command: {cmd}")
            all_outputs.append(f"Output: {result.stdout}")
            if result.stderr:
                all_outputs.append(f"Error: {result.stderr}")
            all_outputs.append("-" * 40)
    
    # Join all outputs with newlines
    return "\n".join(all_outputs)

def commands_parser(commands):
    # Simply split by newlines and return the list
    commands_splitted = commands.split("\n")
    return [cmd for cmd in commands_splitted if cmd.strip()]
