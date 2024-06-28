---
title: Testing
subtitle: You can have too much of a good thing
date:
---

Before any code goes into production, a set of automated tests should be written and those tests should all pass. Where appropriate (e.g. front-end changes) there should also be a manual check that things work as expected and look right on a range of screen sizes. Where code interacts with existing code or the data layer, the tests for those should also all pass. If the tests are no longer relevant, they should be rewritten.

So far so simple.

Having tests that pass is one thing, but knowing you've got the _right_ tests is another. I take a somewhat pragmatic but rigid approach to this. The bare minimum level of testing as as follows ...

1. Aim for at least 95% code coverage. In the real world, there are always weird edge cases that need to be accommodated and are very hard (or slow) to test reliably - it isn't always worth writing tests for these. If you can explain in a one-line comment why a specific section of code doesn't need testing, then it's OK to skip it. But make that section of code as small as possible - a couple of lines is about right.
2. As a minimum, have test cases for a) the happy path, b) handling the most likely failure path (probably arising from dodgy user data) and c) any bugs that have arisen in production.
3. Unit test and mock everything that it is sensible to unit test. For instance, anything in utils files and the database access layer. Run these tests whenever the relevant files are changed, for **any** reason.
4. End to end test everything. Tests should use a copy of the live database in an environment that is as close to production as possible.
5. Have tests that enforce a data schema across the whole codebase. These don't need to hit the database directly, but should confirm strict typing ... if my code expects a field to be a datetime and yours expects a string, the test should fail. Run these tests for the whole project when the data schema changes for **any** reason.
6. Tests should be quick to run. Don't make me wait more than a minute for the whole suite to run. If it's tricky to achieve this while running end to end tests in a close-to-live environment, then refactor the code or the whole architecture to make it work.
7. Follow a CI/CD process - but keep it as simple as possible. In a small team, a complex CI/CD process can add unhelpful overhead where a simple code review and approval process would have been fine.

The bottom line is that you're always going to find bugs in production, so there's little point in writing hundreds of tests cases for every scenario you can think of. But do test every happy-path scenario because that means you reduce the risk of putting code into production that breaks something else.

A quick word about load testing ...

Periodically (and whenever significant architectural changes are made) it's worth load testing a close-to-live environment to destruction. There are good automated tools for this - put some limits on your auto-scaler and find out how much traffic your system can handle - and where the bottlenecks are. This is useful for a) those times when you get a massive spike in legitimate traffic and b) estimating your future costs given assumptions about growth and traffic.
