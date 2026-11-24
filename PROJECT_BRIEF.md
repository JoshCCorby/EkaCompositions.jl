# Eka: A Project Brief

This document is a narrated explanation of the repository called Eka, written for
an intelligent listener with no background in materials science, machine learning,
or scientific software engineering. It is built from the repository's own README,
its twenty-seven documentation files, its source code, its test suite, its git
history, and the local evidence directories that the project deliberately keeps
out of version control.

Throughout, I separate two kinds of statement. When I say something is stated,
recorded, or documented, it comes from a file in the repository. When I begin a
sentence with "It appears that", I am drawing a conclusion that the repository
does not state outright. Each section ends with a short note on how confident
each part is and where the repository simply does not say.

One practical note before we begin. The repository contains a set of local
directories that are excluded from version control by design, holding the actual
numerical results of the experiments. Those directories are present on the
owner's machine and I have read them, so some numbers in this brief come from
material the project has explicitly chosen not to publish. The project's own
documents describe those results in aggregate; the per-split tables are local.

---

## Episode 1 — What this project is and why it exists

### The problem, in one paragraph

There are far more chemically plausible combinations of elements than anyone has
ever made in a laboratory. Chemists would like a shortlist: given what we already
know about which combinations form real compounds, which untried combinations are
worth the effort of trying? Several research groups have built recommendation
systems for exactly this, borrowing the mathematics that suggests films on a
streaming service. Eka does not try to build a better recommender. It asks a
narrower, more sceptical question: when you test such a system by hiding known
compounds and seeing whether the ranking finds them again, how much of the
apparent success is skill, and how much is an artefact of how you hid them?

That is the whole idea. Hide some known compounds. See if a ranking pulls them
back to the top. Then interrogate, obsessively, whether the test was fair.

### Who built it, and when

The repository names a single author, Joshua Corbett, in its citation metadata,
its licence, and its documentation. The git history shows forty-seven commits by
that one person, plus a handful of automated dependency-update commits from a bot
and the merge commits accepting them. There are no other human contributors.

The timeline is remarkably compressed. The first commit, labelled "Initial Eka.jl
package", is dated 30 August 2026. The most recent, a release commit tagged
version 0.1.1, is dated 7 September 2026. That is nine days from nothing to a
tagged, documented, continuously-tested software package with four frozen
research protocols and a completed benchmark series.

Within those nine days, one day dominates. On 31 August 2026 there are roughly
twenty commits, and they carry the entire scientific arc of the project. The
messages read almost like a lab notebook: add a Materials Project snapshot
exporter and provenance audit, freeze the recovery protocol, add composition-safe
splits, add positive-unlabelled evaluation, add a similarity comparator, exclude
external scores from the primary comparison, add label-sensitivity workflows, add
a chemical-system holdout study, evaluate a fixed-compute element-pair comparator
and package the findings. Every documented protocol in the repository carries the
date 31 August 2026.

The days that follow are different in character. From 4 September onward the
commits are about packaging rather than science: a public interface contract, an
engineering roadmap, package-quality automation, a contributor guide, a
documentation website, a pre-release checklist. Two version tags exist, 0.1.0 on
4 September and 0.1.1 on 7 September.

It appears that the project ran as a single intense research sprint followed by a
deliberate, slower consolidation into something releasable. The engineering
roadmap document, dated 4 September, says as much in its own framing: it covers
"software packaging and documentation quality" and explicitly states that it
"does not propose new science".

### What the project actually produces

It produces four things, and it is careful to say it does not produce a fifth.

It produces a software library written in Julia, called EkaCompositions, with a
command-line program called `eka`. The library reads databases of precomputed
chemical scores, ranks compositions by those scores or by a simple geometric
similarity measure, imports new score tables, and audits databases for records it
cannot safely interpret.

It produces evaluation machinery: a way to snapshot a public materials database,
group its records into chemical compositions, label them by how much experimental
evidence they carry, split them deterministically into training and test sets,
rank the test set by several methods, and measure how many hidden compounds each
method recovered.

It produces four frozen research protocols. These are documents that specify, in
advance and in exhaustive detail, exactly what an experiment will do, before any
result is looked at. The software then refuses to run unless the protocol
document's bytes still hash to the exact value recorded in the code. If you edit
a single character of the protocol, the experiment stops.

And it produces a findings document: a completed benchmark series comparing four
ranking methods across two experimental designs and three labelling rules.

What it explicitly does not produce is a validated discovery model. The release
notes for version 0.1.1 state this in bold: "This is a reproducible ranking
benchmark, not a validated discovery model." The README's scope and limitations
section repeats it from several angles. The project also declines to publish its
record-level data, its rankings, its fitted model parameters, or its computing
environments, on the grounds that the permissions for redistributing
database-derived material had not been fully resolved.

### The central claim

The project's central finding is deflationary, and I think that is what makes it
interesting.

The first experiment held out a fifth of the known compounds at random, one
composition at a time, and asked whether ranking candidates by their chemical
similarity to the training set beat ranking them by how popular their constituent
elements were. Similarity won, but barely: it recovered on average half a
compound more per hundred candidates than the popularity baseline did, across
twenty repeated splits, with ten splits favouring similarity, three ties, and
seven favouring popularity.

The second experiment changed how the compounds were hidden. Instead of hiding
individual compositions, it hid whole chemical systems. A chemical system is just
the set of elements involved, ignoring proportions. Barium, titanium, and oxygen
form one system; strontium, titanium, and oxygen form another. Under the first
design, if barium titanate was in the training set, other barium-titanium-oxygen
compounds could still appear as candidates. Under the second, if the system was
held out, every compound in it was held out.

Under that harsher design, the similarity method did not merely lose its
advantage. It collapsed below chance. Its average recovery of twenty-nine to
thirty compounds per hundred candidates was worse than the roughly thirty-two to
forty-three that pure random selection would be expected to achieve on those same
candidate pools.

That reversal is the project's most substantive result. The findings document
states it directly: maximum cosine similarity to the training set is useful
"chiefly when system proximity is permitted", and forbidding that proximity makes
it "anti-predictive in these system-holdout pools". In plainer words: the
similarity method was not recognising promising chemistry. It was recognising
that a candidate looked almost exactly like something it had already seen.

The project then built a fourth method, a small learned model of which pairs of
elements tend to occur together, and found the mirror image: that model did
nothing useful under composition holdout, but beat the popularity baseline under
system holdout. It then immediately undercut its own good news by pointing out
that under system holdout every compound sharing a system gets an identical score,
so a top-hundred list that looks like a hundred decisions is really about five or
six independent decisions once you account for clustering.

If there is a hypothesis here, it is this: apparent success at materials discovery
benchmarks is substantially an artefact of how the test set was constructed, and
the standard construction is too generous.

### Confidence and gaps

High confidence: the authorship, the dates, the commit sequence, the list of
artefacts, and the headline numerical results. All are stated in tracked files or
readable from git.

Medium confidence: my characterisation of the project's arc as a sprint followed
by consolidation. The commit dates and messages support it strongly, but nobody
wrote it down as a plan.

The name "Eka" is never explained anywhere in the repository. It appears that it
refers to Dmitri Mendeleev's naming convention for elements he predicted but which
had not yet been found, where "eka-silicon" meant the undiscovered element one
place below silicon, later identified as germanium. That reading fits the
project's tagline, "Reading the gaps in the inorganic record", but it is my
inference, not a documented fact.

The repository does not say why this project was undertaken, whether it is
academic work, a portfolio piece, a prelude to a paper, or something else. There
is no thesis file, no manuscript, no submission record, no supervisor, and no
funding acknowledgement. A recurring instruction in the documents is that further
work "requires a new question and prospective protocol", which suggests the work
is complete rather than paused, but no statement of purpose exists.

---

## Episode 2 — The physics

### A necessary correction to the brief

I was asked to explain the physics this project relies on. I have to begin by
being straightforward: this project contains essentially no physics in the sense
of equations of motion, forces, energies, or fields. There is no simulation, no
solver, no differential equation, no thermodynamics, no quantum mechanics, and no
crystal structure anywhere in the code. The word "energy" appears in the
documentation only in sentences saying that no energy filter was applied.

That is not an oversight. It is a design decision, and understanding why is the
best route into the chemistry the project does rely on.

The physics has been done elsewhere, by other people, and arrives here as a
pre-computed label. What Eka manipulates are the shadows those calculations and
those laboratory experiments cast into a database. So this episode explains the
chemical concepts the project stands on, where the real physics enters from
upstream, and the mathematics Eka substitutes for physics inside its own code.

### Compositions, and what they are not

The fundamental object in this codebase is called a Composition. It is a list of
chemical elements with whole-number amounts, reduced to its simplest ratio and
written in alphabetical order.

An element is one of the hundred and eighteen entries on the periodic table,
identified by its symbol: O for oxygen, Ti for titanium, Ba for barium. The code
holds the full list of a hundred and eighteen symbols and rejects anything else.

A composition records proportions, not quantities and not arrangement. The code
treats "MgZn", "Mg2Zn2", and "Zn2Mg2" as one and the same object, because after
alphabetising and dividing by the greatest common divisor all three become the
same canonical string. This is a chemically meaningful choice: a crystal of
magnesium zinc has no fixed size, and doubling the recipe does not make a
different substance.

What a composition emphatically is not is a material. This distinction is the most
important chemical idea in the project and it is stated in the README's very first
limitation: "A Composition represents a reduced element ratio. It does not
represent molecular identity or crystal structure."

Consider carbon. Graphite and diamond have identical compositions and radically
different properties, because the atoms are arranged differently. Chemists call such
alternatives polymorphs, and a composition cannot distinguish them.

Eka deliberately collapses polymorphs together. Every record with the same reduced
formula is grouped into one unit, and the number of distinct crystal structures is
forbidden from influencing anything: "Structure count must not weight sampling,
popularity, or metrics." This stops a heavily-studied compound with thirty recorded
structures from dominating the statistics because it was studied a lot.

### Chemical systems

Above compositions sits a coarser unit called a chemical system: the set of
elements present, with all proportions discarded. Iron oxide and iron sesquioxide
are different compositions in the same iron-oxygen system.

This matters because the project's most important experimental contrast is between
hiding compositions and hiding systems. The system-holdout protocol is unusually
careful to warn that hiding a system does not mean hiding similar chemistry. It
gives the example explicitly: barium titanate and strontium titanate belong to
different systems, so one can sit in the training set while the other is held out,
even though barium and strontium are neighbours in the same column of the periodic
table and their titanates are close structural cousins. Holding out a system
removes exact element-set overlap; it does not remove chemical analogy.

### The chemistry the project scoped itself to

The experimental pool is restricted to what the project consistently calls
oxygen-containing ternaries. A ternary compound contains exactly three distinct
elements. Oxygen-containing means one of them is oxygen.

Oxygen-containing ternaries are an enormous and practically important family: most
ceramics, most battery cathode materials, most superconducting cuprates and most
piezoelectrics live there. But the project refuses to call this family "oxides", for
reasons of chemical precision. A compound can contain oxygen without oxygen playing
its classical oxide role: hydroxides contain an oxygen-hydrogen unit, oxyhalides
contain oxygen and a halogen, and many salts contain oxygen inside a group such as
sulfate. Deciding which count as oxides needs the oxidation state of the oxygen,
which needs electron distribution, which needs exactly the physics this project does
not do. So the scope string embedded throughout the code reads, verbatim,
"oxygen-containing ternaries; not oxidation-state-validated oxides".

The actual snapshot contains twenty-four thousand and twenty records, collapsing
into twelve thousand five hundred and six distinct compositions.

### Where the real physics enters: the provenance label

The project's entire notion of a "positive" example rests on one field in the
upstream database called `theoretical`.

The Materials Project is a large public database of inorganic materials built around
density functional theory, a quantum-mechanical method for computing a crystal's
electronic structure and energy from first principles. Most entries are computed
rather than observed. But when an entry traces to a record in an experimental
crystallography database, meaning someone actually made the substance and measured
its structure, it carries the flag `theoretical = false`.

Eka's labelling rule is built entirely on that flag. A composition group is
labelled positive if at least one of its records is explicitly marked as not
theoretical. It is labelled unlabelled if every record is explicitly theoretical.
It is labelled unresolved if the flag is missing somewhere and no positive exists,
and unresolved groups are thrown out of both training and evaluation.

In the actual snapshot, five thousand three hundred and fifty-nine compositions
came out positive, seven thousand one hundred and forty-seven unlabelled, and
none unresolved.

Two things about this rule deserve emphasis, because the repository emphasises
them relentlessly. First, a positive means experimental provenance, not verified
synthesis. Nobody re-read the original papers. The documents call it an
"experimental-provenance proxy" and never anything stronger. Second, unlabelled
does not mean negative. A composition that nobody has made may be impossible, or
may simply be uninteresting, or may be waiting for someone to try. The phrase
"unlabelled is not negative" recurs so often across the documentation that it
functions as a refrain.

This is why the whole evaluation is described as positive-unlabelled learning: a
setting where you have confirmed positive examples and a pool of unknowns, but no
confirmed negatives at all. Ordinary classification metrics such as
false-positive rate are meaningless here, and the protocol forbids reporting them.

There is a further subtlety the project surfaced and then investigated: one
thousand three hundred and forty-three composition groups are mixed, containing
both experimentally-sourced and purely-theoretical records. This is chemically
reasonable, since one polymorph may be known in the laboratory while another is
only computed. The original rule calls such groups positive. The project ran an
entire follow-on study asking what happens if you instead exclude them, or treat
them as unlabelled.

### The mathematics that stands in for physics

Three ranking methods do the real work, and none of them is physical.

The popularity baseline scores a candidate by how common its elements are in the
training set. For each element, count how many training compositions contain it.
For a candidate, add up those counts across its elements, then divide by the
number of elements times the number of training compositions. A candidate made of
elements that appear in lots of known compounds scores high. An unseen element
contributes zero. Because every candidate here contains oxygen and every training
composition does too, oxygen contributes exactly one third to every score, so all
the variation comes from the other two elements. The documentation points this out
itself.

The similarity method treats each composition as a vector. Imagine a hundred and
eighteen-dimensional space with one axis per element, and place a composition at
the point whose coordinates are its element counts, zero everywhere else. Then
measure the cosine of the angle between two such vectors. Two compositions
pointing in the same direction score one; two sharing no elements score zero. A
candidate's score is the largest cosine it achieves against any single training
composition. In plain terms: how close is this candidate to the nearest thing we
already know?

The project is blunt that this is not a chemical distance. The README calls it
"cosine overlap between element-count vectors" and says it is "not a probability,
learned embedding or chemical-substitution model". The measure has no idea that
barium and strontium behave alike. It has no idea that oxygen is reactive. It
knows only how much numerical overlap two count-vectors have.

The random method ranks candidates by a cryptographic hash of their formula, giving
a reproducible but arbitrary order. Its purpose is to supply a floor.

### The learned model, described in words

The fourth method is the only thing in the project that is fitted to data, and it
is small by design.

The idea is co-occurrence. Take every composition in the training set, strip out
the oxygen, and you are left with a pair of elements. Count how often each
unordered pair appears. That gives a large square table, one row and column per
non-oxygen element, a hundred and seventeen of each, with a count in each cell.

Oxygen is deliberately removed from these axes. Since every composition in scope
contains oxygen, leaving it in would create a node connected to everything, which
would dominate the structure without carrying information. The feasibility
document says exactly this.

Raw counts are then compressed through a function that grows quickly at first and
then flattens, scaled by the same function applied to the training size. Going from
zero occurrences to one is a big move; going from fifty to fifty-one barely
registers. This stops a handful of heavily-studied pairs from swamping everything.

The model then explains that whole table with a much smaller description. It gives
each of the hundred and seventeen elements a short list of four non-negative numbers,
and predicts the association between two elements as the sum of their corresponding
numbers multiplied together. Four numbers per element is far less information than a
full table of pairwise counts, so the model is forced to find real structure,
grouping elements that behave alike.

The quantity being minimised has three parts, and each has a plain meaning. The
first is the squared disagreement between predicted and observed association,
summed over every pair, which pushes the model to reproduce what it saw. The
second is a weight on that disagreement: pairs actually observed get full weight,
while pairs never observed get one percent of the weight. That asymmetry is the
positive-unlabelled problem showing up inside the model. An element pair with no
recorded compound is nudged gently toward zero, not asserted to be impossible.
The third part is a penalty on the size of the numbers themselves, which stops any
element from acquiring an enormous score just to fit noise. All the numbers are
constrained to be non-negative, which makes them interpretable as amounts of
something rather than arbitrary coordinates.

The fitting procedure walks downhill on this quantity, checking at each step that it
actually went down and halving the step size until it does. It stops when the
remaining slope is small enough, or after two thousand steps, whichever comes first.

### Assumptions, and what would break

The project is unusually explicit about its own load-bearing assumptions, so this
section is largely a restatement of things the documents already concede.

The first assumption is that composition alone carries enough signal. Structure,
synthesis conditions, temperature, pressure and defects are all absent. If what makes
a compound real depends mainly on structural feasibility rather than elemental
compatibility, the representation is too coarse and every method here measures the
wrong thing.

The second is that the experimental-provenance flag is a usable proxy for
"someone made this". If the flag is unreliable, or if it is systematically more
often set for compounds studied in certain decades or certain countries or certain
research fashions, then the model is learning the sociology of materials research
rather than its chemistry. The findings document concedes this directly: "Factors
can reflect research frequency."

The third is that absence is weak evidence. The positive-unlabelled framing exists to
avoid treating unmade compounds as failed experiments. If most unlabelled compositions
really are impossible, the methods are doing better than the metrics suggest; if most
are merely untried, they are doing worse.

The fourth is that element-count cosine is a meaningful notion of nearness. Here
the project's own diagnostic is quietly damning. The system-holdout study measured,
for every candidate, its maximum cosine similarity to the training set, and the
averages cluster around 0.957 to 0.976 in every design and every labelling policy.
Almost everything is almost maximally similar to something. It appears that this
measure has very little dynamic range on this pool, which would explain why a
method built on it behaves erratically. The repository reports these numbers but
does not draw that conclusion.

The fifth is the one the project most carefully polices: that hiding data is a
valid substitute for predicting the future. It is not, and the findings document
says so. "This task recovers withheld provenance labels from a single
contemporaneous MP snapshot: it is partition reconstruction, not chronological
discovery prediction." The obvious alternative, using database timestamps to
simulate discovery over time, is forbidden by an explicit standing rule: "Do not
infer first-publication dates from MP creation timestamps."

### Confidence and gaps

High confidence: everything about the composition model, the labelling rule, the
scope definition, and the three baseline methods. All are implemented in code I
have read and documented in protocols that the code enforces by hash.

High confidence on the learned model's specification, which is stated twice, once
in the feasibility document and once in the frozen protocol, and matches the
Julia implementation term for term.

Inference, clearly marked: my reading that the similarity measure is saturated and
therefore weakly informative. The numbers are the project's own; the interpretation
is mine.

Substantial gap: there is no physical or chemical validation anywhere. No
structure, no energy, no stability, no charge balance, no synthesis condition. The
project states this repeatedly as a limitation rather than hiding it, but a
listener should not come away imagining any physics was checked.

Substantial gap: the repository never characterises the upstream database's own
biases beyond noting that they exist. How the Materials Project decided what to
compute, and how its experimental flags were assembled, are treated as given.

---

## Episode 3 — The computer science

### The shape of the thing

The software is a Julia package. Julia is a language designed for numerical work
that aims to be as fast as C while reading like Python. The package depends on nine
libraries and the list is conspicuously short: a SQLite driver and its interface
layer, a JSON reader, an argument parser, a date library, a printing library, a
hashing library, a configuration parser and a precompilation helper.

There is no machine-learning framework, no linear-algebra package, no plotting or
statistics library. The design document explains why: "Cosine similarity is
implemented directly and needs neither an ML framework nor a linear-algebra
dependency." Even the learned model writes its inner loops by hand, to keep
"accumulation deterministic" and "avoid a new dependency or threaded BLAS state".
Threaded matrix libraries can add numbers in different orders on different runs,
producing tiny floating-point differences that would break bit-for-bit
reproducibility.

The source is about two thousand five hundred lines across thirteen files, in two
tiers. The lower tier is the stable package: compositions, ranking, database access,
import, benchmarking, snapshots, auditing, splits, positive-unlabelled evaluation and
the command line. The upper tier is a module called Research holding the four
experimental workflows. Nothing there is exported, no research command reaches the
command line, and the stability document says these interfaces "may change between any
two releases with no deprecation path". They live inside the package purely so they
get compiled and tested alongside everything else.

### The core data structure

The Composition type is the foundation and it is worth dwelling on because a
surprising amount of the project's correctness rests on it.

It is immutable, holding a tuple of element-to-amount pairs plus the canonical
string. The constructor sums repeated symbols, divides all amounts by their greatest
common divisor, sorts the symbols alphabetically, and builds the string.

Crucially, equality and hashing are defined on the reduced terms, so two compositions
describing the same substance are the same object as far as the language is concerned,
including as dictionary keys or set members. The README demonstrates this with an
assertion that a set containing "MgZn" and "Zn2Mg2" has exactly one element. The
stability document calls this "load-bearing for callers" and promises not to change
it.

The parser is strict to the point of hostility, accepting only a capital letter, an
optional lowercase letter and optional digits, repeated. Parentheses, charges, isotope
labels, fractional amounts and whitespace are all rejected. This has a real cost,
documented honestly: the upstream score database contains about twenty-one thousand
nine hundred rows using symbols outside the periodic table, including deuterium and
tritium notation and unexplained tokens like "Bx" and "Cz". The package refuses all of
them rather than guessing, because "converting labels to standard elements, silently
skipping them, or adding isotope semantics would be a separate design decision".

### How data flows from raw source to result

Five stages, each writing a new directory and never modifying an earlier one.

First, export. A Python script queries the Materials Project's official client for
non-deprecated materials containing oxygen and exactly three elements, excluding a
dataset called GNoME. It writes the decoded source records, a normalised table for
Julia, and a metadata file recording the database version, the exact retrieval
timestamp, the query parameters and hashes of the other two files. The snapshot in
use records version 2026.04.13 retrieved on 31 August 2026 at 12:16:39 UTC.

Second, audit. A Julia command re-reads the snapshot, verifies both hashes,
independently re-normalises every original record and checks it produces the matching
row of the normalised table, groups records by canonical composition, and assigns the
label. It writes a grouped table, a summary of counts, an itemised list of every
excluded record with its reason, and a readable report.

Third, split. A second command reconstructs the audit from scratch to confirm it
matches, then generates twenty training-and-test divisions, writing the training
compositions, candidates, held-out positives and evaluation labels for each, plus a
manifest hashing all of them.

Fourth, evaluate. A third command validates all twenty splits before the first ranker
runs, so a corrupted bundle cannot produce partial results, then runs the three
methods and computes the metrics.

Fifth, analyse. Independent Python scripts read the saved outputs and re-derive them
from scratch, checking that the recorded numbers follow from the recorded
memberships.

### Determinism as an engineering obsession

The single most distinctive technical choice in this project is its refusal to use
ordinary randomness or ordinary hashing anywhere.

Julia's built-in hash function is seeded per process, so the same input can produce
different values in different runs, and global random number generators carry state
any other code can disturb. Either would make an experiment unreproducible in subtle,
hard-to-detect ways. The protocol forbids both: "Never use the language's
process-dependent hash() or global RNG state."

In their place everything uses SHA-256, a cryptographic hash that maps any input to a
fixed-length value, identically on any machine forever. To choose which compounds to
hold out for split seven, the code hashes a string built from a fixed label, the number
seven and the compound's formula, sorts by the results, and takes the first chunk.
Different purposes use different prefix labels, so the same seed number cannot produce
correlated choices in two places. Score ties are broken by yet another hash with a
fixed seed, so identical scores always appear in the same order.

The result is that a split is not stored so much as it is a fact, recomputable by
anyone with the same inputs, on any platform, at any time.

### Provenance as a type of security

The second distinctive choice is treating the experiment's integrity like a
security problem, with an adversary in mind.

Protocol documents are pinned by content hash inside the source code. A function
reads the document from the docs directory and throws an error unless its SHA-256
matches a literal string compiled into the program. There are four such pins. The
engineering roadmap lists this as its first binding constraint and states the
consequence: those documents "are never moved, renamed, reformatted or edited. A
change means a new protocol identifier and a new pin."

The verification chain does not stop at hashes. When the evaluator loads a saved split
bundle it does not trust the recorded hashes. It reads the original snapshot, copies
its bytes into a temporary directory, re-runs the entire audit on those bytes,
regenerates every split from scratch, and compares the resulting membership files byte
for byte against what the bundle claims. The documentation names the threat this
defeats: "Updating a corrupted label file and its checksums is insufficient:
reconstruction still detects disagreement with the frozen source."

Output directories are created with an operation that fails if the directory already
exists, serving as an exclusive reservation. A code comment notes that this reservation
deliberately sits outside the cleanup handler, because if another process won the race,
deleting its directory would be catastrophic.

The release gate is a Python script that rejects dependency lockfiles and environment
files by name at any depth, any tracked file containing an absolute home-directory path,
anything over two megabytes, anything under the data, logs or reports directories, and
files matching credential or private-key patterns.

### Leakage prevention expressed as an interface

The cleverest piece of design is how the project stops information from the answers
leaking into the ranking.

The ranking function takes training compositions, candidate compositions, a method
name and two seeds. It has no parameter for labels. None. The documentation says it
flatly: "There is no argument for labels, source IDs, stored scores, or bundle paths."
Labels are held by the caller and attached only after the ranking is computed and
written. This turns a discipline problem into a structural one: you cannot
accidentally let the answer influence the ranking, because the function has no way to
receive it. The learned model follows the same pattern.

The protocols then add a test that catches any remaining leakage empirically: two
of the labelling policies have identical training sets but different candidate
pools, so the code refits both independently and asserts that the resulting model
parameters, the entire optimisation trace, and all shared candidate scores are
exactly equal. If a label had somehow influenced the fit, that check would fail.

### Performance, and why it did not matter much

The work is small by modern standards, and the project measured rather than
assumed.

The similarity computation compares about eight thousand two hundred candidates
against about four thousand three hundred training compositions, roughly thirty-five
million pairs per split. A naive implementation would build the full matrix, which the
documentation calculates at two hundred and sixty-nine megabytes. Instead it streams,
one candidate at a time, tracking only the running maximum: 0.132 seconds and 3.2
megabytes. The complete ranking including hashing and sorting takes 0.141 seconds per
split, so all twenty take about three seconds. The documentation draws the right
conclusion: "no batching tier, caching, or approximation is needed and none was added."

The learned model's total fitting cost across all one hundred and twenty fits was
18.71 seconds, with ranking taking 0.83 seconds. The findings document adds a
characteristically dry caveat: these are "measured computation costs, not a recorded
total of implementation effort".

### Testing and validation

The test suite is large relative to the code: roughly four thousand five hundred
and eighty-three individual Julia assertions and thirty-six Python tests.

Several categories stand out. Hand-calculated fixtures, where a human worked out
the expected metric on paper. Finite-difference checks on the learned model's
gradient, comparing the analytical slope against a numerical estimate. Corruption
tests that modify a saved file and rewrite its recorded checksum, verifying that
reconstruction still catches it. A test asserting the streaming similarity agrees
with the pairwise version to the last bit rather than within a tolerance. A test
asserting an allocation bound, proving no pairwise matrix is ever built.

The two-language structure is itself a validation strategy: Julia produces the
results, Python independently reconstructs them from the saved files. But the
project is honest about the limit of this. The label-sensitivity document states
that full similarity recomputation "is established by the separate Julia rerun, not
by pretending the Python analyzer implements another independent cosine engine".

Continuous integration runs Julia 1.10 and the current stable release on Linux,
plus current stable on macOS and Windows, with Python 3.11 through 3.14 for the
analysis scripts.

### Known limitations and technical debt

The project documents its own debt, which makes this section easy.

The most consequential finding is buried in the results. One hundred and one of the
one hundred and twenty model fits hit the two-thousand-iteration ceiling rather than
converging. Only nineteen met the stopping criterion. This was anticipated and
deliberately frozen as a fixed-compute evaluation, precisely so that nobody could
increase the iteration count after seeing which setting produced a nicer table. A
later run raised the ceiling to twenty thousand; all one hundred and twenty then
converged, fifty-five of the top-hundred lists changed, some by as many as
forty-eight of their hundred entries, but the average hit count barely moved. The
project's conclusion is precise: aggregate means were stable while individual
recommendations were compute-budget-sensitive.

The provenance system makes ordinary refactoring expensive. Two research modules
hash about ten source files, four scripts, two documents, and the project file into
their recorded manifests. Any byte change to any of them changes recorded hashes and
breaks key-for-key comparison with the saved baselines. The engineering roadmap
lists this as the explicit reason not to reformat the source, and formatting is
deferred to the next version boundary.

There is a documented inconsistency where one component writes a schema version as
the integer one while another writes it as the string "one". The stability document
calls it "a known wart" and defers the fix because correcting it would break
existing readers.

The exported name `main` is generic enough to collide with other packages, and the
intent is to stop exporting it at version 0.2.0.

The most fundamental limitation is structural. Because the record-level data,
rankings and fitted parameters are not published, nobody outside the owner's machine
can reproduce the real results: "public exact real reproduction requires separately
available input artifacts." A reader can run the synthetic workflow, which exercises
the software, but its outputs are explicitly "not scientific evidence".

One more limitation worth flagging for anyone reading the documentation: several
guides are organised around "Day 1", "Day 2", "Day 3" and "Day 4" milestones that
correspond to nothing a new reader can locate. It appears these were a working
schedule during the 31 August sprint that was never translated into
reader-facing language.

### Does the code match the claims?

I checked, because the brief asked me to. Broadly, yes, to an unusual degree.

The README's option table matches the command-line definitions. The seven commands
described are the six subcommands plus the default query mode implemented in the
code. The protocol's stated formulas for popularity and similarity match the Julia
implementations term for term. The learned model's specification matches its
implementation, including the exact initialisation formula. The labelling rule in
the protocol matches the audit code. The counts quoted in the documents match the
actual audit summary file on disk.

The one apparent discrepancy is that the frozen v1 protocol, written in advance,
says the positive-unlabelled command is "still a proposed future interface, not an
available command", while the command plainly exists today. The project anticipated
this and addressed it in a later document, explaining that the protocol's statement
"describes the freeze date" and that the protocol is deliberately never edited after
freezing. That is the pinning system working as intended rather than a defect.

### Confidence and gaps

High confidence throughout this section. Everything described is code I have read
or documentation the code enforces.

The one genuine gap: I have not run the test suite or reproduced any experiment.
The counts of test assertions come from the project's own records, not from my own
execution.

---

## Episode 4 — Where this sits in the literature, and why it matters

### Every source the repository actually cites

The repository's citation footprint is small and every item is traceable.

The intellectual parent is a 2018 paper by Atsuto Seko, Hiroyuki Hayashi, Hisashi
Kashima and Isao Tanaka, "Matrix- and tensor-based recommender systems for the
discovery of currently unknown inorganic compounds", in Physical Review Materials,
volume 2, article 013805. It applies recommender-system mathematics to chemistry. A
streaming service builds a table of users against films with ratings in some cells and
gaps in most, then factorises it to predict the gaps. Seko and colleagues built the
analogous table for inorganic compounds, using known compounds from crystallographic
databases as the observed entries, and scored combinations that have never been
reported. They released a database of those scores.

Eka's relationship to this work is layered, and the project is scrupulous about it.
Eka reuses eight composition-and-score pairs from the upstream repository's README
as test fixtures, and preserves the upstream BSD three-clause notice for them. Eka
can read the released score database. Eka measured that database's properties: over
four point seven million rows across four tables, of which about twenty-two thousand
use symbols the package cannot parse. And Eka explicitly does not reproduce the
model, does not evaluate its scientific quality, and does not include its scores in
the main comparison.

That exclusion is a substantive scientific decision and one of the most instructive
documents in the repository. The review found three problems. The stated training
sources for the upstream model overlap almost exactly with the databases Eka's
positive label is drawn from, so held-out positives are likely to be training data
for that model. There is no published training list and no verifiable cutoff date,
so you cannot partition the pool into "could have seen" and "could not have seen".
And coverage is correlated with the outcome being predicted: only 6.18 percent of
Eka's positive compositions carry an upstream score, against 31.59 percent of the
unlabelled ones. That last finding follows logically from the upstream model's own
stated purpose, which is to score currently unknown compositions. A list of unknowns
is roughly the complement of a list of knowns. Evaluating a recovery benchmark on
that list would mostly measure the selection rule.

The document's closing reasoning is worth quoting for its restraint: omission is
"the honest option when the confounder is this directly tied to the outcome".

The data source is the Materials Project, cited as A. Jain and colleagues,
"Commentary: The Materials Project: A materials genome approach to accelerating
materials innovation", APL Materials volume 1, article 011002, 2013. Eka uses it for
two things only: the pool of oxygen-containing ternaries, and the
experimental-provenance flag.

The learned model cites two methodological sources. The first is Kuang, Ding, and
Park's 2012 paper "Symmetric Nonnegative Matrix Factorization for Graph Clustering",
presented at the SIAM International Conference on Data Mining, which supplies the
family of factorisation used when the table being factorised is symmetric — as a
table of element-pair co-occurrences necessarily is, since the pair of barium and
titanium is the same as the pair of titanium and barium. The feasibility document
is careful: the objective, representation, initialisation, and optimiser "are
specified above, rather than imported from that paper's code".

The second is Hu, Koren, and Volinsky's 2008 paper "Collaborative Filtering for
Implicit Feedback Datasets". Its contribution is conceptual: when your data records
what people did rather than what they said, absence is ambiguous, so you should
attach an explicit and lower confidence to the zeros rather than treating them as
negatives. That is precisely the reasoning behind weighting unobserved element pairs
at one percent. Eka adds the warning that the analogy "does not establish that
materials missing from a database are negative examples".

One further paper is cited as motivation: "Probing out-of-distribution
generalization in machine learning for materials", published in Communications
Materials in 2024. It is referenced for the distinction between a nominal chemistry
holdout and genuine extrapolation, and the roadmap notes that it "motivates the
similarity diagnostic" but "does not predict this project's result". This is the
closest thing in the repository to an acknowledgement that other people have
noticed the same problem.

Several technical sources are cited without being research literature: the Materials
Project's own client code and provenance implementation, its database release notes,
the Creative Commons Attribution 4.0 deed, and a statistics paper on the fallacy of
inferring significance from overlapping confidence intervals. That is the complete
list. There is no related-work section and no positioning against contemporary
methods.

### The neighbourhood this work sits in

Because the repository does not survey its field, what follows is context I am
supplying, and it should be treated as my framing rather than the project's.

It appears that computational materials discovery contains at least four families
of approach. Physics-based screening computes the energy of candidate structures
and keeps the stable ones; this is what the Materials Project does, and it is
expensive and needs a proposed structure. Machine-learned property prediction
learns formation energy or another property from composition and structure, with
graph neural networks currently prominent. Generative modelling produces candidate
structures directly. And composition-level recommendation, ignoring structure
entirely, is what Seko and colleagues did and what Eka evaluates.

Eka does not compete with any of these. It sits at a right angle to all of them,
asking about the validity of the evaluation rather than the quality of the method.
The nearest intellectual neighbours are therefore not materials papers at all but
the methodological literature on data leakage and evaluation design in applied
machine learning. That literature is not cited here.

### If the claims hold, what follows

The first and strongest implication is a methodological warning. If similarity to
the nearest known compound is the strongest method under random composition
holdout and worse than chance under system holdout, then random composition
holdout is measuring something other than discovery ability, and any benchmark
using that design may be reporting inflated numbers. The project turned a baseline
into a diagnostic instrument: because the similarity method cannot learn anything,
its performance reads out how much the test set resembles the training set.

The second is a sharper version of the same point.
Under composition holdout, only sixteen to twenty-two percent of held-out positives
belong to systems absent from training. On that subgroup the learned model recovered
seventeen, twenty-four, and twenty-two positives across the three labelling policies,
against uniform-random expectations of roughly forty-two, forty-five, and
thirty-nine. It did worse than chance on precisely the compounds that would
represent genuinely novel chemistry. The apparent overall signal is concentrated
among candidates whose element combination was already in training.

The third is the clustering result. A top-hundred list under system holdout contains
on average only 13.5 distinct chemical systems, only nine of which supply any hit,
with a concentration equivalent to about 5.68 equally-weighted systems, and a single
system can occupy fifty-two of the hundred rows. A hundred recommendations that look
like a hundred decisions are, in effect, about six.

The fourth implication is about practice rather than results. It appears that the
repository functions as a worked example of how to conduct a small computational
study so that its negative results are as trustworthy as its positive ones: freeze
the protocol before looking, pin it by content hash so the freeze is enforced by
the machine, build the leakage prevention into the function signatures, report every
branch including the unfavourable ones, and refuse to increase the compute budget
after seeing the answer.

### What a sceptical reviewer would say

I would expect a hostile reviewer to raise the following, in roughly this order.

You have one dataset. Twenty splits of one snapshot are twenty overlapping views of
the same data, and the project says so itself: "Repeated holdouts of one snapshot,
not independent experimental datasets." Everything reported is variation within a
single sample. No confidence intervals, no significance tests, and correctly so —
but that means the headline effects, a mean advantage of half a compound per
hundred in the pilot, have no established precision.

Your labels are proxies you never validated. A positive means at least one database
record was flagged as non-theoretical. Nobody read a paper. The project concedes
this and even considered a literature audit, then correctly declined to run one
retroactively. A reviewer would say the entire dependent variable is unaudited.

Your best-performing model mostly did not converge. One hundred and one of one
hundred and twenty fits stopped because they ran out of iterations. The project
anticipated this, froze it deliberately, disclosed it in bold, and later showed that
raising the limit changed more than half the recommendation lists. A reviewer would
accept the disclosure and still be unconvinced by the model.

Your representation cannot distinguish stoichiometry. The element-pair model gives
every compound in a chemical system exactly the same score, resolved into an order
by a hash. So the model cannot express the difference between iron oxide and iron
sesquioxide.

Your task is not the task you care about. Reconstructing a hidden partition of a
present-day snapshot is not predicting what will be discovered. The project agrees
and forbids the timestamp-based alternative on the grounds that database creation
dates do not establish discovery chronology. A reviewer would call this a
well-reasoned dead end that leaves the interesting question untouched.

Nobody can check your work. The snapshot, the rankings, the fitted factors, and the
environments are all local. A reader gets the code and a synthetic demonstration
that proves the software runs. The reproduction claims in the documents are
themselves carefully hedged as same-platform reruns using an existing package cache,
not clean-room reproductions.

There is no external review. One author, no co-authors, no institutional
affiliation stated, no preprint, no submission. The protocols are described honestly
as internal freezes and not as "formal external preregistration", which is exactly
right and also exactly the limitation.

And finally: for all the apparatus, the scientific yield is one sentence. Similarity
to nearby known chemistry predicts recovery when nearby chemistry is allowed in the
test set, and fails when it is not. That is real and useful. A reviewer would still
ask whether it needed four frozen protocols and a hash-pinned provenance chain, and
whether the effort reads better as an engineering exercise that produced a result.

### Confidence and gaps

High confidence: every citation listed, every exclusion decision, every number
quoted. All are in the repository.

Clearly marked inference: the survey of competing approaches, the positioning
relative to the leakage literature, and the framing of the sceptic's case. None of
this appears in the repository.

Real gaps: the repository contains no related-work discussion, no comparison against
any published benchmark, no discussion of graph neural networks or generative
approaches, and no citation of any methodological work on evaluation design beyond
the single out-of-distribution paper. Anyone wanting to place this work properly
would have to build that context from outside.

---

## Appendix A — Glossary

**Arity** — the number of distinct elements in a composition. Binary is two,
ternary three, quaternary four.

**Canonical formula** — Eka's single agreed way of writing a composition:
alphabetical symbols, whole numbers reduced to lowest terms, explicit ones written.

**Chemical system** — the set of elements in a compound, ignoring proportions.

**Composition** — a ratio of elements; the fundamental unit here, and explicitly
not a structure or a material.

**Cosine similarity** — a measure of how closely two lists of numbers point in the
same direction, running from zero for no overlap to one for identical direction.

**Density functional theory** — a quantum-mechanical method for computing a
material's electronic structure and energy from first principles. It produced the
upstream database, but no part of Eka.

**GNoME** — a specific Materials Project dataset carrying different licensing terms,
excluded from every query in this project.

**Held-out positive** — a known compound deliberately hidden from training so the
ranking can be tested on whether it finds it again.

**Holdout** — the act of hiding part of your data to test on. Composition holdout
hides individual compounds; system holdout hides whole element combinations.

**Hits at k** — the number of hidden compounds found in the top k of a ranking.

**Leakage** — when information about the answer reaches the method being tested,
inflating its apparent performance.

**Nonnegative matrix factorisation** — explaining a table of nonnegative numbers as
the product of two smaller nonnegative tables, forcing the model to find structure.

**Oxide** — strictly, a compound where oxygen carries a particular oxidation state.
This project says oxygen-containing instead.

**Polymorph** — one of several distinct crystal arrangements of the same composition,
such as graphite and diamond.

**Popularity baseline** — ranking a candidate by how common its elements are among
known compounds.

**Positive-unlabelled learning** — a setting with confirmed positive examples and a
pool of unknowns, but no confirmed negatives.

**Prevalence** — the fraction of a candidate pool that is actually positive.

**Projected gradient descent** — walking downhill on an objective while forcing the
answer back into an allowed region, here the region where all numbers are at least
zero.

**Protocol freeze** — writing down and hashing the full experimental design before
looking at any result.

**Rank** — the number of hidden dimensions a factorisation is allowed; fixed at
four here.

**Recall** — the fraction of all hidden compounds that a ranking found.

**Regularisation** — a penalty discouraging a model from using large numbers.

**SHA-256** — a cryptographic hash producing a fixed-length fingerprint of any input,
identical everywhere for identical input.

**Snapshot** — a frozen copy of a query result with its metadata and hashes, so an
experiment refers to an unchanging input.

**Split sensitivity** — how much a result varies across repeated overlapping splits
of one dataset. Deliberately distinguished from statistical uncertainty.

**Stoichiometry** — the numerical proportions of elements in a compound.

**Theoretical flag** — the upstream database field marking whether an entry has any
experimental provenance. Eka's entire labelling rule rests on it.

**Unlabelled** — a composition with no experimental provenance in the snapshot.
Repeatedly and emphatically not a negative.

**Unresolved** — a composition whose provenance flags are incomplete, excluded from
the experiment entirely.

---

## Appendix B — Reference list

**Seko, A., Hayashi, H., Kashima, H., and Tanaka, I. (2018).** "Matrix- and
tensor-based recommender systems for the discovery of currently unknown inorganic
compounds." *Physical Review Materials*, volume 2, article 013805. DOI
10.1103/PhysRevMaterials.2.013805. Cited in the README and the external-score
review; authors, year, venue and DOI all appear in the repository. The paper itself
is not included.

**Seko, A. (2024).** The `sekocha/recommender` software repository and its released
score database `recommender-2024-07-01.sqlite`, BSD three-clause, copyright 2024
Atsuto Seko. The repository records the database's size as 211,681,280 bytes and its
SHA-256 fingerprint, reviewed 31 August 2026, and reproduces the full licence text.
The database itself is not bundled.

**Jain, A., et al. (2013).** "Commentary: The Materials Project: A materials genome
approach to accelerating materials innovation." *APL Materials*, volume 1, article
011002. DOI 10.1063/1.4812323. Only the first author is named in the repository.

**Kuang, D., Ding, C., and Park, H. (2012).** "Symmetric Nonnegative Matrix
Factorization for Graph Clustering." Cited with a link to a Georgia Tech faculty page
hosting the PDF. **Venue unverified from repository contents**; the date and link
indicate the SIAM International Conference on Data Mining.

**Hu, Y., Koren, Y., and Volinsky, C. (2008).** "Collaborative Filtering for Implicit
Feedback Datasets." Cited with a link to an author-hosted PDF. **Venue unverified
from repository contents**; commonly associated with the IEEE International
Conference on Data Mining.

**"Probing out-of-distribution generalization in machine learning for materials"
(2024).** *Communications Materials*. Cited in the recovery roadmap by title and URL
only. **Authors and year are not stated anywhere in the repository.**

**A paper on confidence-interval overlap**, cited in the pilot document by DOI
10.1198/000313001317097960 alone. **Title, authors, year and venue are not stated
anywhere in the repository**; it appears to be a 2001 note in *The American
Statistician* on why overlapping intervals do not establish non-significance, but
that attribution is unverified.

**Materials Project `emmet-core` provenance implementation.** Version 0.87.2 of
`emmet/core/provenance.py`, verified byte-identical to the upstream main branch on
31 August 2026, SHA-256 recorded in the provenance review. Source code, not a paper.

**Materials Project API client (summary route), database release notes, and Terms of
Use.** Cited respectively for query fields and the GNoME exclusion option, for
version identification and GNoME licensing restrictions, and for the Creative
Commons Attribution 4.0 grant over downloaded content. The supplied copy of the
terms has its SHA-256 recorded, reviewed 31 August 2026.

**Creative Commons Attribution 4.0 International deed**, cited for its attribution,
licence-link and change-notice requirements. **Registry of Open Data on AWS,
Materials Project entry**, cited as the route to the terms link; the project notes it
used the API, not the AWS mirror.

**Corbett, Joshua.** "Eka: composition ranking and reproducible recovery benchmarks",
version 0.1.1, MIT licence, repository at github.com/JoshCCorby/EkaCompositions.jl.

---

## Appendix C — Open questions for further research

1. What does the Materials Project's `theoretical` flag actually mean in practice, how
is it assembled from crystallographic cross-references, and what is its error rate in
either direction?

2. How were the experimental crystallography databases behind that flag — principally
ICSD, ICDD, and the Springer Materials or Pauling File collections — assembled, and
what biases do they carry by era, geography, compound family and commercial interest?

3. What split designs are actually used when evaluating composition-level discovery
models, and how many published benchmarks rely on the random composition holdout this
project argues is too generous?

4. Has anyone else published a formal analysis showing that nearest-neighbour
similarity baselines act as leakage detectors in materials benchmarks, and how do
their conclusions compare with this project's reversal result?

5. What are the standard alternatives for testing extrapolation in materials machine
learning — clustering in a learned embedding space, time-based splits,
leave-one-element-out — and what are the known failure modes of each?

6. Why is the maximum cosine similarity between candidates and training compositions
so uniformly high, around 0.957 to 0.976, and does that saturation mean the
element-count representation cannot discriminate at all on this pool?

7. What is the state of the art in composition-only representations — Magpie-style
elemental descriptors, learned element embeddings such as mat2vec or ElemNet — and how
much better would any of them do on exactly this recovery task?

8. What do data-mined ionic-substitution models say about chemical analogy, and would
they capture the barium-versus-strontium relationship that cosine similarity misses?

9. In the positive-unlabelled learning literature, what unbiased risk estimators exist,
what do they need in the way of a known class prior, and could any apply where the
prior is unknown?

10. How does the weighted symmetric nonnegative matrix factorisation used here relate
to the matrix and tensor factorisations in the Seko 2018 paper, and what would have to
change to make the two genuinely comparable?

11. How sensitive are low-rank co-occurrence models to the chosen rank, and is rank
four defensible for a 117-element vocabulary or far too small to express the structure
of the periodic table?

12. What would a proper convergence study look like, given that raising the iteration
ceiling tenfold converged every fit and changed more than half the recommendation lists
while barely moving the aggregate means?

13. What is the correct statistical treatment for twenty overlapping holdouts of a
single dataset, and is there any defensible way to attach uncertainty to a mean
difference computed across them?

14. Is there any defensible source of first-synthesis dates for inorganic compounds
that would permit a genuine chronological evaluation, given that database creation
timestamps are unusable for this?

15. What fraction of compositions marked unlabelled in a database like this are
genuinely unsynthesisable rather than simply untried, and is there any published
estimate?

16. How do synthesizability-prediction models define their labels, and do they face the
same positive-unlabelled problem this project confronts?

17. What is accepted practice for releasing derived results from a database under a
Creative Commons Attribution licence, and would publishing this project's rankings and
fitted factors have been permissible under the terms it reviewed?

18. Given that the element-pair model scores every composition in a chemical system
identically, what minimal extension would let it discriminate stoichiometry without
becoming a different model?

19. Is the deflationary conclusion here consistent with other fields that confronted the
same problem — drug-target interaction and protein function prediction both have
documented similarity-leakage literatures — and what did those fields do about it?

---

*Prepared from the repository at commit `0629ba9`, tag `v0.1.1`, dated 7 September
2026. Numerical results quoted from the project's tracked findings document and from
local evidence directories that are excluded from version control by design.*
