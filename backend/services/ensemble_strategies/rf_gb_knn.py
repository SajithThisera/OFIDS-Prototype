from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier

def get_ensemble():
    rf = RandomForestClassifier(n_estimators=50, random_state=42)
    gb = GradientBoostingClassifier(n_estimators=50, random_state=42)
    knn = KNeighborsClassifier(n_neighbors=3)
    return VotingClassifier(estimators=[('rf', rf), ('gb', gb), ('knn', knn)], voting='soft')
