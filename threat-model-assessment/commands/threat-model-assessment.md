---
name: threat-model-assessment
description: Conduct security threat model assessments for software projects by analyzing code against countermeasurement requirements and generating GDPR/compliance documentation with optional JIRA integration
---

# Threat Model Assessment Plugin

This plugin helps conduct systematic security threat model assessments following industry best practices and compliance frameworks (GDPR, OWASP, CIS, NIST, etc.).

## How to Use This Plugin

Invoke this plugin when you need to:
- Conduct a threat model assessment for a software product
- Analyze code against security countermeasurement requirements
- Generate compliance documentation (GDPR Article 30, etc.)
- Create JIRA tickets for identified security gaps
- Document data processing activities and security controls

## Workflow

This plugin follows a structured assessment workflow:

1. **Setup**: Collect information about the assessment context
2. **Repository Exploration**: Analyze target codebases
3. **Iterative Assessment**: For each countermeasurement requirement:
   - Extract relevant requirements
   - Analyze codebase for threats
   - Create assessment documentation
   - Optionally create JIRA tickets
4. **Summary Generation**: Create comprehensive markdown summary

## Before You Begin

Ensure you have:
- Access to the codebase(s) being assessed
- (Optional) JIRA credentials configured if creating tickets
- (Optional) Threat model requirements from your assessment framework (e.g., SDElements, OWASP ASVS, CIS Controls)

## Plugin Execution

<INSTRUCTIONS>

## Phase 1: Setup and Information Gathering

### Step 1: Collect Assessment Context

Ask the user the following questions using AskUserQuestion tool:

1. **Project Information**:
   - Question: "What product/project are you assessing?"
   - Header: "Project Name"
   - Capture project name and brief description

2. **Assessment Scope**:
   - Question: "What type of deployment model does this product use?"
   - Header: "Deployment"
   - Options:
     * "Self-hosted product (customers install and run)"
     * "SaaS/Hosted service (we run on behalf of customers)"
     * "Hybrid (both deployment options)"
   - Note: This affects which countermeasures are applicable

3. **Code Locations**:
   - Question: "What codebases should be analyzed?"
   - Header: "Repositories"
   - Free text input to collect:
     * Local directories (absolute paths)
     * Git repository URLs
     * Multiple entries allowed (comma or newline separated)
   - Parse and validate all provided locations

4. **JIRA Integration**:
   - Question: "Should JIRA tickets be created for identified gaps?"
   - Header: "JIRA"
   - Options:
     * "Yes - create JIRA tickets"
     * "No - documentation only"
   - If yes, ask follow-up:
     * "Epic to link tickets to?" (optional, provide epic key like RHAIENG-1247)
     * "Component name?" (e.g., "Llama Stack Core")
     * "Default priority?" (Blocker, Critical, Major, Normal, Minor)

### Step 2: Verify JIRA Configuration (if needed)

If user wants JIRA integration:
- Check for JIRA credentials in `~/.zsh-custom/globals.zsh` or environment variables
- Look for: `JIRA_API_TOKEN`, `JIRA_AUTH_TYPE`
- Check jira-cli config at `~/.config/.jira/.config.yml`
- If not found, guide user to set up credentials
- Test connection with a simple query

### Step 3: Explore Codebases

For each provided code location:
- If local directory: verify it exists and is readable
- If git URL: clone to temporary location
- Use Task tool with subagent_type=Explore to understand:
  * Overall architecture
  * Key components
  * Security-relevant functionality
  * Data handling patterns
  * Entry points and API surfaces

Create initial architecture summary (2-3 paragraphs) documenting:
- What the system does
- Key security-relevant components
- Data flow patterns
- External dependencies

Store this summary for use in assessments.

### Step 4: Initialize Tracking

Create TodoWrite list for tracking:
- Setup phase (mark as completed)
- Countermeasurement assessments (will add dynamically)
- Summary generation (pending)

Initialize assessment data structure:
```python
assessment_data = {
    "project": "<project_name>",
    "deployment_model": "<deployment_type>",
    "repositories": ["<repo1>", "<repo2>"],
    "jira_enabled": True/False,
    "jira_config": {
        "epic": "<epic_key>",
        "component": "<component_name>",
        "priority": "<priority>"
    },
    "countermeasurements": []
}
```

## Phase 2: Iterative Countermeasurement Assessment

### Step 5: Countermeasurement Loop

For each countermeasurement requirement (iterate until user says done):

#### 5.1 Get Countermeasurement Requirement

Ask user: "Please paste the next countermeasurement requirement (or say 'done' to finish)"

If user provides requirement:
- Parse the requirement title/ID (e.g., "T755: Maintain a Data Processing Register")
- Extract the full requirement text
- **Ask for reference URL**: "Please provide the reference URL for this countermeasurement (for traceability)"
  - Store URL in assessment data for linking back to source
  - This will be added to JIRA tickets as a backlink
  - Optional: If user doesn't have URL, proceed without it

If user says "done":
- Skip to Phase 3: Summary Generation

**Read External Links for Context**:
If the countermeasurement description contains external links (e.g., CWE references, documentation):
- Use WebFetch to read each external link
- Extract relevant threat background, attack vectors, and security implications
- Use this context to inform the applicability check and assessment
- Note: Focus on understanding the threat, not implementing solutions

Example external links commonly found:
- CWE (Common Weakness Enumeration) URLs: http://cwe.mitre.org/data/definitions/XXX
- OWASP documentation
- Security best practices guides
- RFC specifications

#### 5.2 Check Applicability (NEW)

**IMPORTANT**: Before spending time on detailed analysis, determine if the countermeasurement is actually applicable to the product.

Perform quick applicability check:
- Read the countermeasurement weakness description
- Identify the underlying technology or pattern it addresses (e.g., "session-based authentication", "SQL databases", "file uploads")
- Search codebase for evidence of that technology/pattern (use Grep with relevant keywords)
- Analyze findings to determine if the product uses the vulnerable technology

Make applicability decision:
- **Applicable**: Product uses the technology/pattern, proceed with full assessment
- **Not Applicable**: Product doesn't use the technology/pattern, document why and skip to next countermeasurement

If **Not Applicable**:
1. Create assessment with "Not Applicable" status
2. Write concise rationale (keep under 1024 characters for compatibility with most assessment tools) explaining:
   - What technology/pattern the countermeasurement addresses
   - Why the product doesn't use that technology/pattern
   - What alternative approach the product uses (if any)
   - Key code references supporting the conclusion
3. Store assessment in assessment_data
4. **Add comment to epic** documenting the "Not Applicable" decision (see instructions below)
5. No JIRA ticket needed
6. Ask for next countermeasurement (skip to step 5.8)

**Guidelines for Not Applicable Rationale**:
- Maximum 1024 characters (common limit for assessment tools)
- Be concise but complete
- Include specific code references (file:line) in analysis paragraphs
- Use numbered lists for clarity
- **Conclusion section**: One line per paragraph, NO code references (suitable for copying to assessment tools)

**Structure**:
1. Opening paragraph: What the countermeasure addresses
2. Analysis paragraph(s): Why it doesn't apply, with code references
3. **Conclusion**: Clean summary suitable for assessment tool (no code refs, one line per paragraph)

**Example Not Applicable Assessment**:
```
**COUNTERMEASUREMENT: T20 - Generate unique session IDs**

**Status**: Not Applicable

This countermeasure addresses session fixation in session-based authentication systems.

Llama Stack (LLS) does not use server-side session management. Analysis of auth.py:89-150 confirms: (1) No session creation, storage, or management; (2) Each request independently authenticated via token validation; (3) No session IDs generated or stored in cookies; (4) User attributes extracted per-request and discarded after. LLS implements stateless authentication using Bearer tokens (JWT, OAuth2/OIDC, GitHub tokens, Kubernetes service account tokens).

**Conclusion (for assessment tool):**
LLS uses stateless token-based authentication, not session-based authentication.
Session fixation countermeasures are not applicable to this architecture.

[Character count: ~672]
```

**Adding "Not Applicable" Comment to Epic**:

When a countermeasurement is determined to be "Not Applicable", add a comment to the epic documenting the decision using the jira_helper.py script:

```python
export JIRA_API_TOKEN="..." && cd ~/Development/ai/rhuss-claude-marketplace/threat-model-assessment && python3 -c "
import sys
from jira_helper import add_comment_to_issue

comment = '''h3. {REQUIREMENT_ID}: {REQUIREMENT_TITLE} - Not Applicable

*Status:* Not Applicable
*Reference:* {reference_url}

*Rationale:*
{Brief explanation paragraph}

{Bulleted analysis with code references}

*Conclusion:* {One-liner summary suitable for assessment tool}'''

if add_comment_to_issue('{epic_key}', comment):
    print('✓ Successfully added {REQUIREMENT_ID} Not Applicable comment to epic')
    sys.exit(0)
else:
    print('ERROR: Failed to add comment to epic', file=sys.stderr)
    sys.exit(1)
"
```

**Comment Format Guidelines**:
- Use `h3.` for the heading with countermeasurement ID and title
- Include reference URL for traceability
- Keep rationale concise and focused
- Use bullet points for analysis with code references
- End with clean conclusion suitable for pasting into assessment tool

#### 5.3 Extract Relevant Parts (if Applicable)

**Only proceed if countermeasurement is Applicable**

Analyze the requirement and determine:
- Which parts are relevant to the deployment model (self-hosted vs SaaS)
- Which parts apply to the product itself vs customer responsibilities
- Gray areas that need clarification

Present analysis to user: "Here's what I found relevant for your <deployment_model> product..."

Ask user: "Which of these aspects should I focus the assessment on?"
- Provide checkboxes for each identified area
- Allow user to select multiple

#### 5.4 Conduct Codebase Analysis

For each selected focus area:
- Use Grep and Read tools to search for relevant code
- Look for:
  * Data storage mechanisms
  * Logging and audit trails
  * User data handling
  * Configuration options
  * Security controls
- Document findings with file paths and line numbers

Add to TodoWrite:
- "Analyzing <requirement_id>: <focus_area_1>"
- "Analyzing <requirement_id>: <focus_area_2>"
- etc.

Mark each as in_progress, then completed as you work through them.

#### 5.5 Create Assessment Documentation

For each focus area, generate assessment using this format:

```
**COUNTERMEASUREMENT ASSESSMENT: [Requirement ID] - [Focus Area]**

**Status**: [Complete | Partial | Not Implemented | Not Applicable]

**Overview**:
[1-2 sentences describing what this countermeasurement addresses]

**Current Implementation**:
[Detailed analysis of what's currently implemented, with code references]
- Component 1: [description with file:line references]
- Component 2: [description with file:line references]

**Gaps Identified**:
[If status is not "Complete", list specific gaps]
- Gap 1: [description]
- Gap 2: [description]

**Out of Scope**:
[External services/dependencies that require separate threat modeling]
- [External service 1]: [why it's out of scope]

**Recommendation**:
[Final assessment and any actions needed]
```

Store this assessment in assessment_data["countermeasurements"].

#### 5.6 Determine Completion Status

Analyze the overall status:
- If all focus areas are "Complete": countermeasurement is complete
- If any are "Partial" or "Not Implemented": identify action items

If action items exist:
- List specific, actionable tasks needed to achieve "Complete" status
- Ask user: "Should I create a JIRA ticket for these action items?"
- If yes (and JIRA is enabled), proceed to create ticket

#### 5.7 Create JIRA Ticket (if requested)

If user wants JIRA ticket:

1. Generate concise JIRA description in wiki markup:
```
h2. Reference
[Include reference URL if provided, e.g., "Source: https://sdelements.com/bunits/..."]

h2. Background
[Brief context about the gap]

h2. Current State
* (/) [What's implemented]
* (x) [What's missing]

h2. Tasks
[Concise list of action items, no implementation details]

h2. Out of Scope
[Customer responsibilities or external dependencies]

h2. Estimated Effort
[Single number in days]
```

**Note**: If user provided reference URL, include it at the top for traceability back to the requirement source.

2. Create ticket using create_jira_issue.py script:

**IMPORTANT**: Use the create_jira_issue.py script from the plugin directory. This script:
- Requires JIRA_API_TOKEN environment variable
- Formats descriptions with proper JIRA wiki markup (h2., h3., *, {{code}})
- Creates tickets via jira-cli
- Links tickets to epics
- Returns ticket key on success

First, ensure JIRA_API_TOKEN is set:
```bash
export JIRA_API_TOKEN="your-jira-api-token-here"
```

**IMPORTANT**: Always use a temporary file for JSON data to avoid shell escaping issues:

```bash
cd ~/Development/ai/rhuss-claude-marketplace/threat-model-assessment && cat > /tmp/jira_ticket.json <<'JSONEOF'
{
  "summary": "[Brief Title] ([Requirement ID])",
  "reference_url": "[reference_url_if_provided]",
  "background": "[Brief context about the gap]",
  "current_state": {
    "implemented": [
      "[What is implemented]",
      "[Another implemented item]"
    ],
    "missing": [
      "[What is missing]",
      "[Another missing item]"
    ]
  },
  "tasks": [
    {
      "title": "[Task Group 1 Title]",
      "items": [
        "[Task 1 description]",
        "[Task 2 description]"
      ]
    },
    {
      "title": "[Task Group 2 Title]",
      "items": [
        "[Task 3 description]"
      ]
    }
  ],
  "out_of_scope": [
    "[Customer responsibility or external dependency]",
    "[Another out of scope item]"
  ],
  "effort_days": 10,
  "epic": "[epic_key]",
  "component": "[component_name]",
  "priority": "[Blocker|Critical|Major|Normal|Minor]"
}
JSONEOF
cat /tmp/jira_ticket.json | python3 create_jira_issue.py
```

**Why use a temporary file?**
- Avoids shell escaping issues with special characters (quotes, parentheses, backslashes)
- Ensures JSON is passed exactly as written without interpretation
- More reliable for complex descriptions with varied punctuation
- Easier to debug if ticket creation fails

**If JIRA_API_TOKEN is not set**, the script will print instructions for creating a Personal Access Token:
1. Go to https://issues.redhat.com/secure/ViewProfile.jspa
2. Click 'Personal Access Tokens'
3. Create token with 90-day expiration
4. Set in environment: `export JIRA_API_TOKEN='your-token'`
5. For persistence, add to ~/.zsh-custom/globals.zsh

**Script output**: Prints ticket key (e.g., "RHAIENG-1234") on success, exits with code 1 on failure.

**JSON Field Reference**:
- `summary`: Ticket title (required)
- `reference_url`: URL to countermeasurement in assessment tool (optional, omit field if not available)
- `background`: Brief context about security gap (required)
- `current_state.implemented`: List of what's already implemented (required)
- `current_state.missing`: List of what's missing (required)
- `tasks`: List of task groups, each with title and items (required)
- `out_of_scope`: List of external items not in product scope (optional, can be empty list)
- `effort_days`: Estimated effort in days (required, number)
- `epic`: Epic key to link to (optional, omit if not linking)
- `component`: Component name (optional)
- `priority`: Blocker/Critical/Major/Normal/Minor (optional, defaults to Critical)

3. Store ticket key in assessment data

4. Update TodoWrite to mark JIRA creation as complete

#### 5.8 Ask for Next Countermeasurement

Ask user: "Assessment complete for [Requirement ID]. Ready for the next countermeasurement? (paste requirement or say 'done')"

Loop back to 5.1 until user says done.

## Phase 3: Summary Generation

### Step 6: Generate Comprehensive Summary

Create a markdown document: `threat-model-assessment-summary.md`

Structure:
```markdown
# Threat Model Assessment Summary

**Project**: [Project Name]
**Date**: [Current Date]
**Deployment Model**: [Self-hosted/SaaS/Hybrid]
**Repositories Assessed**:
- [Repo 1]
- [Repo 2]

## Executive Summary

[2-3 paragraph overview of assessment]
- Number of countermeasurements assessed
- Overall security posture (complete/partial/gaps)
- Critical findings requiring immediate attention
- JIRA tickets created (with links)

## Architecture Overview

[The architecture summary from Phase 1, Step 3]

## Countermeasurement Assessments

[For each countermeasurement, include the full assessment documentation from 5.4]

### [Requirement ID]: [Title]

**Status**: [Overall Status]

**JIRA Ticket**: [Link if created]

[Full assessment text for each focus area]

---

## Summary of Findings

### Completed Countermeasures
- [List of requirements with "Complete" status]

### Partial Implementation
- [List of requirements with "Partial" status, with brief gap summary]

### Not Implemented
- [List of requirements with "Not Implemented" status]

### Not Applicable
- [List of requirements with "Not Applicable" status, with rationale]

## Action Items

[Consolidated list of all action items across all assessments]

### Critical Priority
- [JIRA-XXXX] [Task description]

### High Priority
- [JIRA-XXXX] [Task description]

### Medium Priority
- [JIRA-XXXX] [Task description]

## External Dependencies (Out of Scope)

[List of external services/providers that require separate threat modeling]
- [Service 1]: [Why out of scope, what customer needs to do]
- [Service 2]: [Why out of scope, what customer needs to do]

## Recommendations

[Strategic recommendations for improving security posture]

## Appendix: Assessment Methodology

**Framework**: [Threat modeling framework used, e.g., STRIDE, PASTA, OWASP ASVS, CIS Controls, etc.]
**Focus**: [GDPR compliance, Data protection, etc.]
**Code Analysis Tools**: Claude Code, Grep, AST analysis
**Documentation Standards**: [Standards followed]
```

Save this file to the current working directory.

### Step 6.5: Add Summary to Epic (Optional)

Ask user: "Would you like to add the threat model assessment summary as a comment to the epic?"

If user says yes:

1. **Generate JIRA Wiki Markup Version of Summary**:

Convert the markdown summary to JIRA wiki markup format:
- Headers: Use h1., h2., h3. instead of #, ##, ###
- Bold: Use *text* instead of **text**
- Lists: Use * item (same as markdown)
- Links: Use [text|url] instead of [text](url)
- Code: Use {{code}} instead of `code`
- Inline code: Use {{code}} instead of `code`

Structure the JIRA comment:
```
h1. Threat Model Assessment Summary

*Project:* [Project Name]
*Date:* [Current Date]
*Deployment Model:* [Self-hosted/SaaS/Hybrid]

h2. Executive Summary

Conducted threat model assessment for [Project] using [Framework] security requirements. Assessed [N] countermeasurements:

* *Not Applicable:* [N] countermeasurements ([list])
* *Gaps Identified:* [N] countermeasurements requiring remediation
* *JIRA Tickets Created:* [N] tickets ([list with links])
* *Total Estimated Effort:* [N] days

h3. Critical Findings

# [JIRA-XXXX] (Priority): [Brief description]
# [JIRA-YYYY] (Priority): [Brief description]

h2. Countermeasurements Assessed

h3. [Requirement ID]: [Title] ([JIRA-XXXX])

*Status:* [Status] | *Priority:* [Priority] | *Effort:* [N] days

*Implemented:* [Bulleted list of what's implemented]

*Missing:* [Bulleted list of gaps]

[Repeat for each countermeasurement]

h2. Action Items by Priority

h3. Critical Priority

* [JIRA-XXXX|https://issues.redhat.com/browse/JIRA-XXXX] - [Description] ([N] days)

h3. Major Priority

* [JIRA-YYYY|https://issues.redhat.com/browse/JIRA-YYYY] - [Description] ([N] days)

[Continue for all priorities]

h2. External Dependencies (Out of Scope)

* [Dependency 1]
* [Dependency 2]

h2. Recommendations

h3. Immediate (Next Sprint)

* [Recommendation 1]
* [Recommendation 2]

h3. Medium-term (Next Quarter)

* [Recommendation 3]

h3. Strategic

* [Recommendation 4]
```

2. **Add Comment to Epic**:

Use the jira_helper.py add_comment_to_issue function:

```python
export JIRA_API_TOKEN="..." && cd ~/Development/ai/rhuss-claude-marketplace/threat-model-assessment && python3 <<'PYEOF'
import sys
sys.path.insert(0, '.')
from jira_helper import add_comment_to_issue

comment = '''[JIRA wiki markup summary here]'''

if add_comment_to_issue('[epic_key]', comment):
    print('✓ Successfully added threat model assessment summary to epic [epic_key]')
    sys.exit(0)
else:
    print('ERROR: Failed to add comment to epic', file=sys.stderr)
    sys.exit(1)
PYEOF
```

3. **Confirm Success**:

Inform user: "✓ Threat model assessment summary added to epic [epic_key]"

If user says no:
- Skip to Step 7

### Step 7: Final TodoWrite Update

Mark summary generation as complete.

Display final todo list to user showing all completed work.

## Important Guidelines

### Assessment Quality Standards

1. **Be Specific**: Always include file paths and line numbers in assessments
2. **Be Objective**: Report what exists, not what should exist
3. **Be Clear**: Distinguish between product responsibility and customer responsibility
4. **Be Actionable**: Gap descriptions must be specific enough to implement

### JIRA Ticket Standards

1. **Concise**: No implementation details, just tasks
2. **Actionable**: Each task is clear and achievable
3. **Formatted**: Always use JIRA wiki markup (h2., h3., *, #, {code}, {{monospace}})
4. **Estimated**: Single effort number in days

### Code Analysis Best Practices

1. **Use Task tool**: For exploratory searches, use subagent_type=Explore
2. **Use Grep**: For specific pattern matching
3. **Use Read**: For detailed file examination
4. **Context Aware**: Reference the architecture summary in your analysis
5. **Track Progress**: Update TodoWrite as you complete each analysis

### User Interaction

1. **Ask Questions**: Use AskUserQuestion for structured choices
2. **Provide Options**: Always give clear, distinct options
3. **Confirm Actions**: Before creating JIRA tickets, show preview
4. **Progress Updates**: Keep TodoWrite current so user sees progress
5. **Iterate**: Support multiple countermeasurements without losing context

## Error Handling

If errors occur:
- **JIRA connection failure**: Offer to continue without JIRA, save tickets to file
- **Repository access failure**: Ask user to verify paths/permissions
- **Missing configuration**: Guide user through setup
- **Parse errors**: Ask user to reformat input

Never fail silently - always inform user and offer alternatives.

## Completion Checklist

Before finishing, verify:
- [ ] All countermeasurements assessed
- [ ] All JIRA tickets created (if requested)
- [ ] Summary document generated
- [ ] All TodoWrite items marked complete
- [ ] User has links to all created JIRA tickets
- [ ] Summary file saved to disk

</INSTRUCTIONS>

## Example Usage

```
User: "I want to assess Llama Stack"