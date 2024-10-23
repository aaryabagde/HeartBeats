# HeartBeats: Emotion Based Music Recommendation using ECG Sensor
## Introduction
In recent years, emotional management has become increasingly difficult worldwide, driven by factors such as indebtedness, inflation, and job loss. Chronic stress is a growing global issue, linked to serious health risks like heart disease, depression, and anxiety. While stress reduction methods like exercise and entertainment help, listening to music has been found particularly effective, provided it matches the listener's mood. To enhance emotion recognition, ECG data was used to identify emotional components—arousal and valence. Using the DREAMER dataset, which combines EEG and ECG data, a machine learning model was trained for real-time emotion recognition. The model’s output was then used to recommend music via the Spotify API, creating an end-to-end system with real-time ECG data collection and song suggestions through a web application built using Flask.

## Literature Survey
Several studies have explored music recommendation based on emotion. In "EMUSE - An Emotion Based Music Recommendation System," A. Phaneendra et al. used computer vision and deep learning to detect facial expressions and recommend music based on seven emotions. Another study by M. Uma and S. Metilda Florence utilized facial landmarks to identify mood and suggest music but faced limitations due to lighting conditions and image resolution. Deger AYATA et al. explored emotion recognition via Galvanic Skin Response (GSR) using machine learning algorithms, achieving higher accuracy in detecting arousal and valence through feature extraction techniques like empirical mode decomposition (EMD). These findings suggest that using physiological signals such as EEG, heart rate, and GSR yields better accuracy than facial recognition, and integrating this with machine learning can enhance emotion-based music recommendation systems.

## Dataset
For training our model we made use of the DREAMER Dataset. EEG and ECG signals captured during the emotion stimulation
process using audio-visual cues are stored in the multi-modal database. Following each stimulus, subjects self-assessed their emotional
states in terms of valence and arousal, and the signals from people were logged along with that information. All the
signals were recorded using lightweight, inexpensive, cordless, and off-the-shelf hardware making it compatible with our hardware
system. The classification outcomes for the suggested database's valence, arousal, and dominance are similar to those obtained for
other databases using non-portable, pricey, medical-grade instruments.

## Data PreProcessing and EDA
The DREAMER dataset consisted of raw ECG signal data in .mat format.
This data hat to be first preprocessed and converted to a pandas data frame.For feature extraction we made use of NeuroKit2, a user-friendly package providing easy access to advanced bio signal processing
routines. This package aids is analyzing physiological sensor data without extensive knowledge of biomedical signal processing. We
extracted features from the time domain, frequency domain and non-linear domain. These were Time domain: RMSSD, MeanNN,
SDNN, SDSD, CVNN. Frequency domain: Spectral power density in various frequency bands (Ultra low/ULF, Very low/VLF,
Low/LF, High/HF, Very high/VHF), Ratio of LF to HF power, Normalized LF (LFn) and HF (HFn), Log transformed HF (LnHF).
Nonlinear domain: Spread of RR intervals (SD1, SD2, ratio between SD2 to SD1), Cardiac Sympathetic Index (CSI), Cardial Vagal
Index (CVI), Modified CSI, Sample Entropy (SampEn).

## Modelling
Since this is a multilabel classification problem we approached it using the Binary Relevance Te chnique.
The model was trained to first obtain the target value of Valence (0: Low, 1: High). The same features were than used for det ermining
the target value of Arousal (0: Low, 1: High). The results were than aggregated to result in four possible combinations corresponding
to four emotional states as show in figure 4. After careful consideration of various supervised classification techniques, we observed
the highest accuracy by using the decision tree algorithm. The decision split is calculated using Gini Impurity. This represents the
probability that a random data point would be erroneously classified if it were labelled using the given dataset's class distribution.

## Model Deployment
The output of the emotion recognition model is then used while making a call to the Spotify API and music is recommended as per
the user’s current mood. If the user is experiencing negative emotions, then they are recommended mellow and calm music while they
recommended upbeat, lively music in case of a positive state of mind. We have prepared a fully integrated end-to-end system composed
of hardware as well as software.

## Results
Since the classes were balanced, we decided to go with Accuracy as our success metric. We got an accuracy of 0.87 using Decision Trees Model


