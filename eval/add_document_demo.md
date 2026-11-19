# Add-document demo

Question: *¿Cuál era el salario mínimo interprofesional en 2025?* Document added: `Real_Decreto_87-2025_SMI_2025.pdf` (Real Decreto 87/2025, BOE-A-2025-2576).
Index: 788 -> 801 chunks.

## Step 1: BEFORE: a question the corpus cannot answer

**Prompt:** ¿Cuál era el salario mínimo interprofesional en 2025?

- tool call `search` {"query": "salario minimo interprofesional 2025"} -> ok: 5 passages for: 'salario minimo interprofesional 2025', most similar first.  [1] Real Decreto 126/2026, salario mínimo interprofesional para 2026 | Artículo 1 |
- tool call `search` {"query": "cuantía salario mínimo interprofesional 2025 Real Decreto 87/2025"} -> ok: 5 passages for: 'cuantía salario mínimo interprofesional 2025 Real Decreto 87/2025', most similar first.  [1] Real Decreto 126/2026, salario mínimo interprofesi

**Answer:**

No encuentro esto en los documentos. Los documentos disponibles contienen el Real Decreto 126/2026, que fija el salario mínimo interprofesional para el año 2026 en 1.221 euros al mes (o 40,70 euros al día) [B-smi-0004], pero no recogen la tabla de cuantías concretas del salario mínimo interprofesional para 2025 del Real Decreto 87/2025 [B-smi-0001].

## Step 2: NO: the assistant is asked to add the document and the answer is NO

**Prompt:** Por favor, añade este documento al corpus: /Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf

**Approval asked for `add_document`:** no
- tool call `add_document` {"path": "/Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf"} -> not_approved: The user did not approve adding this file. It was NOT added.
- tool call `search` {"query": "salario minimo interprofesional 2026"} -> ok: 5 passages for: 'salario minimo interprofesional 2026', most similar first.  [1] Real Decreto 126/2026, salario mínimo interprofesional para 2026 | Preliminar |

**Answer:**

El salario mínimo interprofesional para 2026 queda fijado en 40,70 euros al día o 1.221 euros al mes [B-smi-0004]. Esta cuantía se establece en el Real Decreto 126/2026 para cualesquiera actividades en la agricultura, la industria y los servicios [B-smi-0004].

## Step 3: YES: you approve adding the document

**Prompt:** Por favor, añade este documento al corpus: /Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf

**Approval asked for `add_document`:** yes
- tool call `add_document` {"path": "/Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf"} -> ok: Added 'Real_Decreto_87-2025_SMI_2025' (source name: real_decreto_87-2025_smi_2025): 13 passages, 2163 words. It can be searched now.
- tool call `search` {"query": "Real Decreto 87 2025 SMI 2025"} -> ok: 5 passages for: 'Real Decreto 87 2025 SMI 2025', most similar first.  [1] Real_Decreto_87-2025_SMI_2025 | Preliminar | p. 1 | id B-real_decreto_87-2025_smi_2025

**Answer:**

El salario mínimo interprofesional para 2025 queda fijado en 39,47 euros al día o 1184 euros al mes, según esté fijado por días o por meses [B-real_decreto_87-2025_smi_2025-0004].

## Step 4: AFTER: the same question again

**Prompt:** ¿Cuál era el salario mínimo interprofesional en 2025?

- tool call `search` {"query": "salario minimo interprofesional 2025"} -> ok: 5 passages for: 'salario minimo interprofesional 2025', most similar first.  [1] Real_Decreto_87-2025_SMI_2025 | Artículo 1 | p. 2 | id B-real_decreto_87-2025_s

**Answer:**

En 2025, el salario mínimo interprofesional quedó fijado en 39,47 euros al día o 1.184 euros al mes, según estuviera fijado por días o por meses [B-real_decreto_87-2025_smi_2025-0004]. Esta cuantía se estableció mediante el Real Decreto 87/2025 para cualquier actividad en la agricultura, la industria y los servicios [B-real_decreto_87-2025_smi_2025-0001, B-real_decreto_87-2025_smi_2025-0004].

## Step 5: TWICE: add the same file again

**Prompt:** Por favor, añade este documento al corpus: /Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf

**Approval asked for `add_document`:** yes
- tool call `add_document` {"path": "/Users/tessacorreig/Documents/daiist-assignment-3/demo/Real_Decreto_87-2025_SMI_2025.pdf"} -> ok: Skipped: 'Real_Decreto_87-2025_SMI_2025' is already indexed (added before as Real_Decreto_87-2025_SMI_2025.pdf). Nothing was changed.
- tool call `search` {"query": "Real Decreto 87 2025 SMI"} -> ok: 5 passages for: 'Real Decreto 87 2025 SMI', most similar first.  [1] Real_Decreto_87-2025_SMI_2025 | Preliminar | p. 1 | id B-real_decreto_87-2025_smi_2025-0001

**Answer:**

El Real Decreto 87/2025 fija el salario mínimo interprofesional para el año 2025 en 39,47 euros al día o 1184 euros al mes [Real_Decreto_87-2025_SMI_2025 | Artículo 1 | p. 2 | id B-real_decreto_87-2025_smi_2025-0004]. Este documento ya se encontraba previamente añadido en el corpus.

## Step 6: RENAMED: add a copy of the file under another name

**Prompt:** Por favor, añade este documento al corpus: /Users/tessacorreig/Documents/daiist-assignment-3/demo/copia_del_decreto.pdf

**Approval asked for `add_document`:** yes
- tool call `add_document` {"path": "/Users/tessacorreig/Documents/daiist-assignment-3/demo/copia_del_decreto.pdf"} -> ok: Skipped: 'Real_Decreto_87-2025_SMI_2025' is already indexed (added before as Real_Decreto_87-2025_SMI_2025.pdf). Nothing was changed.
- tool call `search` {"query": "añadir documento corpus smi reales decretos"} -> ok: 5 passages for: 'añadir documento corpus smi reales decretos', most similar first.  [1] Real Decreto 126/2026, salario mínimo interprofesional para 2026 | Preli

**Answer:**

No encuentro esto en los documentos. Los documentos cubren las cuantías del salario mínimo interprofesional (Real Decreto 126/2026) y las reglas de incorporación de complementos salariales [B-smi-0005].
