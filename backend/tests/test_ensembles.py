import sys
import os
import numpy as np

# --- Set up import paths  ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENSEMBLE_DIR = os.path.join(BASE_DIR, "backend", "ensemble_strategies")
SERVICES_DIR = os.path.join(BASE_DIR, "backend", "services")
sys.path.append(ENSEMBLE_DIR)
sys.path.append(SERVICES_DIR)

from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, LeaveOneOut

# --- Import all ensemble get_ensemble functions ---
from backend.services.ensemble_strategies.rf_gb import get_ensemble as get_rf_gb
from backend.services.ensemble_strategies.rf_gb_lr import get_ensemble as get_rf_gb_lr
from backend.services.ensemble_strategies.rf_gb_svc import get_ensemble as get_rf_gb_svc
from backend.services.ensemble_strategies.rf_gb_knn import get_ensemble as get_rf_gb_knn
from backend.services.ensemble_strategies.rf_gb_lr_svc import get_ensemble as get_rf_gb_lr_svc

from backend.services.feature_extraction_service import extract_features_from_uploads  # Update this if needed

def run_and_report(ensemble_func, features, labels, name):
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    ensemble = ensemble_func()
    ensemble.fit(X_train, y_train)
    preds = ensemble.predict(X_test)
    acc = accuracy_score(y_test, preds)
    try:
        auc = roc_auc_score(y_test, ensemble.predict_proba(X_test)[:, 1]) if len(set(y_test)) > 1 else None
    except Exception:
        auc = None
    report = classification_report(y_test, preds)
    cm = confusion_matrix(y_test, preds)
    print("="*50)
    print(f"Ensemble: {name}")
    print(f"Accuracy: {acc:.4f}")
    print(f"AUC: {auc}")
    print(f"Classification Report:\n{report}")
    print(f"Confusion Matrix (rows=true, cols=pred):\n{cm}")
    print("Rows: 0=Healthy, 1=Impaired   Cols: 0=Healthy, 1=Impaired")
    print("="*50)

def run_loocv(ensemble_func, features, labels, name):
    loo = LeaveOneOut()
    preds, trues, aucs = [], [], []
    for train_idx, test_idx in loo.split(features):
        X_train, X_test = features[train_idx], features[test_idx]
        y_train, y_test = labels[train_idx], labels[test_idx]
        # check if all classes present in y_train
        if len(set(y_train)) < 2:
            continue
        clf = ensemble_func()
        clf.fit(X_train, y_train)
        pred = clf.predict(X_test)[0]
        preds.append(pred)
        trues.append(y_test[0])
        try:
            proba = clf.predict_proba(X_test)[:, 1][0]
            auc = roc_auc_score([y_test[0]], [proba]) if len(set([y_test[0], pred])) > 1 else np.nan
            aucs.append(auc)
        except Exception:
            aucs.append(np.nan)
    acc = accuracy_score(trues, preds)
    try:
        auc = roc_auc_score(trues, preds) if len(set(trues)) > 1 else None
    except Exception:
        auc = None
    report = classification_report(trues, preds)
    cm = confusion_matrix(trues, preds)
    print("="*60)
    print(f"LOOCV Ensemble: {name}")
    print(f"LOOCV Accuracy: {acc:.4f}")
    print(f"LOOCV AUC: {auc}")
    print(f"LOOCV Classification Report:\n{report}")
    print(f"Confusion Matrix (rows=true, cols=pred):\n{cm}")
    print("Rows: 0=Healthy, 1=Impaired   Cols: 0=Healthy, 1=Impaired")
    print("="*60)

def run_bootstrap(ensemble_func, features, labels, name, n_iter=100):
    rng = np.random.RandomState(42)
    accs, aucs = [], []
    for i in range(n_iter):
        idx = rng.choice(len(features), size=len(features), replace=True)
        X_train, X_test = features[idx], features
        y_train, y_test = labels[idx], labels
        if len(set(y_train)) < 2:
            continue  # skip samples with only one class
        clf = ensemble_func()
        clf.fit(X_train, y_train)
        preds = clf.predict(X_test)
        accs.append(accuracy_score(y_test, preds))
        try:
            auc = roc_auc_score(y_test, preds) if len(set(y_test)) > 1 and len(set(preds)) > 1 else np.nan
            aucs.append(auc)
        except Exception:
            aucs.append(np.nan)
    print("="*60)
    print(f"BOOTSTRAP ({n_iter} resamples) Ensemble: {name}")
    if len(accs) == 0:
        print("Not enough samples for bootstrapping (all resamples had one class only).")
        return
    print(f"Bootstrap Accuracy: {np.mean(accs):.4f} ± {np.std(accs):.4f}")
    print(f"Bootstrap AUC: {np.nanmean(aucs):.4f} ± {np.nanstd(aucs):.4f}")
    print("="*60)

if __name__ == "__main__":
    # Load the features and labels from the uploads directory
    features, labels = extract_features_from_uploads(os.path.join(BASE_DIR, "uploads"))

    # Run standard hold-out test
    run_and_report(get_rf_gb, features, labels, "RandomForest + GradientBoosting")
    run_and_report(get_rf_gb_lr, features, labels, "RandomForest + GradientBoosting + LogisticRegression")
    run_and_report(get_rf_gb_svc, features, labels, "RandomForest + GradientBoosting + SVM")
    run_and_report(get_rf_gb_knn, features, labels, "RandomForest + GradientBoosting + KNeighbors")
    run_and_report(get_rf_gb_lr_svc, features, labels, "RF + GB + LogisticRegression + SVM")

    # Run LOOCV for all
    for func, name in [
        (get_rf_gb, "RandomForest + GradientBoosting"),
        (get_rf_gb_lr, "RandomForest + GradientBoosting + LogisticRegression"),
        (get_rf_gb_svc, "RandomForest + GradientBoosting + SVM"),
        (get_rf_gb_knn, "RandomForest + GradientBoosting + KNeighbors"),
        (get_rf_gb_lr_svc, "RF + GB + LogisticRegression + SVM"),
    ]:
        run_loocv(func, features, labels, name)

    # Run bootstrap for all
    for func, name in [
        (get_rf_gb, "RandomForest + GradientBoosting"),
        (get_rf_gb_lr, "RandomForest + GradientBoosting + LogisticRegression"),
        (get_rf_gb_svc, "RandomForest + GradientBoosting + SVM"),
        (get_rf_gb_knn, "RandomForest + GradientBoosting + KNeighbors"),
        (get_rf_gb_lr_svc, "RF + GB + LogisticRegression + SVM"),
    ]:
        run_bootstrap(func, features, labels, name, n_iter=100)
