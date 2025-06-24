def generate_xai(model, features):
    # Use average feature importances from the ensemble as a proxy for XAI
    try:
        rf = model.named_estimators_['rf']
        gb = model.named_estimators_['gb']
        rf_imp = rf.feature_importances_
        gb_imp = gb.feature_importances_
        avg_imp = (rf_imp + gb_imp) / 2
        # Return as a list for JSON
        return {"average_importance": avg_imp.tolist()}
    except Exception as e:
        return {"error": str(e)}
