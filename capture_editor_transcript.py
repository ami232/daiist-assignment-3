"""Capture a genuine Claude Code subagent session after user sign-in.
No credentials or fictional transcript content are written by this script.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    auth = subprocess.run(['claude', 'auth', 'status'], capture_output=True, text=True)
    if auth.returncode or not json.loads(auth.stdout).get('loggedIn'):
        raise SystemExit('Sign in with claude auth login first. No transcript generated.')
    prompt = ('Delegate this task to the configured corpus-researcher subagent. '
              'The subagent must use only mcp__corpus__search. '
              'Question: Why should supplier contingency planning consider both supporting '
              'infrastructure and inventory buffers? Retrieve evidence for both aspects, '
              'cite exact chunk IDs, and state source locations and limitations. '
              'Do not add documents or change files. Return the subagent answer.')
    command = ['claude', '-p', prompt, '--output-format', 'stream-json', '--verbose',
               '--strict-mcp-config', '--mcp-config', '.mcp.json',
               '--tools', 'Agent', '--allowedTools', 'Agent,mcp__corpus__search',
               '--disallowedTools', 'mcp__corpus__add_document',
               '--forward-subagent-text']
    out = ROOT/'eval/editor_subagent'
    out.mkdir(exist_ok=True)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    (out/'session.jsonl').write_text(result.stdout)
    (out/'stderr.txt').write_text(result.stderr)
    (out/'invocation.json').write_text(json.dumps({'command':command,'exit_code':result.returncode,'role':'Actual Claude Code invocation; inspect tool events before treating as successful subagent evidence.'},indent=2)+'\n')
    if result.returncode:
        raise SystemExit('Editor request failed; actual output saved, no success claimed.')
    print('Real session saved in eval/editor_subagent/. Inspect subagent/tool events before adding to REPORT.md.')

if __name__ == '__main__':
    main()
