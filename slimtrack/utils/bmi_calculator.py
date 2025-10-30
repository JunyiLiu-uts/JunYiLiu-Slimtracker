from config.constants import BMI_CATEGORIES

class BMICalculator:
    @staticmethod
    def get_bmi_category(bmi: float) -> str:
        for category, (min_val, max_val) in BMI_CATEGORIES.items():
            if min_val <= bmi < max_val:
                return category
        return 'unknown'
    
    @staticmethod
    def get_suggestions(bmi: float, weight_trend: float = 0) -> str:
        category = BMICalculator.get_bmi_category(bmi)
        
        suggestions = {
            'underweight': [
                "Increase calorie intake with nutritious foods",
                "Strength training to build muscle mass",
                "Consult a healthcare provider"
            ],
            'normal': [
                "Continue balanced diet and exercise",
                "Regular health check-ups",
                "Stay hydrated and manage stress"
            ],
            'overweight': [
                "Moderate calorie reduction",
                "Regular cardiovascular exercise",
                "Focus on whole foods and portion control"
            ],
            'obese': [
                "Consult healthcare professional",
                "Structured weight loss program",
                "Combination of diet and exercise"
            ]
        }
        
        base_suggestions = suggestions.get(category, [])
        
        # Add trend-based suggestions
        trend_suggestions = []
        if weight_trend < -1:
            trend_suggestions.append(f"Great progress! You've lost {abs(weight_trend):.1f} kg")
        elif weight_trend > 1:
            trend_suggestions.append(f"Note: You've gained {weight_trend:.1f} kg. Review your habits.")
        else:
            trend_suggestions.append("Your weight is stable. Consider setting new goals.")
        
        return base_suggestions + trend_suggestions