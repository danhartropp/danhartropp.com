---
title: Giving an LLM a city to run (sort of)
subtitle: can a frontier model beat a trained specialist on a "reasoning" task?
date: 2026-09-07
---
Frontier models are going into jobs that used to need a purpose-built system. The pitch is attractive: just describe the task and plug in reasoning. This is obviously much easier than developing your own systems and models from scratch and drops the cost of deployment to near zero. But does it really work?

Weirdly, there aren't many people who are keen to run experiments on real-world business processes, so I thought I'd try the next best thing ... giving the model a \[sim\] city to play with.

I also used reinforcement learning to train a specialist model from scratch to see if a frontier model could beat it.

The bottom line: The frontier model can tell you exactly how to run the city. It talks a really good game. But it fails to execute and can't even follow its own plan.

So, to wildly extrapolate a takeaway for the people who won't read any further than this ... if you can define a task accurately, a specially-trained model is likely to beat a frontier LLM. If you can't define the task accurately and you're happy to settle for mediocre performance, then an LLM will work. Just don't trust what it says it's doing.

## The setup

I used Micropolis, an open-source SimCity engine. You get a 32×32 patch of land, a million in funds, and 200 decisions. Each turn you place one thing: a house, a road, a power line, a factory. Your score is the population at the end.

It's a good task for this experiment because nothing pays off at once. A zone is dead ground until a road reaches it and power arrives. Growth compounds, so a decision on turn 10 is worth several on turn 80. You have to sequence, not just choose ... and that requires some form of reasoning.

I trained a specialist model on the simulated city using a tiny convolutional network (about 94K parameters) and a hundred thousand games of practice, played inside a reinforcement learning loop on a laptop GPU. The frontier model (Claude Opus 5) was given tools to interact with the city and no training at all.

For the sake of an independent baseline, I also wrote a dumb heuristic rule ... build a power plant, then alternate road, power, residential and industrial (1:3 ratio) zones until the game ends.

## What they built

Here is what the specialist builds. Yes, it's ugly.

![A dense, fully developed city built by the trained specialist](/static/img/micropolis/city-trained-calm.png)

Dense usage, roads to everything and power everywhere. It's not pretty but it has found a layout that packs the most houses (and other necessary services) between the fewest roads. Note the lack of fire stations. That will become important later. 

Here is the city Claude built, on the same map.

![The frontier model's city: zones along long road spines, most still empty plots](/static/img/micropolis/city-llm-calm.png)

It's a logical layout. **But most of these plots never became anything.** The specialist's map is full of buildings. This one is full of zoning — flat squares marked `R`, laid out correctly, connected to road, connected to power, and empty. Lots of fire stations though. 

## The LLM is a mediocre reasoner


**The LLM scored 427 against the specialist's 951.** A dumb rule scores 71, so the LLM beats that at least, but is only about half as good as the specialist.

The LLM is not failing at the mechanics. It knows a zone needs a road and it gives it one. Just one building in the whole city ends up unpowered. In fact the LLM follows the rules *better* than the specialist does:

| | valid moves | zones built | people per zone |
|---|---|---|---|
| specialist | 90% | 80 | **13.2** |
| frontier model | **99.5%** | 59 | **7.5** |

Nearly every move it makes is legal and lands. It builds a little less, and gets half as much out of each one.

## The LLM can state the strategy. It can't execute it.

This is the most important finding for me.

Before the LLM saw a map, I asked the LLM to write down its plan. It can do this because it will have come across Micropolis (and Sim City) in its training data. Part of the plan read:

> **"Mix: near-even Residential/Commercial/Industrial early because industry and commerce create residential demand; after turn ~50 skew residential, which holds the most people."**

That is exactly right and is basically what the specialist model built. In Micropolis, people arrive because there is work. Residential demand therefore comes from shops and factories. If you just build houses with no economy, the houses stay empty.

Here is what each model actually built:

| | houses | shops | factories |
|---|---|---|---|
| specialist | 37 | **20** | **27** |
| frontier model | 39 | **8** | **7** |

The LLM wrote the rule about jobs and then zoned a dormitory suburb. Its city ended with 327 residents and 44 jobs. The plots stayed empty because there was nothing for anyone to do.

It had the same problem with the concept of returns compounding over time. It said growth compounds and early zones are worth more, but it actually built half as many of them early.

| | zones down by turn 50 | road tiles per zone |
|---|---|---|
| specialist | 38 | **0.9** |
| frontier model | 19 | **1.9** |

It wasn't great at building roads either. The specialist lines development along both sides of one road and lets neighbouring zones pass power to each other. The model ran long spines and hung less off them. Half its turns went on building plumbing.

**The gap is not knowledge. It is the distance between describing a plan and following one for two hundred decisions.**

To give the LLM a fair chance, I let it play again, giving it a full record of every move it had made and whether each one worked, and allowed it to deviate from its plan. In effect, allowing it to learn as it played. Its execution went to near-perfect, but its score got worse, dropping from 443 to 427.

This is, of course, how today's models work, not a permanent fact about machines. The next generation may not have these problems. But for now, **a specialist trained to execute beats a model that sounds like it knows what it is doing** — as long as you can build a good enough model of the world to train it against. This is important because ...

## What if we set the city on fire?

A specialist is only a specialist in the conditions it trained for. So I lit twelve fires during each game, at fixed times, in random places. The specialist's training didn't include fires at all and it was awful at dealing with them.

![The same specialist under fire: sparse development, burnt ground, active fires](/static/img/micropolis/city-trained-fires.png)

**951 to 56.** Scorched ground and fires still burning, barely a district left standing. The specialist does not fight them - it doesn't even know what they are, so it goes on placing houses beside buildings that are alight.

In contrast, the LLM scored **168** when the fires were turned on. So it fell too, but it did not collapse, and it beat the specialist easily.

**This is the real case for general reasoning in production.** It's not that the "reasoning" of today's LLMs is better, it's that LLMs have read about the world. They know what a fire is without being told, so what utterly destroys a specialist model merely costs a lot for an LLM. To put it another way, the failure that hurts you in a live system is the one nobody planned for, and that is where the specialist can't help you.

## Sixteen minutes later ...

I took the same broken specialist model and trained it again with the fires switched on. It took just sixteen minutes to converge on one laptop GPU.

![The retrained specialist under fire: a developed city studded with fire stations](/static/img/micropolis/city-firetrained-fires.png)

**56 to 579.** Three and a half times the LLM's score.

You can see what it learned. The red buildings marked `FD` are fire stations. They are everywhere. It builds three times as many as before and cuts police to pay for them. It worked that out for itself from two hundred games of burning cities down.

Importantly, the specialist did not become useless the rest of the time. In normal conditions it still scores 833 — twelve per cent below where it started, for a tenfold gain when things go wrong.

## What this means if you are deploying

**A frontier model is mediocre, but adaptable and easy to deploy.** The LLM scored half the performance of a purpose-built specialist system, but was deployable in about 5 minutes, just prompt-and-go.

**Saying the answer is not doing it.** The LLM wrote the right strategy and then ignored it. Judge a system on what it does over a long run of decisions, not on how well it explains itself - or risk getting bitten in production.

**The LLM advantage is robustness, not capability.** The LLM wins on the conditions you did not plan for. That is insurance, but it costs performance on the conditions you **did** plan for.

**Closing a gap once you know about it is quick.** Just sixteen minutes in this case. That was the cost of teaching a specialist about fire once fire became a thing. Training (and especially re-training) the model is not expensive.

It's worth noting that the specialist was also thousands of times cheaper to run. It played a full 200-turn game in **0.42 seconds**. The LLM took **42 minutes**. To save you doing the calculation, that's six thousand times slower, every game, forever. Frontier LLM providers typically make you pay per-token to use them as well.

So the real question is not "model or specialist". It's: **can you list the conditions your system will meet in the real world?**

If you can, train a specialist for them. It will be better, it will be far cheaper to run, and adding a condition you missed costs almost nothing once you've spotted it.

But if you cannot - if the things that might happen are open-ended and you will find out which ones matter only when they do - then an LLM is mediocre everywhere but won't collapse. It will cost you about half your performance and several thousand times your compute budget. Of course, if performance matters you could always go old-school and use people instead of an LLM. Just a thought. 

---

*[Micropolis](https://github.com/SimHacker/MicropolisCore) is the GPL-3 open-source release of the original SimCity engine*
