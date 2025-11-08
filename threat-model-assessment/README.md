# Threat Model Assessment Plugin

A Claude Code plugin for conducting systematic security threat model assessments following industry best practices and compliance frameworks (GDPR, OWASP, CIS Controls, NIST, etc.).

## Overview

This plugin automates the process of:
1. Analyzing codebases against security countermeasurement requirements
2. Documenting current implementation status
3. Identifying security gaps
4. Creating JIRA tickets for remediation work
5. Generating comprehensive assessment reports

## Input Requirements

The plugin is designed to work with any threat modeling framework or security compliance standard. Here's what you need to provide:

### Project Context (Initial Setup)
- **Project name**: Name of the product/system being assessed
- **Deployment model**: Self-hosted, SaaS, or hybrid deployment
- **Code repositories**: Local directory paths or Git repository URLs (comma/newline separated)
- **JIRA configuration** (optional): Epic key, component name, default priority

### Per Countermeasurement/Requirement
For each security requirement you want to assess:

1. **Requirement text** (required):
   - The full text of the countermeasurement or security requirement
   - Can be from any source: OWASP ASVS, CIS Controls, internal security policies, compliance frameworks, etc.
   - Should describe what security control needs to be implemented

2. **Reference URL** (optional but recommended):
   - Link back to the requirement in your assessment tool or documentation
   - Enables traceability and creates backlinks in JIRA tickets
   - Examples: SDElements URL, OWASP ASVS section link, internal wiki page

3. **Additional context links** (optional):
   - CWE (Common Weakness Enumeration) URLs: `http://cwe.mitre.org/data/definitions/XXX`
   - OWASP documentation references
   - Security best practices guides
   - RFC specifications
   - The plugin will automatically fetch and analyze these for threat context

### Example Input Format

```
Requirement: T755 - Maintain a Data Processing Register

Reference URL: https://your-assessment-tool.com/requirements/T755

Description: Under GDPR Article 30, organizations must maintain a record of processing
activities containing: (a) the purposes of processing, (b) categories of data subjects,
(c) categories of personal data, (d) retention periods, (e) technical and organizational
security measures.

Additional Context: https://gdpr-info.eu/art-30-gdpr/
```

## Features

✅ **Multi-Repository Support**: Analyze local directories and remote Git repositories
✅ **Iterative Assessment**: Process multiple countermeasurements in one session
✅ **JIRA Integration**: Auto-create tickets with proper formatting
✅ **GDPR Compliance**: Built-in templates for Article 30 data processing registers
✅ **Structured Documentation**: Generate markdown summaries with all findings
✅ **Progress Tracking**: TodoWrite integration for visibility

## Prerequisites

### Required
- Claude Code with plugin support
- Python 3.x
- Access to codebase(s) being assessed

### Required for JIRA Integration
- [jira-cli](https://github.com/ankitpokhrel/jira-cli) - **Required** if you want to create JIRA tickets
- JIRA API token
- JIRA project access

Install jira-cli:
```bash
brew install ankitpokhrel/jira-cli/jira-cli
jira init
```

## Installation

```bash
# Clone the marketplace
cd ~/Development
git clone https://github.com/rhuss/claude-code-dev-marketplace.git

# Install the plugin
mkdir -p ~/.claude/plugins
ln -s ~/Development/claude-code-dev-marketplace/threat-model-assessment \
      ~/.claude/plugins/threat-model-assessment
```

The plugin will be available as `/threat-model-assessment` after restarting Claude Code.

## Configure JIRA (Optional)

If you want automatic JIRA ticket creation:

```bash
# Install jira-cli
brew install ankitpokhrel/jira-cli/jira-cli

# Initialize jira-cli
jira init

# Add API token to your shell config
echo 'export JIRA_API_TOKEN="your-token-here"' >> ~/.zsh-custom/globals.zsh
source ~/.zsh-custom/globals.zsh

# Test configuration
python3 ~/.claude/plugins/threat-model-assessment/jira_helper.py
```

### 4. Restart Claude Code

The plugin will be available as a skill.

## Usage

### Basic Workflow

1. **Invoke the plugin** in Claude Code:
   ```
   I want to conduct a threat model assessment
   ```

2. **Answer setup questions**:
   - Project name and description
   - Deployment model (self-hosted, SaaS, hybrid)
   - Code locations (local paths or Git URLs)
   - JIRA integration preferences

3. **Provide countermeasurement requirements**:
   - Paste requirement text from your threat modeling framework (e.g., SDElements, OWASP ASVS, CIS Controls, compliance docs)
   - Optionally provide reference URL for traceability
   - Claude analyzes and identifies relevant aspects
   - You confirm which aspects to assess

4. **Review findings**:
   - Claude analyzes code and documents current state
   - Identifies gaps and recommends actions
   - Optionally creates JIRA tickets

5. **Repeat for additional countermeasurements**:
   - Say "done" when finished
   - Receive comprehensive summary document

### Example Session

```
User: "I want to conduct a threat model assessment for Llama Stack"

Claude: [Invokes threat-model-assessment plugin]

Claude: "What product/project are you assessing?"
User: "Llama Stack - AI gateway and standardization layer"

Claude: "What type of deployment model does this product use?"
User: "Self-hosted product (customers install and run)"

Claude: "What codebases should be analyzed?"
User: "/Users/rhuss/Development/ai/llama-stack, /Users/rhuss/Development/ai/llama-stack-kubernetes-operator"

Claude: "Should JIRA tickets be created for identified gaps?"
User: "Yes - create JIRA tickets"

Claude: "Epic to link tickets to?"
User: "RHAIENG-1247"

Claude: "Component name?"
User: "Llama Stack Core"

Claude: [Explores codebases, creates architecture summary]

Claude: "Ready for first countermeasurement requirement. Please paste the requirement:"
User: [Pastes T755: Maintain a Data Processing Register]

Claude: [Analyzes requirement, presents relevant aspects]

Claude: "Which aspects should I focus on?"
User: [Selects: conversation/chat history, inference logs, user profile data, access logs]

Claude: [Conducts codebase analysis, generates assessment]

Claude: "Assessment complete. Should I create a JIRA ticket?"
User: "Yes"

Claude: [Creates JIRA-1841 with concise task list]

Claude: "JIRA ticket created: RHAIENG-1841. Ready for next countermeasurement?"
User: [Pastes next requirement or says "done"]

... [Repeat for additional countermeasurements]

Claude: [Generates threat-model-assessment-summary.md]

Claude: "Assessment complete! Summary saved to threat-model-assessment-summary.md"
```

## Assessment Format

Each countermeasurement assessment follows this structure:

```markdown
**COUNTERMEASUREMENT ASSESSMENT: T755 - Conversation/Chat History**

**Status**: Partial

**Overview**:
Addresses the storage and processing of conversation data...

**Current Implementation**:
- ConversationServiceImpl (src/core/conversations.py:50-318):
  Stores conversations in SQL with AuthorizedSqlStore
- Tables: openai_conversations, conversation_items
- Access Control: Cedar-style ABAC policies integrated

**Gaps Identified**:
- No documented retention periods
- No automated data purging
- No data subject access tooling

**Out of Scope**:
- External LLM providers (OpenAI, Anthropic): Require separate DPAs

**Recommendation**:
Implement retention policies and DSAR APIs
```

## JIRA Ticket Format

Auto-generated JIRA tickets use this concise format:

```
h2. Background
Brief context about the security gap

h2. Current State
* (/) What's implemented
* (x) What's missing

h2. Tasks
- Task 1: Brief description
- Task 2: Brief description
- Task 3: Brief description

h2. Out of Scope
Customer responsibilities or external dependencies

h2. Estimated Effort
30 days
```

## Output Files

The plugin generates:

1. **threat-model-assessment-summary.md**: Comprehensive assessment report
   - Executive summary
   - Architecture overview
   - Detailed findings for each countermeasurement
   - Action items with JIRA links
   - Recommendations

2. **JIRA tickets**: One per countermeasurement with gaps (optional)

## Plugin Scripts

The plugin includes two Python scripts for JIRA integration:

### create_jira_issue.py

Main script for creating JIRA tickets with proper wiki markup formatting.

**Usage** (recommended - using temporary file to avoid shell escaping issues):
```bash
export JIRA_API_TOKEN="your-token"
cat > /tmp/jira_ticket.json <<'EOF'
{"summary": "...", "background": "...", ...}
EOF
cat /tmp/jira_ticket.json | python3 create_jira_issue.py
```

**Features**:
- Takes JSON input with structured assessment data
- Formats descriptions as JIRA wiki markup (h2., h3., *, {{code}})
- Validates required fields
- Links tickets to epics
- Prints ticket key on success

**Required Environment Variable**:
- `JIRA_API_TOKEN`: Personal Access Token from JIRA

If not set, the script prints instructions for creating a token at https://issues.redhat.com/secure/ViewProfile.jspa

**JSON Schema**:
```json
{
  "summary": "Ticket title (required)",
  "reference_url": "URL to assessment tool (optional)",
  "background": "Brief context (required)",
  "current_state": {
    "implemented": ["Item 1"],
    "missing": ["Item 2"]
  },
  "tasks": [
    {
      "title": "Task Group",
      "items": ["Task 1", "Task 2"]
    }
  ],
  "out_of_scope": ["External item"],
  "effort_days": 10,
  "epic": "EPIC-123",
  "component": "Component Name",
  "priority": "Critical"
}
```

### jira_helper.py

Low-level helper module for JIRA operations.

**Functions**:
- `create_jira_ticket()`: Create ticket via jira-cli
- `update_jira_ticket()`: Update ticket description
- `verify_jira_config()`: Check JIRA configuration
- `save_ticket_to_file()`: Save ticket data for offline review

Used internally by `create_jira_issue.py`. Can also be imported for custom scripts.

## Configuration

### JIRA Configuration Files

- **Token**: `~/.zsh-custom/globals.zsh` - Contains `JIRA_API_TOKEN`
- **Settings**: `~/.config/.jira/.config.yml` - jira-cli configuration

### Supported Code Locations

- **Local directories**: Absolute paths (e.g., `/Users/rhuss/Development/ai/project`)
- **Git repositories**: HTTPS URLs (e.g., `https://github.com/org/repo.git`)
- **Multiple repositories**: Comma or newline separated

## Customization

### Adding Custom Templates

Edit `threat-model-assessment.md` to add custom assessment templates:

```markdown
### Custom Assessment Type

For [specific compliance framework]:
- [Custom field 1]
- [Custom field 2]
...
```

### Modifying JIRA Format

The plugin uses `create_jira_issue.py` to create JIRA tickets with consistent wiki markup formatting. To customize:

1. **Modify formatting**: Edit `create_jira_issue.py` `format_jira_description()` function
2. **Add custom fields**: Edit `create_jira_issue.py` JSON schema and `create_jira_ticket()` call
3. **Change ticket defaults**: Edit `jira_helper.py` `create_jira_ticket()` function

Example: Adding labels to all tickets:

```python
# In jira_helper.py
def create_jira_ticket(summary, description, **kwargs):
    # Add default labels
    labels = kwargs.get('labels', [])
    labels.append('security')
    labels.append('threat-model')
    # ... rest of function
```

## Troubleshooting

### JIRA Connection Issues

```bash
# Verify configuration
python3 ~/.claude/plugins/threat-model-assessment/jira_helper.py

# Test jira-cli directly
jira me

# Check token
echo $JIRA_API_TOKEN
```

### Plugin Not Found

```bash
# Verify symlink
ls -la ~/.claude/plugins/threat-model-assessment

# Re-create if needed
ln -sf ~/Development/claude-code-dev-marketplace/threat-model-assessment \
       ~/.claude/plugins/threat-model-assessment
```

### Permission Errors

```bash
# Make helper script executable
chmod +x ~/.claude/plugins/threat-model-assessment/jira_helper.py
```

## Best Practices

### For Effective Assessments

1. **Prepare Requirements**: Have countermeasurement requirements ready to paste
2. **Know Your Scope**: Understand deployment model and system boundaries
3. **Review Findings**: Always review before approving JIRA creation
4. **Iterate**: Process related countermeasurements together
5. **Document Decisions**: Note why things are out of scope

### For JIRA Integration

1. **Test First**: Run jira_helper.py test before starting
2. **Use Epics**: Group related security work under epics
3. **Consistent Components**: Use same component for related tickets
4. **Set Priorities**: Be realistic with priorities (not everything is Critical)

## Examples

See the [examples](./examples/) directory for:
- Sample countermeasurement requirements
- Example assessment outputs
- JIRA ticket templates

## Contributing

Found a bug or have a suggestion? Open an issue or PR in the marketplace repository.

## License

MIT License

## Author

Roland Huß (@rhuss)

## Related Plugins

- **code-reviewer**: Review code against standards (from superpowers marketplace)
- **systematic-debugging**: Debug with structured approach (from superpowers marketplace)

## Resources

- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [CIS Controls](https://www.cisecurity.org/controls)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [GDPR Article 30](https://gdpr-info.eu/art-30-gdpr/)
- [SDElements](https://www.securitycompass.com/sdelements/) (example assessment tool)
- [Claude Code Plugin Guide](https://docs.claude.com/claude-code/plugins)
