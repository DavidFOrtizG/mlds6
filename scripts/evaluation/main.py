import keras
import sys
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
sys.path.append("../../")
from src.mlds6.preprocessing.data_generator import DataGenerator
import seaborn as sns
import matplotlib.pyplot as plt

model = keras.models.load_model("../deployment_fastapi/model/asl_model.keras")
model.summary()
test_gen = DataGenerator("../../data/hdf5/test.hdf5", batch_size=1024, shuffle=False)


print("Predicciones..")

predictions = model.predict(test_gen)
predicted_classes = np.argmax(predictions, axis=1)

print("Extracción de clases...")

true_classes = []
for i in range(len(test_gen)):
    _, y_batch = test_gen[i]
    true_classes.extend(np.argmax(y_batch, axis=1))

true_classes = np.array(true_classes)

class_labels = list(test_gen.distinct_labels)

print("\nReporte de Clasificación:")
print(classification_report(true_classes, predicted_classes, target_names=class_labels))

# Compute the confusion matrix
cm = confusion_matrix(true_classes, predicted_classes)

# Plot the confusion matrix
plt.figure(figsize=(20, 15))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=class_labels, yticklabels=class_labels)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.savefig("results/matrix_final.png", bbox_inches='tight')
plt.show()