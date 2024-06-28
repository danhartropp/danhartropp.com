---
title: Refactor for simplicity
subtitle: By simplicity, I mostly mean readability
date:
---

For those that aren't familiar, **refactoring** is like tidying up your code. It’s the process of restructuring existing code without changing its external behaviour. The goal is to make your code simpler, cleaner, and more readable. This can have a huge impact on the maintainability and scalability of your software. Programmers (at least the good ones) spend quite a lot of time refactoring their code ... and that's a good thing.

But it's not quite that simple.

There are often competing goals in play. The process of refactoring code often throws up opportunities to make it run faster - which is a good thing and can reduce running costs. But if this comes at the cost of greater complexity or reduced readability it's probably not worth doing.

Let's take the example of caching. Ignoring for a moment that caching is famously one of the _hard things_ in computer science, it's a common way to speed up software, by reusing common bits of data, rather than fetching or calculating them every time they are needed. This saves time, which means more things can be done in a given period and fewer CPU cycles are needed. But in order to implement caching, more code needs to be written and more tests are required to make sure the code is working properly. Testing a caching mechanism is a little tricky as there needs to be a way of a) making sure the data is cached properly and b) making sure the code still works when the data isn't cached. This doesn't just apply when the cache is being set up - the next developer who comes along is going to have to understand ow the caching works - which is going to take some time. It's probably also a good idea to document the caching mechanism - and the problem it's trying to solve - in case a future developer gets frustrated and deletes it. It **might** be worth doing this kind of refactoring if the overall cost saving from increased performance outweighs the cost of increased developer time - it's definitely worth doing the calculation first!

The other side of this coin is refactoring for readability.
