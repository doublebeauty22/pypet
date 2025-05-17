from pet import Pet
import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    print("\n" + "="*40)
    print("🎮 PyPet - Your Virtual Pet! 🐱")
    print("="*40)
    print("1. 🍖 Feed (Restores energy)")
    print("2. 💼 Work (Chance to find ores)")
    print("3. 🎮 Play (Increases happiness)")
    print("4. 😴 Rest")
    print("5. 📊 Check status")
    print("6. ⭐ Super Rest (costs 2 ores)")
    print("7. 📝 View action log")
    print("8. 🚪 Quit")
    print("="*40)

def print_welcome_art():
    print("""
    ╔══════════════════════════════════╗
    ║        Welcome to PyPet!         ║
    ║      Your Virtual Pet Game       ║
    ╚══════════════════════════════════╝
    """)

def print_welcome_back_art(name):
    print(f"""
    ╔══════════════════════════════════╗
    ║        Welcome Back!             ║
    ║      {name} missed you!           ║
    ╚══════════════════════════════════╝
    """)

def print_quit_art(name):
    print(f"""
    ╔══════════════════════════════════╗
    ║           Goodbye!               ║
    ║    {name} will miss you!          ║
    ║                                 ║
    ║    /\\___/\\                      ║
    ║   (  T_T  )                     ║
    ║   (  =^=  )                     ║
    ║    (____)                       ║
    ╚══════════════════════════════════╝
    """)

def main():
    clear_screen()
    
    # Try to load existing pet
    pet = Pet.load()
    if pet:
        print_welcome_back_art(pet.name)
        time.sleep(1)
    else:
        print_welcome_art()
        name = input("Name your pet: ")
        pet = Pet(name)
        print(f"\n✨ {name} has been born! ✨\n")
        time.sleep(1)

    while True:
        if pet.is_dead():
            print(f"""
    ╔══════════════════════════════════╗
    ║           Game Over!             ║
    ║      {pet.name} has died...        ║
    ║                                 ║
    ║    /\\___/\\                      ║
    ║   (  x x  )                     ║
    ║   (  =^=  )                     ║
    ║    (____)                       ║
    ╚══════════════════════════════════╝
            """)
            pet.delete_save()  # Delete save file when pet dies
            break

        print_menu()
        choice = input("Enter choice (1-8): ")

        clear_screen()
        if choice == "1":
            pet.feed()
        elif choice == "2":
            pet.work()
        elif choice == "3":
            pet.play()
        elif choice == "4":
            pet.rest()
        elif choice == "5":
            pass
        elif choice == "6":
            pet.super_rest()
        elif choice == "7":
            pet.show_log()
        elif choice == "8":
            pet.save()  # Save pet state before quitting
            print_quit_art(pet.name)
            break
        else:
            print("❌ Invalid choice.")

        if choice != "7" and choice != "8":
            print(pet)
            time.sleep(1.5)

        pet.tick()

if __name__ == '__main__':
    main()