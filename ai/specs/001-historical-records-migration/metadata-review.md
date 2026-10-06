# Migration metadata and preservation decisions

Baseline 818e88e; migration date 2026-10-06. Local IDs below are allocated by this
execution. Created dates use an explicit source creation date where present, otherwise the
first recorded Git author-date for the source;
the actual original authoring date is unknown unless stated in the preserved
body. Last source Git date is retained separately from migration `updated`.
Legacy owner/authorship is not established by migration: owner is explicitly
unknown; the migration actor is identified only in the new journal entry.

Historical headings/commands remain evidence. YAML status and the annotation
below express the supported current record state; they do not reopen product
work, authorize archived proposals or establish new hardware/provider acceptance.

| record | status | first recorded Git date | last source Git date | decision and evidence |
| --- | --- | --- | --- | --- |
| `001-emulator-system-volume-delay` | open | 2026-10-06 | 2026-10-06 | Existing local P-107-14 backlog deferred by operator; no resolution or new implementation, corresponding tracking remains #114 on GitHub. Source: `specs/migrate-linux-docker-validation.md` |
| `002-agent-instructions-hierarchy` | done | 2026-10-06 | 2026-10-06 | PR #123 merged 2026-10-06 as 40342ee; supersedes the preserved local-pending heading. Source: `https://github.com/joseluisillana/tonto-kids-assistant/pull/123` |
| `003-agent-secrets-protection` | done | 2026-10-06 | 2026-10-06 | Four repairs/revalidation accepted and documentary closeout merged as e98f43f; #110 covers accidental exposure reduction only, universal isolation deferred. Source: `https://github.com/joseluisillana/tonto-kids-assistant/pull/120` |
| `004-audio-pipeline-phase-3-web-loop` | done | 2026-06-02 | 2026-06-02 | Browser voice loop accepted 2026-06-01; source definition and Week 03 evidence agree. Source: `docs/project-journal/week-03.md#fase-3-web-loop-validation-evidence` |
| `005-audio-pipeline` | done | 2026-05-11 | 2026-06-02 | Raspberry Phase 2B revalidated 2026-05-30, web Phase 3 accepted 2026-06-01; historical contract scope completed. Source: `docs/project-journal/week-03.md#fase-2b-post-tts-revalidation-evidence` |
| `006-ci-local-cache-alignment` | planned | 2026-07-20 | 2026-10-06 | Legacy proposal last explicitly approved for planning 2026-07-20, not implemented as proposed. Superseded by Linux/Docker; retain planned as last supported state, archival only, no execution authorized. Source: `specs/linux-setup-cache-stability.md` |
| `007-conversation-loop` | done | 2026-05-11 | 2026-05-15 | Week 02 closeout 2026-05-15 accepts minimal conversation loop, repeated turns, backend, Raspberry and web. Source: `docs/project-journal/week-02-closeout.md` |
| `008-docker-cleanup` | done | 2026-10-06 | 2026-10-06 | Final accepted #107 matrix includes basic/host/Raspberry cleanup; secret-safe follow-up accepted in #110. Source: `specs/migrate-linux-docker-validation.md` |
| `009-inference-provider-devexpert` | done | 2026-06-13 | 2026-06-13 | Provider phases 0-3 completed 2026-06-13. D025 deprecates real DevExpert operation; done records historical adapter delivery, not current provider availability. Source: `docs/project-journal/week-05.md` |
| `010-inference-provider-openai` | done | 2026-06-13 | 2026-06-13 | Provider phases 0-3 completed 2026-06-13; current adapter contract remains covered, no new real-provider validation in migration. Source: `docs/project-journal/week-05.md` |
| `011-inference-providers` | done | 2026-06-13 | 2026-06-13 | Parent #48 initial phases 0-3 completed 2026-06-13; #53 future backlog is excluded, D025 applies. Source: `docs/project-journal/week-05.md` |
| `012-kivy-ui-docker-emulation` | done | 2026-10-05 | 2026-10-05 | Final #107 emulator acceptance and post-MVP journal evidence establish Docker emulation delivery; this is not Raspberry touch/kiosk acceptance. Source: `specs/migrate-linux-docker-validation.md` |
| `013-kivy-ui-testing-coverage` | done | 2026-10-05 | 2026-10-05 | Real-widget automated suite integrated through #106/#105; #88 physical acceptance is separate. Source: `docs/project-journal/post-mvp-touch-ui.md#2026-10-05--cobertura-de-tests-para-la-ui-kivy` |
| `014-linux-emulator-audio-device-startup` | done | 2026-10-06 | 2026-10-06 | #115 repair integrated and three audible emulator turns accepted in #107 final matrix; #114 volume delay excluded by operator. Source: `specs/migrate-linux-docker-validation.md` |
| `015-linux-emulator-connection-tts` | done | 2026-10-06 | 2026-10-06 | P-107-02/08 repairs and final emulator/CLI voice accepted within #107; source plan contains earlier pending notes retained as history. Source: `specs/migrate-linux-docker-validation.md` |
| `016-linux-setup-cache-stability` | done | 2026-10-06 | 2026-10-06 | Setup/cache repair accepted with official tests/build and final #107 integration; supersedes source in-validation heading. Source: `docs/project-journal/week-06.md#post-mvp--reparación-de-setupcachés-linux-2026-10-05` |
| `017-migrate-linux-docker` | done | 2026-10-03 | 2026-10-05 | Linux/Docker implementation and final #107 validation integrated in a985dac; preserved DRAFT heading is historical, not active status. Source: `https://github.com/joseluisillana/tonto-kids-assistant/pull/108` |
| `018-parallel-agent-workflow` | done | 2026-06-07 | 2026-10-06 | Documentation implementation in commits 4cc27f1/a845d28 and integrated common workflow establishes delivery; original planned heading retained as historical text. Source: `docs/ai-assisted-workflow.md#parallel-agent-workflow` |
| `019-post-migration-stability-validation` | done | 2026-10-06 | 2026-10-06 | Nine-point acceptance in final matrix and operator OK, integrated #108; #88/#114 excluded and D025 enforced. Source: `https://github.com/joseluisillana/tonto-kids-assistant/pull/108` |
| `020-raspberry-listening-indicator` | done | 2026-06-07 | 2026-06-07 | Raspberry indicator accepted 2026-06-07 with two real voice turns; #20/#27 closed with evidence. Source: `docs/project-journal/week-04.md` |
| `021-raspberry-touch-ui` | in-progress | 2026-07-18 | 2026-10-06 | Phases 1-6 and automated coverage completed; #88 kiosk/fallback/final physical validation remains pending. Do not mark the parent spec done. Source: `https://github.com/joseluisillana/tonto-kids-assistant/issues/81` |
| `022-release-v1.0.0` | done | 2026-10-06 | 2026-10-06 | GitHub Release v1.0.0 published 2026-10-06T11:41:52Z, independently verified during migration. Publication completes historical release scope; backlog unchanged. Source: `https://github.com/joseluisillana/tonto-kids-assistant/releases/tag/v1.0.0` |
| `023-web-dependency-audit-remediation` | done | 2026-10-06 | 2026-10-06 | Web audit repair and zero-audit result accepted in Week 06 journal and final #107 matrix. Source: `docs/project-journal/week-06.md#post-mvp--cierre-auditoría-web-p-107-07-2026-10-05` |
| `024-web-listening-indicator` | done | 2026-06-07 | 2026-06-07 | Browser counter/auto-stop/manual-send behavior human accepted 2026-06-07, #23/#25 closed. Source: `docs/project-journal/week-04.md` |
| `025-web-validation-client` | done | 2026-05-15 | 2026-06-02 | Week 02 web integration, Phase 3 microphone loop human acceptance and existing text-speech delivery are recorded in source/plan/journals; completion is historical scope only. Source: `docs/project-journal/week-03.md#fase-3-web-loop-validation-evidence` |
| `026-week-04-demo-stability` | done | 2026-06-02 | 2026-06-07 | Week 04 phases 0-5 closed with dated baseline, resilience, calibration and indicator acceptance. Source: `docs/project-journal/week-04.md` |
| `027-week-05-agent-capability-pack` | done | 2026-06-09 | 2026-10-06 | Capability Pack implemented/integrated #45 and preflight evidence; Linux migration subsequently replaced PowerShell operating examples. Source: `docs/project-journal/week-05.md` |
| `028-week-05-demo-stability` | done | 2026-06-08 | 2026-06-14 | Week 05 phases 0-5 and final demo rehearsal completed 2026-06-13; preserved header date 2026-06-08 is not closure date. Source: `docs/project-journal/week-05.md` |
| `029-week-06-closeout` | done | 2026-06-14 | 2026-06-18 | Week 06 final demo and MVP Definition of Done accepted 2026-06-18. Source: `docs/project-journal/week-06.md` |

## Source preservation ledger

Each source is preserved in its canonical destination, subject only to reviewed
path/link rewrites and appended metadata/provenance. Original bytes can also be
retrieved from baseline 818e88e. SHA-256 is computed from the original source
content, not from generated redirects or metadata. Shared journals/images are
not relocated. No remote GitHub issue definition or comment history is copied.

| original source | canonical destination | original SHA-256 |
| --- | --- | --- |
| `docs/agent-secrets-credential-options.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-credential-options.md` | `0a2dd9582e7d20d9feecb4e4cb4801a2a653ac9e1d47a1ebd8a20a6eb8d0d5d1` |
| `docs/agent-secrets-isolation-design.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-isolation-design.md` | `e741e31a84f4ce043c4a4981a378d13f2d16fc06efd500901f2b4434496718de` |
| `docs/agent-secrets-protection-draft.md` | `ai/specs/003-agent-secrets-protection/artifacts/agent-secrets-protection-draft.md` | `1152f7c7eb907c2933be4805bf3a17e2e3be6c063d9e18b12813db89e31a1a15` |
| `docs/issues/emulator-system-volume-delay.md` | `ai/issues/001-emulator-system-volume-delay/issue.md` | `85d7becc937150d63f0b1d5080fecd7b9672745f153aa762fa2f171d2c58d399` |
| `docs/plans/agent-instructions-hierarchy-implementation-plan.md` | `ai/specs/002-agent-instructions-hierarchy/plan.md` | `0d209f78ac0b537861a9d9bb237205d36b7f5443cdebb08778ad6554d95d8a67` |
| `docs/plans/agent-secrets-protection-implementation-plan.md` | `ai/specs/003-agent-secrets-protection/plan.md` | `30c99ed2a33047b54fa7388abbc12fbc10f0b868f476e7d9274c161aa0e51f96` |
| `docs/plans/ci-local-cache-alignment-implementation-plan.md` | `ai/specs/006-ci-local-cache-alignment/plan.md` | `a3b8a171013c017481eb076293829db7e079cb755f586d047053e96a2aaa659a` |
| `docs/plans/docker-cleanup-implementation-plan.md` | `ai/specs/008-docker-cleanup/plan.md` | `7482595a57c32eee9e656d0ab3886cecde09bedfe95263b62523830c859e34d4` |
| `docs/plans/inference-providers.md` | `ai/specs/011-inference-providers/plan.md` | `958d2f6480baf6708c8cbab12ab4fd8f9245731a1686f27854ff794066878ed8` |
| `docs/plans/kivy-ui-docker-emulation-plan.md` | `ai/specs/012-kivy-ui-docker-emulation/plan.md` | `126a997adbbc1eb9f1c1b489425e4ebd55a97268322ae54e70d8b3a7d724554f` |
| `docs/plans/kivy-ui-testing-coverage-plan.md` | `ai/specs/013-kivy-ui-testing-coverage/plan.md` | `7351d85d6de300b6892934573cb3fe08de29dc7b7be3c20aaa689bb750862e5a` |
| `docs/plans/linux-emulator-audio-device-startup-implementation-plan.md` | `ai/specs/014-linux-emulator-audio-device-startup/plan.md` | `2d11c66050c86c6a774b57fe05dba1a33d12719331096a12abe89e3f7a0237ef` |
| `docs/plans/linux-emulator-connection-tts-implementation-plan.md` | `ai/specs/015-linux-emulator-connection-tts/plan.md` | `b68c5b33765016fec65786298a942ed1eb0a4464a28687cff52a46be174aa4e8` |
| `docs/plans/linux-setup-cache-stability-implementation-plan.md` | `ai/specs/016-linux-setup-cache-stability/plan.md` | `e7bda516b0f6f3f82602250ba9c8596114c014de24c66bfa106fce9d36e43425` |
| `docs/plans/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/plan.md` | `0f3e04b1b2df8a51fd65f0e6deee009cca12aa34b7728aaaeb389a75d8e091b6` |
| `docs/plans/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/plan.md` | `f2e30256bcce4a97601a263015c8fb3e93efa7e80e44b5945e0f0849b940ee5e` |
| `docs/plans/post-migration-stability-validation-implementation-plan.md` | `ai/specs/019-post-migration-stability-validation/plan.md` | `5b5782e704682975f5bb6b1de37ce39dc2819dd39515ee30edae8b81ce1ee234` |
| `docs/plans/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/plan.md` | `5bc51a77d90d5b5b3eb918877486dc6cc78366d4091ac32ae6fac322cf34a3d6` |
| `docs/plans/raspberry-touch-ui-implementation-plan.md` | `ai/specs/021-raspberry-touch-ui/plan.md` | `81bd8aca6f01e862f4aa2892906f28db27164c24f3389f45c5436070d165f305` |
| `docs/plans/release-v1.0.0-implementation-plan.md` | `ai/specs/022-release-v1.0.0/plan.md` | `4edc55e1a76ede1773537cb65db391752395be3a515967d9da6e7b6bbf9ec19e` |
| `docs/plans/web-dependency-audit-remediation-implementation-plan.md` | `ai/specs/023-web-dependency-audit-remediation/plan.md` | `0f2eae3f8f6d7f9b83125f0fae3da5e6441a5af5e8b2202a3378b7f0e0219162` |
| `docs/plans/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/plan.md` | `4c62b01600309d103abbc3efd92a257a8dd7f329d289b22023d283552904cad4` |
| `docs/plans/web-text-chat-spoken-response.md` | `ai/specs/025-web-validation-client/artifacts/text-speech-plan.md` | `489ed329cf8c44dd91e1c0d45c08f3cb63e173db78de40c44f4be29271dedcab` |
| `docs/plans/week-03-phase-2b-opencode.md` | `ai/specs/005-audio-pipeline/plan.md` | `2f0dadbddc49c88324ea9bf80fa8290e0765051680b4de84d5ad7d4e92a342a6` |
| `docs/plans/week-03-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/browser-validation-plan.md` | `a0ef2560bdfe860e7180f200b77a7301746bb32aed9ce48b60f000a1de2ef7da` |
| `docs/plans/week-03-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/plan.md` | `ccab322d78c9c2551ccba473f9377393f5acc5bc25b488df08a0c496d87b5a29` |
| `docs/plans/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/plan.md` | `b996059210c43bd9f410eac6e224eacd40b2b8a1bd8852340e1b4eb4ad63c41e` |
| `docs/plans/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/plan.md` | `0644894a013b7d2b8b6c02a40e44872d09ea675ce53e2cfdd925bc0979d86ddc` |
| `docs/plans/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/plan.md` | `741a29ab424af9e7e9aa428eb31a208dc94df5428a4d5834669d7e6d6763a45d` |
| `docs/plans/week-06-closeout.md` | `ai/specs/029-week-06-closeout/plan.md` | `8e0e2c9f424529373cdce8e7aa744a36ed87aa0345d77cc457412fc173706d2c` |
| `docs/web-dependency-audit-triage.md` | `ai/specs/023-web-dependency-audit-remediation/artifacts/web-dependency-audit-triage.md` | `410866dd356f1e44f7440f5e4699a8e150a258d7be283a7d7037b91f895eac5b` |
| `specs/agent-instructions-hierarchy.md` | `ai/specs/002-agent-instructions-hierarchy/spec.md` | `f6f9387a68869cdcf61a3bb61a22efc36b7f5b53174e2884e492a187c5221292` |
| `specs/agent-secrets-protection.md` | `ai/specs/003-agent-secrets-protection/spec.md` | `76615b6636cfcb7b382ee0259c2da7fd12027a90fee5dd47ea00b071a90e303f` |
| `specs/audio-pipeline-phase-2a-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2a-validation-guide.md` | `8d07ca7f5a517ba5590b4dc9ffc968109aa0d7de3da754be0b428c53e8d50ba8` |
| `specs/audio-pipeline-phase-2b-tts-revalidation.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-tts-revalidation.md` | `98fb7e637071a71d049c8931cb838f2f7a242ad4afa7552076d18d5417c41689` |
| `specs/audio-pipeline-phase-2b-validation-guide.md` | `ai/specs/005-audio-pipeline/artifacts/audio-pipeline-phase-2b-validation-guide.md` | `6f86e3295e7ff86407536ded2eff1d96286e4856d0dbec94a2e3120c8d922cf1` |
| `specs/audio-pipeline-phase-3-browser-manual-validation.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/artifacts/audio-pipeline-phase-3-browser-manual-validation.md` | `07e12430c1051c1da45884c892614d71d8ce6583ffd8bc4d2f29e849226f8d1d` |
| `specs/audio-pipeline-phase-3-web-loop.md` | `ai/specs/004-audio-pipeline-phase-3-web-loop/spec.md` | `b8bc27f47e1f6a9b8e674258437332b851bdde2acfbc160da88ba3e8c36cdea6` |
| `specs/audio-pipeline.md` | `ai/specs/005-audio-pipeline/spec.md` | `1f6c26d7bf3238c37d5eae3a79ef1110b1c80af4e9dc38d65925641a402362da` |
| `specs/ci-local-cache-alignment.md` | `ai/specs/006-ci-local-cache-alignment/spec.md` | `b6f04ead3ce3fc5ac2df746ec65c912be3769cae89518dcff90fdcbe003bc2f5` |
| `specs/conversation-loop.md` | `ai/specs/007-conversation-loop/spec.md` | `6533eb5d83036bba1dafd14783aec38227139a5592c7a6e9b5cae087df15cb6a` |
| `specs/docker-cleanup.md` | `ai/specs/008-docker-cleanup/spec.md` | `76fadbc177b527a714c8b2232e0a851d79eac3038699f88c7e46dd06d5a8719a` |
| `specs/inference-provider-devexpert.md` | `ai/specs/009-inference-provider-devexpert/spec.md` | `d418de14a32fed5571ac6a21403ec745d8a807f0a8606f6676c948d56d76e661` |
| `specs/inference-provider-openai.md` | `ai/specs/010-inference-provider-openai/spec.md` | `07644da9cba682bdd2c7be39b6fc8aa85a81618f5597ed13b9f35946cac02435` |
| `specs/inference-providers.md` | `ai/specs/011-inference-providers/spec.md` | `83047b60ce4480852c2597048a1377f86986891470e494d0a8369ebf122c1c2a` |
| `specs/kivy-ui-docker-emulation.md` | `ai/specs/012-kivy-ui-docker-emulation/spec.md` | `bec6b99f17cad9a1a6913539638051ae03a9e0e06fe83fd5bcfe61087c22a4b0` |
| `specs/kivy-ui-testing-coverage.md` | `ai/specs/013-kivy-ui-testing-coverage/spec.md` | `891457d967e0428f03ca0c13009fc48964b4bccdfeed79ad97d78633dc4bef84` |
| `specs/linux-emulator-audio-device-startup.md` | `ai/specs/014-linux-emulator-audio-device-startup/spec.md` | `fc859acd403429a0c380281488926beecd8d4617a320d927e7418525c8a95e0a` |
| `specs/linux-emulator-connection-tts.md` | `ai/specs/015-linux-emulator-connection-tts/spec.md` | `18c2c928cb673b37f76709895a1ef08970a43dd1130e86633779ea7bbaf932b7` |
| `specs/linux-setup-cache-stability.md` | `ai/specs/016-linux-setup-cache-stability/spec.md` | `a2f1bd8c6d50dfeac2cc869da2d41a28fdffb7115009749142e5c3f769ebe59a` |
| `specs/migrate-linux-docker-validation.md` | `ai/specs/019-post-migration-stability-validation/artifacts/migrate-linux-docker-validation.md` | `e823abafc4901e1f7b10984458f0cfb0c386e0feca1d306e33f4ee6f6462463e` |
| `specs/migrate-linux-docker.md` | `ai/specs/017-migrate-linux-docker/spec.md` | `ebe3cc26a13d03b4495892157fee81aca75104684deee897134bc558619b53a3` |
| `specs/parallel-agent-workflow.md` | `ai/specs/018-parallel-agent-workflow/spec.md` | `2514c2ca3cb0919ccaffbfc28b4a890d8ccb14cb11565bddabb6db1b63c643a8` |
| `specs/post-migration-stability-validation.md` | `ai/specs/019-post-migration-stability-validation/spec.md` | `8ab6fe175cd2b6eeaf88417bfb5e72e119e00f4fd1a830c1985d5cb970d44494` |
| `specs/raspberry-listening-indicator.md` | `ai/specs/020-raspberry-listening-indicator/spec.md` | `f2579c30b2d2c308ec44609308a32edb4fb87c08f07415c35240f33baba43f21` |
| `specs/raspberry-touch-ui.md` | `ai/specs/021-raspberry-touch-ui/spec.md` | `124e69b7d5f142fd9708eb335f415b5d357ccdb5121ceea3ed44006c23a003fd` |
| `specs/release-v1.0.0.md` | `ai/specs/022-release-v1.0.0/spec.md` | `e4a4ddc5bb9a934b1048e61ddd319980b63f7f8405a26ce0c5f4333b30c3a064` |
| `specs/web-dependency-audit-remediation.md` | `ai/specs/023-web-dependency-audit-remediation/spec.md` | `eca5e64f9a68779582e6f0ffec4ec0a5a77c153f6abc275039709ce9e1450a6e` |
| `specs/web-listening-indicator.md` | `ai/specs/024-web-listening-indicator/spec.md` | `37e558dd43e4e19d30531d1f89985c80fd03069a36d18283e8935695c4b34d23` |
| `specs/web-validation-client.md` | `ai/specs/025-web-validation-client/spec.md` | `71119b36636ac3f54486652dc491c15930f5efcbf069090d819de95db55f48cc` |
| `specs/week-04-demo-stability.md` | `ai/specs/026-week-04-demo-stability/spec.md` | `afc01041e6950885eae4a2bc507ea237026ef7a8e4fa7d03ce9c4bc2a027a272` |
| `specs/week-05-agent-capability-pack.md` | `ai/specs/027-week-05-agent-capability-pack/spec.md` | `853eb64b3142821a652788dc56a37f4bba2ab3279ee45226f92f037e7742e3f0` |
| `specs/week-05-demo-stability.md` | `ai/specs/028-week-05-demo-stability/spec.md` | `8eec2e9c56fbcc40f7f8a515b45449cd1d281f72b2ff79f6a5a64834e063ec2c` |
| `specs/week-06-closeout.md` | `ai/specs/029-week-06-closeout/spec.md` | `1fb3120df2b3f81e06293b39771feb4c8cf217535c3e49d6388df49722a127f3` |

Explicit source creation dates override Git recording dates for records 014 and
019: created 2026-10-05, first recorded in Git 2026-10-06. Both facts are retained.

Preservation verification also normalizes nine inherited single trailing spaces
in relocated bodies to satisfy staged diff checks. Intentional Markdown hard
breaks are retained. No content or acceptance criteria change; original hashes
remain exact. The original body comparison accounts only for mapped path rewrites
and this explicit whitespace normalization.

## Additional structural sources preserved before retirement

| original source | preserved destination | original SHA-256 |
| --- | --- | --- |
| `docs/plans/TEMPLATE-spec-implementation-plan.md` | Git baseline `818e88eacbac3989c091d1294c92e26ebeb663f7`; retired without a legacy copy | `f1d7f63dd332ca30f32ff1fdfc246067e7070ffde48c5c1758f5408211425986` |
| `docs/plans/ai-process-instrumentation-plan.md` | `ai/specs/001-historical-records-migration/artifacts/ai-process-instrumentation-plan.md` | `8f3f1bd330336c74993521f01cfbb3d411e6f4e634ddb896bdaf00186e6e06ad` |
| `specs/AGENTS.md` | `ai/specs/AGENTS.md` | `014385d256d39a32b0b49a0f4f59f87f6b057dea9ee38542e5a3d0d5ef391960` |

The original instruction file remains recoverable at the same Git baseline.
Active instructions preserve operating and safety rules while reconciling obsolete
placement clauses with ai/. Only current ai/ rules and templates govern new work.
The operator explicitly requested removal of legacy template references and copies.
