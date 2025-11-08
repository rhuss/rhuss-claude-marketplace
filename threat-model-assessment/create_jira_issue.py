#!/usr/bin/env python3
"""
Create JIRA ticket for threat model assessment countermeasurement.

This script takes structured assessment data as JSON and creates a JIRA ticket
with proper wiki markup formatting.

Environment Variables:
    JIRA_API_TOKEN: Required. JIRA API token for authentication.

Usage:
    echo '{"summary": "...", "background": "...", ...}' | python3 create_jira_issue.py

JSON Input Schema:
    {
        "summary": "Brief title (required)",
        "reference_url": "URL to countermeasurement in assessment tool (optional)",
        "background": "Brief context about the gap (required)",
        "current_state": {
            "implemented": ["Item 1", "Item 2"],
            "missing": ["Item 3", "Item 4"]
        },
        "tasks": [
            {
                "title": "Task group title",
                "items": ["Task 1", "Task 2"]
            }
        ],
        "out_of_scope": ["Item 1", "Item 2"],
        "effort_days": 10,
        "epic": "EPIC-123",
        "component": "Component Name",
        "priority": "Blocker|Critical|Major|Normal|Minor"
    }

Output:
    Prints JIRA ticket key (e.g., "RHAIENG-1234") on success.
    Exits with code 1 on failure.
"""

import json
import os
import sys
from typing import Dict, List, Optional, Any

# Add current directory to path to import jira_helper
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jira_helper import create_jira_ticket, update_jira_ticket


def check_jira_token() -> Optional[str]:
    """Check if JIRA_API_TOKEN is set in environment."""
    token = os.environ.get('JIRA_API_TOKEN')
    if not token:
        print("ERROR: JIRA_API_TOKEN environment variable not set", file=sys.stderr)
        print("", file=sys.stderr)
        print("To create a JIRA API token:", file=sys.stderr)
        print("1. Go to https://issues.redhat.com/secure/ViewProfile.jspa", file=sys.stderr)
        print("2. Click 'Personal Access Tokens' in the left sidebar", file=sys.stderr)
        print("3. Click 'Create token'", file=sys.stderr)
        print("4. Give it a name (e.g., 'threat-model-assessment')", file=sys.stderr)
        print("5. Set expiration (recommended: 90 days)", file=sys.stderr)
        print("6. Copy the token and set it in your shell:", file=sys.stderr)
        print("", file=sys.stderr)
        print("   export JIRA_API_TOKEN='your-token-here'", file=sys.stderr)
        print("", file=sys.stderr)
        print("For persistent setup, add to ~/.zsh-custom/globals.zsh:", file=sys.stderr)
        print("   echo 'export JIRA_API_TOKEN=\"your-token-here\"' >> ~/.zsh-custom/globals.zsh", file=sys.stderr)
        print("   source ~/.zsh-custom/globals.zsh", file=sys.stderr)
        return None
    return token


def format_jira_description(data: Dict[str, Any]) -> str:
    """
    Format assessment data as JIRA wiki markup.

    Args:
        data: Dictionary with assessment data

    Returns:
        Formatted JIRA description in wiki markup
    """
    parts = []

    # Reference section (optional)
    if data.get('reference_url'):
        parts.append(f"h2. Reference")
        parts.append(f"Source: {data['reference_url']}")
        parts.append("")

    # Background section
    parts.append("h2. Background")
    parts.append(data['background'])
    parts.append("")

    # Current State section
    parts.append("h2. Current State")
    current = data.get('current_state', {})
    for item in current.get('implemented', []):
        parts.append(f"* (/) {item}")
    for item in current.get('missing', []):
        parts.append(f"* (x) {item}")
    parts.append("")

    # Tasks section
    parts.append("h2. Tasks")
    parts.append("")

    for i, task_group in enumerate(data.get('tasks', []), start=1):
        parts.append(f"h3. {i}. {task_group['title']}")
        for item in task_group['items']:
            parts.append(f"* {item}")
        parts.append("")

    # Out of Scope section
    if data.get('out_of_scope'):
        parts.append("h2. Out of Scope")
        for item in data['out_of_scope']:
            parts.append(f"* {item}")
        parts.append("")

    # Estimated Effort section
    parts.append("h2. Estimated Effort")
    parts.append(f"{data['effort_days']} days")

    return '\n'.join(parts)


def validate_input(data: Dict[str, Any]) -> List[str]:
    """
    Validate required fields in input data.

    Returns:
        List of error messages (empty if valid)
    """
    errors = []

    if not data.get('summary'):
        errors.append("Missing required field: summary")

    if not data.get('background'):
        errors.append("Missing required field: background")

    if 'current_state' not in data:
        errors.append("Missing required field: current_state")
    elif not isinstance(data['current_state'], dict):
        errors.append("current_state must be a dictionary")

    if 'tasks' not in data:
        errors.append("Missing required field: tasks")
    elif not isinstance(data['tasks'], list) or len(data['tasks']) == 0:
        errors.append("tasks must be a non-empty list")

    if 'effort_days' not in data:
        errors.append("Missing required field: effort_days")
    elif not isinstance(data['effort_days'], (int, float)):
        errors.append("effort_days must be a number")

    return errors


def main():
    """Main entry point."""
    # Check for JIRA token
    if not check_jira_token():
        sys.exit(1)

    # Read JSON from stdin
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate input
    errors = validate_input(data)
    if errors:
        print("ERROR: Invalid input data:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    # Format description as wiki markup
    description = format_jira_description(data)

    # Create JIRA ticket
    ticket_key = create_jira_ticket(
        summary=data['summary'],
        description=description,
        epic=data.get('epic'),
        component=data.get('component'),
        priority=data.get('priority', 'Critical'),
        issue_type='Story'
    )

    if not ticket_key:
        print("ERROR: Failed to create JIRA ticket", file=sys.stderr)
        sys.exit(1)

    # Update description to ensure wiki markup is preserved
    # (jira-cli sometimes auto-converts on create)
    if not update_jira_ticket(ticket_key, description):
        print(f"WARNING: Created {ticket_key} but failed to update description", file=sys.stderr)
        print(ticket_key)
        sys.exit(0)

    print(ticket_key)
    sys.exit(0)


if __name__ == '__main__':
    main()
