# Claude Code Personal Plugin Marketplace

This repository contains custom Claude Code plugins for security, development, and automation workflows.

## Available Plugins

### 🔒 threat-model-assessment

Conduct systematic security threat model assessments for software projects.

**Features:**
- Analyze code against security countermeasurement requirements
- Generate GDPR/compliance documentation
- Create JIRA tickets for identified security gaps
- Support multiple repositories (local and remote)
- Generate comprehensive markdown assessment summaries

**Use Cases:**
- GDPR Article 30 compliance (data processing registers)
- SDElements threat model requirements
- Security architecture reviews
- Compliance documentation

[→ View Plugin Documentation](./threat-model-assessment/README.md)

## Installation

### Option 1: Local Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/rhuss/claude-code-dev-marketplace.git
   cd claude-code-dev-marketplace
   ```

2. Link plugins to Claude Code:
   ```bash
   # Create Claude Code plugins directory if it doesn't exist
   mkdir -p ~/.claude/plugins

   # Symlink the plugin
   ln -s "$(pwd)/threat-model-assessment" ~/.claude/plugins/threat-model-assessment
   ```

3. Restart Claude Code

### Option 2: Direct Use

You can also use plugins directly by referencing their skill files:

```bash
# In Claude Code
/skill /path/to/claude-code-dev-marketplace/threat-model-assessment/threat-model-assessment.md
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
