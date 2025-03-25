from typing import List

max_retry = 3


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
        curr_retries = 0
        while True:
            value = input(prompt)
            if curr_retries >= max_retry:
                raise ValueError("Input a string")
            elif value == "":
                return None
            if type(value) is str:
                return value
            else:
                print("invalid, input string")
                curr_retries += 1

    def get_list_str(values: List[str], prompt: str) -> str:
        curr_retries = 0
        while True:
            value = input(prompt)

            if curr_retries >= max_retry:
                raise ValueError("Input Beckoff or Raritan")
            elif type(value) is not str:
                curr_retries += 1
                print("invalid, Beckhoff or Raritan")
                continue
            elif value in values:
                return value
            else:
                curr_retries += 1
