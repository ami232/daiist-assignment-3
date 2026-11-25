# Adding a document: before and after

**Unanswerable question (q28):** How many inches of snow in 12 hours trigger a Winter Storm Warning in Memphis, Tennessee?

## Before (from the evaluation run, `eval/answers.jsonl`)

> The corpus does not cover the specific local snow criteria for Memphis, Tennessee. 
> 
> NWS local warning criteria are set by individual regional and local offices (with specific heavy snow criteria maintained online at www.weather.gov/snow-criteria) [NWSI-10-513, section App-D, pp. 41-42].

## Adding the document through the agent (approval step)

```
$ uv run python agent.py 'Please add the file extra_documents/NWS-Memphis-Winter-Criteria.pdf to the corpus.'

The agent wants to add 'extra_documents/NWS-Memphis-Winter-Criteria.pdf' to the index. Allow? [y/N] y
  [sections] saved 3/3 new vectors
```

Document: NWS Memphis, "Criteria for Winter Storm Watches/Warnings and Winter Weather Advisories", https://www.weather.gov/media/meg/WinterStormCriteriaMEG.pdf (public domain), 3 chunks.

Adding the same file again:

```
Already indexed: NWS-Memphis-Winter-Criteria (3 chunks) has not changed, so nothing was embedded.
```

## After

```
$ uv run python main.py ask "How many inches of snow in 12 hours trigger a Winter Storm Warning in Memphis, Tennessee?"
```

> For areas covered by the NWS Memphis office that fall under "elsewhere" (which includes Shelby County / Memphis), a Winter Storm Warning for heavy snow requires accumulations of **3 inches or more in 12 hours** (or 4 inches or more in 24 hours) [NWS-Memphis-Winter-Criteria, p. 1].
>
> *(Note: Forecasters also have discretion to issue warnings for severe impacts to travel, commerce, or life and property even if numerical criteria are not fully met [NWS-Memphis-Winter-Criteria, p. 2].)*

[1 tool call, 3,247 + 148 tokens, 9.8 s]
