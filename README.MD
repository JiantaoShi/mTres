# Regression analysis of scRNA-seq data

This is a set of wrapper scripts for the regression analysis of scRNA-seq data. If use the scripts here, please cite the original [Tres](https://github.com/data2intelligence/Tres) publication. Both `signature.centroid.expand` and `Tres.kegg` were directly downloaded from the `Tres` code base.

## Input
The gene expression input is a pandas data frame, saved wither as a `TAB` separated CSV file. The procedures to normalize the data:

- filtering out genes that are not expressed in most cells
- Scaling counts to a fixed number (100,000)
- log2(counts + 1)
- Mean centralization on all cells

## Signature/pathway activity
For given pathways/signatures, the following script calculates a score for each cell which quantifies the overall activity of given signatures/pathways.

```
usage: mtres_response.py [-h] -E EXPRESSION_FILE -G GENESETS_GMT_FILE -S SIGNATURE_NAME_FILE -O OUTPUT_TAG

optional arguments:
  -h, --help            show this help message and exit
  -E EXPRESSION_FILE, --expression_file EXPRESSION_FILE
                        Gene expression file.
  -G GENESETS_GMT_FILE, --genesets_GMT_file GENESETS_GMT_FILE
                        Background gene sets in GMT format.
  -S SIGNATURE_NAME_FILE, --signature_name_file SIGNATURE_NAME_FILE
                        Names of the signatures, one name in one line.
  -O OUTPUT_TAG, --output_tag OUTPUT_TAG
                        Prefix for output files.
```

Please make sure gene set names specified with `-S` can be found in GMT input file.

## Weighted signatures
Alternatively, a signature can be represented by a numeric vector. The activities of such signatures can be calculated using the following scripts:

```
usage: mtres_signaling.py [-h] -E EXPRESSION_FILE -M MODEL_MATRIX_FILE -O OUTPUT_TAG

optional arguments:
  -h, --help            show this help message and exit
  -E EXPRESSION_FILE, --expression_file EXPRESSION_FILE
                        Gene expression file.
  -M MODEL_MATRIX_FILE, --model_matrix_file MODEL_MATRIX_FILE
                        Quantitative signatures for cytokines.
  -O OUTPUT_TAG, --output_tag OUTPUT_TAG
                        Prefix for output files.
```

## Interaction analysis
This script is to test whether there are interaction between two variables, using [Ridge regression](https://github.com/data2intelligence/ridge_significance).

```
usage: mtres_interaction.py [-h] [-E EXPRESSION_FILE] -R RESPONSE_DATA -S SIGNALING_DATA [-O OUTPUT_TAG] [-C COUNT_THRESHOLD] [-RK RESPONSE_KEY]
                            [-SK SIGNALING_KEY] [-QC]

optional arguments:
  -h, --help            show this help message and exit
  -E EXPRESSION_FILE, --expression_file EXPRESSION_FILE
                        Gene expression file.
  -R RESPONSE_DATA, --response_data RESPONSE_DATA
                        Precomputed response data frame.
  -S SIGNALING_DATA, --signaling_data SIGNALING_DATA
                        Precomputed signaling data frame.
  -O OUTPUT_TAG, --output_tag OUTPUT_TAG
                        Prefix for output files.
  -C COUNT_THRESHOLD, --count_threshold COUNT_THRESHOLD
                        Minimal number of cells needed for regression [100].
  -RK RESPONSE_KEY, --response_key RESPONSE_KEY
                        Name of response in the data table [Proliferation].
  -SK SIGNALING_KEY, --signaling_key SIGNALING_KEY
                        Name of signaling in the data table [TGFB1].
  -QC, --run_qc         whether run QC workflow
```
