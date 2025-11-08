# Claude Code Personal Plugin Marketplace

This repository contains custom Claude Code plugins for security, development, and automation workflows.

## Available Plugins

### 🔒 threat-model-assessment

Automate security assessments with AI-powered code analysis against any threat modeling framework or compliance standard.

**Features:**
- Framework-agnostic: Works with OWASP ASVS, CIS Controls, NIST, GDPR, internal policies, or any security framework
- AI-powered codebase analysis with file-level precision
- Iterative assessment of multiple requirements in a single session
- Automated gap analysis and remediation recommendations
- Optional JIRA integration for ticket creation
- Comprehensive markdown assessment reports

**Use Cases:**
- OWASP ASVS security assessments
- CIS Controls compliance verification
- NIST framework implementation reviews
- GDPR Article 30 data processing registers
- Internal security policy audits
- Security architecture reviews

[→ View Plugin Documentation](./threat-model-assessment/README.md)

## Installation

Add the marketplace and install plugins:

```
/plugin marketplace add rhuss/claude-code-dev-marketplace
/plugin install threat-model-assessment@claude-code-dev-marketplace
```

Then invoke the plugin:

```
/threat-model-assessment
```

## Plugin Development

### Creating a New Plugin

1. Create a new directory under the repository root:
   ```bash
   mkdir my-new-plugin
   ```

2. Create the skill file:
   ```bash
   touch my-new-plugin/my-new-plugin.md
   ```

3. Follow the plugin structure:
   ```markdown
   ---
   name: my-new-plugin
   description: Brief description of what the plugin does
   ---

   # Plugin Title

   [Documentation and instructions]

   <INSTRUCTIONS>
   [Detailed workflow for Claude to follow]
   </INSTRUCTIONS>
   ```

4. Add any helper scripts (Python, shell, etc.) in the same directory

5. Create a README.md documenting usage and examples

### Plugin Guidelines

- Use clear, structured instructions for Claude
- Break complex workflows into phases and steps
- Use TodoWrite for progress tracking
- Use AskUserQuestion for user interaction
- Provide error handling guidance
- Include examples and use cases

## Contributing

This is a personal plugin marketplace, but suggestions and improvements are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see individual plugin directories for specific licensing.

## Author

Roland Huß (@rhuss)

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [Plugin Development Guide](https://docs.claude.com/claude-code/plugins)
- [Skill Framework Reference](https://docs.claude.com/claude-code/skills)
