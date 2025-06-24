from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression

def get_ensemble():
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=50, random_state=42)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    return VotingClassifier(estimators=[('rf', rf), ('gb', gb), ('lr', lr)], voting='soft')
