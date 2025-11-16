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
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def predict_risk(self, user_responses):
        try:
            feature_vector = self._create_feature_vector(user_responses)
            probability = self.model.predict_proba(feature_vector)[0, 1]

            risk_label = "At risk" if probability > 0.5 else "Not at risk"

            return {
                'risk_percentage': round(probability * 100, 2),
                'risk_label': risk_label,
                'probability': probability
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            return None

    def _create_feature_vector(self, responses):
        features = pd.DataFrame(0, index=[0], columns=self.feature_names)

        feature_mapping = self._get_feature_mapping()

        for response_key, value in responses.items():
            if response_key in feature_mapping:
                feature_name = feature_mapping[response_key]
                if feature_name in self.feature_names:
                    features[feature_name] = value

        return features

    def _get_feature_mapping(self):
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
            'sex_male': 'SEX',
            'family_dementia': 'NACCFAM'
        }


def conduct_questionnaire():
    print("\n" + "=" * 60)
    print("DEMENTIA RISK ASSESSMENT QUESTIONNAIRE")
    print("=" * 60)
    print("Please answer the following questions about yourself:\n")

    responses = {}

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
    print("DEMENTIA RISK ASSESSMENT RESULTS")
    print("=" * 60)

    print(f"\nYour estimated risk of having dementia is {prediction['risk_percentage']}%")
    print(f"Classification: {prediction['risk_label']}")

    print(f"\nEXPLANATION:")
    if prediction['risk_label'] == "Not at risk":
        print("Based on your responses, your risk of dementia is below the concerning threshold.")
        print("This suggests that your current lifestyle and health factors are associated")
        print("with lower dementia risk compared to the general population.")
    else:
        print("Based on your responses, your risk of dementia is above the concerning threshold.")
        print("This suggests that some of your current factors may be associated with")
        print("higher dementia risk compared to the general population.")

    print(f"\nRECOMMENDATIONS:")
    if prediction['risk_label'] == "Not at risk":
        print("* Continue maintaining healthy lifestyle habits")
        print("* Stay socially active and mentally engaged")
        print("* Regular physical activity and balanced nutrition")
        print("* Annual health check-ups to monitor your wellbeing")
    else:
        print("* Consult with a healthcare provider for proper assessment")
        print("* Consider cognitive screening during your next medical visit")
        print("* Focus on improving cardiovascular health and social connections")
        print("* Maintain regular physical activity and mental stimulation")
        print("* Manage any lifestyle factors that may contribute to risk")

    print("\n" + "=" * 60)
    print("Important: This is a screening tool for educational purposes.")
    print("It is not a medical diagnosis. Always consult healthcare")
    print("professionals for medical advice and proper assessment.")
    print("=" * 60)


def main():
    print("Welcome to MindScope Dementia Risk Assessment")
    print("A machine learning based screening tool\n")

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

                if model_files:
                    MODEL_PATH = str(model_files[0])
                    print(f"\nUsing: {MODEL_PATH}")
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