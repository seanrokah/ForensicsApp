from openai import OpenAI
client = OpenAI()
def generate_commands(sceanrio_1, os_type, number_of_commands):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""
You are an expert Digital Forensics and Incident Response (DFIR) investigator with extensive cybersecurity experience. 

TASK:
- Analyze the provided incident scenario
- Generate exactly {number_of_commands} forensically sound {os_type} commands to investigate the incident
- Focus on evidence collection, threat hunting, and identifying indicators of compromise

REQUIREMENTS:
- Return ONLY executable {os_type} commands with NO explanations or commentary
- Each command must be on its own line
- Ensure commands are non-destructive and preserve forensic integrity
- Focus on log analysis, memory forensics, network traffic analysis, and file system investigation
- Commands should help identify malware, unauthorized access, data exfiltration, or persistence mechanisms

COMMAND TYPES TO CONSIDER:
- File system analysis (finding modified/suspicious files)
- Process and memory inspection
- Network connection examination
- Log analysis (system, application, security logs)
- Registry analysis (for Windows)
- Artifact collection and timeline creation

FORMAT: (dont add bash/powershell/cmd at the beginning of the command or any other shell)
[command 1]
[command 2]
...and so on

The output will be executed on the system and the results analyzed for further investigation. and again please generate only {number_of_commands} commands.
"""},
            {"role": "user", "content": f"the scenario : {sceanrio_1}"},
        ],
    )
    print (completion.choices[0].message.content)
    return completion.choices[0].message.content
