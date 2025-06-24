import matplotlib
matplotlib.use("Agg")  # Use non-GUI backend for macOS/server compatibility
import matplotlib.pyplot as plt

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import os

def train_and_evaluate(features, labels, feature_names=None, output_dir="outputs"):
    from sklearn.model_selection import train_test_split

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )

    ensemble = VotingClassifier(estimators=[
        ('rf', RandomForestClassifier(n_estimators=10, random_state=42)),
        ('gb', GradientBoostingClassifier(n_estimators=10, random_state=42)),
    ], voting="soft")
    ensemble.fit(X_train, y_train)
    preds = ensemble.predict(X_test)
    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, ensemble.predict_proba(X_test)[:, 1]) if len(set(y_test)) > 1 else 0
    report = classification_report(y_test, preds, output_dict=True)

    # --- XAI: Feature Importance ---
    rf_imp = ensemble.named_estimators_['rf'].feature_importances_
    gb_imp = ensemble.named_estimators_['gb'].feature_importances_
    avg_imp = (rf_imp + gb_imp) / 2

    if feature_names is None:
        feature_names = [f'Feature {i+1}' for i in range(len(avg_imp))]

    plt.figure(figsize=(6, 4))
    plt.bar(feature_names, avg_imp)
    plt.title("Feature Importance (Ensemble)")
    plt.tight_layout()
    feat_path = os.path.join(output_dir, "feature_importance.png")
    plt.savefig(feat_path)
    plt.close()

    # --- Confusion Matrix ---
    cm = confusion_matrix(y_test, preds)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Healthy", "Impaired"])
    disp.plot(cmap="Blues")
    plt.title("Confusion Matrix")
    plt.tight_layout()
    cm_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()

    return {"accuracy": acc, "auc": auc, "report": report}
