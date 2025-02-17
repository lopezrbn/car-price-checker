import reflex as rx
import pandas as pd
from typing import Dict, List
from datetime import date
from .pipeline import make_prediction

from .data.cars_manuf_and_models import cars


class State(rx.State):

    # Base vars
    current_year: int = date.today().year
    manufacturers_list: List[str] = list(cars.keys())
    models_list: List[str] = []
    years_list: List[str] = list(range(current_year, 2009, -1))
    fuels_list: List[str] = ["Diesel", "Gasolina", "Eléctrico"]
    transmissions_list: List[str] = ["Manual", "Automática"]
    cars: Dict[str, List] = cars
    selected_manufacturer: str = ""
    selected_model: str = ""
    selected_year: str = ""
    selected_fuel: str = ""
    selected_transmission: str = ""
    selected_power: int = 0
    selected_kms: int = 0
    selected_doors: int = 0
    predicted_value: int = 0

    def reset_selected_vars(self):
        self.selected_manufacturer = ""
        self.selected_model = ""
        self.selected_year = ""
        self.selected_fuel = ""
        self.selected_transmission = ""
        self.selected_power = 0
        self.selected_kms = 0
        self.selected_doors = 0
        self.predicted_value = 0

    # Event handlers
    def set_selected_manufacturer(self, value):
        self.selected_manufacturer = value
        self.models_list = self.cars[value]
        self.selected_model = ""

    
    def search_handler(self):
        car_to_predict: Dict = {
            "year": int(self.selected_year) if self.selected_year != "" else 0,
            "month": 6,
            "km": int(self.selected_kms) if self.selected_kms != "" else 0,
            "power_hp": int(self.selected_power) if self.selected_power != "" else 0,
            "no_doors": 5,
            "age": self.current_year - (int(self.selected_year) if self.selected_year != "" else 0) - 1,
            "fuel": self.selected_fuel,
            "transmission": self.selected_transmission.lower(),
        }
        X_pred = pd.DataFrame([car_to_predict, ], index=[0])
        print(X_pred)
        self.predicted_value = make_prediction(self.selected_manufacturer, self.selected_model, X_pred)
        if self.predicted_value < 0:
            self.predicted_value = "Not enough data to predict the value of this car"
        else:
            self.predicted_value = int(self.predicted_value)
        print(f"Predicted value: {self.predicted_value}")
        return rx.redirect("/results")
    

    def back_handler(self):
        self.reset_selected_vars()
        return rx.redirect("/")


    # Computed vars
    @rx.var
    def predicted_value_formatted(self):
        if isinstance(self.predicted_value, int):
            predicted_value_formatted = ""
            for i, digit in enumerate(str(self.predicted_value)[::-1]):
                if i % 3 != 0:
                    predicted_value_formatted += digit
                else:
                    predicted_value_formatted += "." + digit
            predicted_value_formatted = predicted_value_formatted[-1:0:-1]
            predicted_value_formatted += " €"
            return predicted_value_formatted
        else:
            return self.predicted_value