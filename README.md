# Plant biosignal classification

**This notebook aims to classify electrophysiology signals regarding their quality by using machine learning techniques.**<br/>
*Learn more about my background and this exciting project through [this article written by Vivent SA company](https://www.phytlsigns.com/aspiring-data-hero-tells-us-about-his-experience-with-vivent/?utm_content=162147497&utm_medium=social&utm_source=linkedin&hss_channel=lcp-10439639).*<br />
*Please, also find [my live presentation on YouTube (in french)](https://youtu.be/-pawzPjUb9U?t=2649).*

**Problem:**
<ul>
    <li>When first connecting electrodes to plants, sometimes electrodes are not correctly inserted and this leads to poor quality recordings. We manually review all experimental data after 24 and 48 hours to check on signal quality and then recommend to users to reinsert electrodes if necessary.</li>
</ul>

**An ideal solution:**
<ul>
    <li>Automating the task of identifying poor electrode placements and ensure this problem is diagnosed as early as possible.</li>
</ul>

**Raw data:**
<ul>
    <li>Records from 48 plant traces between September 28th, 2020 and March 9th, 2021.</li>
    <li>Signals are recorded at 256 samples per second. The data is then resampled to 1Hz (the value for one second is the mean of the 256 samples).</li>
    <li>The data is stored in 1970 distinct parquet files. Each file corresponds to one day of one plant recording.</li>
    <li>The data is unlabeled, which means good and bad signals have never been classified yet.</li>
</ul>

**Upstream preprocessing of this notebook:**
<ul>
    <li>Labeling signals on a daily basis (1 day => 1 signal => 1 label).</li>
    <li>Extracting features from the signals. Sliding window of 1 hour over the dataset to compute mean, variance and standard deviation for each period.</li>
    <li>Filling NAN values with the constant value 0</li>
    <li>Removing 162 over 1970 uncomplete signals (records which do not cover a whole day)</li>
    <li>Store the resulting dataset into a CSV file.</li>
</ul>

**Resulting data:**
<ul>
    <li>A CSV file of 1808 rows 73 columns (24 hours * 3 features).</li>
</ul>

**Variables:**
<ul>
    <li>hour_mean_voltage: mean of the recorded voltage in the time window (in millivolt mV)</li>
    <li>hour_var_voltage: variance of the recorded voltage in the time window (in millivolt mV)</li>
    <li>hour_std_voltage: standard deviation of the recorded voltage in the time window (in millivolt mV)</li>
</ul>

**Target**:
<ul>
    <li>label (<strong>0</strong>: good signal, <strong>1</strong>: bad signal)</li>
</ul>

**Machine Learning models:**
<ul>
    <li>This notebook explores different model classifiers like KNN, SVM, Random Forest, Gradient Boosting or AdaBoost. Pipelines have been created so that the notebook may be easily replicable with other models or data sources.</li>
</ul>

**Performance metrics:**
<ul>
    <li><strong>Recall:</strong> the main objective is to avoid false negative, which means to classify a bad signal as a good signal (recall = bad signals predicted correctly out of the real number of bad signals).</li>
    <li><strong>F1-Score:</strong> Our classes are a little imbalanced, which may slightly affect our accuracy indicator.</li>
</ul>

**Objectives:**
<ul>
    <li>Recall: 0.85 minimum</li>
    <li>F1-Score: 0.80 minimum</li>
</ul>

*N.B: Many preprocessing techniques have been tried upstream of this notebook, like different time windows, imputation methods or extracted features. The one that is presented in this document showed the best result on this dataset, but may differ if using on other data sources.*
