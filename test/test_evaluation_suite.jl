using TOML

const EvaluationSuite = EkaCompositions.Research.EvaluationSuite
const ES = EvaluationSuite

function suite_fixture(root)
    files = Dict(
        "provenance/input.tsv" => "composition\nLiNaO\n",
        "provenance/audit.jl" => "audit = 1\n",
        "provenance/code.jl" => "code = 1\n",
        "provenance/Manifest.toml" => "manifest = 1\n",
        "memberships/split-00.tsv" => "composition\tlabel\nCaLiO2\tpositive\n",
        "provenance/protocol.md" => "# Synthetic protocol\n",
    )
    for (path, text) in files
        destination = joinpath(root, split(path, '/')...)
        mkpath(dirname(destination))
        write(destination, text)
    end
    code = ES.source_identity(root, ["provenance/code.jl"];
        commit="0123456789abcdef", dirty=false,
        dependency_locks=["provenance/Manifest.toml"])
    scientific = Dict{String,Any}(
        "dataset" => Dict("id" => "synthetic-ternaries", "version" => "1",
            "retrieval_metadata" => "fixture generated in test",
            "input_hashes" => Dict("provenance/input.tsv" => ES.digest(codeunits(files["provenance/input.tsv"])))),
        "audit" => Dict("algorithm" => "synthetic-audit-v1",
            "implementation_hashes" => Dict("provenance/audit.jl" => ES.digest(codeunits(files["provenance/audit.jl"])))),
        "code" => code,
        "protocol" => Dict("id" => "synthetic-suite-v1",
            "sha256" => ES.digest(codeunits(files["provenance/protocol.md"])),
            "artifact" => "provenance/protocol.md"),
        "split" => Dict("algorithm" => "synthetic-system-holdout-v1",
            "label_policy" => "original",
            "membership_hashes" => Dict("memberships/split-00.tsv" =>
                ES.digest(codeunits(files["memberships/split-00.tsv"])))),
        "candidates" => Dict("definition" => "all disjoint synthetic candidates",
            "exclusion_counts" => Dict("training_overlap" => 0)),
        "methods" => Dict("pair_frequency" => Dict("model_id" => PF.MODEL_ID)),
        "seed_roles" => Dict("tie" => 20260901, "split" => 0),
        "metric" => Dict("algorithm" => "recovery_metrics", "version" => "1",
            "budgets" => [1, 3], "grouping_rule" => "unordered element set",
            "denominator_counts" => Dict("candidates" => 4, "relevant" => 2)),
    )
    environment = Dict{String,Any}(
        "julia_version" => string(VERSION), "python_version" => "not-used",
        "os" => string(Sys.KERNEL), "architecture" => string(Sys.ARCH),
        "cpu" => Sys.CPU_NAME, "threads" => Threads.nthreads(), "accelerator" => "none")
    model = PF.fit(["LiNaO", "LiKO", "MgCaO"])
    ranking = PF.rank_candidates(model, ["LiNaO2", "Li2NaO3", "CaLiO2", "KNaO2"])
    evaluations = [(split_id="split-00", method="pair_frequency", ranking=ranking,
        relevant=["CaLiO2", "KNaO2"])]
    artifacts = Dict(path => read(joinpath(root, split(path, '/')...)) for path in keys(files))
    return (; scientific, environment, evaluations, artifacts)
end

function rewrite_inventory!(bundle, changed_path)
    inventory_path = joinpath(bundle, "inventory.toml")
    inventory = TOML.parsefile(inventory_path)
    inventory["deterministic_file_hashes"][changed_path] = ES.digest(read(joinpath(bundle, split(changed_path, '/')...)))
    EkaCompositions.recovery_write_toml(inventory_path, inventory)
    run_path = joinpath(bundle, "run.toml")
    run = TOML.parsefile(run_path)
    run["inventory_sha256"] = ES.digest(read(inventory_path))
    EkaCompositions.recovery_write_toml(run_path, run)
end

function rewrite_run_identity!(mutate, bundle)
    run_path = joinpath(bundle, "run.toml")
    inventory_path = joinpath(bundle, "inventory.toml")
    run = TOML.parsefile(run_path)
    inventory = TOML.parsefile(inventory_path)
    mutate(run, inventory)
    run["run_id"] = ES.run_id(run["scientific"])
    inventory["run_id"] = run["run_id"]
    EkaCompositions.recovery_write_toml(inventory_path, inventory)
    run["inventory_sha256"] = ES.digest(read(inventory_path))
    EkaCompositions.recovery_write_toml(run_path, run)
    return run["run_id"]
end

@testset "Uniform evaluation bundle" begin
    mktempdir() do root
        fixture = suite_fixture(root)
        first_path = joinpath(root, "bundle-a")
        first_result = ES.write_bundle(first_path; fixture...,
            runtime_rows=[(split_id="split-00", method="pair_frequency", seconds=1.25)])

        @test length(first_result.run_id) == 64
        @test length(first_result.inventory_sha256) == 64
        @test length(first_result.rankings) == 4
        @test getproperty.(first_result.metrics, :budget) == [1, 3]
        @test isfile(joinpath(first_path, "run.toml"))
        @test isfile(joinpath(first_path, "inventory.toml"))
        @test isfile(joinpath(first_path, "rankings.tsv"))
        @test isfile(joinpath(first_path, "metrics.tsv"))
        @test isfile(joinpath(first_path, "runtime.tsv"))

        # A fixed scientific configuration and deterministic ranking reproduce
        # exactly even when runtime observations differ.
        second_path = joinpath(root, "bundle-b")
        second_result = ES.write_bundle(second_path; fixture...,
            runtime_rows=[(split_id="split-00", method="pair_frequency", seconds=99.0)])
        @test second_result.run_id == first_result.run_id
        @test second_result.inventory_sha256 == first_result.inventory_sha256
        @test read(joinpath(second_path, "run.toml")) == read(joinpath(first_path, "run.toml"))
        @test read(joinpath(second_path, "inventory.toml")) == read(joinpath(first_path, "inventory.toml"))
        @test read(joinpath(second_path, "rankings.tsv")) == read(joinpath(first_path, "rankings.tsv"))
        @test read(joinpath(second_path, "metrics.tsv")) == read(joinpath(first_path, "metrics.tsv"))
        @test read(joinpath(second_path, "runtime.tsv")) != read(joinpath(first_path, "runtime.tsv"))

        @test_throws ArgumentError ES.write_bundle(first_path; fixture...)
        missing_parent = joinpath(root, "missing", "bundle")
        @test_throws ArgumentError ES.write_bundle(missing_parent; fixture...)

        failed = joinpath(root, "partial")
        @test_throws ErrorException ES.write_bundle(failed; fixture...,
            _after_reserve=_ -> error("injected write failure"))
        @test !ispath(failed)
    end
end

@testset "Evaluation schema and identity validation" begin
    mktempdir() do root
        fixture = suite_fixture(root)
        for mutate in (
                value -> delete!(value["dataset"], "version"),
                value -> (value["dataset"]["extra"] = "no"),
                value -> (value["metric"]["budgets"] = [3, 1]),
                value -> (value["code"]["source_tree_sha256"] = repeat("0", 64)),
                value -> (value["code"]["dirty"] = "false"))
            scientific = deepcopy(fixture.scientific)
            mutate(scientific)
            @test_throws ArgumentError ES.write_bundle(joinpath(root, "invalid-$(rand(UInt))");
                scientific, environment=fixture.environment,
                evaluations=fixture.evaluations, artifacts=fixture.artifacts)
        end
        bad_environment = deepcopy(fixture.environment)
        bad_environment["threads"] = "1"
        @test_throws ArgumentError ES.write_bundle(joinpath(root, "bad-environment");
            scientific=fixture.scientific, environment=bad_environment,
            evaluations=fixture.evaluations, artifacts=fixture.artifacts)

        clean = ES.source_identity(root, ["provenance/code.jl"];
            commit="abc", dirty=false)
        dirty_flag = ES.source_identity(root, ["provenance/code.jl"];
            commit="abc", dirty=true)
        @test clean["source_tree_sha256"] == dirty_flag["source_tree_sha256"]
        @test clean["dirty"] === false && dirty_flag["dirty"] === true
        write(joinpath(root, "provenance", "code.jl"), "code = 2\n")
        changed = ES.source_identity(root, ["provenance/code.jl"];
            commit="abc", dirty=true)
        @test changed["source_tree_sha256"] != clean["source_tree_sha256"]
    end
end

@testset "Evaluation tamper detection" begin
    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        original = ES.write_bundle(bundle; fixture...)

        # A changed captured source fails before any checksum rewrite.
        input_path = joinpath(bundle, "provenance", "input.tsv")
        write(input_path, "composition\nLiKO\n")
        @test_throws ArgumentError ES.validate_bundle(bundle)

        # Rewriting the artifact hash, inventory, run ID and all internal links
        # creates a different internally consistent run. The externally recorded
        # run ID still detects that coordinated provenance rewrite.
        run_path = joinpath(bundle, "run.toml")
        run = TOML.parsefile(run_path)
        new_hash = ES.digest(read(input_path))
        run["scientific"]["dataset"]["input_hashes"]["provenance/input.tsv"] = new_hash
        run["run_id"] = ES.run_id(run["scientific"])
        inventory_path = joinpath(bundle, "inventory.toml")
        inventory = TOML.parsefile(inventory_path)
        inventory["run_id"] = run["run_id"]
        inventory["deterministic_file_hashes"]["provenance/input.tsv"] = new_hash
        EkaCompositions.recovery_write_toml(inventory_path, inventory)
        run["inventory_sha256"] = ES.digest(read(inventory_path))
        EkaCompositions.recovery_write_toml(run_path, run)
        @test ES.validate_bundle(bundle).run_id == run["run_id"]
        @test_throws ArgumentError ES.validate_bundle(bundle; expected_run_id=original.run_id)
    end


    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        ES.write_bundle(bundle; fixture...)
        captured = joinpath(bundle, "provenance", "input.tsv")
        rm(captured)
        symlink(joinpath(root, "provenance", "input.tsv"), captured)
        @test_throws ArgumentError ES.validate_bundle(bundle)
    end

    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        original = ES.write_bundle(bundle; fixture...)
        ranking_path = joinpath(bundle, "rankings.tsv")
        text = read(ranking_path, String)
        write(ranking_path, replace(text, "observed_pair" => "observed_pair_rewritten"; count=1))
        rewrite_inventory!(bundle, "rankings.tsv")
        # Coverage is diagnostic, so metric reconstruction remains valid after
        # checksums are rewritten. An external inventory identity detects it.
        @test ES.validate_bundle(bundle).run_id == original.run_id
        @test_throws ArgumentError ES.validate_bundle(bundle;
            expected_inventory_sha256=original.inventory_sha256)
    end

    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        ES.write_bundle(bundle; fixture...)
        metrics = joinpath(bundle, "metrics.tsv")
        write(metrics, replace(read(metrics, String), "\t0\t" => "\t1\t"; count=1))
        rewrite_inventory!(bundle, "metrics.tsv")
        @test_throws ArgumentError ES.validate_bundle(bundle)
    end


    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        original = ES.write_bundle(bundle; fixture...)
        membership = joinpath(bundle, "memberships", "split-00.tsv")
        write(membership, "composition\tlabel\nKNaO2\tpositive\n")
        changed = ES.digest(read(membership))
        rewrite_run_identity!(bundle) do run, inventory
            run["scientific"]["split"]["membership_hashes"]["memberships/split-00.tsv"] = changed
            inventory["deterministic_file_hashes"]["memberships/split-00.tsv"] = changed
        end
        @test ES.validate_bundle(bundle).run_id != original.run_id
        @test_throws ArgumentError ES.validate_bundle(bundle; expected_run_id=original.run_id)
    end

    mktempdir() do root
        fixture = suite_fixture(root)
        bundle = joinpath(root, "bundle")
        original = ES.write_bundle(bundle; fixture...)
        rewrite_run_identity!(bundle) do run, _
            run["scientific"]["methods"]["pair_frequency"]["model_id"] = "rewritten-model"
        end
        @test ES.validate_bundle(bundle).run_id != original.run_id
        @test_throws ArgumentError ES.validate_bundle(bundle; expected_run_id=original.run_id)
    end
end
