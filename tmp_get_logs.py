import subprocess, json
p = subprocess.run(['gcloud.cmd', 'logging', 'read', 'resource.type="cloud_run_revision" AND resource.labels.service_name="backend-toledo" AND severity>=ERROR', '--limit', '20', '--format=json'], capture_output=True, text=True, encoding='utf-8')
try:
    logs = json.loads(p.stdout)
    for log in logs:
        payload = log.get('textPayload', '')
        if 'sqlalchemy' in payload or 'Error' in payload or 'Exception' in payload or 'ProgrammingError' in payload or 'relation' in payload or 'column' in payload:
            print("--- LOG ENTRY ---")
            print(payload[:1000] if payload else None)
except json.JSONDecodeError:
    print("Could not parse JSON. Output was:")
    print(p.stdout[:500])
    print("STDERR:")
    print(p.stderr[:500])
