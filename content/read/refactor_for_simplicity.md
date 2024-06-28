---
title: Refactor for simplicity
subtitle: By simplicity, I mostly mean readability
date:
---

For those that aren't familiar, **refactoring** is like tidying up your code. It’s the process of restructuring existing code without changing its external behaviour. The goal is to make your code simpler, cleaner, and more readable. This can have a huge impact on the maintainability and scalability of your software. Programmers (the good ones anyway) spend quite a lot of time refactoring their code ... and that's a good thing.

But it's not quite that simple.

There are often competing goals in play. The process of refactoring code often throws up opportunities to make it run faster - which is a good thing and can reduce running costs. But if this comes at the cost of greater complexity or reduced readability it's probably not worth doing.

Let's take the example of caching. Ignoring for a moment that caching is famously one of the _hard things_ in computer science, it's a common way to speed up software, basically by reusing common bits of data rather than fetching or calculating them every time they are needed. This saves time, which means more things can be done in a given period and fewer CPU cycles are needed.

However, in order to implement caching, more code needs to be written and more tests are required to make sure the code is working properly. Testing a caching mechanism can be tricky as there needs to be a way of a) making sure the data is cached properly and b) making sure the code still works when the data isn't cached. This doesn't just apply when the cache is being set up - the next developer who comes along is going to have to understand how the caching works - which is going to take some time. It's probably also a good idea to document the caching mechanism - and the problem it's trying to solve - in case a future developer gets frustrated and deletes it. It **might** be worth doing this kind of refactoring if the overall cost saving from increased performance outweighs the cost of increased developer time - but it probably isn't and you should do the calculation first!

The other side of this coin is refactoring for readability.

Given the choice, I would much rather be presented with code that is readable and doesn't work, than working code that is hard to understand. This sometimes takes people by surprise, as they assume that the bare-minimum standard for code is that it should work. This is true, for code that makes it into production. Although even then there will always be hidden bugs and edge cases, so maybe it's more accurate to say it's _mostly_ true for production code.

But before code makes it into production, at least two people will (should) work on it - the person that wrote it and the person that reviews it. Reviewing readable code can be a very quick process, but reviewing poorly written code can take a very long time. It's also quicker to find and squash bugs in code that is readable ... and this is time that really matters once the code is in production.

Determining how "readable" code is can be something of a subjective exercise. What makes sense to me may not make sense to you. The most important thing is consistency. Things should be where I expect to find them and formatted in a way that my eye expects to see. In short, follow the style guide.

You have got a style guide, haven't you?

Things should be named sensibly and consistently (noting that naming things is the other _hard thing_ in computer science). They should describe the reality of their purpose, variables should be nouns and functions should be verbs. Get those things right and most code becomes self-documenting. It should always be clear from the code itself _what_ is happening and _how_ - but if it isn't clear _why_ that thing is necessary then it might be worth adding a short comment.

Opinions vary about the correct level of abstraction and how much repetition is acceptable. My view is that it should be possible to understand any individual logical unit of code based only on what fits on one screen of text. Utility functions are great and can reduce complexity, but only if what they are doing is obvious from their name and there are no hidden side effects ... otherwise each one adds more cognitive load as the reader has to dig further and further into the code to understand what's happening.

Certainly, typing the same thing out twice is a good indicator that you should consider an abstraction, but I don't treat it as a hard rule. Again, the most important thing is to be consistent in approach so the person who has to read the code in three months' time (that person could well be you) can make sense of it quickly if they are familiar with the overall codebase.

In summary, when refactoring (and you should refactor often) consider readability first, then overall simplicity, then performance if absolutely necessary.
