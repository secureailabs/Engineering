import shap

explainer = shap.TreeExplainer(__model)
explanation = explainer(__data)

__explanation_values = explanation.values
__explanation_base_values = explanation.base_values
__expected_value = explainer.expected_value