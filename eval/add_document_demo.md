# Add-document demo

**Question (q34, unanswerable in the evaluated corpus):** How is the summary risk indicator class from 1 to 7 calculated for a PRIIP?

**Document added:** Commission Delegated Regulation (EU) 2017/653, the PRIIPs regulatory technical standards (`reserve/CELEX_32017R0653_EN_TXT.pdf`, source name `PRIIPs RTS`, 92 chunks in the `sections` design), added through the agent with `add_document` after approval at the terminal.

## Before (from the evaluation run, `eval/answers.jsonl`)

> The provided corpus does not contain the specific calculation methodology for the summary risk indicator class (1 to 7) for a PRIIP. It notes that the methodology underpinning the presentation of risk and reward is to be specified in regulatory technical standards [PRIIPs | Article 8, p. 13].

3,356 tokens, 1 search.

## After (`main.py ask`, with the PRIIPs RTS indexed)

> The Summary Risk Indicator (SRI) for a PRIIP is determined by applying the methodology for the presentation of risk set out in Annex II and the technical aspects for the presentation of the SRI set out in Annex III [PRIIPs RTS | Article 3 (‘What are the risks and what could I get in return?’ section), pp. 6-7].
>
> Market risk is measured by the annualised volatility corresponding to the value-at-risk (VaR) at a confidence level of 97,5 % over the recommended holding period [PRIIPs RTS | ANNEX II (METHODOLOGY FOR THE PRESENTATION OF RISK), p. 15]. The PRIIP is assigned a Market Risk Measure (MRM) class according to the following table [PRIIPs RTS | ANNEX II (METHODOLOGY FOR THE PRESENTATION OF RISK), p. 15]:
>
> | MRM class | VaR-equivalent volatility (VEV) |
> | :--- | :--- |
> | 1 | < 0,5 % |
> | 2 | 0,5 % - 5,0 % |
> | 3 | 5,0 % - 12 % |
> | 4 | 12 % - 20 % |
> | 5 | 20 % - 30 % |
> | 6 | 30 % - 80 % |
> | 7 | > 80 % |
>
> For the purposes of determining market risk, PRIIPs are divided into four categories [PRIIPs RTS | ANNEX II (METHODOLOGY FOR THE PRESENTATION OF RISK), p. 15]. The SRI is presented in the key information document using a numerical scale from 1 to 7, where 1 is the lowest risk class and 7 is the highest [PRIIPs RTS | ANNEX III (PRESENTATION OF SRI), p. 26].

8,477 tokens, 9.95 s, 1 search. The citation guardrail fired on the first draft (tags shortened to `Annex II, p. 15`, `Article 3, p. 6`, and two tags merged into one); the agent's rewrite used the exact tags.

## Already indexed

`add_document` identifies a document by its name (the file name, mapped to `PRIIPs RTS`). The same file with identical content (same SHA-256) is skipped and nothing is re-embedded; a changed file has its old chunks removed and the new ones embedded.
