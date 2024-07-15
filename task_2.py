from pathlib import Path
def get_cats_info(path_input):
    path = Path(path_input)

    if path.exists():
        with open("salary.txt", "r") as fh:
            lines = [i.strip() for i in fh.readlines()]

        cats_list = []
        for i in lines:
            values = i.split(",")
            keys = ["id", "name", "age"]
            cat_dict = dict(zip(keys, values))
            cats_list.append(cat_dict)
        print(cats_list)

    else:
        print(f"{path} не існує")

cats_info = get_cats_info("cats.txt")
