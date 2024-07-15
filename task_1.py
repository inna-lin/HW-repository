from pathlib import Path
def total_salary(path_input):
    path = Path(path_input)

    if path.exists():
        fh = open(path, 'r')

        lines = []
        for i in fh.readlines():
            lines.append(i.strip())
        fh.close()

        sum = 0

        for i in lines:
            _, value = i.split(",")
            sum = sum + int(value)

        average = int(sum / len(lines))

        print (f"Загальна сума заробітної плати: {sum}, Середня заробітна плата: {average}")

    else:
        print(f"{path} не існує")

path = total_salary("salary.txt")