---
title: "[Brutally] optimising for cost"
subtitle: serverless is cheap until it isn't ... so design for the price list
date: 2026-10-08
---
Serverless compute is a wonderful deal when you're small. You only pay for what you use, it all scales to zero when not in use, and the free tiers are generous enough that a side project can live on them indefinitely. The catch is that the bill scales linearly with usage, and the number of operations a system performs has a habit of multiplying in ways nobody notices until the invoice arrives.

I've recently spent some time building a frost and rain alerting service at [weather.danhartropp.com](https://weather.danhartropp.com), and I set myself a deliberately unreasonable target from the start: it had to be able to run a million forecasts every night without the bill becoming a problem ... and the million users should all arrive in the same month. I don't expect anything like that traffic, but designing for that kind of scale now should prevent an annoying bill later. It should also help prevent the far more likely case, which is just enough users to tip me over the free tier and start paying for it out of my own pocket.

The bottom line: if you know where your costs scale (per request, per user per day, or per byte) you can usually arrange the design so the expensive multiplier never arrives, and for bursty/batchy operations you might be able to stay inside a free tier. If you don't know, the default patterns will quietly pick the most expensive option for you. It's mostly just reading the pricing page and doing a few sums before writing the code. 

## What the app actually does

Each day, a batch job downloads the Met Office's UK forecast, which is published as open data. For every place someone has subscribed to, it samples the forecast at that point, adds a set of terrain descriptors (how sheltered it is, whether cold air pools there, that sort of thing), and runs two small machine learning models that predict how much colder the ground will get than the Met Office forecast says. If the answer crosses the frost threshold, the subscriber gets a push notification. Rain works in a similar way but is simpler, because the Met Office already publishes a probability for 8,667 sites across the UK ... so the job just looks up the nearest one and applies a calibration curve.

This means there are two very different halves to the system. There's a small website where people search for a place, drop a pin on a map and subscribe, and there's a batch job that runs twice a day and does the actual forecasting.

## Where the money goes when Hacker News finds you

The (imaginary) scenario I used to stress-test the design was the classic hug of death ... a link lands on the front page of something like Hacker News and a few hours later a very large number of people have all arrived at once. The typical costs of what happens next break down like this:

| What a visitor does/gets | What it touches | What you're charged for |
|---|---|---|
| loads a page | the web server | requests and CPU-seconds |
| searches for a place | a geocoding service | requests |
| looks at the map | map tiles | bytes sent |
| subscribes | the database | writes |
| a forecast every night from then on | the batch job | reads, writes and compute, per subscriber |

The first four rows are the one-off spike, and they are where things will visibly fail if the budget gets blown. The last row is the one that matters, because **a hug of death in this case is a brief spike in the request path but a permanent step in the batch path.** Every subscriber you gain is a database read, a forecast and a write every single night from then on.

## One big read beats a million small ones

The subscriptions live in Firestore, Google's serverless document database, which charges per document read and written. The obvious design for the nightly job is to read each subscription, forecast it, and write each result back as a document. At a million subscribers that's a million reads and a million writes every night.

Firestore is cheap per operation, so this doesn't sound like much. A nightly full scan is about **$9 a month** and writing the results back costs about **$27 a month** more. It's not a lot, but I would somewhat resent paying hundreds a year to send other people weather alerts when there's a better way. 

Instead, the job writes its results as one file in cloud storage (Google Cloud Storage, which charges per object rather than per row). A night's forecasts for a million points come to about 40 MB compressed, written as a single object. That's **one billable operation instead of a million.** It's also a far better format for the job that really needs it, because those files double as the training data for the next version of the model.

The reads take a bit more thought. The job also writes a snapshot of the subscriptions it used, and the next run starts from that snapshot and only asks Firestore for documents that have changed since. Even on a really busy day that's about 30,000 documents rather than a million, so **a 97% reduction**, and at those volumes it costs essentially nothing. Materialising the data like this is a useful trick, provided that nothing is ever deleted. A hard delete would be invisible to the batch job, and the user would carry on getting alerts after they'd unsubscribed. Soft deleting (marking the row as "deleted") solves this problem. 

It's worth noting that the compute isn't the expensive part either. Both frost models together take about 180 microseconds per point, so a million points is about three minutes of a single CPU core. The whole batch fits on one machine, well inside Cloud Run's free allowance of 180,000 vCPU-seconds a month. In fact the job **can't** usefully be spread across more machines, because the Met Office publishes whole-UK grids (around 500 MB a run), and every extra machine would just download the same files again.

## Don't pay for everyone opening the notification at once

The other spike in this system is self-inflicted. When a frost alert goes out, thousands of people get a notification at roughly the same time, and a good number of them tap it. If the page behind that tap looked up the forecast or the subscription, every notification sent would become a database read at exactly the moment of peak load. So it doesn't. **The alert page is built entirely from its own URL**: the kind of alert, the place name, the probability and the temperature all travel in the link. Opening it touches no database and no storage at all, which means it costs effectively nothing however many people open it.

There's a security cost to this (anything in a URL can be edited by whoever has it), so every value is checked against a hard-coded fixed list or a valid range, and anything that doesn't parse is dropped rather than displayed. Viewing the place on a map does need a database read, so that's a link the reader has to click rather than something every recipient gets automatically.

## Put the heavy bytes where they're cheap

Most of the site is tiny. The pages are rendered on the server and weigh between 851 bytes and 2.5 KB, and a first visit including the stylesheet is about **1.6 KB.** Everything works with JavaScript switched off, and a single server instance handled about 575 requests a second (that's about 50 million views a day) in load testing at 20% CPU. A massive front-page traffic spike is well within what one small instance can absorb, and the service scales to zero when nobody's using it.

The map is the exception. The mapping library alone is about 300 KB compressed (two orders of magnitude more than the rest of the site) and map tiles are where traffic really adds up. GCP has quite high cloud egress charges, so as well as making sure the map only loads on the one page that needs it, the tiles come from a single file of UK map data hosted on Cloudflare R2, which doesn't charge for data transfer. The browser then uses range requests to read just the parts of that file it needs. There's no map provider, no API key and no per-tile fee. Thank you Cloudflare!

## A brief diversion into geocoding

Searching for places is the one part of the site that relies on a third party, and it turned out to be the part with the nastiest surprise in the terms of service. Most geocoding providers have a generous free tier, but it only covers displaying results temporarily. Storing coordinates you got from them, which is exactly what a subscription is, needs a paid licence. For the provider I started with, that was **$5 per 1,000 requests with no free tier**, which at a million sign-ups a month is roughly **$5,000 a month** for a service whose entire batch side costs tens of dollars. Again, not likely I'd ever get that much traffic, but it would be a bad month if I did ... and even a fraction of that would be noticeable. 

I looked at self-hosting the open-source alternatives (which needed a server running permanently at $30–70 a month), but in the end I built my own UK place search from open data (Ordnance Survey, ONS and OpenStreetMap), which runs on the same scale-to-zero model as everything else. The free tier covers about 25 busy instance-hours a month, which at measured throughput is several million searches, and the residual cost is a pound or two a month for storage and data transfer. 

The geosearch engine is still under active development (inferring intent from ambiguous queries is a surprisingly interesting problem), so that's a story for another post.

