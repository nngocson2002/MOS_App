# MOS Evaluation Application

## Introduction
This application is designed for Mean Opinion Score (MOS) evaluation of audio samples.

## Installation
1. Set up a Conda environment.
2. Install the required dependencies by running:

```shell
pip install -r requirements.txt
```

## Quick Start

To launch the application, execute:
```shell
python app.py
```

Evaluation results will be saved into `results` directory.

## Data Preparation
Before running the application, prepare a folder containing `N` CSV files, where `N` is the number of participants expected to perform evaluations.

Each CSV file should have four columns with `n` rows (`n` can vary between files):
- `filepath`: Path to the audio file being evaluated.
- `gt`: Ground-truth audio corresponding to `filepath`.
- `model`: The model that generated `filepath`.
- `transcript`: Ground-truth transcript of `filepath`.

Refer to the sample in the [data](./samples/data) directory.

## How Does This Tool Work?

The `MOSApp` class in `app.py` loads and stores each CSV file as an attribute. When users enter their IDs, the application automatically assigns a unique CSV file to each user, ensuring that no two users evaluate the same file.

Each user's progress is saved in the `progress` directory. If a user returns to finish their evaluation and enters the same ID as before, their previous progress will be automatically restored.