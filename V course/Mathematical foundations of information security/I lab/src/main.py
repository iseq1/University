from src.controllers.main_controller import MainController

if __name__ == "__main__":
    print("=== Basic demo ===")
    MainController.demo_basic()
    print("\n=== Bent demo ===")
    MainController.demo_bent()
    print("\n=== S-box search demo (n=5 heuristic) ===")
    MainController.demo_sbox_search()