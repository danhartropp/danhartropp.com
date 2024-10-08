---
title: Documentation
subtitle: Getting a great user experience from a good product
date:
---

Documentation - so often an afterthought in the development process and so often seen as users accepting defeat. There's a lot of subjectivity in this space, not least because of the variation between products and users. Some can legitimately be expected to <a href="https://en.wikipedia.org/wiki/RTFM">RTFM</a> before using a product - others should be able to dive and and work it out. There are also legal requirements relevant to some products. 

Over all, my view is that, in an ideal world ... 

1) high level concepts and the purpose of the product should be explained clearly up-front
2) reference material should be comprehensive, and easy to access from the product itself
3) it should be possible to get meaningful results from the product without having to read the docs at all 

Of course, we're not in an ideal world so I've gathered together a few more high-level thoughts that might be useful for anyone trying to write (or re-write) technical documentation. 


### DDD?

We're familiar with Test Driven Development and getting the User Experience right early in a product's development ... documentation is almost certainly going to be part of that experience. Sadly, we often leave writing the docs until after the product is ready for release. After all, there's no point writing documentation for something that could change during the development process is there?

But what if we flipped that on its head? If we assume that new users will need to consult the documentation early on, then why not write the docs first (or at least the outline), to make sure we're delivering an excellent user experience? Reference material and detailed screenshots can probably wait - but from a UX point of view, what do we want users to experience from their first contact with the documentation ... and how does the product need to work to deliver that? 


## Start with why?

A common pattern with documentation for software libraries is to include a short example on the first page of the documentation - and often on the first page of the website. It's a good example of the "show, don't tell" communication principle. This helps address an issue with a lot of open source software products, which do a really poor job of explaining *why* the project exists ... what is the problem they are trying to solve? If I have to learn how to use the product before I can understand what it does (and therefore whether I need it) I'm very unlikely to bother. 

Including a short example early on does a few different things. It gives context to a potential user. At the most basic level, if I don't recognise the kind of inputs and outputs the example is dealing with, this probably isn't something I need. It also helps me compare to existing solutions ... does it look more flexible, does it have more features, is it easier to use? Finally, it gives a sense of what using the product will be like - and will it fit with my existing code base? This last point is really important for developer experience and is most easily conveyed with a few short code examples.  


## Readability and cognitive load

People generally use a product because they want the benefits that product brings. Good documentation is an important, but indirect, part of making those benefits happen - the more time a user has to spend in the documentation, the less time they are spending using the product and the longer it will take for the benefits to arrive. 

Make it easy to use the docs and you'll make it easier to use the product. A big part of this (as with code and really any written material) is readability, consistency and reducing cognitive load. These things all help users to navigate the documentation, find what they are looking for and understand it. My advice is to take a pretty rigid approach here - particularly in relation to cognitive load. Don't explain high level concepts in reference material (but linking to them is a great idea) and don't get bogged down in covering every possible parameter when writing a how-to guide. Users generally want to use the docs for as little time as possible before getting back to using the product ... as a documentation author, your job is to make that as easy for them as possible. 

## Diátaxis

If you're the sort of person who reads a lot of documentation (this applies to most programmers) then you may have noticed a trend for organising documentation into categories such as how-to guides, tutorials, concepts and reference material. This is a very popular structure and has been formalised into a framework called <a href="https://diataxis.fr/">Diátaxis.</a> 

This is well worth looking into ... it's essentially a set of guidelines for writing the right kind of documentation for a particular use case. It splits concepts along two axes ... action-cognition and acquisition-application. These in turn lead to the categories listed above. Once you're familiar with the concepts, you'll start to see them in all sorts of documentation. 

It's an excellent idea and a very accessible website, full of useful information for anyone involved in writing technical documentation. 


## Self-documenting code (and products)

It is possible (in theory) to write code that is self-documenting, by using descriptive names and clear structures. The idea is that the code is so easy to follow that additional documentation is unnecessary. This works up to a point, but even very clearly written code can't explain *why* something is being done a particular way. Comments are very useful for explaining *why* and if they written in a structured way, can be  pulled together and formatted by scripts to make documentation. Typically this approach is used for reference material, rather than detailed conceptual guides. With automated checks in place, it becomes very easy to make sure that your code library is 100% documented. 

To be honest, I'm not a huge fan of what tends to come out of these systems. This kind of documentation is great for code inspection tools in modern editors, which can save a lot of time having to flick back and forth between files, but it usually doesn't add much more value than that. 

Writing great documentation (including reference material) takes time and effort - there are no short cuts. If you've got great reference documentation, putting the relevant sections in the right place in the code is wonderful and makes it immediately available - but you need to have great docs in the first place. Too often, what actually gets generated is a basic description of a function, listing it's parameters and return type. Using strong typing allows modern editors to do the same thing, without giving the product manager false hope that 100% documentation coverage has been achieved.  



## Success criteria

As with code, there is always going to a subjective element to assessing the quality of documentation. There are some obvious metrics that can be applied, such as feature/function coverage and word count, but these don't tell us much about whether the documentation is useful. 

However, when docs are served over the web (which these days is pretty much all the time) it becomes possible to track their use to identify areas of the product that are under-documented, or where the content isn't clear enough. 

It also becomes possible to track use of the docs over time. Typically, a user will consult the documentation more when they first start using a product and less over time. Good documentation should help the user become proficient (and therefore consult the docs less frequently) quicker than bad documentation. There is also likely to be a shift over time from accessing high-level concepts to low-level reference material. If the curve looks different for specific bits of the product, it might be worth looking again at the docs. It might also be worth looking again at the product, but that's a different issue. 

Having success metrics in mind makes it possible to apply analytics techniques such as A/B testing to versions of the docs in order to improve them over time. The key point is to define what those metrics are before you start running experiments and before you start writing. 
