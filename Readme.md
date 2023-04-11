# Modifies Eval

There are 3 main changes to the already exiting Trackeval code:
    - The code is modified to work with the SkyData annotations
    - MetricsResources
    - SkyDataAnnotationTools

## MetricsResources
the folder contains definitions for different metrics and formulars.
The folder also contains references to the metrics used in the paper.

## SkyDataAnnotationTools
The folder contains a script to generate a fake submission like file from ground truth (gt) annotations.
Depending on the capacity you can increase the test file size.

### Usage

download the SkyData annotations  from the [train_SKYVOS.json](https://www.skydata.ai/) and place the annotations in the folder `SkyDataAnnotationTools/gt_files/`

```bash
cd SkyDataAnnotationTools
python3 generate_fake_submission.py

# the generated file will be in the folder `SkyDataAnnotationTools` and will be named `fake_submission_from_gt.json`
#copy the train_SKYVOS to `data/gt/skydata_challenge/skydata/`
#copy the fake_submission_from_gt.json to `data/trackers/skydata_challenge/skydata/example_tracker/data/`

```
## Evaluation

```bash
python3 scripts/run_skdata_challenge.py 
```


## Resources
- download data folder from [data](https://www.skydata.ai/)

