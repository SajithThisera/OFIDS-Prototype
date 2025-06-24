
def compute_landmark_importance(landmark_features, labels):
    from sklearn.ensemble import RandomForestClassifier
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    rf.fit(landmark_features, labels)
    return rf.feature_importances_
