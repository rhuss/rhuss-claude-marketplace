---
name: threat-model-assessment
description: Conduct security threat model assessments for software projects by analyzing code against countermeasurement requirements and generating GDPR/compliance documentation with optional JIRA integration
---

# Threat Model Assessment Plugin

This plugin helps conduct systematic security threat model assessments following industry best practices (SDElements, GDPR compliance, etc.).

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
- (Optional) SDElements or other threat model requirements

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
     * "Default priority?" (Critical, High, Medium, Low)

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

If user says "done":
- Skip to Phase 3: Summary Generation

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
2. Write concise rationale (max 1024 characters for SDElements) explaining:
   - What technology/pattern the countermeasurement addresses
   - Why the product doesn't use that technology/pattern
   - What alternative approach the product uses (if any)
   - Key code references supporting the conclusion
3. Store assessment in assessment_data
4. No JIRA ticket needed
5. Ask for next countermeasurement (skip to step 5.8)

**Guidelines for Not Applicable Rationale**:
- Maximum 1024 characters (SDElements limit)
- Be concise but complete
- Include specific code references (file:line) in analysis paragraphs
- Use numbered lists for clarity
- **Conclusion section**: One line per paragraph, NO code references (this gets pasted into SDElements)

**Structure**:
1. Opening paragraph: What the countermeasure addresses
2. Analysis paragraph(s): Why it doesn't apply, with code references
3. **Conclusion**: Clean summary suitable for SDElements (no code refs, one line per paragraph)

**Example Not Applicable Assessment**:
```
**COUNTERMEASUREMENT: T20 - Generate unique session IDs**

**Status**: Not Applicable

This countermeasure addresses session fixation in session-based authentication systems.

Llama Stack (LLS) does not use server-side session management. Analysis of auth.py:89-150 confirms: (1) No session creation, storage, or management; (2) Each request independently authenticated via token validation; (3) No session IDs generated or stored in cookies; (4) User attributes extracted per-request and discarded after. LLS implements stateless authentication using Bearer tokens (JWT, OAuth2/OIDC, GitHub tokens, Kubernetes service account tokens).

**Conclusion (for SDElements):**
LLS uses stateless token-based authentication, not session-based authentication.
Session fixation countermeasures are not applicable to this architecture.

[Character count: ~672]
```

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

2. Use the Python helper script to create ticket:
```python
import sys
sys.path.append('/Users/rhuss/Development/ai/claude-code-dev-marketplace/threat-model-assessment')
from jira_helper import create_jira_ticket

ticket_key = create_jira_ticket(
    summary=f"[Requirement ID]: [Brief Title]",
    description=jira_description,
    epic=assessment_data["jira_config"]["epic"],
    component=assessment_data["jira_config"]["component"],
    priority=assessment_data["jira_config"]["priority"]
)
```

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

**Framework**: [SDElements, OWASP, NIST, etc.]
**Focus**: [GDPR compliance, Data protection, etc.]
**Code Analysis Tools**: Claude Code, Grep, AST analysis
**Documentation Standards**: [Standards followed]
```

Save this file to the current working directory.

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