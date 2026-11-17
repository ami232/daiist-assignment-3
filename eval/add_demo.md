# Adding a document: before and after

Unanswerable test question q31; added document: Wikipedia, *Padel* (CC BY-SA 4.0), as plain text.

### 1. Before (original corpus)

**Q:** What is the maximum length of the wrist safety cord attached to a padel racket?

**A:** The corpus does not cover this; it only mentions that the handle end must have a non-elastic cord put around the wrist as protection against accidents, without specifying a maximum length [blanes2022 p.2].

Tool calls: search({"query": "maximum length of the wrist safety cord attached to a padel racket"}), search({"query": "wrist safety cord maximum length padel racket"})

Approvals: []

### 2. Add the document (human approval required)

**Q:** Please add the document corpus/extra/padel_wikipedia.txt to the corpus.

**A:** The document `corpus/extra/padel_wikipedia.txt` has been successfully added to the corpus (13 chunks embedded). You can now ask questions related to its content, and I will cite it accordingly.

Tool calls: add_document({"path": "corpus/extra/padel_wikipedia.txt"})

Approvals: [{'event': 'approval', 'tool': 'add_document', 'args': {'path': 'corpus/extra/padel_wikipedia.txt'}, 'approved': True}]

### 3. After

**Q:** What is the maximum length of the wrist safety cord attached to a padel racket?

**A:** The handle of a padel racket must feature a non-elastic safety cord with a maximum length of 35 centimetres (14 in) [padel_wikipedia p.1].

Tool calls: search({"query": "wrist safety cord maximum length padel racket"})

Approvals: []

### 4. Adding the same file again

**Q:** Please add the document corpus/extra/padel_wikipedia.txt to the corpus.

**A:** The document `corpus/extra/padel_wikipedia.txt` is already indexed in the padel corpus.

Tool calls: add_document({"path": "corpus/extra/padel_wikipedia.txt"})

Approvals: [{'event': 'approval', 'tool': 'add_document', 'args': {'path': 'corpus/extra/padel_wikipedia.txt'}, 'approved': True}]
