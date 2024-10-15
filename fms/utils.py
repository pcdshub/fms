from typing import List

class TypeEnforcer:
    def get_bool(prompt: str) -> bool:
        while True:
            try:
                value = bool(input(prompt))
                if value == "":
                    value = False 
                return value
            except ValueError:
                print("invalid, input bool")

    def get_int(prompt: str) -> int:
        while True:
            try:
                value = int(input(prompt))
                return value
            except ValueError:
                print("invalid, input int")

    def get_str(prompt: str) -> str:
        while True:
            try:
                value = str(input(prompt))
                return value
            except ValueError:
                print("invalid, input string")
    def get_list_str(values: List[str], prompt: str) -> str:
        while True:
            try:
                value = str(input(prompt))
                if value not in values:
                    raise(ValueError())
                return value
            except ValueError:
                print("invalid, Beckhoff or Raritan")
