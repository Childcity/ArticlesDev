---
name: scopus-article-reference-style
description: Draft or revise a research article using the paragraph structure and explanatory academic style of the supplied pseudo-Gaussian interpolation paper. Use when the user requests this reference style for a new journal manuscript, especially in applied mathematics, computational geometry, numerical modeling, or engineering.
---

# Write a research article in the reference paper's style

## Purpose and authority

Write an original, evidence-based journal manuscript in clear academic English, following the explanatory sequence of the supplied reference, "pseudo_gaussian_grid_ric_formatted (2).doc", whose English title is "Implicit curves and surfaces modeling with pseudo-Gaussian interpolation". Preserve its movement from a practical representation problem to related approaches, mathematical construction, illustrative experiments, limitations, and a restrained conclusion. Improve its grammar and precision. Do not reproduce its typographical errors, unsupported generalizations, or research-specific claims as facts about another study.

This is a self-contained writing skill. The paragraph templates and source map below provide the reference's complete textual structure; the original document is not required for future use. They are reusable paragraph models, not a verbatim transcription. Each source prose paragraph has a corresponding model or an explicitly identified language equivalent. Front matter, headings, lists, equation positions, figures, declarations, and bibliography entries are also accounted for.

The reference is a style example, not evidence that a journal is currently indexed or that a manuscript satisfies a publisher's requirements. Scopus indexing does not define a single manuscript style. Follow the selected journal's current author instructions for mandatory sections, length, references, disclosures, and formatting. If no journal is specified, use the reference structure below and describe the result as a journal-style draft. Do not claim acceptance, indexing, novelty, or readiness for submission without the necessary checks.

This file is distributed as plain text. For use as a Codex skill, save its complete contents, including the opening YAML front matter, as SKILL.md in a directory named scopus-article-reference-style. For another LLM, provide the complete file as instructions together with the study materials. Do not require another skill, a particular operating system, or access to the reference document to apply these writing instructions.

## Working inputs and missing information

Read the supplied research materials before drafting. Establish the research question, application, object being modeled or studied, existing approach, proposed contribution, definitions, assumptions, method, evidence, limitations, and intended audience. Obtain the target journal and article type if supplied. Record the available equations, datasets, code, experimental settings, results, figures, and verified references. Use supplied author details and confirmed declarations only.

Ask only for information that materially blocks an accurate manuscript. Continue with sections supported by available material. A topic alone is not enough to write a completed research paper with authentic results: in that case, produce a clearly identified proposed-study draft or manuscript framework, and mark missing evidence as {RESULT REQUIRED: description}, {SOURCE REQUIRED: claim}, or {AUTHOR CONFIRMATION: declaration}. Keep a separate short completion list outside the manuscript. Never fill a missing result with a plausible number or describe a proposed experiment as completed.

Use a private evidence ledger while writing: for each substantive claim, record the supporting supplied result, calculation, figure, or verified source. Distinguish established background, mathematical consequence, observation, interpretation, hypothesis, and future work. If tools or browsing are available, verify bibliographic details against the original publication, publisher, DOI record, or official repository. If verification is unavailable, preserve uncertainty and mark the citation for checking. Do not invent a reference, DOI, quotation, experiment, dataset, approval, or author contribution.

## The style to reproduce

Use a technical but explanatory voice. Begin with a concrete engineering or scientific difficulty. Explain why the obvious solution is unsuitable before introducing the proposed alternative. Connect each mathematical choice to its practical consequence. Show what the method can do, demonstrate where it fails, and identify the unresolved research question.

Use connected paragraphs with a topic sentence, explanation or evidence, and an implication or transition. Usually develop one main claim in three to six sentences, but retain short definition paragraphs and brief equation lead-ins when they improve the derivation. This length is guidance, not a quota. Alternate explanatory prose with equations and meaningful figures. Do not turn the manuscript into a checklist or a sequence of compressed bullet points.

Use "we" for actions performed by the authors: "We define", "We consider", "We evaluate", and "We propose". Use present tense for definitions, established relationships, figure descriptions, and the paper's argument. Use past tense for procedures actually carried out and observations already obtained. Use qualified language for interpretation: "suggests", "may", "within the tested range", and "for the configuration considered". Replace conversational expressions such as "let's", "of course", "remember", and "gone wrong" with precise academic wording.

Prefer clear verbs: define, represent, construct, interpolate, approximate, evaluate, compare, store, transmit, estimate, and verify. Retain the exact technical distinction between these verbs. Introduce abbreviations at first substantive use. Keep terminology, spelling convention, indexing, and notation consistent. Use grammatical English even when following the reference's paragraph order. Avoid inflated novelty claims, promotional adjectives, unnecessary repetition, and universal conclusions from a single example.

Useful transitions include "A common approach is ...", "However, this representation ...", "We therefore consider ...", "For clarity, we first examine ...", "Under these assumptions ...", "Figure X compares ...", "This observation suggests ...", and "The principal limitation is ...". Vary them naturally; do not begin every paragraph with the same formula.

The reference does not have a separate Results section: examples appear within the methodological development and Discussion. Retain this arrangement when appropriate. If the target journal requires separate Results and Discussion sections, move the corresponding paragraphs while preserving the definition-to-evidence-to-limitation sequence. Do not force a computational-method paper's equations or dimensional extension onto an unrelated empirical study; map their explanatory roles to the actual method and record any inapplicable slots in the private coverage check.

## Manuscript order

Use this order unless the user's instructions or journal requirements override it:

1. Classification code if required; title; authors; corresponding author.
2. Abstract, with two connected paragraphs in the reference pattern; keywords.
3. A parallel-language title, author block, abstract, and keywords only when required.
4. Abbreviations, if needed.
5. Problem statement.
6. Literature review.
7. Methods.
8. Definition of the principal function, object, mechanism, or model component.
9. Construction of the complete method, including a simpler case and a generalization when relevant.
10. Selection of the principal design variable or experimental setting, with illustrative results.
11. Discussion, including limitations, a failure case where available, parameter effects, and a focused follow-up experiment.
12. Conclusion.
13. Conflict of interest; funding; data availability; use of artificial intelligence.
14. References.

The supplied document places Ukrainian front matter before English front matter and includes an overview figure between the English abstract and keywords. Preserve these placements only when compatible with the chosen journal. In the absence of a bilingual requirement, write the English version and omit duplicate translations, without removing any distinct scientific content. Add journal-required sections such as ethics approval, author contributions, or code availability when applicable; they are additions to the reference, not sections found in it.

## How to use the paragraph templates

Source labels S001-S139 identify units in the extracted reference in their original order. They are audit labels, not paragraph numbers for the new manuscript. Some equation-table units contain both a displayed equation and the prose that follows it. These are separated explicitly below. Blank and image-only units are recorded as layout elements.

Every prose model below is complete English wording with semantic replacement fields in braces. Replace the fields with supported information and rewrite the sentences as necessary for the new study. The fields are intentional template variables, not unfinished skill instructions. Numeric citations such as [1] refer to the new manuscript's verified bibliography, not automatically to the reference paper's bibliography. Never leave unused braces, source labels, "Purpose", "Model paragraph", or editorial directions in a completed manuscript.

Preserve every relevant paragraph function in a full-length draft. Merge neighboring functions only when they remain explicit or a journal's word limit requires compression. Add methodological detail where the new study requires it. A short draft may retain the sequence at a smaller scale. Do not silently omit negative results or limitations merely to resemble a successful example.

## Complete paragraph and element library

### Front matter and abstracts

S001 — Classification code.
Include "UDC {verified classification code}" only if required by the journal. The reference uses a UDC line; do not transfer its code to an unrelated topic.

S002 — Ukrainian title.
If required, provide a natural Ukrainian equivalent of the final English title. Model: "{Дослідження або моделювання об'єкта} за допомогою {назва методу}". Preserve the contribution and scope, not the source's subject matter.

S003 — Ukrainian author line.
Use the authors' confirmed Ukrainian names in the agreed authorship order: "{Ім'я Прізвище}, {Ім'я Прізвище}, ...". Do not copy the reference's authors or infer authorship from supplied files.

S004 — Ukrainian corresponding-author line.
Model: "Автор-кореспондент: {ім'я та прізвище}, {підтверджена електронна адреса}". Add affiliations or identifiers only from confirmed information or journal requirements.

S005 — English title.
Use a specific technical title naming the object and method, such as "{Modeling/analysis/reconstruction} of {object} using {method}". Avoid claims such as "optimal", "universal", or "highly accurate" unless the evidence justifies them. A grammatically polished rendering of the reference title is "Modeling implicit curves and surfaces using pseudo-Gaussian interpolation"; this is an example, not the title of the new paper.

S006 — English author line.
Use the authors' confirmed publication names and agreed order. Follow the journal's affiliation and identifier format. Do not infer transliterations when the authors have established publication names.

S007 — English corresponding-author line.
Model: "Corresponding author: {confirmed name}, {confirmed email address}."

S008 — Ukrainian abstract, paragraph 1: context and practical obstacle.
Use only for a required parallel-language abstract. Translate the finalized English S011 faithfully. Polished model: "Розвиток {галузь або технологія} підвищує вимоги до {об'єкт або процес}. Наявні підходи дають змогу {поточна можливість}, проте їх застосування обмежене {конкретне обмеження}. Безпосередній спосіб розв'язання цієї задачі полягає в {очевидний підхід}. Однак його практичне використання ускладнюють {підтверджені технічні або організаційні причини}. Тому актуальною є задача {точне формулювання потреби}." Do not add a claim absent from the English abstract.

S009 — Ukrainian abstract, paragraph 2: conventional representation and proposed change.
Translate the finalized English S012 faithfully. Polished model: "Поширений підхід передбачає {базовий спосіб подання або оброблення даних}, після чого {спосіб відновлення або аналізу}. У цій роботі запропоновано {основна зміна методу}. Такий підхід дає змогу {ступінь свободи або нова можливість} на етапі {відповідний етап}. Результати {тип дослідження} показують {підтверджений результат} за умов {межі застосування}. Отримані результати свідчать про {обґрунтоване значення}, водночас {основне обмеження}." Use the same numbers and qualifications as in English.

S010 — Ukrainian keywords.
Provide a faithful Ukrainian keyword set corresponding to S017. Correct spelling and terminology; do not add unrelated terms merely to increase discoverability.

S011 — English abstract, paragraph 1: application, need, and inadequacy of the obvious solution.
Model paragraph: "Recent developments in {application area} have increased the need for {specific capability}. Although existing systems support {current functionality}, {precisely scoped representation, analysis, or implementation problem} remains unresolved in {setting}. A direct approach would be to {obvious solution}. However, this approach requires {technical burden} and may be unsuitable when {additional practical constraint}. These limitations motivate a representation that {desired property}."
Keep this paragraph focused on the problem. Verify historical or field-wide statements. A claim that no standard exists requires current evidence and a clearly defined scope.

S012 — English abstract, paragraph 2: baseline, contribution, and demonstrated outcome.
Model paragraph: "A common approach represents {object} by {baseline data}, from which {quantity or model} is recovered using {existing procedure}. We instead propose {specific methodological change}. This formulation permits {design choice} before {construction, storage, or evaluation stage}, allowing {mechanism of the intended benefit}. In {actual evaluation}, the method achieved {supported outcome} under {comparison conditions}. The results indicate {bounded implication}, while {principal unresolved limitation} remains to be addressed."
Include a numerical result when one is available and appropriate. Otherwise state the demonstrated qualitative outcome without inventing a metric. Do not promise equal memory use, constant evaluation cost, or improved accuracy unless the new evidence supports those claims.

S013 — Overview figure assets.
The source has a three-part visual comparison: original object, conventional model, and model with adjusted design choices. For the new study, use actual comparable outputs. Keep axes, scales, domains, and visual settings consistent. A schematic must be identified as a schematic.

S014 — Blank layout unit.
No scientific paragraph belongs here; use ordinary figure spacing if needed.

S015 — Figure 1 caption.
Model: "Figure 1. {Reference object or quantity}, its representation using {baseline}, and its representation using {proposed configuration}." Identify panels as (a)-(c) when applicable. Keep the caption descriptive; report unsupported numerical or superiority claims nowhere in it.

S016 — Blank layout unit.
Use spacing only. Do not insert filler prose.

S017 — English keywords.
Use a concise journal-compliant set covering the research object, representation, method, and application. Model: "Keywords: {object}; {method family}; {specific method}; {representation}; {application}." Reproduce neither the source's exact count nor its terms unless they fit the new work.

S018 — Abbreviations heading.
Use "Abbreviations" when the list improves readability or the journal requires it. Define terms in the text as well when required.

S019 — Abbreviation entry 1, a domain-specific format or framework.
S020 — Abbreviation entry 2, a domain-specific standard or system.
S021 — Abbreviation entry 3, a storage or representation format.
S022 — Abbreviation entry 4, a specialized methodological extension.
S023 — Abbreviation entry 5, an additional relevant format or tool.
S024 — Abbreviation entry 6, the main methodological family.
S025 — Abbreviation entry 7, the principal modeled quantity.
S026 — Abbreviation entry 8, an additional technical term used in the paper.
For every retained entry, use "{ABBREVIATION} — {verified expansion}". These eight entries mirror the source's list positions, not a requirement to invent eight abbreviations. Include only terms actually used and follow the journal's ordering rule.

### Problem statement

S027 — Heading: "Problem statement".

S028 — Practical problem, baseline representation, and its limitation.
Model paragraph: "The problem of {practical task} is closely related to the representation of {scientific object}. Retaining {complete information or process} would preserve {desirable property}, but it is often impractical because of {specific constraints}. In practice, {object or process} is therefore treated as {available interface or simplified representation}. The resulting model uses {accessible information}, and its accuracy is limited by {identified mechanism}. Under {explicit assumptions}, this limitation can be expressed as {verified bound or qualified observation}."
Do not copy the source's grid-distance error claim as a general theorem. If no bound is established, describe the limitation qualitatively and cite evidence.

S029 — Concise research objective.
Model paragraph: "We investigate whether {proposed modification} can improve {target property} while maintaining {specified resource or operational constraint}. The objective is to determine {precise research question} for {defined class of problems}."
State an aim here; reserve the answer for supported results and conclusions.

### Literature review

S030 — Heading: "Literature review".

S031 — Conventional representation and two research directions within it.
Model paragraph: "Because {direct representation} is impractical in {setting}, existing methods generally use {surrogate or structured representation} [1]. A common approach stores {data type} in {data structure}, enabling {operation or reconstruction}. Research within this framework has focused on {first improvement} [2] and {second improvement} [3]. These developments address {benefit}, but leave {relevant limitation} unresolved under {conditions}."
Explain what each source contributes. Do not attach a citation to a broader claim than the source supports.

S032 — Alternative methodological family and its trade-off.
Model paragraph: "An alternative approach uses {second method family} to represent {object or relationship} [4, 5]. In this case, the representation problem becomes one of {parameters, training, estimation, or model specification}. Different formulations balance {accuracy or fidelity} against {storage, computation, or data requirements}. Consequently, the choice of model remains dependent on {application-specific criterion}."

S033 — Position the proposed method between existing approaches.
Model paragraph: "The proposed approach combines {useful property of the first family} with {useful property of the second family}. We retain {structural feature}, but replace {existing component} with {new component}. The resulting representation stores {actual model information} and is evaluated through {core mechanism}. This distinction provides the basis for the construction developed below."
Use "combines" only if the connection is real. Otherwise explain the precise departure from the prior methods.

S034 — Adjacent literature and evidence of methodological maturity.
Model paragraph: "Related methods have also been developed for {adjacent problem}. A review by {verified authors} [6] describes {relevant scope}, while {verified authors} [7] compare {specific alternatives}. These studies establish {supported background finding}. However, their treatment of {difference in task or assumptions} does not directly resolve the problem considered here."
Use a count of reviewed studies only when checked and relevant. Do not copy the reference's review count.

S035 — Extension involving additional information or constraints.
Model paragraph: "Some formulations incorporate {additional observations, derivatives, or constraints} alongside {primary data} [8, 9]. This extension enables {supported benefit}, but requires {additional input or assumption}. Its relevance to the present work lies in {specific methodological connection}."

S036 — Selected method and reason for modification.
Model paragraph: "In this work, we adopt {specific method} [10, 11]. Its direct application is limited by {identified difficulty}. To obtain {required property}, we replace or modify {component} while retaining {essential behavior}. The resulting formulation is described in the following sections."
Establish a gap through the reviewed evidence. Do not infer global novelty merely because these selected papers do not discuss the proposed idea.

### Methods and definition of the principal component

S037 — Heading: "Methods".

S038 — Overview of the research procedure.
Model paragraph: "We derive {mathematical object or algorithm} using {actual analytical, symbolic, or computational procedure}. We then evaluate {specific properties} through {actual experiments or analyses}. The evaluation considers {test cases}, {comparators}, and {assessment criteria}, with {important settings} held fixed. The following sections describe the construction and the evidence used to assess it."
The source's methods overview is brief. Expand it as needed to report reproducible solver choices, parameter ranges, software versions, hardware when material, random seeds, stopping criteria, datasets, and uncertainty assessment. Do not describe software or experiments that were not used.

S039 — Component-definition heading.
Replace "Pseudo-Gaussian function" with the name of the new study's principal component.

S040 — Formal definition and domain.
Model paragraph: "We define {symbol or named object} on {domain} as a {type of mathematical or computational object} satisfying the following conditions. The parameter {symbol} controls {property}, while {second symbol} specifies {second property}."

S041 — First defining condition.
State the verified normalization, reference value, initial condition, or corresponding property. Model lead-in: "At {reference point or state}, {object} satisfies {condition}." Display the actual expression if mathematical.

S042 — Second defining condition.
State the verified boundary, endpoint, or termination condition. Model lead-in: "At {boundary or limiting state}, {object} satisfies {condition}."

S043 — Derivative, regularity, or compatibility conditions.
Model: "For {specified orders or indices}, {derivatives, constraints, or compatibility quantities} satisfy {verified condition}." Give the index set explicitly and do not confuse a finite set of vanishing derivatives with all derivatives.

S044 — Behavior on the first exterior region.
Model: "For {first region outside the active domain}, we set {object} equal to {defined value or behavior}."

S045 — Behavior on the second exterior region.
Model: "For {second region outside the active domain}, the same definition gives {value or behavior}." If the new model has no such region, map these boundary roles to its actual domain assumptions rather than inventing symmetry.

S046 — Intuitive explanation of the definition.
Model paragraph: "This construction reproduces {desired behavior} near {reference state}, while restricting {activity or influence} to {specified region}. The restriction is important because it permits {practical consequence}. Figure 2 compares the proposed component with {relevant reference component}."

S047 — Component-comparison image.
Show the actual functions, mechanisms, or responses being compared. Label parameters, axes, units, and line styles clearly.

S048 — Figure 2 caption.
Model: "Figure 2. Comparison of {reference component} ({line or panel designation}) and {proposed component} ({designation}) for {parameter values}."

S049 — Link between defining conditions and model regularity.
Model paragraph: "The conditions imposed on {component} determine {regularity, compatibility, or stability property} of the complete model. In particular, {justified mathematical implication}. This property controls {observable consequence} in {application}. The statement applies under {necessary assumptions}."
In mathematical papers, distinguish smoothness within a support region from smoothness across its boundary. Do not infer positive definiteness, invertibility, or approximation quality from smoothness alone.

S050 — Choose a representation and derive its constraints.
Model paragraph: "To construct {component} for prescribed {parameters}, we use {representation}. The requirement of {symmetry or structure} restricts the admissible terms to {permitted terms}. The remaining coefficients are determined by imposing {conditions}. This leads to the following system."
Justify the number of unknowns, independent constraints, and any claimed minimal degree. Do not copy the reference's degree formula without checking the actual derivation.

S051 — Equation (1), followed by the solvability explanation.
Equation role: the system that determines the component's coefficients. Insert the new study's actual system and define its unknowns.
Model paragraph: "With {parameters} fixed, the unknown quantities in Eq. (1) are {coefficients}. The system is {linear or nonlinear} in these unknowns and is solved using {actual method}. Existence and uniqueness follow from {established condition}, or are assessed numerically through {reported diagnostic}. The solution defines {component} for the selected parameter values."
Do not assert uniqueness merely because a system is square or linear.

S052 — Identify a simplification or closed-form pattern.
Model paragraph: "The solutions for {tested cases} exhibit {observed algebraic or structural pattern}. This suggests {candidate simplified representation}. For {specified cases}, the resulting expressions are given in Eqs. (2)-(5). {A derivation establishes the general identity / The pattern is currently verified only for the cases shown}."
Select the last sentence to match the evidence. Clearly distinguish a conjecture, a finite symbolic check, and a proof.

S053 — Equations (2)-(5), followed by the computational consequence.
Equation roles: four illustrative special cases or successive explicit forms. Use only as many actual cases as the new argument needs; preserve the role of showing how the general construction behaves in concrete instances. Renumber the manuscript consecutively if the count changes.
Model paragraph: "The principal distinction between {reference component} and {proposed component} is {specific structural property}. Consequently, when the component is used within {complete model}, only {relevant subset} contributes to the evaluation at {query or state}. Contributions outside {specified region or criterion} vanish or are excluded by construction. This permits {computational simplification} without changing {defined mathematical expression or validated outcome}."

S054 — Short transition from the component to the complete model.
Model paragraph: "This property allows the globally defined model to be evaluated through {local or restricted computation}. We now use the component to construct {complete method}."

### Construction of the complete method

S055 — Complete-model heading.
Replace "Pseudo-Gaussian interpolating function" with the precise name of the proposed model or algorithm.

S056 — Define the aggregate model in words.
Model paragraph: "The proposed {model} is defined as {composition of components} associated with {finite set, grid, domain, or architecture}. Each component is controlled by {coefficient or parameter}. Together, these quantities determine {modeled function or output}."

S057 — Introduce the simplest informative setting.
Model paragraph: "For clarity, we first consider {simpler case}. Let {domain or structure} contain {dimensions or number of elements}, with {origin, reference state, or indexing convention}. The spacing or relationship between neighboring elements is {definition}. The elements are therefore specified as follows."
Use separate symbols for dimension, smoothness order, sample count, and spacing; the source sometimes reuses symbols in ways that should not be imitated.

S058 — Equation (6), followed by the component definition.
Equation role: coordinates, indices, or structural arrangement of the simpler case.
Model paragraph: "At each {location or element} defined in Eq. (6), we associate {component} with {parameters}. Its value at {query point or input} is defined by {construction principle}."

S059 — Equation (7), followed by the aggregate-model lead-in.
Equation role: a single basis function, local operator, component response, or analogous unit.
Model paragraph: "Let {coefficient symbols} denote the weights associated with these components. The complete model is obtained by {summation, composition, or other actual operation}."

S060 — Equation (8), followed by evaluation-cost reasoning.
Equation role: the complete model in the simpler setting.
Model paragraph: "Although Eq. (8) is written over {entire index set}, evaluation at {input} requires only {active subset}. A component contributes when {precise activation condition}. If the number of active components is bounded independently of {total problem size}, the evaluation cost is {derived complexity} with respect to that size. This statement assumes {fixed parameters and access mechanism} and does not include {construction or preprocessing costs}."
For a regular grid with spacing h in d dimensions and compact-support radius r, a useful explicit estimate is O((1 + r/h)^d) active candidates, provided neighboring centers can be accessed directly. Calling this O(1) in total grid size requires fixed d and bounded r/h; include the cost of evaluating each basis function if its order varies. Distinguish evaluation, neighbor lookup, coefficient fitting, and storage. Do not carry over the source's O(N^2)-to-O(1) wording without defining N and the actual algorithm.

S061 — Specify the free coefficients and fitting constraints.
Model paragraph: "The quantities {coefficients} fully specify {model} once {shared metadata or structure} is fixed. To fit {target quantity}, we select {number} constraint locations or observations satisfying {admissibility condition}. Their associated values are obtained from {actual source or procedure}. Imposing {interpolation, approximation, or estimation requirement} gives the following system."
Give the relationship between the number of unknowns and observations. Explain whether the system is square, overdetermined, or underdetermined and whether regularization is used.

S062 — Equation (9), followed by solution and matrix structure.
Equation role: the fitting or interpolation system in the simpler setting.
Model paragraph: "The system is {linear or nonlinear} in {unknowns}. Because {specific structural reason}, its matrix has {sparsity or other verified structure}. We solve it using {actual solver}, with {tolerance, regularization, or stopping rule}. The resulting coefficients are associated with {model elements} and are then used to evaluate Eq. (8)."
Report conditioning and residuals when material. Local support can create sparsity, but it does not by itself establish invertibility, numerical stability, or a bounded solve time.

S063 — Introduce the generalization.
Model paragraph: "The construction extends to {higher-dimensional or more general setting} by {specific modification}. The definition of {unchanged component} is retained, while {coordinates, indexing, or operators} are expanded to account for {new feature}. The extension requires {additional assumption, if any}."
If the generalization is only theoretical, say so; do not imply that experiments in the simpler setting validate it empirically.

S064 — Define the generalized domain.
Model paragraph: "Let the generalized domain contain {dimensions or elements}, with {reference location or state} and {spacing or relationship}. We index its elements by {index set and ranges}. Their locations or relationships are defined as follows."

S065 — Equation (10), followed by a brief lead-in.
Equation role: coordinates or structural arrangement in the generalized case.
Model wording: "The corresponding {basis functions or local components} are defined by"

S066 — Equation (11), followed by a brief lead-in.
Equation role: the generalized component.
Model wording: "The complete {model} then takes the form"

S067 — Equation (12), followed by a brief lead-in.
Equation role: the generalized aggregate model.
Model wording: "The coefficients {symbols} are obtained by solving"

S068 — Equation (13), followed by the central design distinction.
Equation role: the generalized fitting or interpolation system.
Model paragraph: "In both {simpler setting} and {generalized setting}, the locations or quantities used to impose constraints need not coincide with those used to define the model components. This distinction permits {specific design freedom}. By storing {actual representation}, the proposed formulation preserves this choice at {construction stage}, while evaluation uses {fixed representation}."
For coefficient-based models, specify whether the fitting locations are needed after fitting. Account for all metadata needed to reconstruct the model. Do not imply that one scalar per node is the whole file size if origins, spacing, support parameters, precision, or other descriptors are also needed.

### Choice of the principal design variable and illustrative results

S069 — Design-choice heading.
Adapt "Choosing the interpolation points" to the study's actual design variable, for example "Selection of sampling locations" or "Choice of regularization parameters".

S070 — Identify the main variable and separate it from other controls.
Model paragraph: "The behavior of {model} depends on {principal design variable}. Other influential factors include {parameter 1}, {parameter 2}, and {parameter 3}. These parameters govern {accuracy-resource or other trade-off}, whereas {principal variable} determines {distinct effect}. We therefore examine this choice explicitly while holding {other settings} fixed."
Use observational language only if supported by actual experiments. Otherwise frame this paragraph as motivation for the planned analysis.

S071 — Define the default configuration.
Model paragraph: "A natural baseline is to set {design variable} according to {default rule}. This choice aligns {two relevant quantities} and provides a reference configuration for assessing the proposed modification."

S072 — Introduce a concrete test object and comparison.
Model paragraph: "We illustrate the construction using {test object}, shown in Figure 3. The object is evaluated on {specified domain or discretization}, with {relevant settings}. Figure 4 presents the result obtained with the baseline choice of {design variable}."
Provide the actual geometry, data source, sample count, domain, or analytic definition needed to reproduce the example.

S073 — Test-object figure.
Show the reference object and its actual discretization or experimental setting.

S074 — Figure 3 caption.
Model: "Figure 3. {Reference object or quantity} and the {grid, sampling pattern, or experimental configuration} used in the illustrative example."

S075 — Baseline-result figure.
Show the baseline under the same comparison settings as the proposed method.

S076 — Figure 4 caption.
Model: "Figure 4. {Modeled quantity or output} obtained with {baseline design rule} using {essential settings}."

S077 — Explain what the baseline already achieves and what it costs.
Model paragraph: "The baseline configuration represents {target quantity} using {stored or estimated information}. Its storage requirement is {derived or measured amount}, compared with {baseline amount} under {identical precision and metadata assumptions}. After {precomputation}, evaluation requires {actual operations}. This establishes a reference for assessing the effect of changing {design variable}."
Use equal-storage or equal-runtime wording only when all relevant quantities have been compared. Distinguish coefficient preparation from later evaluation.

S078 — Introduce the modified selection rule and intended local benefit.
Model paragraph: "We next select {design variables} according to {explicit rule}. Each {selected element} is chosen to satisfy {criterion}, subject to {constraints}. This concentrates {samples, constraints, or resolution} near {region of interest}. Figure 5 shows the resulting model and its agreement with {reference quantity} in that region."
Write the full rule, including ties, boundary behavior, feasibility checks, and parameter values when material. Do not turn a visually plausible improvement into a quantified accuracy claim without measurement.

S079 — Modified-configuration figure.
Show the new output with the same reference, axes, and visual scales used for the baseline.

S080 — Figure 5 caption.
Model: "Figure 5. {Modeled quantity} obtained using {modified selection rule} with {parameter value and unit, if applicable}."

S081 — State the limited validation status of the illustrative rule.
Model paragraph: "The selection rule examined here has been evaluated only for {actual scope}. It serves to demonstrate {principle}, rather than to establish a general-purpose procedure. The example indicates that {bounded observation}. Further evaluation is required to determine its behavior for {untested cases or conditions}."
If broader validation exists, report it accurately; do not artificially describe a mature study as preliminary merely to mirror the reference.

S082 — Explain which parts of the model remain fixed.
Model paragraph: "Changing {selection or fitting rule} modifies {coefficients or learned quantities}, while {model structure} remains unchanged. The evaluation procedure therefore continues to use {same operations}, provided that {assumptions}. The additional work is confined to {actual preparation or optimization stage}. Consequently, {supported implication for evaluation cost or representation size}."

### Discussion

S083 — Heading: "Discussion".

S084 — State the feasible region and fixed-resource trade-off.
Model paragraph: "The freedom to choose {design variable} is subject to {geometric, algebraic, or practical constraints}. In particular, {individual constraint}, and the total number of {constraints or model elements} is limited by {available degrees of freedom}. Improving agreement in {region of interest} may therefore reduce agreement elsewhere. This trade-off is appropriate when {application priority}, but may be unsuitable for {different objective}."

S085 — Explain the trade-off through a carefully bounded analogy.
Model paragraph: "This behavior is analogous to {relevant familiar concept}, in which {important information} is retained at the expense of {less important information}. The analogy concerns {specific shared property}, rather than mathematical equivalence. Which features should be preserved depends on the intended application. A representation should therefore be evaluated against {application-specific criterion}, not only against {aggregate or unrelated criterion}."
The source uses a lossy-compression analogy. Use it only when appropriate; it is not evidence of compression efficiency.

S086 — First downstream application that needs additional fidelity.
Model paragraph: "For {first downstream task}, accurate representation of {secondary property} is also required. Methods such as {verified examples} use {specific information or assumption} during {operation}. An improvement in {primary objective} does not necessarily preserve this information. Accordingly, the proposed model should be tested for {relevant consistency or downstream outcome} before it is used in this setting."
If discussing level-set extraction or contouring, accurately distinguish scalar-value interpolation, geometric sampling, and gradient requirements. Do not claim that all contouring methods require a globally linear signed distance function.

S087 — Second downstream application that requires fidelity away from the target region.
Model paragraph: "A second example is {application requiring broader fidelity}. In this setting, {operation} depends on {quantity} over {wider region or range}. Although the proposed design can emphasize selected regions, the locations needed by the downstream task may not be known in advance. The resulting mismatch limits the benefit of optimizing only {selected target}."
For implicit geometry, distinguish a scalar field with the desired zero set from a true signed distance function. Correct geometry at level zero does not establish distance accuracy, unit gradient magnitude, or correct offsets elsewhere.

S088 — Summarize the boundary of usefulness.
Model paragraph: "The ability to choose {design variable} is useful, but it does not provide uniform improvement for every application. A configuration that benefits {target task} may be less suitable for {counterexample or alternative task}. Its value must therefore be assessed in relation to the intended use."

S089 — Introduce a demonstrated failure case.
Model paragraph: "A further limitation is that controlling {fitted quantities} does not necessarily control {global shape, topology, stability, or behavior}. The reconstructed result may differ from the reference between {constraint locations or observed states}. Figure 6 presents a case in which {specific observed failure} occurs under {stated configuration}."
Use an actual observed failure, not an invented counterexample. If no failure case was evaluated, explain the untested risk or available theoretical limitation and omit the fictional experiment.

S090 — Failure-case figure assets.
Use a matched reference/result comparison that makes the failure visible. Include error, topology, or residual information when available.

S091 — Figure 6 caption.
Model: "Figure 6. {Reference quantity} and the result obtained with {configuration}, illustrating {specific observed discrepancy}." Prefer this to the source's informal phrase "gone wrong".

S092 — Compare the successful and unsuccessful cases under controlled settings.
Model paragraph: "The configuration in Figure 6 uses the same {parameters} as the example in Figure 5. The principal change is {controlled difference}. The different outcomes indicate sensitivity to {candidate factor} within the tested cases. They do not, by themselves, establish {stronger causal or general claim}."

S093 — Introduce the sensitivity factors.
Model paragraph: "The behavior of the model is governed by the following factors. Each factor affects {accuracy, regularity, or resource use} through a different mechanism."

S094 — Factor 1.
Model list item: "1. {Support, interaction range, or analogous parameter}, which controls {extent of influence}."

S095 — Factor 2.
Model list item: "2. {Order, regularity, model capacity, or analogous parameter}, which controls {smoothness or expressive capability}."

S096 — Factor 3.
Model list item: "3. {Spacing, resolution, or sample density}, which determines {discretization or information density}."

S097 — Factor 4.
Model list item: "4. {Selection, placement, or allocation rule}, which determines {where constraints or resources are concentrated}."
These four positions preserve the source's factor-list structure. Use the actual number and identity of factors in the new study; do not invent a four-factor model.

S098 — Report what is and is not established about these factors.
Model paragraph: "We investigated the effects of {factors} using {actual experiment set}. The results establish {supported finding}, but do not yet identify {unresolved relationship}. In particular, {uncertain or inconclusive observation}. A more systematic analysis of {missing coverage} is needed before a general selection rule can be proposed."
Do not imply that inconclusive results were obtained if the study did not examine the question. Distinguish untested, inconclusive, and negative findings.

S099 — First parameter: possible improvement and computational price.
Model paragraph: "Increasing {interaction-range parameter} improved {observed property} in {tested cases}, but the same change did not resolve {failure} in {other tested cases}. No general relationship has yet been established within {scope}. A larger value also increases {number of contributing components or actual cost}. The parameter must therefore be selected by balancing {measured benefit} against {resource requirement}."
If the evidence supports only one case, describe that case and omit unsupported statements about other cases.

S100 — Boundary or coverage requirement.
Model paragraph: "Because evaluation near {location or boundary} depends on {neighboring information}, the computational domain should include {required margin or coverage}. In the present implementation, this is achieved by {actual construction rule}. Figure 7 illustrates the effect of {tested margin change}."
Derive or empirically justify the margin. Distinguish a physical distance from a number of grid cells, and state how partial support at boundaries is handled.

S101 — Boundary-margin comparison assets.
Show the cases with and without the tested domain extension or coverage change.

S102 — Figure 7 caption.
Model: "Figure 7. Effect of extending {domain or coverage} by {tested amount} on {observed model property}." Do not imply that the same margin is sufficient for all problems.

S103 — Second parameter: a limited improvement and diminishing returns.
Model paragraph: "Increasing {order or capacity parameter} improved {property} over {tested range}. Beyond this range, the additional complexity produced {actual observed effect}. This suggests that {qualified interpretation}, although the available experiments do not establish {unproven general rule}. Further work should compare {alternative components or formulations} under equivalent evaluation conditions."
Do not transplant the reference's illustrative parameter values or treat smoother functions as automatically more accurate.

S104 — Third parameter: the conventional resource-accuracy trade-off.
Model paragraph: "Increasing {resolution or sample density} is a conventional way to improve {approximation or measurement quality}, at the expense of {storage and computation}. In the proposed formulation, the relationship is also affected by {method-specific behavior}. In particular, {verified distinction from the baseline}. Excessively increasing {resource} would diminish the intended advantage of {proposed representation or method}."
For interpolants, do not assume that values remain between neighboring observations unless a shape-preservation property has been proved.

S105 — Return to the central design variable.
Model paragraph: "The preceding observations motivate a closer examination of {principal design variable}. Unlike {other parameters}, this choice changes {fitted information or allocation} while leaving {specific evaluation or storage property} unchanged under {assumptions}. In the available experiments, it provided {supported benefit}. We therefore consider its selection explicitly in the following experiment."
Replace the source's strong "only consistent way" language with a claim bounded by the tested methods and cases.

S106 — Focused optimization or refinement experiment.
Model paragraph: "For the case shown in Figure 6, we retained {fixed model and selection mechanism} and varied {decision variable}. We minimized {explicit objective} over {domain} using {actual optimizer, initialization, stopping criteria, and settings}. The best value found was {reported value}, with {objective value or measured outcome}. Figure 8 shows the resulting model."
Define the objective, evaluation sample or integration domain, units, and constraints. State whether the solution is local, global, or simply the best found. Report only meaningful numerical precision. Do not copy the reference's value 0.081384 into another study. Separate calibration performance from performance on independent test cases.

S107 — Figure 8 caption and associated image.
Model: "Figure 8. {Modeled quantity} after selecting {parameter} by {optimization or refinement procedure}, with {reported value and relevant conditions}." This unit in the source includes the final result figure; include the actual result or explicitly identify a schematic.

S108 — Interpret the refinement and identify the remaining question.
Model paragraph: "The experiment indicates that {design-variable selection} should account for {case-specific feature}. The value found for {parameter} suggests {plausible interpretation}, but does not establish a general optimum. A different rule that emphasizes {relevant information} may provide {testable expected benefit}. Evaluating this possibility requires {specific additional analysis or experiment}."

### Conclusion

S109 — Heading: "Conclusion".
Use "Conclusions" instead if required by the journal. Keep this section in connected prose, following the seven functions below.

S110 — Restate the contribution and bounded overall finding.
Model paragraph: "This study presents {method} for {problem}. The approach represents {object} through {core construction} and permits {central design freedom}. The analysis and experiments demonstrate {supported overall finding} for {tested conditions}. Its principal advantage is {evidence-based benefit}, subject to {main limitation}."
Do not claim superiority to all conventional interpolation or modeling methods. Name the comparator and scope when making a comparative claim.

S111 — Summarize the computational result.
Model paragraph: "The {locality or other structural property} of the proposed method limits evaluation to {active subset or essential operations}. Under {fixed assumptions}, the resulting cost is {derived complexity or measured performance}. This result concerns {evaluation stage}; {fitting or preprocessing} has a separate cost of {known complexity or reported requirement}."
Omit unavailable complexity figures instead of inventing them. Use the same definitions and assumptions as in the Methods section.

S112 — Summarize the representation and storage result.
Model paragraph: "The representation stores {actual quantities} for each {model element}, together with {required shared metadata}. Under {precision and size assumptions}, its storage requirement is {derived or measured amount}. Compared with {specific baseline}, this corresponds to {supported storage comparison}."
State equality only when all counted quantities are equivalent. Distinguish coefficient-array size, total serialized size, and temporary fitting memory.

S113 — Summarize the distinct modeling freedom.
Model paragraph: "A central feature of the method is the ability to choose {design variables} before {model parameters} are finalized. This allows the available constraints to emphasize {region, feature, or task}. In {actual comparison}, the choice improved {specific result}, while {known trade-off} remained."

S114 — Describe practical integration or format compatibility.
Model paragraph: "Because the model uses {data structure}, it can be integrated with {verified software, workflow, or format} through {actual mechanism}. Reconstruction requires {metadata and interpretation rules}. {Implemented integration or compatibility evidence} supports this possibility; {unimplemented extension} remains future work."
If compatibility has not been tested, use conditional wording and state what must be verified. The reference names 3MF, HDF5, NRRD, and DICOM; these are not automatically suitable, standardized, interoperable, or currently supported for the new representation. Verify the relevant specification and distinguish a container that can hold bytes from software that understands their semantics.

S115 — Identify parameter-related research still needed.
Model paragraph: "The effects of {parameter group} require further investigation. A systematic study should examine {ranges and interactions} using {appropriate evaluation criteria}. This would clarify how to balance {accuracy, resources, or stability} for {intended application class}."
Name concrete unresolved questions rather than adding a generic future-work sentence.

S116 — End with the principal unresolved research problem.
Model paragraph: "The main remaining challenge is {central unresolved problem}. The procedure examined here establishes {actual demonstrated contribution}, but does not yet provide {missing general capability}. Developing and validating {specific strategy} is therefore the next step toward {practical application}."
End with a precise limitation and research direction, not an unsupported promise of widespread impact. If the new study resolves this challenge, identify its actual remaining limitation instead of preserving an obsolete one.

### Declarations

S117 — Heading: "Conflict of interest".

S118 — Conflict-of-interest statement.
Use only after confirmation. No-conflict model: "The authors declare no competing financial or non-financial interests relevant to this study." Where interests exist, state their nature and any role in the research using the journal's required wording. If unknown, use {AUTHOR CONFIRMATION: competing interests} in the draft and list it as unresolved. Do not infer the absence of a conflict.

S119 — Heading: "Funding".
This is the idiomatic equivalent of the source heading "Financing"; use the journal's prescribed label.

S120 — Funding statement.
If confirmed, model: "This research received no external funding." If funded, model: "This work was supported by {funder} under grant {verified identifier}. The funder {confirmed role in design, analysis, interpretation, and publication}." Distinguish no external grant from no financial or institutional support of any kind. If unknown, use {AUTHOR CONFIRMATION: funding and funder role}.

S121 — Heading: "Data availability".

S122 — Data-availability statement.
Use the statement that matches the actual research. Public-data model: "The data supporting the findings of this study are available in {repository} at {persistent identifier}, under {license or access conditions}." Restricted-data model: "The data are subject to {actual restriction}; access is governed by {confirmed procedure}." A no-data statement is appropriate only if no new data were created or analyzed. Computational outputs and supporting numerical files may be research data even when no external dataset was collected. Address code separately if required. If unresolved, use {AUTHOR CONFIRMATION: data and code availability}.

S123 — Heading: "Use of artificial intelligence".

S124 — AI-use declaration.
Describe the actual use and follow the selected journal's current policy. When applicable and confirmed, model: "During preparation of this manuscript, the authors used {tool and version, if required} for {specific purpose}. The authors reviewed and edited the resulting material and take responsibility for the final content." Report AI used in the research method within Methods as well, with sufficient detail for assessment. Do not copy the reference's declaration that no AI was used when an LLM has drafted, rewritten, translated, or otherwise assisted with the new manuscript. Do not assert completed author review before it has occurred. Until confirmed, mark {AUTHOR CONFIRMATION: AI assistance, review, and required disclosure}.

### References

S125 — Heading: "References".
Use numbered in-text citations in order of first appearance when the journal permits the reference's numerical style. Apply the selected journal's bibliography format consistently. Cite only works actually used. A new topic requires a new bibliography; neither the source's eleven-entry count nor its reference identities are mandatory.

The following entries account for every bibliography paragraph in the reference. Their functions help construct a literature review; they are not preverified references for a new paper. Replace each retained slot with a relevant, checked source. Use accurate author names, title, year, venue, volume, issue, page range or article number, and DOI when available. Do not invent a DOI for a work that has none. Distinguish a preprint identifier from the DOI of a published version.

S126 — Reference slot [1]: an earlier construction illustrating the complexity of direct representation.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume}({issue}), {pages or article number}. {Verified DOI URL, if available}."

S127 — Reference slot [2]: a representative structured or grid-based representation.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume}({issue}), {pages}. {Verified DOI URL, if available}."

S128 — Reference slot [3]: a method enriching the representation with additional information.
Bibliographic model: "{Authors}. ({Year}). {Paper title}. In {Official conference proceedings title} (pp. {page range}). {Verified DOI URL, if available}."

S129 — Reference slot [4]: a representative alternative model family.
Bibliographic model: "{Authors}. ({Year}). {Paper title}. In {Official conference proceedings title} (pp. {page range}). {Verified DOI URL, if available}."

S130 — Reference slot [5]: a second formulation in the alternative model family.
Bibliographic model: "{Authors}. ({Year}). {Paper title}. {Proceedings or journal title}, {volume}, {pages or article identifier}. {Verified publication identifier}." If citing a preprint instead of the proceedings version, identify it as a preprint and use its correct metadata.

S131 — Reference slot [6]: a review of the adjacent methodological literature.
Bibliographic model: "{Authors}. ({Year}). {Review title}. {Journal}, {volume}({issue}), {pages or article number}. {Verified DOI URL, if available}."

S132 — Reference slot [7]: a comparative study of related approximations or methods.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume}, {pages or article number}. {Verified DOI URL, if available}."

S133 — Reference slot [8]: a formulation using derivative information or analogous constraints.
Bibliographic model: "{Authors}. ({Year}). {Paper title}. In {Official conference proceedings title} (pp. {page range}). {Publisher, if required}. {Verified DOI URL, if available}."

S134 — Reference slot [9]: a complementary formulation using the same additional information.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume}({issue}), {pages}. {Verified DOI URL, if available}."

S135 — Reference slot [10]: a methodological antecedent of the selected interpolation or modeling approach.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume or issue as applicable}, {pages}. {Verified DOI URL, if available}."

S136 — Reference slot [11]: a further application or development of the selected approach.
Bibliographic model: "{Authors}. ({Year}). {Article title}. {Journal}, {volume or issue as applicable}, {pages}. {Verified DOI URL, if available}."

S137 — Trailing blank unit.
S138 — Trailing blank unit.
S139 — End-of-document blank unit.
These contain no scientific text. They complete the source coverage record and must not create empty paragraphs at the end of the new manuscript.

## Mathematical, experimental, and figure-writing rules

Introduce every displayed equation in prose and explain its role afterward. Define symbols, index ranges, domains, assumptions, and units at first use. Use equation numbers consecutively in the new manuscript. Treat Eqs. (1)-(13) above as reference positions, not a requirement for exactly thirteen formulas. The original file contains embedded equation objects; this skill preserves every equation's rhetorical position and purpose, rather than claiming to transcribe those objects. Derive or use the new study's actual equations.

Use separate notation for the domain, basis centers, fitting locations, coefficients, support radius, grid spacing, smoothness order, and number of samples. Check dimensions and index ranges. State the conditions for existence, uniqueness, convergence, stability, and complexity separately. If a condition is assumed rather than proved, identify it as an assumption. If a mathematical statement is uncertain, verify it or qualify it; linguistic polish must not conceal uncertainty.

Keep comparisons fair and explicit. Report the same domain, precision, evaluation points, hardware or runtime conditions when relevant, error definition, and resource budget for compared methods. State whether a result concerns local error, whole-domain error, geometry, topology, derivative fidelity, or downstream performance. These quantities are not interchangeable. Explain whether observations are deterministic examples, repeated measurements, or statistical estimates, and report uncertainty where appropriate.

For an optimization experiment, describe the objective, domain, constraints, search procedure, stopping rule, and validation design. Distinguish a better fit to calibration data from generalization. Do not present an optimizer's output as a proven global optimum unless a valid guarantee exists. Match reported precision to the evidence.

Introduce every figure before or near its placement. Use informative captions, consistent scales, units, legends, and panel identifiers. State the parameter values needed to interpret the comparison. Pair visual observations with quantitative metrics when available. A plot, schematic, or generated illustration is not a substitute for computed or measured evidence. If a figure is unavailable, provide a labeled figure specification for the draft; do not describe an unseen result as observed.

For the reference's eight-figure progression, preserve these functions when relevant: overview comparison; component behavior; reference object and domain; baseline result; modified result; failure example; boundary or coverage effect; refined result. If figures are combined or omitted for a legitimate reason, preserve the associated argument in the text and update all cross-references.

## Drafting workflow

1. Build the evidence ledger and terminology list from the study materials. Identify the contribution, comparator, claims that can be supported, and missing information.
2. Make a paragraph plan using the source functions above. Retain the practical-problem-to-method-to-limitation progression. Record where journal requirements change the organization.
3. Draft the definitions, construction, and reproducible evaluation first. Ensure that the mathematical and experimental account is correct before writing claims about it.
4. Draft the examples and Discussion, including the scope of validation, observed failures, competing explanations, and resource trade-offs. Describe only work actually performed.
5. Draft the Problem statement and Literature review so they lead to the actual contribution. Verify each source-to-claim relationship.
6. Draft the Conclusion from the demonstrated results. Then write the title and two abstract paragraphs so they agree with the manuscript. Prepare a faithful second-language version only when needed.
7. Add accurate declarations and references. Apply the journal's required structure and length. If producing Word, LaTeX, or another formatted artifact, use the environment's available authoring tools and inspect the rendered output when available.
8. Perform the coverage, language, and evidence checks below. Deliver the manuscript in the requested format, with a separate concise list of unresolved inputs if any remain.

## Completion checks

Coverage: Account for every relevant source prose function, all required front matter, and the declarations. Check the two abstract paragraphs, two problem-statement paragraphs, six literature-review paragraphs, methods overview, component definition and construction, complete-model derivation, selection example, discussion sequence, seven conclusion paragraphs, and four declaration paragraphs. The source includes short mathematical conditions and list entries; preserve their information without forcing them to become artificial long paragraphs. Check all eight figure roles and thirteen equation roles, adapting their number only when the new study or journal justifies it.

Scientific support: Ensure that every result, number, comparison, complexity claim, mathematical property, and statement of novelty has support. Verify that no results, parameter values, author details, contact information, journal status, or disclosures were accidentally inherited from the reference. Ensure that conclusions do not exceed the evidence. A two-dimensional example does not establish three-dimensional experimental performance, and one successful model does not establish robustness.

Language: Read paragraphs as an argument, not as isolated templates. Remove grammatical errors, contractions, awkward literal translations, redundant transitions, unexplained abbreviations, and inconsistent terminology. Keep uncertainty and limitations visible. Replace the source's informal or absolute formulations with precise academic equivalents. Do not mechanically repeat the same paragraph opening.

Cross-references: Check that every citation resolves to a real bibliography entry, every listed reference is used where appropriate, every equation and figure is numbered in order, and all captions and in-text references agree. Check symbol consistency throughout, including in captions and abstracts.

Declarations: Obtain or clearly mark confirmation of authorship details, competing interests, funding, data availability, and AI assistance. A draft with unresolved declarations or evidence gaps is not submission-ready. Keep the missing-information list separate from the clean manuscript, except for explicit markers needed in an incomplete draft.

Final output: Provide a complete manuscript when sufficient evidence exists. Otherwise provide the most complete supported draft possible, identify it as incomplete, and list the precise missing evidence or confirmations. Do not output this skill's audit labels or instructions as article content. Do not claim that the manuscript meets every Scopus journal's standards or guarantee publication.

## Reusable invocation

"Use the scopus-article-reference-style skill to write a research article on {topic}. The intended journal is {journal, if known}. The actual contribution is {contribution}. Use the supplied {derivations, data, code, results, figures, and verified references}. Preserve the reference's complete argumentative sequence and paragraph functions in polished academic English. Adapt the headings only where the journal requires it. Do not invent results or citations. Provide {requested output format} and a separate list of any missing evidence or author confirmations."
