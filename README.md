# FCM-TRADER

## About

This is a ficticious project. An attempt to apply prompt/context engineering to drive coding with AI using Gemini-2.5-Pro, Cline and Aider.

Though the project name is called "FCM-Trader", the system features does not execute any trades. After few iterations (you can see from the postfixes) and the feature list has excluded "trade execution"...no integration with brokerage services for simplicity sake.

## Status & History

The project shown here has only completed slightly more than Epic 1. You won't see the complete git history here, as I work on it separately in a private workspace.

## Opinion

I am both an Electrical Engineer and Software Engineer by training. I quite process driven. Agentic AI coding works only with proper context engineering built into your workflow (ctrl.md & agent specific context)

I don't use Claude Code (the current premium standard for ai coding) or their very performant Sonnet4/Opus4, I prefer to be agent or model agnostic. Hence, my current preference is Gemini 2.5 Pro, which has generous access and large context window. This makes it very good my purpose.

When I'm more proficient in using AI agent to assist in building or troubleshooting apps/systems, I may consider subscribing in future, else really your employer should cover that (right?).

## Model
- gemini-2.5-pro **coding**
- gemini-2.5-flash **planning**

## Agents

### Aider
This a more of a "pair-programming" agent. And good for precision changes. I like they way it keeps session history locally in the workspace. Also using it need to very hands-on with "human in the loop" approach.

There is a "Aider Composer" VSCode extension for more friendlier diff of code changes.

### Gemini Cli
It's a lot more automous than Aider and a lot more polished in assisting app building.

### Cline & Gemini Code Assist
Both are great IDE agents, and they do come with a certain context setup that shape their default behaviour.

A lot of times, they do ignore your instructions and I have do repeat reminder or reload context files which adds to the token cost.

I used Cline a lot, partly it's opensource and model agnostic.

### Claude Code / Cursor

Eventually, I think I need to subscribe and use them as they some of the most popular and highly rated ones. And they built an ecosystem around them that we really cannot ignore.

## **BMAD** Framework

https://github.com/bmad-code-org/BMAD-METHOD

This is a very comprehensive framework for agile coding with AI agent. And it does come with support for different platforms like Cursor, Claude Code, Gemini Cli, Cline, RooCode, ...etc

I learn a lot a lot from it, especially about context engineering. The folks behind it has it all well thought yet being agent agnostic.

It serve a very good foundation, but you need to add-on your specific preferrences and biases.

A word of caution, it can be token expensive.


## Next
I will continue on this project to hopefully complete the tasks (`task.md`). I will update this repo at some intervals, while I still have other side projects.

