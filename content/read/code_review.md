---
title: Code Review
subtitle: The single best way to write code good
date:
---

I'll start with a definition in case there's anyone reading this who isn't familiar with professional coding practices. A code review is a bit like a peer review in academia. One or more people check code that's been written by someone else, with the aim of ensuring the code is of good quality.

In theory, it's a simple enough process ... person A writes some code and sends it to person B, who reads the code and makes comments/suggestions as to how it can be improved - or asks questions if something is unclear. In practice, there's a lot of devil in the detail and a number of things need to be in place before code reviews are effective.

Much of what follows has been distilled from elsewhere ... mostly <a href="https://google.github.io/eng-practices/review/">here</a>.

## Standards and expectations

The person writing the code and the person reviewing it need to have a shared understanding of what good code looks like. A common way of achieving this is with a style guide or coding manual. This sets out the preferred way of doing things, from stylistic issues like spaces-vs-tabs through to security things such as banned packages. Good style guides evolve over time, but it's often helpful to start somewhere such as <a href="https://google.github.io/styleguide/">here</a>. Style guides often specify that certain tools should be used, such as linters, compiler flags etc ... a common configuration for these tools is also then required.

As well as code stuff, it is also helpful to have standards and expectations for things like tests (what types of test, what is the acceptable minimum level of code coverage), the size and content of pull requests (what is mandatory, what is optional) and the circumstances in which the code review process can be skipped (ideally never, but in small teams this isn't always realistic).

## Approach and tone

A lot has been written about how to conduct a good code review and practices vary between organisations. In my view, it helps to remember that you are reviewing something that a real person has written - and that a real person will read your review - but **you are reviewing the code, not the person who wrote it**.

Overall, be kind and constructive. Phrasing something as a question can soften the impact considerably. Take time to explain why you think something and, if possible, refer to a common standard. If there is no agreed standard, this might be a good opportunity to update the style guide. If you're being nitpicky, then say that explicitly ... and it's OK for people to do something differently if a) their way isn't objectively worse or b) it is worse, but it makes very little difference.

## Objective

The high level objective of the code review process is to make the whole codebase better over time. This should be the fundamental question each time code is reviewed ... does this code make the overall codebase better, or worse?

Better is obviously a subjective term - the style guide is the ultimate arbiter. Better is also quite a woolly term ... if code runs faster but is harder to read, is it better? HINT: No, unless there's a very strong business reason that the code needs to run faster and there was no other way of doing it.

Knowing that someone else is going to read the code that you're writing is a powerful motivator to write easily readable code. This benefits not only the code reviewer, but also the next person who has to work on that part of the codebase.

It is also worth noting that, in order to make the codebase better, explanations need to be done _in the code_ not just in the code review notes. If something needs explaining, refactor the code or add comments if you have to - don't rely on the code review notes themselves.

## What to look for

1. Is the purpose of the change clear from the pull request?
2. Can you understand what the code is doing and why it is necessary?
3. Could the code have been written more clearly/simply/readably?
4. Do the comments explain _why_ something is necessary?
5. Are tests in place that cover every line of changed code?
6. Are there any TODO, NOTE or similar comments that need to be addressed?
7. Read every line of the change - check for typos and naming conventions.
8. Take a step back and check things like titles (yes, I know).
