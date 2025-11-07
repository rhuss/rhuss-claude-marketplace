#!/usr/bin/env python3
"""
JIRA Helper for Threat Model Assessment Plugin

This module provides functions to create and update JIRA tickets
for threat model assessment findings.

Configuration:
- JIRA API token should be in ~/.zsh-custom/globals.zsh as JIRA_API_TOKEN
- Or set environment variable JIRA_API_TOKEN
- JIRA config should be in ~/.config/.jira/.config.yml

Usage:
    from jira_helper import create_jira_ticket, verify_jira_config

    # Verify JIRA is configured
    if verify_jira_config():
        # Create ticket
        ticket_key = create_jira_ticket(
            summary="Implement Data Retention Policies",
            description="h2. Tasks\\n* Implement retention config\\n...",
            epic="RHAIENG-1247",
            component="Llama Stack Core",
            priority="Critical"
        )
        print(f"Created: {ticket_key}")
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any


def read_jira_config() -> Dict[str, Any]:
    """
    Read JIRA configuration from jira-cli config file.

    Returns:
        Dict with JIRA configuration (server, project, epic field, etc.)
    """
    config_path = Path.home() / ".config" / ".jira" / ".config.yml"

    if not config_path.exists():
        raise FileNotFoundError(
            f"JIRA config not found at {config_path}. "
            "Please run 'jira init' to configure jira-cli."
        )

    # Parse YAML config (simple parsing, assumes standard format)
    config = {}
    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()

                    if key == 'server':
                        config['server'] = value
                    elif key == 'key' and 'project' not in config:
                        # First 'key' under project
                        config['project'] = value
                    elif key == 'login':
                        config['login'] = value
                    elif key == 'link' and 'epic' not in config:
                        # Epic link custom field
                        config['epic_field'] = value

    return config


def get_jira_token() -> Optional[str]:
    """
    Get JIRA API token from environment or globals.zsh file.

    Returns:
        API token string or None if not found
    """
    # Check environment variable first
    token = os.environ.get('JIRA_API_TOKEN')
    if token:
        return token

    # Check globals.zsh file
    globals_path = Path.home() / ".zsh-custom" / "globals.zsh"
    if globals_path.exists():
        with open(globals_path, 'r') as f:
            for line in f:
                if line.strip().startswith('export JIRA_API_TOKEN='):
                    # Extract token from export statement
                    token = line.split('=', 1)[1].strip().strip('"\'')
                    return token

    return None


def verify_jira_config() -> bool:
    """
    Verify JIRA configuration is available and working.

    Returns:
        True if JIRA is properly configured, False otherwise
    """
    try:
        config = read_jira_config()
        token = get_jira_token()

        if not token:
            print("❌ JIRA API token not found.", file=sys.stderr)
            print("   Set JIRA_API_TOKEN in ~/.zsh-custom/globals.zsh or environment", file=sys.stderr)
            return False

        if not config.get('server'):
            print("❌ JIRA server not configured in ~/.config/.jira/.config.yml", file=sys.stderr)
            return False

        # Test connection with jira-cli
        result = subprocess.run(
            ['jira', 'me'],
            env={**os.environ, 'JIRA_API_TOKEN': token},
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode != 0:
            print(f"❌ JIRA connection test failed: {result.stderr}", file=sys.stderr)
            return False

        print(f"✓ JIRA configured: {config['server']} (project: {config.get('project', 'unknown')})")
        return True

    except Exception as e:
        print(f"❌ JIRA configuration error: {e}", file=sys.stderr)
        return False


def create_jira_ticket(
    summary: str,
    description: str,
    epic: Optional[str] = None,
    component: Optional[str] = None,
    priority: str = "Critical",
    issue_type: str = "Story"
) -> Optional[str]:
    """
    Create a JIRA ticket for threat model assessment findings.

    Args:
        summary: Ticket summary/title
        description: Full description in JIRA wiki markup format
        epic: Epic key to link to (e.g., "RHAIENG-1247")
        component: Component name (e.g., "Llama Stack Core")
        priority: Priority (Critical, High, Medium, Low)
        issue_type: Issue type (Story, Task, Bug, etc.)

    Returns:
        Created ticket key (e.g., "RHAIENG-1841") or None if failed
    """
    try:
        config = read_jira_config()
        token = get_jira_token()

        if not token:
            raise ValueError("JIRA API token not found")

        # Save description to temp file
        desc_file = Path("/tmp/jira_description_temp.txt")
        desc_file.write_text(description)

        # Build jira-cli command
        cmd = [
            'jira', 'issue', 'create',
            '-t', issue_type,
            '-s', summary,
            '-T', str(desc_file),
            '-y', priority,
            '--web'  # Open in browser after creation
        ]

        # Add component if provided
        if component:
            cmd.extend(['-C', component])

        # Execute creation
        result = subprocess.run(
            cmd,
            env={**os.environ, 'JIRA_API_TOKEN': token},
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Failed to create JIRA ticket: {result.stderr}", file=sys.stderr)
            return None

        # Extract ticket key from output
        # Output format: "✓ Issue created\nhttps://issues.redhat.com/browse/RHAIENG-1841"
        ticket_key = None
        for line in result.stdout.split('\n'):
            if 'browse/' in line:
                ticket_key = line.split('browse/')[-1].strip()
                break

        if not ticket_key:
            print("⚠️  Ticket created but couldn't extract key", file=sys.stderr)
            print(result.stdout)
            return None

        # Link to epic if provided
        if epic:
            epic_result = subprocess.run(
                ['jira', 'epic', 'add', epic, ticket_key],
                env={**os.environ, 'JIRA_API_TOKEN': token},
                capture_output=True,
                text=True,
                timeout=10
            )

            if epic_result.returncode != 0:
                print(f"⚠️  Ticket created but epic link failed: {epic_result.stderr}", file=sys.stderr)
            else:
                print(f"✓ Linked {ticket_key} to epic {epic}")

        print(f"✓ Created JIRA ticket: {ticket_key}")
        print(f"  URL: {config['server']}/browse/{ticket_key}")

        return ticket_key

    except Exception as e:
        print(f"❌ Error creating JIRA ticket: {e}", file=sys.stderr)
        return None


def update_jira_ticket(
    ticket_key: str,
    description: Optional[str] = None,
    summary: Optional[str] = None,
    priority: Optional[str] = None
) -> bool:
    """
    Update an existing JIRA ticket.

    Args:
        ticket_key: Ticket key (e.g., "RHAIENG-1841")
        description: New description in JIRA wiki markup (optional)
        summary: New summary (optional)
        priority: New priority (optional)

    Returns:
        True if successful, False otherwise
    """
    try:
        config = read_jira_config()
        token = get_jira_token()

        if not token:
            raise ValueError("JIRA API token not found")

        # Build update payload
        payload = {"fields": {}}

        if description:
            payload["fields"]["description"] = description

        if summary:
            payload["fields"]["summary"] = summary

        if priority:
            payload["fields"]["priority"] = {"name": priority}

        if not payload["fields"]:
            print("⚠️  No fields to update", file=sys.stderr)
            return False

        # Save payload to temp file
        payload_file = Path("/tmp/jira_update_payload.json")
        payload_file.write_text(json.dumps(payload, indent=2))

        # Use curl for update (jira-cli doesn't handle complex updates well)
        cmd = [
            'curl', '-X', 'PUT',
            '-H', f'Authorization: Bearer {token}',
            '-H', 'Content-Type: application/json',
            '--data', f'@{payload_file}',
            f'{config["server"]}/rest/api/2/issue/{ticket_key}'
        ]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode != 0:
            print(f"❌ Failed to update JIRA ticket: {result.stderr}", file=sys.stderr)
            return False

        print(f"✓ Updated JIRA ticket: {ticket_key}")
        return True

    except Exception as e:
        print(f"❌ Error updating JIRA ticket: {e}", file=sys.stderr)
        return False


def save_ticket_to_file(
    summary: str,
    description: str,
    filename: str = "jira_ticket_draft.txt"
) -> str:
    """
    Save ticket information to a file (fallback when JIRA creation fails).

    Args:
        summary: Ticket summary
        description: Ticket description in JIRA wiki markup
        filename: Output filename

    Returns:
        Path to created file
    """
    content = f"""JIRA Ticket Draft
=================

Summary: {summary}

Description:
{description}
"""

    filepath = Path.cwd() / filename
    filepath.write_text(content)

    print(f"✓ Ticket saved to: {filepath}")
    return str(filepath)


if __name__ == "__main__":
    # Test the configuration
    print("Testing JIRA configuration...")
    print()

    if verify_jira_config():
        print()
        print("✓ JIRA is properly configured and ready to use!")
        print()
        print("Example usage:")
        print('  from jira_helper import create_jira_ticket')
        print('  ticket_key = create_jira_ticket(')
        print('      summary="Fix security vulnerability",')
        print('      description="h2. Issue\\nDescription here...",')
        print('      epic="RHAIENG-1247",')
        print('      component="Llama Stack Core",')
        print('      priority="Critical"')
        print('  )')
    else:
        print()
        print("❌ JIRA configuration needs attention")
        print()
        print("Setup instructions:")
        print("1. Run: jira init")
        print("2. Add JIRA_API_TOKEN to ~/.zsh-custom/globals.zsh")
        print("3. Run this script again to verify")
