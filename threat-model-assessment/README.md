# Threat Model Assessment Plugin

A Claude Code plugin for conducting systematic security threat model assessments following industry best practices (SDElements, GDPR compliance, OWASP, etc.).

## Overview

This plugin automates the process of:
1. Analyzing codebases against security countermeasurement requirements
2. Documenting current implementation status
3. Identifying security gaps
4. Creating JIRA tickets for remediation work
5. Generating comprehensive assessment reports

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
- Access to codebase(s) being assessed

### Optional (for JIRA integration)
- [jira-cli](https://github.com/ankitpokhrel/jira-cli) installed
- JIRA API token configured
- JIRA project access

## Installation

### 1. Clone the Marketplace Repository

```bash
cd ~/Development
git clone https://github.com/rhuss/claude-code-dev-marketplace.git
```

### 2. Install the Plugin

```bash
# Create Claude Code plugins directory
mkdir -p ~/.claude/plugins

# Symlink the plugin
ln -s ~/Development/claude-code-dev-marketplace/threat-model-assessment \
      ~/.claude/plugins/threat-model-assessment
```

### 3. Configure JIRA (Optional)

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
   - Paste requirement text from SDElements, compliance docs, etc.
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
User: "I want to assess Llama Stack for GDPR compliance"

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

Edit `jira_helper.py` to customize ticket creation:

```python
def create_jira_ticket(summary, description, **kwargs):
    # Add custom fields
    # Modify default priority
    # Add labels, etc.
    ...
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

- [SDElements Documentation](https://www.securitycompass.com/sdelements/)
- [GDPR Article 30](https://gdpr-info.eu/art-30-gdpr/)
- [OWASP Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- [Claude Code Plugin Guide](https://docs.claude.com/claude-code/plugins)
