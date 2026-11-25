"""One-time snapshot creator, not required at grading time.

The bundled source texts were extracted from Python 3.13's locally installed
pydoc_data.topics (generated from docs.python.org), under the PSF License.
Do not re-run against another Python version without reviewing citations.
"""
from pathlib import Path
import sys
import json
from pydoc_data.topics import topics
from collections import Counter

if sys.version_info[:2] != (3, 13):
    raise SystemExit('This script requires Python 3.13; otherwise 3.12 docs could be mislabeled as 3.13')

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'source_docs'; OUT.mkdir(exist_ok=True)
groups = {
 'data_model': ('Python Language Reference: Data Model','https://docs.python.org/3.13/reference/datamodel.html', ['objects','types','specialnames','customization','attribute-access','context-managers','numeric-types','sequence-types','callable-types','typesfunctions','typesmethods','typesmodules','bltin-code-objects','bltin-type-objects','bltin-ellipsis-object','bltin-null-object','specialattrs']),
 'expressions': ('Python Language Reference: Expressions','https://docs.python.org/3.13/reference/expressions.html', ['atom-identifiers','atom-literals','attribute-references','subscriptions','slicings','calls','await','power','unary','binary','shifting','bitwise','comparisons','booleans','assignment-expressions','lambda','exprlists','dict','lists','in','conversions','operator-summary']),
 'simple_statements': ('Python Language Reference: Simple Statements','https://docs.python.org/3.13/reference/simple_stmts.html', ['assignment','augassign','assert','pass','del','return','yield','raise','break','continue','import','global','nonlocal']),
 'compound_statements': ('Python Language Reference: Compound Statements','https://docs.python.org/3.13/reference/compound_stmts.html', ['compound','if','else','while','for','try','with','function','class','async']),
 'execution_model': ('Python Language Reference: Execution Model','https://docs.python.org/3.13/reference/executionmodel.html', ['execmodel','naming','dynamic-features','exceptions']),
 'lexical_analysis': ('Python Language Reference: Lexical Analysis','https://docs.python.org/3.13/reference/lexical_analysis.html', ['identifiers','id-classes','strings','numbers','integers','floating','imaginary']),
 'builtin_types': ('Python Library Reference: Built-in Types','https://docs.python.org/3.13/library/stdtypes.html', ['truth','typesseq','typesseq-mutable','typesmapping','string-methods']),
 'string_formatting': ('Python Library Reference: String Formatting','https://docs.python.org/3.13/library/string.html', ['formatstrings']),
}
used=[k for _,_,ks in groups.values() for k in ks]
print('unused',sorted(set(topics)-set(used)))
print('dupes', [k for k,n in Counter(used).items() if n>1])
manifest=[]
for group,(title,url,ks) in groups.items():
 filename=f'{group}.md'
 lines=[f'# {title}', '',f'Source URL: {url}', 'Reference version: Python 3.13', 'Licence: Python Software Foundation License Version 2 (https://docs.python.org/3.13/license.html)', 'Local extraction: CPython 3.13 pydoc_data.topics generated from the official documentation', '']
 for k in ks:
  text=topics[k].strip()
  lines.extend([f'### TOPIC: {k}',text,''])
 path=OUT/filename
 path.write_text('\n'.join(lines), encoding='utf-8')
 manifest.append({'source':group,'title':title,'file':filename,'url':url,'license':'PSF License 2.0','version':'3.13','words':sum(len(topics[k].split()) for k in ks),'topics':ks})
 print(group,len(ks),sum(len(topics[k].split()) for k in ks))
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(OUT/'LICENSE-ATTRIBUTION.md').write_text('''# Source and licence\n\nThese snapshots reproduce extracts of the **Python 3.13 documentation** generated into CPython’s `pydoc_data.topics` standard-library module. Official documentation is published at https://docs.python.org/3.13/ and licensed under the Python Software Foundation License Version 2: https://docs.python.org/3.13/license.html.\n\nEach file records the public source URL. `manifest.json` records the topics used, document version and word count. The sections are regrouped into original reference-page categories (and one library formatting category), not independently authored documents. The corpus is for educational research; check the current version of the Python documentation for operational decisions.\n\n`incoming/pdb_reference.md` is an optional **holdout** document, excluded from the initial corpus, for a controlled before/after add-document experiment.\n''')
print('Total corpus words:',sum(row['words'] for row in manifest))
# An official document held out from the initial corpus for the add-document experiment
incoming=ROOT/'incoming';incoming.mkdir(exist_ok=True)
(incoming/'pdb_reference.md').write_text('\n'.join(['# Python Library Reference: pdb — The Python Debugger', 'Source URL: https://docs.python.org/3.13/library/pdb.html', 'Reference version: Python 3.13','Licence: Python Software Foundation License Version 2 (https://docs.python.org/3.13/license.html)','', '### TOPIC: debugger', topics['debugger'].strip(), '']),encoding='utf-8')
