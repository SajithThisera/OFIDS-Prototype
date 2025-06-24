from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC

def get_ensemble():
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=50, random_state=42)
    svc = SVC(probability=True, random_state=42)
    return VotingClassifier(estimators=[('rf', rf), ('gb', gb), ('svc', svc)], voting='soft')
