# Heading

## [Date: YYYY-MM-DD]

### Experiments

- Description of experiment
- Parameters used
- Results observed
  '''python
  (code here)
  '''
  > ![Alt Text for a experiment plot](/"path/to"/experimentresults.jpg)

### Insights and Thoughts

- Key findings
- Questions raised

### Next Steps

- Planned experiments
- Items to investigate

````

2. ### **Best Practices**
- **Date your entries**: Always include timestamps for each entry
- **Be detailed**: Include experiment parameters, code snippets, and specific observations
- **Link to commits**: Reference relevant commits by their SHA when documenting code-related insights
- **Include visualizations**: Embed or reference plots, graphs, and diagrams
- **Track hypotheses**: Document what you're testing and why
- **Record failures**: Failed experiments are as valuable as successes
- **Note resources**: Keep track of papers, documentation, and external resources consulted
3. ### Keeping Your Journal Private

To prevent your research journal from being committed to the main branch, use these methods:

#### Method 1: Using .gitignore (Recommended)
1. **Create or edit** the `.gitignore` file in the project root:

```bash
# Create .gitignore if it doesn't exist
touch .gitignore
````

2.  **Add your journal files** to `.gitignore`:

```
# Private research journals
journals/research-journal.md
journals/journal-file-name.md
```

Resources:
https://project.inria.fr/keops/what-are-gap-junctions/

3.  **Verify it's ignored**:

```bash
git status  # Your journal should not appear in untracked files
```

### Team Collaboration on Journals

While individual journals should remain private, consider:

- **Shared insights document**: Create a separate `INSIGHTS.md` or `FINDINGS.md` for team-wide learnings
- **Meeting notes**: Use a `meetings/` directory for collaborative documentation
- **Experiment logs**: Create a shared experiment tracking system separate from personal journals

#### Template for Journal Entries

```markdown
## [Date: 2026-01-31]

### Goals for Today

- [ ] Task 1
- [ ] Task 2

### Experiments Conducted

#### Experiment: [Name]

**Hypothesis**:
**Method**:
**Parameters**:
**Results**:
**Conclusion**:

### Code Changes

- Commit: [SHA] - [Description]
- Files modified:

### Insights & Questions

- Insight 1
- Question 1

### Tomorrow's Plan

- Item 1
- Item 2

### References

- Paper/Link 1
- Paper/Link 2
```
