import time
from recipe_system.manager import RecipeManager
from recipe_system.recipe import Recipe
from recipe_system.sorting import BubbleSort, MergeSort
from recipe_system.logic import eval_expr, truth_table
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'recipes.csv')


def input_list(prompt: str):
    s = input(prompt + " (separate items with ;): ")
    return [i.strip() for i in s.split(';') if i.strip()]


def show_recipe_detail(r: Recipe):
    print(f"Name: {r.name}\nCategory: {r.category}\nPrice: ${r.price:.2f}\nTime: {r.time_minutes} minutes")
    print(f"Ingredients: {', '.join(r.ingredients)}")
    print("Steps:")
    for i, s in enumerate(r.steps, 1):
        print(f"  {i}. {s}")
    print(f"Calories: {r.calories} | Difficulty: {r.difficulty}")


def performance_test(manager: RecipeManager):
    sizes = [10, 50, 100]
    print("Performance test (Bubble vs Merge):")
    for n in sizes:
        sample = (manager.recipes * ((n // max(1, len(manager.recipes))) + 1))[:n]
        b = BubbleSort()
        m = MergeSort()
        start = time.time()
        b.sort(sample, key_func=lambda r: r.time_minutes)
        t_b = time.time() - start
        start = time.time()
        m.sort(sample, key_func=lambda r: r.time_minutes)
        t_m = time.time() - start
        print(f"n={n}: Bubble {t_b:.6f}s, Merge {t_m:.6f}s")


def main():
    manager = RecipeManager()
    # Attempt load from local CSV first
    default_csv = os.path.join(os.getcwd(), 'recipes.csv')
    if os.path.exists(default_csv):
        path = default_csv
    else:
        path = DATA_PATH
    try:
        manager.load_csv(path)
    except Exception as e:
        print("Could not load CSV:", e)

    while True:
        print('\n--- Recipe Selection System ---')
        print('1) View all recipes')
        print('2) View recipe details / Order')
        print('3) Add recipe')
        print('4) Edit recipe')
        print('5) Delete recipe')
        print('6) Search by name')
        print('7) Search by category')
        print('8) Search by ingredient')
        print('9) Logical search')
        print('10) Show truth table for expression')
        print('11) Sort recipes')
        print('12) Performance test')
        print('13) Export CSV')
        print('0) Exit')
        choice = input('Choose an option: ').strip()

        if choice == '1':
            for i, r in enumerate(manager.recipes, 1):
                print(f"{i}. {r}")

        elif choice == '2':
            name = input('Recipe name: ')
            r = manager.find_by_name(name)
            if r:
                show_recipe_detail(r)
            else:
                print('Not found')

        elif choice == '3':
            name = input('Name: ')
            category = input('Category: ')
            price = float(input('Price: '))
            time_m = int(input('Time minutes: '))
            ingredients = input_list('Ingredients')
            steps = input_list('Steps')
            calories = int(input('Calories (0 if unknown): '))
            diff = input('Difficulty: ')
            manager.add_recipe(Recipe(name, category, price, time_m, ingredients, steps, calories, diff))
            print('Added')

        elif choice == '4':
            name = input('Recipe name to edit: ')
            r = manager.find_by_name(name)
            if not r:
                print('Not found')
                continue
            print('Leave blank to keep current value')
            new_name = input(f'Name [{r.name}]: ') or r.name
            new_cat = input(f'Category [{r.category}]: ') or r.category
            new_price = input(f'Price [{r.price}]: ')
            new_time = input(f'Time minutes [{r.time_minutes}]: ')
            new_ings = input(f'Ingredients (;) [{";".join(r.ingredients)}]: ')
            new_steps = input(f'Steps (;) [{";".join(r.steps)}]: ')
            new_cal = input(f'Calories [{r.calories}]: ')
            new_diff = input(f'Difficulty [{r.difficulty}]: ') or r.difficulty
            r.name = new_name
            r.category = new_cat
            if new_price: r.price = float(new_price)
            if new_time: r.time_minutes = int(new_time)
            if new_ings: r.ingredients = [i.strip() for i in new_ings.split(';') if i.strip()]
            if new_steps: r.steps = [s.strip() for s in new_steps.split(';') if s.strip()]
            if new_cal: r.calories = int(new_cal)
            r.difficulty = new_diff
            print('Updated')

        elif choice == '5':
            name = input('Recipe name to delete: ')
            ok = manager.delete_recipe(name)
            print('Deleted' if ok else 'Not found')

        elif choice == '6':
            name = input('Name to search: ')
            r = manager.find_by_name(name)
            if r: print(r)
            else: print('Not found')

        elif choice == '7':
            cat = input('Category: ')
            res = manager.search_by_category(cat)
            for r in res: print(r)

        elif choice == '8':
            ing = input('Ingredient: ')
            res = manager.search_by_ingredient(ing)
            for r in res: print(r)

        elif choice == '9':
            expr = input('Enter logical expression (e.g. "(contains_chicken and cheap) or quick"): ')
            matched = []
            for r in manager.recipes:
                env = {
                    'contains_chicken': any('chicken' in i.lower() for i in r.ingredients),
                    'cheap': r.price < 4.0,
                    'quick': r.time_minutes <= 15,
                    'healthy': r.calories < 400,
                }
                try:
                    if eval_expr(expr, env):
                        matched.append(r)
                except Exception as e:
                    print('Error evaluating expression:', e)
                    matched = []
                    break
            for r in matched:
                print(r)

        elif choice == '10':
            expr = input('Expression for truth table (use variable names): ')
            try:
                vars_, rows = truth_table(expr)
                print(' | '.join(vars_) + ' | Result')
                for vals, res in rows:
                    print(' | '.join(str(v) for v in vals) + ' | ' + str(res))
            except Exception as e:
                print('Error:', e)

        elif choice == '11':
            alg = input('Algorithm (bubble/merge): ').strip().lower()
            key = input('Primary key (price/time): ').strip().lower()
            expr = input('Optional logical expression for secondary key (leave blank to skip): ').strip()
            sorter = BubbleSort() if alg == 'bubble' else MergeSort()
            def keyfunc(r):
                primary = r.price if key == 'price' else r.time_minutes
                secondary = 0
                if expr:
                    env = {
                        'contains_chicken': any('chicken' in i.lower() for i in r.ingredients),
                        'cheap': r.price < 4.0,
                        'quick': r.time_minutes <= 15,
                        'healthy': r.calories < 400,
                    }
                    try:
                        secondary = 0 if eval_expr(expr, env) else 1
                    except Exception:
                        secondary = 1
                return (primary, secondary)
            sorted_list = sorter.sort(manager.recipes, key_func=keyfunc)
            manager.recipes = sorted_list
            print('Sorted')

        elif choice == '12':
            performance_test(manager)

        elif choice == '13':
            path = input('Export path (filename.csv): ').strip()
            if not path:
                path = 'exported_recipes.csv'
            manager.save_csv(path)
            print('Saved to', path)

        elif choice == '0':
            break
        else:
            print('Unknown option')


if __name__ == '__main__':
    main()
