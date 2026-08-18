---
title: Search method shootout
subtitle: using a benchmark on a specific task
date: 2026-08-10
---
*Second of three posts. [Part 1](/read/careful_design_beats_clever_tools.html) covered building an honest benchmark honest enough to trust. This post is the reference companion: each retrieval method in turn — how it works, where it came from, what it typically scores in the literature, how we implemented it, and how it did on our data.*  

---

A note on the numbers: Results quoted below are MRR@10 on the benchmark set of UK Parliamentary Questions. MRR is Mean Reciprocal Rank … 0.5 means the first genuinely-correct answer typically sits around position two of the 10 items retrieved. 0.8 means it's usually right at the top. For comparison with “our results” I’m also quoting typical results for the various methods on standard datasets … MS MARCO passage dev in this case.   

---

## 1. BM25 (keyword search)

**How it works:** BM25 scores a document by how often the query's words appear in it, taking account of two extra factors: *saturation* (the tenth occurrence of a word adds far less than the second) and *length normalisation* (a match in a short document counts for more than one buried in a long document). 

**History:** Okapi BM25 came out of Robertson and Walker's work at City University London in the mid-1990s (building on the probabilistic relevance framework of the 1970s). It is still the default ranking function in Lucene, Elasticsearch and OpenSearch \- which means it quietly powers a very large fraction of the world's search boxes.

**Typical results:** Around **0.18–0.19 MRR@10** on MS MARCO.

**Implementation notes.** I used `bm25s`, a fast pure-Python implementation (100–500× quicker than `rank_bm25`, near-Lucene quality). It runs on CPU, the index is a few hundred megabytes, and lookups are sub-millisecond. BM25 is seriously quick, which is exactly why it's the baseline to beat.

**Our result:** **0.56** **MRR@10** \[0.54–0.57\]. Notably stronger than its MS MARCO reputation, precisely because PQ answers share wording with their questions. A genuinely strong, nearly-free baseline. This is honestly a good enough result for production use on our data, but I suspect we can do better. 

## 2. RM3 query expansion (pseudo-relevance feedback)

**How it works.** Run the search once, *assume* the top handful of results are relevant, harvest the words that distinguish them from the rest, add those to the query, and search again. The idea is to bridge vocabulary gaps - if the answer says "clinician" and you asked about "doctors", expansion can pull it in.

**History.** Relevance models are Lavrenko and Croft (2001); RM3 is the widely-used interpolated variant. Pseudo-relevance feedback is one of the oldest tricks in information retrieval and adds a lot for classic news/legal collections.

**Typical results.** While it *helps* on those older collections, it is well documented to *hurt* on MS MARCO passage, where judgements are sparse and a single wrong assumption in the first pass drags the expanded query off-topic ("query drift").

**Implementation notes.** A standard PRF pass layered on top of our BM25 index. This needs a second retrieval round, so roughly double the query cost, still CPU-only and still very quick.

**Our result:** fair **0.50** \[0.48–0.51\] *below* plain BM25. On this data the expansion added more drift than signal, exactly matching the MS MARCO pattern. A useful reminder that fancier is not a synonym for "better". This is why we benchmark. 

## 3. SPLADE (learned sparse retrieval)

**How it works.** SPLADE keeps keyword search's cheap, inspectable inverted index but replaces hand-tuned term statistics with a language model. A model predicts, for every word in its vocabulary, how strongly a document is "about" that word — *including words the document never uses* (so a passage about pensions can score well for "retirement" without actually containing that word). The result is a sparse, weighted, expanded bag of words that can be searched very efficiently. 

**History.** SPLADE is Formal, Piwowarski and Clinchant at Naver Labs Europe (2021), refined through SPLADE++ to **SPLADE-v3** (2024).

**Typical results.** SPLADE-v3 reaches **0.42 MRR@10** on MS MARCO. 

**Implementation notes.** I used the `naver/splade-v3` model from Huggingface. SPLADE is (should be) the best of both worlds … encoding is compute-intensive and happens on GPU; but search is sparse dot-product on CPU. 

**Our result:** **0.58** **MRR@10** \[0.57–0.60\] — statistically tied with BM25 (the intervals overlap). SPLADE's learned expansion is its edge on MS MARCO, but on a corpus where questions already echo their answers, BM25 was getting most of that benefit for free, so the expansion had little left to add. At this point I was starting to question whether this was going anywhere. 

## 4. Dense semantic search (off the shelf model)

**How it works.** A bi-encoder embeds the question and every candidate answer into the same high-dimensional vector space, trained so that a question lands near its answer. Retrieval is then nearest-neighbour search by cosine similarity, so a question and its answer can match on *meaning* even with no shared words at all. This is what most people today mean by search using "AI embeddings".

**History.** DPR (Karpukhin et al., 2020) made dense retrieval competitive; contrastive pre-training then made it general-purpose: Contriever (Izacard et al., 2021), E5 (2022), BGE (2023), and the current crop of instruction-tuned embedding models.

**Typical results.** Strong bi-encoders land around **0.33–0.40 MRR@10** on MS MARCO

**Implementation notes.** I used `jina-embeddings-v5-text-small` — a 0.6B parameter model on a Qwen3 backbone with a retrieval adapter. This was the strongest sub-1B open-weight model on the MTEB multilingual leaderboard at the time, which keeps the fine-tune (next section) affordable. Using embeddings at scale needs an index - I used **FAISS flat (exact) search** rather than an approximate index. This isn’t necessarily needed for production, but gets rid of a layer of noise in the results. 

**Our result:** **0.74** **MRR@10** \[0.72–0.75\]. Boom. A clear step above every lexical method, even untuned. And because it was being tested on questions published *after* the model's training cut-off (Part 1's memorisation control), we can be confident that advantage comes from skill, not regurgitated training data.

## 5. Dense semantic search (fine-tuned model)

**How it works.** Exactly the model above, given a training pass on *our* question→answer pairs so the vector space is shaped to this domain. I used use a contrastive objective (`MultipleNegativesRankingLoss`: pull each question toward its answer, push it away from every other answer in the batch) with specifically chosen hard negatives.

**History.** In-domain fine-tuning of bi-encoders is standard practice and consistently the highest-return step available — yet it's the one teams most often skip in favour of reaching for a flashier method or getting an existing model into production quickly. 

**Typical results.** Fine-tuning a decent base on in-domain pairs commonly adds **0.05–0.15 MRR** over off-the-shelf, depending on how far the domain sits from the model's pre-training.

**Implementation notes.** a LoRA adapter trained on the frozen backbone, on a rented A100 GPU for a few hours. Crucially the fine-tuning used the *train* split only and the evaluation was done on the untouched later slice.

**Our result:** **0.81 MRR@10** \[0.80–0.83\]. +0.07 over the same model off-the-shelf. A decent jump for a cost you basically only have to pay once when you fine-tune the model. After that it’s the same in production as using the off the shelf version. 

## 6. Hybrid (reciprocal rank fusion)

**How it works.** Run two retrievers (here: fine-tuned dense and BM25) and merge their ranked lists by Reciprocal Rank Fusion - each document scores the sum of 1/(k + its rank) across the lists, so a document ranked highly by *either* method floats up. The theory: lexical and semantic search fail on different questions, so their union should be stronger than either.

**History.** RRF is Cormack, Clarke and Büttcher (2009). It's everywhere in production because it's parameter-light, needs no score calibration between systems, and rarely makes things worse.

**Typical results.** Fusing complementary rankers usually buys a small, consistent gain — and is often the easy last few points in a competition system.

**Implementation notes.** Weighted RRF, with the dense/BM25 weight swept on the dev slice and then applied to test exactly once. In production running this costs the sum of both pipelines plus a trivial fusion step.

**Our result:** **0.82** **MRR@10** \[0.81–0.84\].  Statistically indistinguishable from fine-tuned dense alone. On this data, once the embedding model was tuned it had already captured what BM25 would have contributed, so the hybrid added nothing measurable. Hybrids often earn their keep; here the fine-tune got there first. Worth noting that in some production use-cases the keyword bit carries more weight: if you’re searching for a person’s name, for instance. 

## 7. A frontier API model: (Gemini)

**How it works.** Instead of hosting an embedding model, you call one. Google's `gemini-embedding-001` is a frontier-scale embedding model sitting behind an API: send text, get a 3072-dimensional vector back. It sits at or near the top of the public MTEB leaderboard, and it uses **Matryoshka** dimensions, which means you can truncate the 3072-vector to 1024 (or 768) with almost no quality loss (I measured 0.798 at 1024 vs 0.802 at full width), so it drops straight into a 1024-dim index.

**History.** The lineage runs from Google's `text-embedding` models to the Gemini-family embeddings (generally available in early 2026). Matryoshka Representation Learning (Kusupati et al., 2022\) is the trick that lets one model serve many dimensionalities from a single vector.

**Typical results.** Frontier API embedders (Gemini, OpenAI `text-embedding-3-large`, Voyage, Cohere) top the public leaderboards, above every open sub-1B model.

**Implementation notes.** I called it on Vertex AI, batch endpoint, at **$0.075 per million tokens** (batch). Encoding the entire benchmark (271k documents plus the query sets, \~50M tokens) cost **under $4**. Two things you *cannot* do, though, and both matter: you cannot **fine-tune** it (it's a black box), and every document you encode **leaves your infrastructure** for a US API.

The fine-tuning thing took me down a bit of a dead end. Since the Gemini model is frozen and closed, one option is a small **projection head**: take Gemini's 3072-vector and train a little network on our question→answer pairs to reshape it toward our domain. It **did nothing** - 0.803 with the head versus 0.802 raw. But this could be an interesting technique for “translating” between embedding models … project them all into the same embedding space using a trained adapter and you can swap the backend model. Normally you’re stuck with the one you started with, which creates risk if the model is discontinued etc. 

**Our result:** **0.80** **MRR@10** \[0.79–0.81\]. Read that against the fine-tuned jina model's 0.81 \[0.80–0.83\]: the confidence intervals overlap almost entirely. **A frontier general model, out of the box, matches our domain-fine-tuned specialist.** Depending on where you sit that's either deflating or liberating.

## The scoreboard

| Method | Fair MRR@10 | 95% CI |
| :---- | :---- | :---- |
| Hybrid (tuned dense + BM25) | **0.82** | \[0.81–0.84\] |
| Dense, fine-tuned (jina) | **0.81** | \[0.80–0.83\] |
| **Frontier API (Gemini)** | **0.80** | \[0.79–0.81\] |
| Dense, off-the-shelf | **0.74** | \[0.72–0.75\] |
| SPLADE (learned sparse) | 0.58 | \[0.57–0.60\] |
| BM25 (keyword) | 0.56 | \[0.54–0.57\] |
| RM3 (query expansion) | 0.50 | \[0.48–0.51\] |

So, we have two methods that are basically tied at ~0.8. Which one to pick depends on what the production workload looks like. If you’ve got enough documents coming in through the day to keep a small GPU spinning then the fine-tuned local model works out pretty cheap and you get to own the model itself with no upstream dependencies … but you do have to manage infrastructure. If your workload is lumpy, or you just want an easy life, then the API route is likely to be the clear winner. 
