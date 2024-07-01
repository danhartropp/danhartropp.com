---
title: Testing (and load testing)
subtitle: You can have too much of a good thing
date:
---

Before any code goes into production, a set of automated tests should be written and those tests should all pass. Where appropriate (e.g. front-end changes) there should also be a manual check that things work as expected. Where code interacts with existing code or the data layer, the tests for those should also all pass. If the tests are no longer relevant, they should be rewritten to make sure they all pass.

So far so simple.

Having tests that pass is one thing, but knowing you've got the _right_ tests is another. I take a somewhat pragmatic but rigid approach to this. The bare minimum level of testing as as follows ...

1. Aim for at least 95% code coverage. In the real world, there are always weird edge cases that need to be accommodated and are very hard (or slow) to test reliably - it isn't always worth writing tests for these. If you can explain in a one-line comment why a specific section of code doesn't need testing, then it's OK to skip it. But make that section of code as small as possible - a couple of lines is about right.
2. As a minimum, have test cases for a) the happy path, b) handling the most likely failure path (probably arising form user data) and c) any bugs that have arisen in production.
3. Unit test and mock everything that it is sensible to unit test. For instance, anything in utils files, the database access layer etc etc. Run these tests whenever the relevant files are changed, for **any** reason.
4. End to end test everything. Access a copy of the live database in an environment that is as close to production as possible.
5. Have a suite of tests that check compatibility at the data layer. These don't need to hit the database directly, but should confirm strict typing ... if my code requires a datetime and yours passes a string, the test should fail. Run these tests for the whole project when any files in the data access layer are changed for **any** reason.
6. Tests should be quick to run. Don't make me wait more than a minute for the whole suite to run. If it's tricky to achieve this and run end to end tests in a close-to-live environment, then refactor the code or the whole architecture to make it work.
7. Follow a CI/CD process that ensures tests pass before code gets into production. But be pragmatic about this ... if your team is tiny and you're dealing with non-critical code that takes a while to test completely, it might be sensible to allow simultaneous deployment and testing in some cases (like urgent bug fixes).

The bottom line is that you're always going to find bugs in production, so there's little point in writing hundreds of tests cases for every scenario you can think of. But do test every happy-path scenario because that means you reduce the risk of putting code into production that breaks something else.

A quick word about load testing ...

Periodically (and whenever significant architectural changes are made) it's worth load testing a close-to-live environment to destruction. There are good automated tools for this - put some limits on your auto-scaler and find out how much traffic your system can handle. This is useful for a) those times when you get a massive spike in legitimate traffic and b) estimating your future costs given assumptions about growth and traffic.
