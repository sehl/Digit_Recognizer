# Digit_Recognizer
My code for identifying digit classes from the Kaggle/MNIST dataset

16 March 2016 --
  digit_recognizer.py:
    1. Sorts training data by category
    2. Detects 100 data clusters within each category
    3. Calculates the distance to all 1,000 means for each datum.
    3. Uses distances as input to a Logistic Regression Classifier to predict each image's digit classification.

  digits_out.csv: Resulting submission from above (modified)
