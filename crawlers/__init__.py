import json
from youmed.symptoms_list import crawl_symptoms_list
from youmed.symptom_detail import crawl_symptom_detail

if __name__ == "__main__":
    symptoms_list = crawl_symptoms_list()
    print(symptoms_list)