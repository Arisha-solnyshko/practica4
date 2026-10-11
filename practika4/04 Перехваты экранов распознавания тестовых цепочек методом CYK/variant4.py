from collections import defaultdict


# Практическая работа № 4, вариант 4.
# Независимая проверка НФХ-грамматики алгоритмом CYK.
PRODUCTIONS = {
    "S": ["VM"],
    "E": ["EN", "EO", "TP", "TQ", "BU", "HR", "IZ", "a", "b", "c", "d"],
    "T": ["TP", "TQ", "BU", "HR", "IZ", "a", "b", "c", "d"],
    "U": ["BU", "HR", "IZ", "a", "b", "c", "d"],
    "I": ["DI", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "V": ["a", "b", "c", "d"],
    "D": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "A": ["+"],
    "B": ["-"],
    "C": ["*"],
    "F": ["/"],
    "G": ["="],
    "H": ["("],
    "J": [")"],
    "K": ["."],
    "M": ["GE"],
    "N": ["AT"],
    "O": ["BT"],
    "P": ["CU"],
    "Q": ["FU"],
    "R": ["EJ"],
    "Z": ["KI"],
}


def build_indexes():
    terminal_to_vars = defaultdict(set)
    pair_to_vars = defaultdict(set)
    for lhs, right_sides in PRODUCTIONS.items():
        for rhs in right_sides:
            if len(rhs) == 1:
                terminal_to_vars[rhs].add(lhs)
            elif len(rhs) == 2 and rhs[0].isupper() and rhs[1].isupper():
                pair_to_vars[(rhs[0], rhs[1])].add(lhs)
            else:
                raise ValueError(f"Правило {lhs} -> {rhs} не находится в НФХ")
    return terminal_to_vars, pair_to_vars


def cyk(word: str):
    if not word:
        return False, []

    terminal_to_vars, pair_to_vars = build_indexes()
    length = len(word)
    table = [[set() for _ in range(length)] for _ in range(length)]

    for position, symbol in enumerate(word):
        table[position][0].update(terminal_to_vars.get(symbol, set()))

    for substring_length in range(2, length + 1):
        for start in range(length - substring_length + 1):
            for split in range(1, substring_length):
                left = table[start][split - 1]
                right = table[start + split][substring_length - split - 1]
                for left_var in left:
                    for right_var in right:
                        table[start][substring_length - 1].update(
                            pair_to_vars.get((left_var, right_var), set())
                        )

    return "S" in table[0][length - 1], table


def show_table(word: str, table):
    for substring_length in range(1, len(word) + 1):
        cells = []
        for start in range(len(word) - substring_length + 1):
            value = "".join(sorted(table[start][substring_length - 1])) or "-"
            cells.append(value)
        print(f"length={substring_length}: {cells}")


def main():
    tests = [
        "a=b",
        "b=-c",
        "c=a+b",
        "d=a*b",
        "a=(b)",
        "b=12.34",
        "c=0.5/d",
        "e=a",
        "a=1e2",
        "a=b+",
        "a=1..2",
        "a=(b*c",
    ]

    for word in tests:
        accepted, _ = cyk(word)
        print(f"{word:12} -> {'ACCEPT' if accepted else 'REJECT'}")

    print("\nТаблица CYK для b=12.34:")
    _, table = cyk("b=12.34")
    show_table("b=12.34", table)


if __name__ == "__main__":
    main()

