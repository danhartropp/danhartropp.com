---
title: Certification and data protection
subtitle: Tedious box ticking or vital back-covering
date:
---

NOTE: This is based on UK experience ... it may not apply in other places. It is also not legal advice and you should not reply on it!

Aside from internal documentation (which is very important) there are two main kinds of documentation that require attention from the tech lead in a startuppy environment.

The first is what I'll loosely call "quality certification". These are only likely to be of interest to B2B firms - and even then only if you're selling to serious corporate/enterprise outfits with dedicated purchasing departments. At the top end (and unlikely to be relevant for a startup) are the ISO accreditations e.g. ISO 9001 (Quality) and ISO 27001 (Data Security). There are also a raft of certifications you can get that designed to reassure potential clients that you'll be careful with their data. These include things like "Cyber Essentials" (applicable for most firms) and PCI-DSS(relevant for those handling credit card details).

I'm not a fintech expert, but if you're handling card payments you should work out for yourself which bits of PCI-DSS apply to you and what you should do about it - it looks like a total pain and probably something you should just outsource to <a href="https://stripe.com/gb/guides/pci-compliance">stripe</a>.

The other certifications only ever seem to come up in tender/qualification documents that have been written by purchasing teams. Over the years, I've been surprised at how often I've been asked whether my firm has these certifications, how often I've said "no" and how little anyone has cared. I've been left with the impression that the purchasing want to say they've asked the question, but don't really care about the answer. That said, I've always been able to tell a compelling story about the security and resilience measures in place, even if there is no certificate to show them.

My personal view about these schemes is that they are based on sound principles, but the fact you've got a certificate doesn't mean you've applied those principles well. You may have a comprehensive risk and mitigation strategy written down and refresh it every quarter, but if you've misjudged a risk or repeatedly fail to mitigate it, then the register isn't much use.

Your mileage may vary of course ... and if having certification is important for your clients, then you'll just need to suck it up and get certified. There are lots of firms that can help with the process and provide template documentation to make it all easier.

Which brings us on to data security and privacy. This is a trickier area, not least because it concerns the law, as opposed to contractual requirements (although contracts in this space are important ... see below). It's also something that's worth taking seriously for its own sake ... careless handling of sensitive information has the potential to make life very unpleasant for some people and I don't think that's a responsibility that should be taken lightly.

It is almost certainly prudent to get some legal advice in this area - and get contracts and T&C documents etc drafted by a professional who understands your business. But having a contract that's been written by a lawyer isn't a defence - so it pays to understand this topic yourself, at least at a high level. The good news is if you're in the UK is that there is some really good (if lengthy) guidance on the <a href="https://ico.org.uk/for-organisations/advice-for-small-organisations/">ICO website</a>.

What it basically boils down to is this ... you need to know what data you're holding, why you're holding it, what you plan to do with it and who is responsible for it. You then need to make sure you've got a lawful basis for holding it (i.e. permission) and that you've taken sensible precautions to keep it secure. You need to be particularly careful if you are holding (anywhere on systems under your control) data about people's race, religion, political opinions, trade union membership, health, biometrics, sex life or sexual orientation. See the relevant bits of the ICO website for more information. There are separate requirements that relate to marketing activity, particularly around direct marketing aimed at the public. Anyone that you are holding information about has a right to see that information - and there is a requirement for most organisations to register with the ICO.

The requirements are also a bit different depending on whether you are a "data controller" or a "data processor" - the former is responsible for how the data is used, the latter just processes it under instruction. There's a good chance your firm will be both - a controller of your own information and a processor of your clients' information. If that's the case, then make sure your contract is clear about who is responsible for what (make them responsible for their own information as far as possible). Again, this is particularly important if clients are storing sensitive personal information on your systems - and if you're not set up to secure that kind of data, make sure the contract is clear that they shouldn't store it on your systems!

This can all get quite complicated quite quickly, but a good starting point is the <a href="https://ico.org.uk/for-organisations/advice-for-small-organisations/checklists/data-protection-self-assessment/">ICO checklist for small organisations</a>. Start there and then speak to a lawyer once you've worked out the sort of questions you want them to answer.
