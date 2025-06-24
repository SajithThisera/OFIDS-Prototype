from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier

def get_ensemble():
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=50, random_state=42)
    return VotingClassifier(estimators=[('rf', rf), ('gb', gb)], voting='soft')
