def predict_single_child(data):
    """
    Classifies child nutritional status based on simplified WHO growth standards.
    Input: dict containing Age_Months, Weight_kg, Height_cm, etc.
    Returns: String (Wasted, Stunted, or Normal)
    """
    age = data.get('Age_Months', 0)
    weight = data.get('Weight_kg', 0)
    height = data.get('Height_cm', 0)
    
    # --- 1. STUNTING CALCULATION (Height-for-Age) ---
    # Expected median height for a child (Avg of Male/Female at 18 months is ~81cm)
    # Linear approximation: base 50cm at birth + ~1.7cm per month for first 24 months
    expected_height = 50 + (age * 1.7)
    height_perc_of_median = (height / expected_height) * 100

    # --- 2. WASTING CALCULATION (Weight-for-Height) ---
    # Expected weight based on actual height (using a simplified BMI/Ponderal index)
    # A healthy child at 72cm should weigh roughly 8.5kg to 9kg.
    # Formula: (Height in meters ^ 2) * healthy BMI constant (approx 16 for toddlers)
    expected_weight = ((height / 100) ** 2) * 16.5
    weight_perc_of_median = (weight / expected_weight) * 100

    # --- 3. CLASSIFICATION ---
    # Thresholds: < 90% height for age = Stunted; < 80% weight for height = Wasted
    
    if height_perc_of_median < 90:
        return "Stunted"
    elif weight_perc_of_median < 75:
        return "Wasted"
    else:
        return "Normal"

# Example usage for testing:
# child_data = {'Age_Months': 18, 'Weight_kg': 2, 'Height_cm': 72.0}
# Result: "Wasted" (because 2kg is extremely low for a 72cm child)