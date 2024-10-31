---
title: The Grug Brain Developer
subtitle: Wisdom from grugbrain.dev
date:
---

It's quite rare that I read something on the internet and agree with every word of it. <a href="https://www.grugbrain.dev">grugbrain.dev</a> is an exception. The original is written in a "caveman" style which I quite like, but it makes the content a little harder to digest, so (with a little help from ChatGPT) I've translated and summarised it here. If you like this version, check out the original ... which also has pictures. 


# The Practical Developer's Guide

### Introduction
This is a collection of practical insights on software development from a "Grug Brained" developer: someone who's been in the field for years, has seen a lot, and learned from mistakes (often the hard way). 

### Complexity: The True Enemy
The biggest challenge is complexity. You can’t always see complexity as it creeps into a codebase, but you can feel its impact as small changes break everything. Avoid complexity by simplifying wherever possible and understanding how each addition could make the system more fragile.

### Saying No
The best weapon against complexity is “No.” Saying no to unnecessary features, abstractions, or time-wasting requirements is vital for keeping things simple. While saying yes might be good for your career, saying no keeps your project manageable, understandable, and useful in the long term.

### When to Compromise
When “No” isn’t an option, look for the 80/20 solution: build 80% of the feature with 20% of the effort. It might not have every bell and whistle, but it’ll deliver the value and help keep complexity at bay. Managers often won’t even notice if you skip the last 20% of complexity.

### Factoring Your Code
When building out a system, don’t over-design it early on. Let natural boundaries emerge as you work, where functionality can be isolated with minimal dependencies on the rest of the system. Waiting for these "cut points" to appear organically will save time and reduce the risk of over-abstracting.

### Testing
Testing is crucial, but balance is key. Start with basic unit tests, but don’t overdo it in early stages. Focus more on integration tests as the system grows, and build a few key end-to-end tests that cover the main workflows. Avoid mock-heavy testing unless absolutely necessary.

### Agile
Agile methods are fine, but don’t take them too seriously. Agile can be a useful framework, but the real value in development comes from prototyping, good tooling, and hiring talented developers. Agile isn’t a magic solution to every problem.

### Refactoring
Refactoring is often necessary but should be done carefully. Small, incremental changes are safer than large, sweeping ones. Keep end-to-end tests updated to catch breaking changes early. And remember, too much abstraction can make refactoring a nightmare.

### Chesterton's fence (Respecting Legacy Code)
There’s often a reason why old code is structured a certain way, even if it’s messy. Don’t rip out old code unless you fully understand its purpose. Sometimes code is ugly for a reason, and changing it can introduce unintended bugs.

### Microservices
Getting the structure of code right is a hard problem. Microservices require this problem to be solved correctly and then add a network call. (Personal note: the ability to scale some services independtly of others can be very helpful, although it comes at the cost of complexity). 

### Tools and Debugging
Learning and mastering your development tools is a big productivity boost. IDEs, debuggers, and code completion can speed up development and help you troubleshoot faster. Take the time to understand these tools deeply - indcluding conditional breakpoints and stack travsersal. 

### Type Systems
Type systems are most useful for autocompleting and catching simple errors, not for building hyper-abstract models. While strong typing has its place, avoid overusing generics and complex abstractions—they can make code hard to work with and maintain.

### Expression Complexity
Avoid cramming too much logic into one line. Break up complex conditions into clear, named variables to improve readability and debugging. Although it may mean more lines of code, it’s easier to understand and maintain.

### DRY (Don't Repeat Yourself)
While avoiding repeated code is generally good, DRY can go too far. Sometimes, duplicating a small amount of simple code is easier to understand than creating overly complicated abstractions.

### Separation of Concerns (SoC)
SoC is a popular principle, but rigidly separating concerns can sometimes create unnecessary complexity. In contrast, the Locality of Behaviour principle says that "The behaviour of a unit of code should be as obvious as possible by looking only at that unit of code". This flies in the face of classical thinking, but makes code easier to read and maintain in the real world. The implementation of logic can still be abstracted away, provided the invocation of that logic is obvious. 

### Closures
Closures are helpful, especially for abstracting operations over collections, but they can become complex quickly. Use them sparingly, as they can lead to convoluted code that’s hard to debug.

### Logging
Logging is essential, especially for production systems. Use structured logs and track request IDs for distributed systems. Well-organised logging can be a lifesaver in debugging but is often overlooked.

### Concurrency
Concurrency is hard, so lean toward simpler concurrency models, like stateless request handlers or job queues, which minimize the chance of complex interactions and bugs.

### Optimization
Premature optimization wastes time. Profile first: always have data to back up any optimization efforts, focusing on real bottlenecks rather than theoretical improvements.

### APIs
Good APIs should be easy to understand and not require deep knowledge of the underlying implementation. Create intuitive methods for simple cases and more complex interfaces for advanced cases where they are needed.

### Parsing
Recursive descent parsing is usually simpler and more maintainable than using parser generators. While it might not be the latest trend, it works well for most real-world parsing needs.

### The Visitor Pattern
Avoid. 

### Front-End Development
Avoid unnecessarily splitting frontend and backend, especially for smaller projects. Heavy front-end frameworks can add unneeded complexity, so keep things simple with minimal JavaScript where possible.

### Fads
Be cautious with trends, especially in frontend development. New tools and patterns often recycle old ideas and may add more complexity than they’re worth.

### Fear of Looking Dumb (FOLD)
FOLD stops people from admitting when things are confusing or complex. Senior developers should lead by example, asking questions openly. Reducing FOLD creates a healthier team environment and better code.

### Imposter Syndrome
Most developers feel imposter syndrome at some point. Remember, if you’re learning and improving, you’re on the right path. The feeling of not knowing what you’re doing is more common than you think.

