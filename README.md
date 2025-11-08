# rhuss' Personal Plugin Marketplace

This repository contains custom Claude Code plugins for security, development, and automation workflows.

## Available Plugins

### 🔒 threat-model-assessment

Turn security requirements into actionable code assessments. Provide a threat description and your code repositories, and the plugin analyzes your implementation to identify what's in place and what's missing.

**How it works:**
1. Paste a security requirement from your threat model
2. Specify your code repositories (local or Git URLs)
3. AI analyzes the code to assess current security controls
4. Receive detailed findings with file references and gap analysis
5. Optionally auto-generate JIRA tickets for remediation work

**Perfect for:**
- Architects validating security designs against actual implementation
- Developers ensuring security requirements are properly coded
- Security teams conducting compliance assessments
- Anyone who needs to verify code matches security requirements

[→ View Plugin Documentation](./threat-model-assessment/README.md)

## Installation

**Step 1:** Add this marketplace to Claude Code:

```
/plugin marketplace add rhuss/rhuss-claude-marketplace
```

**Step 2:** Install any plugin from the marketplace:

```
/plugin install <plugin-name>@rhuss-claude-marketplace
```

**Step 3:** Invoke the plugin using its slash command:

```
/<plugin-name>
```

**Example** (installing threat-model-assessment):
```
/plugin install threat-model-assessment@rhuss-claude-marketplace
/threat-model-assessment
```

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
