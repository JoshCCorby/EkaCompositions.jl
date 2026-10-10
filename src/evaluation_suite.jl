"""Uniform, self-validating result bundles for prospective evaluation suites."""
module EvaluationSuite
using ...EkaCompositions
using SHA, TOML

const SCHEMA_ID = "eka-evaluation-suite-v1"
const SCHEMA_VERSION = 1
const RANKING_HEADER = (:split_id, :method, :rank, :composition, :score,
    :tie_key, :coverage, :observed_relevant)
const METRIC_FIELDS = (:budget, :hits, :candidate_count, :relevant_count,
    :observed_label_fraction, :recall, :enrichment, :random_expected_hits,
    :random_expected_hits_numerator, :random_expected_hits_denominator, :dcg,
    :ndcg, :selected_system_count, :relevant_system_count, :hit_system_count,
    :system_recall, :effective_hit_systems, :largest_hit_system_fraction,
    :cutoff_score, :cutoff_tie_size, :cutoff_tie_selected, :cutoff_tie_crosses)
const METRIC_HEADER = (:split_id, :method, METRIC_FIELDS...)
const SCIENTIFIC_KEYS = Set(("dataset", "audit", "code", "protocol", "split",
    "candidates", "methods", "seed_roles", "metric"))
const ENVIRONMENT_KEYS = Set(("julia_version", "python_version", "os",
    "architecture", "cpu", "threads", "accelerator"))

check(ok, message) = ok || throw(ArgumentError(message))
digest(bytes) = bytes2hex(sha256(bytes))
valid_digest(value) = value isa AbstractString && length(value) == 64 &&
    all(character -> character in "0123456789abcdef", value)

function safe_path(value, label="artifact path"; allow_outputs=false)
    check(value isa String && !isempty(value) && !isabspath(value) &&
        !occursin('\\', value), "$label must be a safe relative path")
    parts = split(value, '/')
    check(all(part -> !isempty(part) && part != "." && part != "..", parts),
        "$label must be a safe relative path")
    check(!(value in ("run.toml", "inventory.toml", "runtime.tsv")),
        "$label uses a reserved bundle path")
    allow_outputs || check(!(value in ("rankings.tsv", "metrics.tsv")),
        "$label uses a reserved bundle path")
    return value
end

function plain(value, label="configuration")
    if value isa AbstractDict
        result = Dict{String,Any}()
        for (key, item) in value
            check(key isa AbstractString, "$label keys must be strings")
            name = String(key)
            check(!haskey(result, name), "duplicate $label key: $name")
            result[name] = plain(item, "$label.$name")
        end
        return result
    elseif value isa AbstractVector || value isa Tuple
        return Any[plain(item, label) for item in value]
    elseif value isa Bool || value isa String || value isa Integer
        return value
    elseif value isa AbstractFloat
        check(isfinite(value), "$label contains a non-finite number")
        return Float64(value)
    end
    throw(ArgumentError("$label contains unsupported value type $(typeof(value))"))
end

function exact_keys(table, expected, label)
    check(table isa AbstractDict, "$label must be a table")
    actual = Set(String(key) for key in keys(table))
    actual == Set(expected) || throw(ArgumentError("$label has missing or unexpected keys"))
end

function nonempty_string(table, key, label)
    value = get(table, key, nothing)
    check(value isa String && !isempty(value), "$label.$key must be a nonempty string")
    return value
end

function hash_table(value, label; allow_outputs=false)
    check(value isa AbstractDict, "$label must be a table")
    result = Dict{String,String}()
    for (path, hash) in value
        check(path isa String, "$label keys must be paths")
        safe_path(path, "$label path"; allow_outputs)
        check(valid_digest(hash), "$label[$path] must be a lowercase SHA-256 digest")
        result[path] = hash
    end
    return result
end


function source_tree_digest(relevant, dependency)
    check(isempty(intersect(Set(keys(relevant)), Set(keys(dependency)))),
        "source and dependency-lock paths must be disjoint")
    entries = sort!(collect(merge(relevant, dependency)); by=first)
    identity = join(("$path\0$(hash)\n" for (path, hash) in entries))
    return digest(codeunits(identity))
end

function validate_scientific(value)
    scientific = plain(value, "scientific")
    exact_keys(scientific, SCIENTIFIC_KEYS, "scientific")

    dataset = scientific["dataset"]
    exact_keys(dataset, ("id", "version", "retrieval_metadata", "input_hashes"), "dataset")
    for key in ("id", "version", "retrieval_metadata"); nonempty_string(dataset, key, "dataset"); end
    hash_table(dataset["input_hashes"], "dataset.input_hashes")

    audit = scientific["audit"]
    exact_keys(audit, ("algorithm", "implementation_hashes"), "audit")
    nonempty_string(audit, "algorithm", "audit")
    hash_table(audit["implementation_hashes"], "audit.implementation_hashes")

    code = scientific["code"]
    exact_keys(code, ("commit", "dirty", "source_tree_sha256", "relevant_file_hashes",
        "dependency_lock_hashes"), "code")
    nonempty_string(code, "commit", "code")
    check(code["dirty"] isa Bool, "code.dirty must be Boolean")
    check(valid_digest(code["source_tree_sha256"]), "code.source_tree_sha256 must be a SHA-256 digest")
    relevant = hash_table(code["relevant_file_hashes"], "code.relevant_file_hashes")
    dependency = hash_table(code["dependency_lock_hashes"], "code.dependency_lock_hashes")
    check(code["source_tree_sha256"] == source_tree_digest(relevant, dependency),
        "code.source_tree_sha256 differs from its file hashes")

    protocol = scientific["protocol"]
    exact_keys(protocol, ("id", "sha256", "artifact"), "protocol")
    nonempty_string(protocol, "id", "protocol")
    check(valid_digest(protocol["sha256"]), "protocol.sha256 must be a SHA-256 digest")
    safe_path(nonempty_string(protocol, "artifact", "protocol"), "protocol artifact")

    split = scientific["split"]
    exact_keys(split, ("algorithm", "label_policy", "membership_hashes"), "split")
    nonempty_string(split, "algorithm", "split")
    nonempty_string(split, "label_policy", "split")
    hash_table(split["membership_hashes"], "split.membership_hashes")

    candidates = scientific["candidates"]
    exact_keys(candidates, ("definition", "exclusion_counts"), "candidates")
    nonempty_string(candidates, "definition", "candidates")
    counts = candidates["exclusion_counts"]
    check(counts isa AbstractDict && all(key isa String && value isa Integer &&
        !(value isa Bool) && value >= 0 for (key, value) in counts),
        "candidates.exclusion_counts must map strings to nonnegative integers")

    methods = scientific["methods"]
    check(methods isa AbstractDict && !isempty(methods), "methods must be a nonempty table")
    for (method, config) in methods
        check(method isa String && !isempty(method) && config isa AbstractDict,
            "methods must map nonempty names to configuration tables")
    end
    seeds = scientific["seed_roles"]
    check(seeds isa AbstractDict && all(key isa String && value isa Integer &&
        !(value isa Bool) && value >= 0 for (key, value) in seeds),
        "seed_roles must map strings to nonnegative integers")

    metric = scientific["metric"]
    exact_keys(metric, ("algorithm", "version", "budgets", "grouping_rule",
        "denominator_counts"), "metric")
    for key in ("algorithm", "version", "grouping_rule"); nonempty_string(metric, key, "metric"); end
    budgets = metric["budgets"]
    check(budgets isa AbstractVector && !isempty(budgets) &&
        all(value -> value isa Integer && !(value isa Bool) && value > 0, budgets) &&
        length(unique(budgets)) == length(budgets) && issorted(budgets),
        "metric.budgets must be sorted unique positive integers")
    denominators = metric["denominator_counts"]
    check(denominators isa AbstractDict && all(key isa String && value isa Integer &&
        !(value isa Bool) && value >= 0 for (key, value) in denominators),
        "metric.denominator_counts must map strings to nonnegative integers")
    return scientific
end

function validate_environment(value)
    environment = plain(value, "environment")
    exact_keys(environment, ENVIRONMENT_KEYS, "environment")
    for key in setdiff(ENVIRONMENT_KEYS, Set(("threads",)))
        nonempty_string(environment, key, "environment")
    end
    check(environment["threads"] isa Integer && !(environment["threads"] isa Bool) &&
        environment["threads"] >= 1, "environment.threads must be a positive integer")
    return environment
end

function toml_bytes(content)
    io = IOBuffer()
    TOML.print(io, content; sorted=true)
    return take!(io)
end

run_id(scientific) = digest(toml_bytes(Dict("scientific" => validate_scientific(scientific))))

"""
    source_identity(root, files; commit, dirty)

Return the strict `code` table used by a suite configuration. File names are
safe relative paths, and the source-tree digest binds their sorted path/digest
pairs. The caller supplies the recorded VCS commit and dirty flag explicitly.
"""
function source_identity(root, files; commit, dirty, dependency_locks=String[])
    check(commit isa String && !isempty(commit), "commit must be a nonempty string")
    check(dirty isa Bool, "dirty must be Boolean")
    normal = String[]
    for path in files
        push!(normal, safe_path(String(path), "source file"))
    end
    locks = String[]
    for path in dependency_locks
        push!(locks, safe_path(String(path), "dependency lock"))
    end
    check(length(unique(vcat(normal, locks))) == length(normal) + length(locks),
        "duplicate source or dependency-lock path")
    relevant = Dict(path => digest(read(joinpath(root, split(path, '/')...))) for path in normal)
    dependency = Dict(path => digest(read(joinpath(root, split(path, '/')...))) for path in locks)
    return Dict{String,Any}("commit" => commit, "dirty" => dirty,
        "source_tree_sha256" => source_tree_digest(relevant, dependency),
        "relevant_file_hashes" => relevant, "dependency_lock_hashes" => dependency)
end

function declared_hashes(scientific)
    result = Dict{String,String}()
    tables = (scientific["dataset"]["input_hashes"],
        scientific["audit"]["implementation_hashes"],
        scientific["code"]["relevant_file_hashes"],
        scientific["code"]["dependency_lock_hashes"],
        scientific["split"]["membership_hashes"])
    for table in tables, (path, hash) in table
        check(!haskey(result, path), "artifact path is declared more than once: $path")
        result[path] = hash
    end
    path = scientific["protocol"]["artifact"]
    check(!haskey(result, path), "protocol artifact path is declared more than once: $path")
    result[path] = scientific["protocol"]["sha256"]
    return result
end

function artifact_bytes(artifacts)
    check(artifacts isa AbstractDict, "artifacts must be a path-to-bytes table")
    result = Dict{String,Vector{UInt8}}()
    for (path, value) in artifacts
        check(path isa String, "artifact keys must be paths")
        safe_path(path)
        bytes = value isa AbstractString ? Vector{UInt8}(codeunits(value)) :
            value isa AbstractVector{UInt8} ? Vector{UInt8}(value) :
            throw(ArgumentError("artifact $path must contain bytes or text"))
        result[path] = bytes
    end
    return result
end

cell(value) = value === nothing ? "" : value isa Bool ? (value ? "true" : "false") : string(value)
function table_bytes(header, rows)
    io = IOBuffer()
    println(io, join(string.(header), '\t'))
    for row in rows
        values = map(name -> getproperty(row, name), header)
        check(all(value -> !occursin(r"[\t\r\n]", cell(value)), values),
            "TSV values must not contain tabs or newlines")
        println(io, join(cell.(values), '\t'))
    end
    return take!(io)
end

function evaluation_rows(evaluations, scientific)
    check(evaluations isa AbstractVector && !isempty(evaluations),
        "evaluations must be a nonempty collection")
    budgets = Int.(scientific["metric"]["budgets"])
    allowed_methods = Set(keys(scientific["methods"]))
    ranking_rows, metric_rows = NamedTuple[], NamedTuple[]
    seen = Set{Tuple{String,String}}()
    split_memberships = Dict{String,Tuple{Set{Composition},Set{Composition}}}()
    for evaluation in evaluations
        for field in (:split_id, :method, :ranking, :relevant)
            check(hasproperty(evaluation, field), "evaluation is missing $field")
        end
        split_id, method = evaluation.split_id, evaluation.method
        check(split_id isa String && !isempty(split_id), "split_id must be a nonempty string")
        check(method isa String && method in allowed_methods, "evaluation method is not configured")
        key = (split_id, method)
        check(!(key in seen), "duplicate split/method evaluation")
        push!(seen, key)
        rows = evaluation.ranking
        check(rows isa AbstractVector && !isempty(rows), "ranking must be a nonempty collection")
        compositions = Composition[]
        scores = Union{Nothing,Float64}[]
        ties, coverages = String[], String[]
        for row in rows
            for field in (:composition, :score, :tie_key)
                check(hasproperty(row, field), "ranking row is missing $field")
            end
            composition = row.composition isa Composition ? row.composition : Composition(row.composition)
            push!(compositions, composition)
            score = row.score
            check(score === nothing || score isa Real && !(score isa Bool) && isfinite(score),
                "ranking scores must be finite real values or all missing")
            push!(scores, score === nothing ? nothing : Float64(score))
            check(row.tie_key isa String && valid_digest(row.tie_key), "ranking tie_key must be a SHA-256 digest")
            push!(ties, row.tie_key)
            coverage = hasproperty(row, :coverage) ? row.coverage : "not_applicable"
            check(coverage isa String && !isempty(coverage), "ranking coverage must be a nonempty string")
            push!(coverages, coverage)
        end
        numeric = all(!isnothing, scores)
        check(numeric || all(isnothing, scores), "ranking scores must be either all present or all missing")
        numeric && check(issorted(Float64.(scores); rev=true), "ranking scores must be descending")
        relevant = EkaCompositions.evaluation_compositions(evaluation.relevant, "relevant")
        ranking_set, relevant_set = Set(compositions), Set(relevant)
        check(length(ranking_set) == length(compositions), "duplicate canonical ranking composition")
        check(issubset(relevant_set, ranking_set), "relevant composition absent from ranking")
        membership = (ranking_set, relevant_set)
        if haskey(split_memberships, split_id)
            check(split_memberships[split_id] == membership,
                "methods for one split must share candidates and relevance")
        else
            split_memberships[split_id] = membership
        end
        for index in eachindex(compositions)
            push!(ranking_rows, (split_id=split_id, method=method, rank=index,
                composition=formula(compositions[index]), score=scores[index],
                tie_key=ties[index], coverage=coverages[index],
                observed_relevant=compositions[index] in relevant_set))
        end
        metrics = recovery_metrics(compositions, relevant; budgets,
            scores=numeric ? Float64.(scores) : nothing)
        for metric in metrics
            push!(metric_rows, (; split_id, method, metric...))
        end
    end
    sort!(ranking_rows; by=row -> (row.split_id, row.method, row.rank))
    sort!(metric_rows; by=row -> (row.split_id, row.method, row.budget))
    return ranking_rows, metric_rows
end

"""
    write_bundle(output; scientific, environment, evaluations, artifacts,
                 runtime_rows=nothing)

Write a new schema-v1 evaluation bundle. The deterministic run ID hashes only
the canonical scientific configuration. Complete rankings and recomputed metrics
are inventoried with all declared provenance artifacts. Runtime rows are saved
separately and deliberately excluded from deterministic identity.
"""
function write_bundle(output; scientific, environment, evaluations, artifacts,
        runtime_rows=nothing, _after_reserve=nothing)
    target = abspath(output)
    check(!ispath(target) && !islink(target), "refusing to overwrite evaluation bundle")
    check(isdir(dirname(target)), "output parent must exist")
    scientific = validate_scientific(scientific)
    environment = validate_environment(environment)
    artifacts = artifact_bytes(artifacts)
    declared = declared_hashes(scientific)
    check(Set(keys(artifacts)) == Set(keys(declared)),
        "artifacts must exactly match paths declared by the scientific configuration")
    for (path, expected) in declared
        check(digest(artifacts[path]) == expected, "declared artifact hash mismatch: $path")
    end
    rankings, metrics = evaluation_rows(evaluations, scientific)
    ranking_data = table_bytes(RANKING_HEADER, rankings)
    metric_data = table_bytes(METRIC_HEADER, metrics)
    id = run_id(scientific)
    runtime_data = if runtime_rows === nothing
        nothing
    else
        check(runtime_rows isa AbstractVector && !isempty(runtime_rows),
            "runtime_rows must be a nonempty collection")
        header = keys(first(runtime_rows))
        check(all(row -> keys(row) == header, runtime_rows), "runtime rows must share one schema")
        table_bytes(header, runtime_rows)
    end

    mkdir(target)
    try
        _after_reserve === nothing || _after_reserve(target)
        for (path, bytes) in artifacts
            destination = joinpath(target, split(path, '/')...)
            mkpath(dirname(destination))
            write(destination, bytes)
        end
        write(joinpath(target, "rankings.tsv"), ranking_data)
        write(joinpath(target, "metrics.tsv"), metric_data)
        runtime_data === nothing || write(joinpath(target, "runtime.tsv"), runtime_data)
        hashes = Dict(path => digest(bytes) for (path, bytes) in artifacts)
        hashes["rankings.tsv"] = digest(ranking_data)
        hashes["metrics.tsv"] = digest(metric_data)
        inventory = Dict{String,Any}("schema_id" => SCHEMA_ID,
            "schema_version" => SCHEMA_VERSION, "run_id" => id,
            "deterministic_file_hashes" => hashes,
            "excluded_files" => runtime_data === nothing ? String[] : ["runtime.tsv"])
        inventory_data = toml_bytes(inventory)
        write(joinpath(target, "inventory.toml"), inventory_data)
        run = Dict{String,Any}("schema_id" => SCHEMA_ID,
            "schema_version" => SCHEMA_VERSION, "run_id" => id,
            "inventory_sha256" => digest(inventory_data),
            "runtime_file" => runtime_data === nothing ? "" : "runtime.tsv",
            "scientific" => scientific, "environment" => environment)
        write(joinpath(target, "run.toml"), toml_bytes(run))
    catch
        rm(target; recursive=true)
        rethrow()
    end
    return validate_bundle(target; expected_run_id=id)
end

function parse_tsv(bytes, expected_header, label)
    text = String(copy(bytes))
    check(endswith(text, '\n') && !occursin('\r', text), "$label must use LF and a trailing newline")
    lines = split(text, '\n'; keepempty=true)
    pop!(lines)
    check(!isempty(lines) && split(first(lines), '\t'; keepempty=true) == collect(string.(expected_header)),
        "$label has the wrong header")
    width = length(expected_header)
    rows = [split(line, '\t'; keepempty=true) for line in lines[2:end]]
    check(all(row -> length(row) == width, rows), "$label has a malformed row")
    return rows
end

function bundle_files(root)
    return Set(replace(relpath(joinpath(dir, name), root), '\\' => '/')
        for (dir, _, names) in walkdir(root) for name in names)
end

function bundle_path(root, relative)
    check(relative isa String && !isempty(relative) && !isabspath(relative) &&
        !occursin('\\', relative), "unsafe bundle path")
    parts = split(relative, '/')
    check(all(part -> !isempty(part) && part != "." && part != "..", parts),
        "unsafe bundle path")
    current = root
    for part in parts
        current = joinpath(current, part)
        check(!islink(current), "bundle paths must not traverse symbolic links")
    end
    return current
end

"""
    validate_bundle(path; expected_run_id=nothing, expected_inventory_sha256=nothing)

Strictly validate schema keys, declared provenance, deterministic inventory,
ranking structure, and a byte-exact recomputation of every metric. Supplying an
externally recorded run or inventory identity detects coordinated edits that
also rewrite the bundle's internal checksums.
"""
function validate_bundle(path; expected_run_id=nothing, expected_inventory_sha256=nothing)
    root = abspath(path)
    check(isdir(root) && !islink(root), "evaluation bundle does not exist or is a symbolic link")
    run_bytes = read(bundle_path(root, "run.toml"))
    run = EkaCompositions.recovery_toml(run_bytes, "evaluation run")
    exact_keys(run, ("schema_id", "schema_version", "run_id", "inventory_sha256",
        "runtime_file", "scientific", "environment"), "run")
    check(run["schema_id"] == SCHEMA_ID && run["schema_version"] == SCHEMA_VERSION,
        "unsupported evaluation schema")
    scientific = validate_scientific(run["scientific"])
    environment = validate_environment(run["environment"])
    id = run_id(scientific)
    check(run["run_id"] == id, "run ID differs from scientific configuration")
    expected_run_id === nothing || check(expected_run_id == id, "run ID differs from external expectation")

    inventory_bytes = read(bundle_path(root, "inventory.toml"))
    inventory_hash = digest(inventory_bytes)
    check(valid_digest(run["inventory_sha256"]) && run["inventory_sha256"] == inventory_hash,
        "inventory hash mismatch")
    expected_inventory_sha256 === nothing || check(expected_inventory_sha256 == inventory_hash,
        "inventory differs from external expectation")
    inventory = EkaCompositions.recovery_toml(inventory_bytes, "evaluation inventory")
    exact_keys(inventory, ("schema_id", "schema_version", "run_id",
        "deterministic_file_hashes", "excluded_files"), "inventory")
    check(inventory["schema_id"] == SCHEMA_ID && inventory["schema_version"] == SCHEMA_VERSION &&
        inventory["run_id"] == id, "inventory identity mismatch")
    hashes = hash_table(inventory["deterministic_file_hashes"], "inventory hashes";
        allow_outputs=true)
    check(Set(keys(hashes)) == union(Set(keys(declared_hashes(scientific))),
        Set(("rankings.tsv", "metrics.tsv"))),
        "inventory has missing or unexpected deterministic files")
    runtime_file = run["runtime_file"]
    check(runtime_file isa String && runtime_file in ("", "runtime.tsv"), "invalid runtime_file")
    excluded = inventory["excluded_files"]
    check(excluded isa AbstractVector && excluded == (runtime_file == "" ? Any[] : Any["runtime.tsv"]),
        "invalid inventory exclusions")
    expected_files = Set(vcat(["run.toml", "inventory.toml"], collect(keys(hashes)),
        runtime_file == "" ? String[] : ["runtime.tsv"]))
    check(bundle_files(root) == expected_files, "bundle has missing or unexpected files")
    for (relative, expected) in hashes
        check(digest(read(bundle_path(root, relative))) == expected,
            "deterministic file hash mismatch: $relative")
    end
    declared = declared_hashes(scientific)
    check(all(haskey(hashes, path) && hashes[path] == hash for (path, hash) in declared),
        "scientific provenance does not match deterministic inventory")

    cells = parse_tsv(read(bundle_path(root, "rankings.tsv")), RANKING_HEADER, "rankings.tsv")
    ranking_rows = NamedTuple[]
    methods = Set(keys(scientific["methods"]))
    for row in cells
        split_id, method = String(row[1]), String(row[2])
        check(!isempty(split_id) && method in methods, "invalid ranking split or method")
        rank = tryparse(Int, row[3]); check(rank !== nothing && rank > 0, "invalid ranking rank")
        composition = Composition(row[4]); check(formula(composition) == row[4], "ranking formula is not canonical")
        score = isempty(row[5]) ? nothing : tryparse(Float64, row[5])
        check(isempty(row[5]) || score !== nothing && isfinite(score), "invalid ranking score")
        check(valid_digest(row[6]), "invalid ranking tie key")
        check(!isempty(row[7]), "invalid ranking coverage")
        check(row[8] in ("true", "false"), "invalid observed_relevant flag")
        push!(ranking_rows, (split_id=split_id, method=method, rank=rank,
            composition=composition, score=score, tie_key=String(row[6]), coverage=String(row[7]),
            observed_relevant=row[8] == "true"))
    end
    check(!isempty(ranking_rows), "rankings.tsv must not be empty")
    groups = Dict{Tuple{String,String},Vector{NamedTuple}}()
    for row in ranking_rows
        push!(get!(groups, (row.split_id, row.method), NamedTuple[]), row)
    end
    evaluations = NamedTuple[]
    for ((split_id, method), rows) in groups
        sort!(rows; by=row -> row.rank)
        check(getproperty.(rows, :rank) == collect(1:length(rows)), "ranking ranks must be contiguous")
        compositions = getproperty.(rows, :composition)
        check(length(unique(compositions)) == length(compositions), "duplicate ranking composition")
        scores = getproperty.(rows, :score)
        check(all(isnothing, scores) || all(!isnothing, scores), "partially missing ranking scores")
        all(!isnothing, scores) && check(issorted(Float64.(scores); rev=true), "ranking scores are not descending")
        relevant = [row.composition for row in rows if row.observed_relevant]
        check(!isempty(relevant), "ranking has no relevant composition")
        rebuilt = [(composition=row.composition, score=row.score, tie_key=row.tie_key,
            coverage=row.coverage) for row in rows]
        push!(evaluations, (; split_id, method, ranking=rebuilt, relevant))
    end
    rebuilt_rankings, rebuilt_metrics = evaluation_rows(evaluations, scientific)
    check(table_bytes(RANKING_HEADER, rebuilt_rankings) == read(bundle_path(root, "rankings.tsv")),
        "rankings.tsv is not in canonical order")
    check(table_bytes(METRIC_HEADER, rebuilt_metrics) == read(bundle_path(root, "metrics.tsv")),
        "metrics.tsv differs from ranking reconstruction")
    return (; path=root, run_id=id, inventory_sha256=inventory_hash,
        scientific, environment, rankings=rebuilt_rankings, metrics=rebuilt_metrics)
end

end
