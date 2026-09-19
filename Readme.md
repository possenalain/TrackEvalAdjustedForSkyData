# TrackEval for SkyData

An adaptation of [TrackEval](https://github.com/JonathonLuiten/TrackEval) for evaluating **multi-object tracking and video instance segmentation on SkyData**, a UAV video dataset whose annotations use a YouTube-VIS-style JSON format.

It was developed for research on aerial video, where the standard evaluation code does not read the dataset's annotations out of the box.

> This is a modified copy of the upstream TrackEval project and keeps its MIT license and original documentation ([`OriginalReadme.md`](OriginalReadme.md)). All the metric implementations come from upstream; the additions listed below are specific to SkyData.

## What was added

| Addition | Where | What it does |
|---|---|---|
| SkyData dataset class | [`trackeval/datasets/skydata.py`](trackeval/datasets/skydata.py) | Loads SkyData ground truth and tracker output so upstream TrackEval can evaluate them. |
| Runner script | [`scripts/run_skydata_challenge.py`](scripts/run_skydata_challenge.py) | Command-line entry point, same style as the other `run_*.py` scripts. |
| Format description | [`docs/Skydata-format.txt`](docs/Skydata-format.txt) | The JSON schema for ground truth and predictions (COCO-style, adapted to video). |
| Metric explainers | [`MetricsResources/`](MetricsResources/) | Notebooks and notes on how each metric is defined, implemented and interpreted, with references to the metrics used in the paper. |
| Fake-submission generator | [`SkyDataAnnotationTools/`](SkyDataAnnotationTools/) | Builds a tracker-style prediction file from the ground truth, so you can sanity-check the whole pipeline end to end and stress-test it with larger files. |

## Metrics

Everything upstream TrackEval computes is available; the ones reported in this work are **HOTA** (with DetA, AssA, LocA and related sub-metrics), **CLEAR MOT** (MOTA, MOTP, ID switches, mostly-tracked/lost, ...), **Identity** (IDF1, IDR, IDP) and **TrackMAP** (AP/AR by object size). See [`MetricsResources/metricsUSed.md`](MetricsResources/metricsUSed.md) for the full list.

## Usage

**1. Get the data.** Download the SkyData annotations (`train_SKYVOS.json`) from the [shared folder](https://drive.google.com/drive/folders/1TjyGmMsLRCY44EZbhvwA2_rbdu7orkzE?usp=sharing) and place the file in `SkyDataAnnotationTools/gt_files/`.

**2. (Optional) Generate a fake submission from the ground truth.**

```bash
cd SkyDataAnnotationTools
python3 create_fake_submission_from_gt.py
# writes SkyDataAnnotationTools/gt_files/fake_submission_from_gt_<n>.json
```

**3. Put the files where the evaluator looks for them.**

```
data/gt/skydata_challenge/skydata/                              <- train_SKYVOS.json
data/trackers/skydata_challenge/skydata/example_tracker/data/   <- your predictions (or the fake submission)
```

**4. Run the evaluation.**

```bash
pip install -r requirements.txt
python3 scripts/run_skydata_challenge.py
```

Pass `--help` to see every option (metrics, splits, output folders, parallelism), as with the upstream `run_*.py` scripts.

## Repository layout

```
trackeval/               # evaluation library (upstream, plus datasets/skydata.py)
scripts/                 # run_*.py entry points for each benchmark (upstream, plus run_skydata_challenge.py)
docs/                    # annotation format descriptions, including Skydata-format.txt
MetricsResources/        # notebooks and notes explaining the metrics
SkyDataAnnotationTools/  # fake-submission generator for sanity checks
tests/                   # upstream test suite
```

## Credits

Built on [TrackEval](https://github.com/JonathonLuiten/TrackEval) by Jonathon Luiten and contributors, released under the MIT license. If you use the HOTA metric or the evaluation code, please cite the upstream project as described in [`OriginalReadme.md`](OriginalReadme.md).

## License

MIT, inherited from upstream. See [`LICENSE`](LICENSE).
