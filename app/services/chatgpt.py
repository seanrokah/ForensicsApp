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


def generate_analyze(commands_output, sceanrio_2):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"""
You are an expert Digital Forensics and Incident Response (DFIR) analyst with extensive cybersecurity experience.

TASK:
- Analyze the provided `{commands_output}` based on `{sceanrio_2}`.
- Identify any **suspicious or malicious indicators** (e.g., ransomware, trojans, unauthorized access, lateral movement, persistence mechanisms).
- Look for **patterns matching known MITRE ATT&CK techniques**.
- Determine if any **anomalous behavior**, such as connections to **unknown IPs**, **execution of suspicious binaries**, or **registry modifications**, is present.

ANALYSIS REQUIREMENTS:
- Assess if any executed commands indicate **malicious activity** or unusual system behavior.
- If the commands reveal suspicious files, processes, or connections, **explain why** they are dangerous.
- Cross-reference findings with **MITRE ATT&CK tactics, techniques, and procedures (TTPs)**.
- Assign a **maliciousness score from 1 to 100** (1 = Not Malicious, 100 = Extremely Malicious).
- Justify the score with evidence found in the command output.
- Please use the {commands_output} to understand if there is something malicious , the user {sceanrio_2} is just for the background , you need according to the commands output to understand the maliciouness of the commands.

OUTPUT FORMAT:
- **Threat Analysis:** [Explain if anything is suspicious and why]
- **Indicators of Compromise (IoCs):** [List any suspicious files, IPs, registry modifications, or network activity]
- **MITRE ATT&CK Mapping:** [List any relevant techniques, tactics, or procedures]
- **Maliciousness Score:** [1-100]
- **Conclusion & Recommendations:** [Provide a summary and next steps]

Be precise, objective, and forensic-driven in your assessment.
"""},
            {"role": "user", "content": f"Please use the system command instruction to generate the analyzitation of the scenario following the commadns"},
        ],
    )
    print (completion.choices[0].message.content)
    return completion.choices[0].message.content
