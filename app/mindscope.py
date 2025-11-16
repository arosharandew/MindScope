import os
import sys
import joblib
import pandas as pd
import numpy as np
from pathlib import Path


class DementiaRiskPredictor:
    def __init__(self, model_path):
        try:
            self.package = joblib.load(model_path)
            self.model = self.package['model']
            self.feature_names = self.package['feature_names']
            print("Model loaded successfully!")
            print(f"Model: {self.package.get('model_name', 'LightGBM')}")
            print(f"Expected features: {len(self.feature_names)}")
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def predict_risk(self, user_responses):
        try:
            feature_vector = self._create_feature_vector(user_responses)

            # Debug: Check feature dimensions
            print(f"Created features: {feature_vector.shape[1]}")
            print(f"Model expects: {len(self.feature_names)}")

            probability = self.model.predict_proba(feature_vector)[0, 1]
            risk_level = self._classify_risk(probability)

            return {
                'risk_percentage': round(probability * 100, 2),
                'risk_level': risk_level,
                'probability': probability,
                'key_factors': self._get_key_factors(user_responses)
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def _create_feature_vector(self, responses):
        # Start with zeros ONLY for the features the model expects
        features = pd.DataFrame(0, index=[0], columns=self.feature_names)

        # Map responses to available features
        feature_mapping = self._get_feature_mapping()

        for response_key, value in responses.items():
            if response_key in feature_mapping:
                feature_name = feature_mapping[response_key]
                if feature_name in self.feature_names:
                    features[feature_name] = value

        return features

    def _get_feature_mapping(self):
        # Map questionnaire responses to actual feature names in the model
        return {
            'age': 'NACCAGE',
            'education': 'EDUC',
            'bills_difficulty': 'BILLS',
            'shopping_difficulty': 'SHOPPING',
            'meal_prep_difficulty': 'MEALPREP',
            'independence': 'INDEPEND',
            'social_visits': 'INVISITS',
            'phone_calls': 'INCALLS',
            'tobacco_use': 'TOBAC30',
            'alcohol_frequency': 'ALCFREQ',
            'sex_male': 'SEX',  # Will be set to 1 for male, 2 for female
            'family_dementia': 'NACCFAM'
        }

    def _classify_risk(self, probability):
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.7:
            return "Medium Risk"
        else:
            return "High Risk"

    def _get_key_factors(self, responses):
        factors = []

        age = responses.get('age', 0)
        if age > 75:
            factors.append("Age-related risk")
        elif age > 65:
            factors.append("Advanced age")

        if responses.get('bills_difficulty', 0) > 2:
            factors.append("Difficulty managing finances")
        if responses.get('shopping_difficulty', 0) > 2:
            factors.append("Difficulty with shopping")
        if responses.get('meal_prep_difficulty', 0) > 2:
            factors.append("Difficulty preparing meals")

        if responses.get('social_visits', 0) >= 4:
            factors.append("Limited social engagement")

        if responses.get('tobacco_use', 0) == 3:  # Current smoker
            factors.append("Current tobacco use")

        return factors[:3]


def conduct_questionnaire():
    print("\n" + "=" * 60)
    print("DEMENTIA RISK ASSESSMENT QUESTIONNAIRE")
    print("=" * 60)
    print("Please answer the following questions about yourself:\n")

    responses = {}

    # 1. Age
    while True:
        try:
            age = int(input("1. What is your age? "))
            if 18 <= age <= 120:
                responses['age'] = age
                break
            else:
                print("Please enter a valid age (18-120)")
        except ValueError:
            print("Please enter a number")

    # 2. Sex (store as numeric)
    print("\n2. What is your biological sex?")
    print("   1. Male")
    print("   2. Female")
    while True:
        sex_choice = input("   Enter choice (1-2): ").strip()
        if sex_choice == '1':
            responses['sex_male'] = 1
            break
        elif sex_choice == '2':
            responses['sex_male'] = 2
            break
        else:
            print("Please enter 1 or 2")

    # 3. Education
    print("\n3. What is the highest number of years of education completed?")
    print("   (e.g., 12 = high school, 16 = college, 18 = masters, etc.)")
    while True:
        try:
            educ = int(input("   Years of education: "))
            if 0 <= educ <= 25:
                responses['education'] = educ
                break
            else:
                print("Please enter between 0-25 years")
        except ValueError:
            print("Please enter a number")

    # 4-6. Daily activities
    activity_questions = {
        'bills_difficulty': "managing finances and paying bills",
        'shopping_difficulty': "shopping for groceries or personal items",
        'meal_prep_difficulty': "preparing meals"
    }

    print("\n4-6. For each activity, rate your level of difficulty (1-4):")
    print("   1 - No difficulty")
    print("   2 - Some difficulty")
    print("   3 - Much difficulty")
    print("   4 - Unable to do")

    for key, activity in activity_questions.items():
        while True:
            try:
                difficulty = int(input(f"   Difficulty {activity} (1-4): "))
                if 1 <= difficulty <= 4:
                    responses[key] = difficulty
                    break
                else:
                    print("Please enter 1-4")
            except ValueError:
                print("Please enter a number 1-4")

    # 7. Independence level
    print("\n7. Overall, how independent are you in daily activities?")
    print("   1 - Completely independent")
    print("   2 - Mostly independent")
    print("   3 - Somewhat dependent")
    print("   4 - Very dependent")
    while True:
        try:
            independence = int(input("   Enter choice (1-4): "))
            if 1 <= independence <= 4:
                responses['independence'] = independence
                break
            else:
                print("Please enter 1-4")
        except ValueError:
            print("Please enter a number 1-4")

    # 8-9. Social engagement
    print("\n8-9. How often do you (1-5):")
    print("   1 - Daily")
    print("   2 - Several times weekly")
    print("   3 - Weekly")
    print("   4 - Monthly")
    print("   5 - Rarely/Never")

    while True:
        try:
            visits = int(input("   Have visitors or social interactions? (1-5): "))
            if 1 <= visits <= 5:
                responses['social_visits'] = visits
                break
            else:
                print("Please enter 1-5")
        except ValueError:
            print("Please enter a number 1-5")

    while True:
        try:
            calls = int(input("   Make or receive phone calls? (1-5): "))
            if 1 <= calls <= 5:
                responses['phone_calls'] = calls
                break
            else:
                print("Please enter 1-5")
        except ValueError:
            print("Please enter a number 1-5")

    # 10. Tobacco use
    print("\n10. Do you currently smoke or have you smoked regularly in the past?")
    print("    1. Never smoked")
    print("    2. Former smoker")
    print("    3. Current smoker")
    while True:
        smoke_choice = input("    Enter choice (1-3): ").strip()
        if smoke_choice in ['1', '2', '3']:
            responses['tobacco_use'] = int(smoke_choice)
            break
        else:
            print("Please enter 1, 2, or 3")

    # 11. Alcohol frequency
    print("\n11. How often do you drink alcohol?")
    print("    1. Never")
    print("    2. Occasionally (monthly)")
    print("    3. Regularly (weekly)")
    print("    4. Daily")
    while True:
        alcohol_choice = input("    Enter choice (1-4): ").strip()
        if alcohol_choice in ['1', '2', '3', '4']:
            responses['alcohol_frequency'] = int(alcohol_choice)
            break
        else:
            print("Please enter 1, 2, 3, or 4")

    # 12. Family history (store as numeric: 1 for Yes, 0 for No)
    print("\n12. Has anyone in your immediate family (parents, siblings) been diagnosed with dementia?")
    while True:
        family = input("   (Y)es or (N)o: ").strip().lower()
        if family in ['y', 'yes']:
            responses['family_dementia'] = 1
            break
        elif family in ['n', 'no']:
            responses['family_dementia'] = 0
            break
        else:
            print("   Please enter Y or N")

    print("\n" + "=" * 60)
    print("Questionnaire completed! Processing your responses...")
    print("=" * 60)

    return responses


def display_results(prediction):
    print("\n" + "=" * 60)
    print("YOUR DEMENTIA RISK ASSESSMENT RESULTS")
    print("=" * 60)

    print(f"\nESTIMATED RISK: {prediction['risk_percentage']}%")
    print(f"   (Based on people with similar profiles)")

    print(f"\nCLASSIFICATION: {prediction['risk_level']}")

    if prediction['key_factors']:
        print(f"\nKEY FACTORS INFLUENCING YOUR RISK:")
        for factor in prediction['key_factors']:
            print(f"   * {factor}")

    print(f"\nRECOMMENDATIONS:")
    if prediction['risk_level'] == "Low Risk":
        print("   * Continue maintaining healthy lifestyle habits")
        print("   * Stay socially active and engaged")
        print("   * Regular physical activity is beneficial")
        print("   * Annual health check-ups are recommended")

    elif prediction['risk_level'] == "Medium Risk":
        print("   * Consider discussing cognitive health with your doctor")
        print("   * Increase social and mental activities")
        print("   * Manage lifestyle factors carefully")
        print("   * Regular exercise and balanced diet are important")

    else:
        print("   * Consult with a healthcare provider for proper assessment")
        print("   * Consider comprehensive cognitive screening")
        print("   * Focus on improving social connections")
        print("   * Maintain mental stimulation and physical activity")
        print("   * Regular medical follow-ups are strongly recommended")

    print("\n" + "=" * 60)
    print("Remember: This is a screening tool, not a medical diagnosis.")
    print("   Always consult healthcare professionals for medical advice.")
    print("=" * 60)


def main():
    print("Welcome to MindScope Dementia Risk Assessment")
    print("   Using machine learning for early risk detection\n")

    MODEL_PATH = r"../results/models/final_deployment_model.pkl"

    if not os.path.exists(MODEL_PATH):
        print(f"Model file not found at: {MODEL_PATH}")
        print("Looking for available model files...")

        models_dir = Path("../results/models")
        if models_dir.exists():
            model_files = list(models_dir.glob("*.pkl"))
            if model_files:
                print("Found these model files:")
                for i, model_file in enumerate(model_files, 1):
                    print(f"   {i}. {model_file.name}")

                # Try to use the first available model
                if model_files:
                    MODEL_PATH = str(model_files[0])
                    print(f"\nTrying to use: {MODEL_PATH}")
            else:
                print("No .pkl model files found in models directory")
                return
        else:
            print("Models directory not found")
            return

    try:
        predictor = DementiaRiskPredictor(MODEL_PATH)
        responses = conduct_questionnaire()
        prediction = predictor.predict_risk(responses)

        if prediction:
            display_results(prediction)
        else:
            print("Sorry, we encountered an error processing your assessment.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please make sure your model file is accessible and valid.")


if __name__ == "__main__":
    main()