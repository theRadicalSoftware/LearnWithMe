import pygame
import random
import time
import sys
import json
import os

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Learning Game")

# Load the title screen image and scale it to fit the screen
title_image = pygame.image.load("assets/images/title_screen.png")
title_image = pygame.transform.scale(title_image, (screen_width, screen_height))

# Load background images for different screens
account_screen_bg = pygame.image.load("/home/rory/LearningGame/assets/images/account_screen.png")
account_screen_bg = pygame.transform.scale(account_screen_bg, (screen_width, screen_height))
create_account_bg = pygame.image.load("/home/rory/LearningGame/assets/images/createAccount_screen.png")
create_account_bg = pygame.transform.scale(create_account_bg, (screen_width, screen_height))
choose_account_bg = pygame.image.load("/home/rory/LearningGame/assets/images/chooseAccount_screen.png")
choose_account_bg = pygame.transform.scale(choose_account_bg, (screen_width, screen_height))
game_mode_bg = pygame.image.load("/home/rory/LearningGame/assets/images/game_mode_screen.png")
game_mode_bg = pygame.transform.scale(game_mode_bg, (screen_width, screen_height))
classroom_screen_bg = pygame.image.load("/home/rory/LearningGame/assets/images/classroom_screen.png")
classroom_screen_bg = pygame.transform.scale(classroom_screen_bg, (screen_width, screen_height))
level_selector_bg = pygame.image.load("/home/rory/LearningGame/assets/images/level_selector_screen.png")
level_selector_bg = pygame.transform.scale(level_selector_bg, (screen_width, screen_height))

# Load the level portal image
apple_picker_portal = pygame.image.load("/home/rory/LearningGame/assets/images/applePicker_level_portal.png")
apple_picker_portal = pygame.transform.scale(apple_picker_portal, (180, 180))  # Slightly larger size

# Load the pigCare_level_portal image
pig_care_portal = pygame.image.load("/home/rory/LearningGame/assets/images/pigCare_level_portal.png")
pig_care_portal = pygame.transform.scale(pig_care_portal, (180, 180))  # Adjust size to match apple picker portal


# Load the back arrow image
back_arrow_img = pygame.image.load("/home/rory/LearningGame/assets/images/back_arrow.png")
back_arrow_img = pygame.transform.scale(back_arrow_img, (50, 50))
back_arrow_rect = back_arrow_img.get_rect(bottomleft=(20, screen_height - 20))

# Button settings
button_font = pygame.font.Font(None, 36)
instruction_font = pygame.font.Font(None, 32)  # Smaller font for "Enter your name"
popup_font = pygame.font.Font(None, 40)  # Font for popup text
button_text_color = (255, 255, 255)  # White text color
button_color = (175, 60, 60)  # Soft, apple-inspired red
button_shadow_color = (150, 45, 45)  # Slightly darker for depth
button_hover_color = (200, 80, 80)  # Lighter shade for hover effect

# Define buttons for the title screen
start_button_text = button_font.render("Start Learning", True, button_text_color)
start_button_rect = start_button_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
options_button_text = button_font.render("Options", True, button_text_color)
options_button_rect = options_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

# Define buttons for the "Start Learning" screen
create_account_text = button_font.render("Create Account", True, button_text_color)
create_account_rect = create_account_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
choose_account_text = button_font.render("Choose Account", True, button_text_color)
choose_account_rect = choose_account_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))

tooltip_font = pygame.font.Font(None, 50)  # Font for tooltips


# Account data storage file
accounts_file = "accounts.json"

# Load accounts from the file
def load_accounts():
    if os.path.exists(accounts_file):
        with open(accounts_file, "r") as file:
            return json.load(file)
    return []

# Save accounts to the file
def save_accounts():
    with open(accounts_file, "w") as file:
        json.dump(accounts, file)

# Initialize accounts
accounts = load_accounts()

# Load profile pictures
profile_pics = [
    pygame.image.load("/home/rory/LearningGame/assets/images/profilePic_01.png"),
    pygame.image.load("/home/rory/LearningGame/assets/images/profilePic_02.png")
]

# Scale profile pictures for display
profile_pics = [pygame.transform.scale(pic, (100, 100)) for pic in profile_pics]

# Draw a textured button with optional hover color and extra padding
def draw_textured_button(surface, text_surf, button_rect, color, shadow_color, hover=False, padding=20):
    offset = -2 if hover else 0
    adjusted_rect = button_rect.inflate(padding, padding).move(0, offset)  # Add padding
    shadow_rect = adjusted_rect.move(2, 2)

    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=15)

    button_surf = pygame.Surface((adjusted_rect.width, adjusted_rect.height), pygame.SRCALPHA)
    button_surf.fill((0, 0, 0, 0))
    pygame.draw.rect(button_surf, color, button_surf.get_rect(), border_radius=15)

    surface.blit(button_surf, adjusted_rect.topleft)
    pygame.draw.rect(surface, (255, 255, 255), adjusted_rect, width=3, border_radius=15)
    surface.blit(text_surf, text_surf.get_rect(center=adjusted_rect.center))

# Function to display a popup message
def show_popup(message):
    popup_bg = pygame.Surface((400, 150), pygame.SRCALPHA)
    popup_bg.fill((0, 0, 0, 180))
    popup_rect = popup_bg.get_rect(center=(screen_width // 2, screen_height // 2))

    message_text = popup_font.render(message, True, (255, 255, 255))
    message_rect = message_text.get_rect(center=(popup_rect.width // 2, popup_rect.height // 2))

    popup_bg.blit(message_text, message_rect)
    screen.blit(popup_bg, popup_rect.topleft)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type in {pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN}:
                waiting = False

def display_pause_menu(selected_account):
    """Displays the pause menu with options to resume or quit."""
    resume_button_text = button_font.render("Resume", True, button_text_color)
    resume_button_rect = resume_button_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))

    quit_button_text = button_font.render("Quit to Level Selector", True, button_text_color)
    quit_button_rect = quit_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))

    pause_menu_width, pause_menu_height = 400, 300
    pause_menu_x = (screen_width - pause_menu_width) // 2
    pause_menu_y = (screen_height - pause_menu_height) // 2
    pause_menu_rect = pygame.Rect(pause_menu_x, pause_menu_y, pause_menu_width, pause_menu_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if resume_button_rect.collidepoint(mouse_x, mouse_y):  # Resume game
                    return
                elif quit_button_rect.collidepoint(mouse_x, mouse_y):  # Quit to level selector
                    level_selector_screen(selected_account)
                    return

        # Draw semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Semi-transparent black
        screen.blit(overlay, (0, 0))

        # Draw the pause menu
        pygame.draw.rect(screen, (255, 255, 255), pause_menu_rect, border_radius=15)
        pygame.draw.rect(screen, (200, 80, 80), pause_menu_rect, width=5, border_radius=15)

        # Draw buttons
        draw_textured_button(screen, resume_button_text, resume_button_rect, button_color, button_shadow_color)
        draw_textured_button(screen, quit_button_text, quit_button_rect, button_color, button_shadow_color)

        pygame.display.flip()



# Function to handle the apple picker level screen
def apple_picker_level_screen(selected_account):
    # Initial position of the profile picture
    profile_pic = profile_pics[selected_account["profile_pic"]]
    profile_pic_x = (screen_width - profile_pic.get_width()) // 2
    profile_pic_y = screen_height - profile_pic.get_height() - 21
    is_jumping = False
    jump_frame = 0
    jump_height = 90
    jump_duration = 30
    move_speed = 7
    apples_collected = 0

    # Timer setup: 5 minutes in seconds
    start_time = time.time()
    total_time = 5 * 60  # 5 minutes in seconds

    # Fonts for apple counter and timer
    apple_counter_font = pygame.font.Font(None, 100)
    timer_font = pygame.font.Font(None, 100)

    # Load images
    apple_image = pygame.image.load("/home/rory/LearningGame/assets/images/apple_item.png")
    apple_image = pygame.transform.scale(apple_image, (60, 60))
    basket_image = pygame.image.load("/home/rory/LearningGame/assets/images/appleBasket_item.png")
    basket_image = pygame.transform.scale(basket_image, (70, 70))

    # List to store apples and baskets
    apples = []
    baskets = []
    apple_spawn_timer = 0

    # Buttons for pause overlay
    resume_button_text = button_font.render("Resume", True, button_text_color)
    resume_button_rect = resume_button_text.get_rect(center=(screen_width // 2, screen_height // 2 - 40))
    quit_button_text = button_font.render("Quit to Level Selector", True, button_text_color)
    quit_button_rect = quit_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 40))

    def display_game_over():
        """Display the game over popup with options."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_accounts()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if return_button_rect.collidepoint(mouse_pos):
                        level_selector_screen(selected_account)
                        return
                    elif restart_button_rect.collidepoint(mouse_pos):
                        return apple_picker_level_screen(selected_account)

            # Draw semi-transparent overlay
            overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Semi-transparent black
            screen.blit(overlay, (0, 0))

            # Draw the popup box
            box_width, box_height = 500, 300
            box_x = (screen_width - box_width) // 2
            box_y = (screen_height - box_height) // 2
            box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, border_radius=15)

            # Add a border to the box
            pygame.draw.rect(screen, (200, 80, 80), box_rect, width=5, border_radius=15)

            # Display game over text
            game_over_text = popup_font.render("You collected all the apples!", True, (0, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 80))
            screen.blit(game_over_text, game_over_rect)

            # Draw buttons
            draw_textured_button(screen, return_button_text, return_button_rect, button_color, button_shadow_color)
            draw_textured_button(screen, restart_button_text, restart_button_rect, button_color, button_shadow_color)

            pygame.display.flip()

    # Buttons for game over overlay
    return_button_text = button_font.render("Return to Level Selector", True, button_text_color)
    return_button_rect = return_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 20))
    restart_button_text = button_font.render("Play Again", True, button_text_color)
    restart_button_rect = restart_button_text.get_rect(center=(screen_width // 2, screen_height // 2 + 80))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_selector_screen(selected_account)
                    return
                elif event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    jump_frame = 0
                elif event.key == pygame.K_p:  # Pause the game
                    display_pause_menu(selected_account)


        # Calculate remaining time
        elapsed_time = time.time() - start_time
        remaining_time = max(total_time - elapsed_time, 0)
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)

        # End the game if the timer reaches zero
        if remaining_time <= 0:
            show_popup("Time's up! You collected {} apples.".format(apples_collected))
            level_selector_screen(selected_account)
            return

        # Movement logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            profile_pic_x -= move_speed
        if keys[pygame.K_RIGHT]:
            profile_pic_x += move_speed
        profile_pic_x = max(0, min(screen_width - profile_pic.get_width(), profile_pic_x))

        # Jump logic
        if is_jumping:
            progress = jump_frame / jump_duration
            jump_offset = -4 * jump_height * (progress - 0.5) ** 2 + jump_height
            jump_frame += 1
            if jump_frame >= jump_duration:
                is_jumping = False
                jump_offset = 0
        else:
            jump_offset = 0

        # Spawn apples
        apple_spawn_timer += 1
        if apple_spawn_timer > 60:
            apple_x = random.randint(0, screen_width - apple_image.get_width())
            apples.append({"x": apple_x, "y": 0})
            apple_spawn_timer = 0

        # Move apples
        for apple in apples:
            apple["y"] += 5

        # Check for collisions
        for apple in apples[:]:
            apple_rect = pygame.Rect(apple["x"], apple["y"], apple_image.get_width(), apple_image.get_height())
            profile_rect = pygame.Rect(profile_pic_x, profile_pic_y - jump_offset, profile_pic.get_width(), profile_pic.get_height())
            if apple_rect.colliderect(profile_rect):
                apples.remove(apple)
                apples_collected += 1

                # Add basket for every 10 apples
                if apples_collected % 10 == 0:
                    basket_x = screen_width - basket_image.get_width() - 20
                    basket_y = screen_height - (len(baskets) + 1) * basket_image.get_height() - 20
                    baskets.append({"x": basket_x, "y": basket_y})

                # Win condition
                if apples_collected >= 80:
                    display_game_over()
                    return

        # Remove off-screen apples
        apples = [apple for apple in apples if apple["y"] < screen_height]

        # Draw background
        apple_picker_bg = pygame.image.load("/home/rory/LearningGame/assets/images/applePicker_level_screen.png")
        apple_picker_bg = pygame.transform.scale(apple_picker_bg, (screen_width, screen_height))
        screen.blit(apple_picker_bg, (0, 0))

        # Draw timer
        timer_text = timer_font.render(f"{minutes:02}:{seconds:02}", True, (255, 0, 0))  # Red color
        timer_rect = timer_text.get_rect(center=(100, 100))
        screen.blit(timer_text, timer_rect)

        # Draw apple counter
        apple_counter_text = apple_counter_font.render(str(apples_collected), True, (255, 255, 255))
        apple_counter_rect = apple_counter_text.get_rect(center=(screen_width - 120, 80))
        screen.blit(apple_counter_text, apple_counter_rect)

        # Draw apples
        for apple in apples:
            screen.blit(apple_image, (apple["x"], apple["y"]))

        # Draw baskets
        for basket in baskets:
            screen.blit(basket_image, (basket["x"], basket["y"]))

        # Draw profile picture
        screen.blit(profile_pic, (profile_pic_x, profile_pic_y - jump_offset))

        pygame.display.flip()


def pig_care_level_screen(selected_account):
    # Load the piggie caretaker background image
    pig_care_bg = pygame.image.load("/home/rory/LearningGame/assets/images/piggieCareTaker_level_screen.png")
    pig_care_bg = pygame.transform.scale(pig_care_bg, (screen_width, screen_height))

    # Load the hay bale image
    hay_bale_image = pygame.image.load("/home/rory/LearningGame/assets/images/hayBale_item.png")
    hay_bale_image = pygame.transform.scale(hay_bale_image, (100, 100))

    # Load the hay bundle image for the bubble
    hay_bundle_image = pygame.image.load("/home/rory/LearningGame/assets/images/hayBundle_item.png")
    hay_bundle_image = pygame.transform.scale(hay_bundle_image, (50, 50))

    # Load the pig image
    pig_image = pygame.image.load("/home/rory/LearningGame/assets/images/piggie_animal.png")
    pig_image = pygame.transform.scale(pig_image, (100, 100))

    # Load pig stats
    pig_fed_count = selected_account.get("pig_fed_count", 0)
    pig_happiness_level = min(4, pig_fed_count // 3 + 1)  # Calculate happiness based on feedings



    # Load the heart image
    heart_image = pygame.image.load("/home/rory/LearningGame/assets/images/heart_item.png")
    heart_image = pygame.transform.scale(heart_image, (100, 100))



    # Get the profile picture
    profile_pic = profile_pics[selected_account["profile_pic"]]

    # Initial profile picture position
    profile_pic_x = (screen_width - profile_pic.get_width()) // 2
    profile_pic_y = screen_height - profile_pic.get_height() - 130

    # Position the hay bale to the left of the profile image
    hay_bale_x = profile_pic_x - hay_bale_image.get_width() - 110
    hay_bale_y = profile_pic_y + (profile_pic.get_height() - hay_bale_image.get_height()) // 2 - 35

    # Initial pig position and movement
    pig_x = random.randint(0, screen_width - pig_image.get_width())
    pig_y = random.randint(305, screen_height - profile_pic.get_height() - 120)
    pig_speed_x = random.choice([-.50, .50])  # Random initial direction
    pig_speed_y = random.choice([-.50, .50])

    # Movement speed
    move_speed = 3

    # Define vertical boundaries for the profile picture and pig
    upper_boundary = 305
    lower_boundary = screen_height - profile_pic.get_height() - 120

    # Track whether hay has been picked up and given to the pig
    hay_picked_up = False
    hay_given_to_pig = False
    heart_timer = 0  # Timer for displaying the heart

    # Pig's name
    pig_name = selected_account.get("pig_name", None)


    def name_pig():
        """Prompts the user to name the pig."""
        input_text = ""
        naming = True
        while naming:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_accounts()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text.strip():
                        return input_text.strip()
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isprintable():
                        input_text += event.unicode

            # Display naming prompt
            screen.fill((0, 0, 0, 180))  # Semi-transparent overlay
            prompt_text = button_font.render("Enter a name for the pig:", True, (255, 255, 255))
            input_display = button_font.render(input_text, True, (255, 255, 255))
            screen.blit(prompt_text, (screen_width // 2 - 150, screen_height // 2 - 50))
            screen.blit(input_display, (screen_width // 2 - 150, screen_height // 2))
            pygame.display.flip()
    
    def display_pig_info():
        """Displays a modal with information about the pig."""
        info_displaying = True
        while info_displaying:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_accounts()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_z):  # Close the modal with RETURN or Z
                        info_displaying = False
                    elif event.key == pygame.K_r:  # Rename the pig
                        new_name = name_pig()
                        if new_name:
                            selected_account["pig_name"] = new_name
                            save_accounts()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, mouse_y = event.pos
                        if close_button_rect.collidepoint(mouse_x, mouse_y):  # Check if clicked on close button
                            info_displaying = False

            # Modal background
            modal_rect = pygame.Rect(screen_width // 6, screen_height // 6, (screen_width * 2) // 3, (screen_height * 5) // 6)
            pygame.draw.rect(screen, (255, 255, 255), modal_rect)
            pygame.draw.rect(screen, (0, 0, 0), modal_rect, 4)


            # Close button
            close_button_rect = pygame.Rect(modal_rect.right - 40, modal_rect.top + 10, 30, 30)
            pygame.draw.rect(screen, (255, 0, 0), close_button_rect)
            close_font = pygame.font.Font(None, 30)
            close_text = close_font.render("X", True, (255, 255, 255))
            screen.blit(close_text, (close_button_rect.centerx - close_text.get_width() // 2,
                                    close_button_rect.centery - close_text.get_height() // 2))

            # Pig name
            name_font = pygame.font.Font(None, 50)
            name_text = name_font.render(f"Name: {pig_name}", True, (0, 0, 0))
            screen.blit(name_text, (modal_rect.centerx - name_text.get_width() // 2, modal_rect.top + 50))

            # Times fed
            fed_text = name_font.render(f"Times Fed: {pig_fed_count}", True, (0, 0, 0))
            screen.blit(fed_text, (modal_rect.centerx - fed_text.get_width() // 2, modal_rect.top + 120))

            # Happiness level
            happiness_text = name_font.render("Happiness:", True, (0, 0, 0))
            screen.blit(happiness_text, (modal_rect.centerx - happiness_text.get_width() // 2, modal_rect.top + 190))

            # Display hearts for happiness
            for i in range(pig_happiness_level):
                heart_x = modal_rect.centerx - (pig_happiness_level * 36) + (i * 50)
                screen.blit(heart_image, (heart_x, modal_rect.top + 210))

            # Pig image
            screen.blit(pig_image, (modal_rect.centerx - pig_image.get_width() // 2, modal_rect.top + 300))

            # Rename option
            rename_text = name_font.render("Press R to Rename", True, (0, 0, 0))
            screen.blit(rename_text, (modal_rect.centerx - rename_text.get_width() // 2, modal_rect.bottom - 100))

            pygame.display.flip()



    # Game loop for the Piggie Care screen
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    level_selector_screen(selected_account)
                    return
                elif event.key == pygame.K_x:
                    # Interaction logic for picking up or giving hay
                    profile_rect = pygame.Rect(profile_pic_x, profile_pic_y, profile_pic.get_width(), profile_pic.get_height())
                    hay_bale_rect = pygame.Rect(hay_bale_x, hay_bale_y, hay_bale_image.get_width(), hay_bale_image.get_height())
                    pig_rect = pygame.Rect(pig_x, pig_y, pig_image.get_width(), pig_image.get_height())

                    # Pick up the hay bale
                    if profile_rect.colliderect(hay_bale_rect) and not hay_picked_up:
                        hay_picked_up = True

                    # Give the hay to the pig
                    if profile_rect.colliderect(pig_rect) and hay_picked_up and not hay_given_to_pig:
                        hay_given_to_pig = True
                        hay_picked_up = False
                        heart_timer = pygame.time.get_ticks()  # Start the heart display timer

                        pig_fed_count += 1  # Increment feed count
                        selected_account["pig_fed_count"] = pig_fed_count  # Save to account
                        pig_happiness_level = min(4, pig_fed_count // 3 + 1)  # Recalculate happiness
                        save_accounts()  # Persist changes

                elif event.key == pygame.K_z:
                    # Interaction logic for naming the pig
                    profile_rect = pygame.Rect(profile_pic_x, profile_pic_y, profile_pic.get_width(), profile_pic.get_height())
                    pig_rect = pygame.Rect(pig_x, pig_y, pig_image.get_width(), pig_image.get_height())

                    if profile_rect.colliderect(pig_rect) and not hay_picked_up and pig_name is None:
                        pig_name = name_pig()
                        selected_account["pig_name"] = pig_name
                        save_accounts()

                    if profile_rect.colliderect(pig_rect) and pig_name:
                        display_pig_info()

                elif event.key == pygame.K_p:  # Pause the game
                    display_pause_menu(selected_account)


        

        # Movement logic for the profile picture
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            profile_pic_x -= move_speed
        if keys[pygame.K_RIGHT]:
            profile_pic_x += move_speed
        if keys[pygame.K_UP]:
            profile_pic_y -= move_speed
        if keys[pygame.K_DOWN]:
            profile_pic_y += move_speed

        # Ensure the profile picture stays within screen bounds
        profile_pic_x = max(0, min(screen_width - profile_pic.get_width(), profile_pic_x))
        profile_pic_y = max(upper_boundary, min(lower_boundary, profile_pic_y))

        # Pig movement logic
        pig_x += pig_speed_x
        pig_y += pig_speed_y

        # Reverse direction if the pig hits the bounds
        if pig_x <= 0 or pig_x >= screen_width - pig_image.get_width():
            pig_speed_x = -pig_speed_x
        if pig_y <= upper_boundary or pig_y >= lower_boundary:
            pig_speed_y = -pig_speed_y

        # Draw the background
        screen.blit(pig_care_bg, (0, 0))

        # Draw the hay bale
        screen.blit(hay_bale_image, (hay_bale_x, hay_bale_y))

        # Draw the pig
        screen.blit(pig_image, (pig_x, pig_y))

        # Draw the profile picture
        screen.blit(profile_pic, (profile_pic_x, profile_pic_y))

        # Display pig's name if named
        if pig_name:
            name_font = pygame.font.Font(None, 40)  # Larger, bold font
            name_text = name_font.render(pig_name, True, (153, 50, 204))  # Bright purple color
            screen.blit(name_text, (pig_x + pig_image.get_width() // 2 - name_text.get_width() // 2, pig_y - 20))

        # Display prompt to name the pig
        profile_rect = pygame.Rect(profile_pic_x, profile_pic_y, profile_pic.get_width(), profile_pic.get_height())
        pig_rect = pygame.Rect(pig_x, pig_y, pig_image.get_width(), pig_image.get_height())
        if profile_rect.colliderect(pig_rect) and not hay_picked_up and pig_name is None:
            prompt_text = button_font.render("Press Z to name the pig", True, (0, 0, 0))
            screen.blit(prompt_text, (profile_pic_x, profile_pic_y - 30))

        # Display the "Press X to pick up" prompt if near the hay bale and not picked up
        hay_bale_rect = pygame.Rect(hay_bale_x, hay_bale_y, hay_bale_image.get_width(), hay_bale_image.get_height())
        if profile_rect.colliderect(hay_bale_rect) and not hay_picked_up:
            pickup_text = button_font.render("Press X to pick up", True, (0, 0, 0))
            pickup_text_rect = pickup_text.get_rect(center=(profile_pic_x + profile_pic.get_width() // 2,
                                                            profile_pic_y - 20))
            screen.blit(pickup_text, pickup_text_rect)

        # Display hay bundle above profile picture if picked up
        if hay_picked_up:
            bubble_rect = pygame.Rect(profile_pic_x + profile_pic.get_width() // 2 - 40, profile_pic_y - 70, 80, 80)
            pygame.draw.ellipse(screen, (255, 255, 255), bubble_rect)
            pygame.draw.ellipse(screen, (0, 0, 0), bubble_rect, 2)
            screen.blit(hay_bundle_image, (bubble_rect.x + 15, bubble_rect.y + 15))

        # Display the heart above the pig if hay was given
        if hay_given_to_pig:
            current_time = pygame.time.get_ticks()
            if current_time - heart_timer < 2000:  # Display the heart for 2 seconds
                heart_rect = pygame.Rect(pig_x + pig_image.get_width() // 2 - 52, pig_y - 90, 50, 50)
                screen.blit(heart_image, heart_rect.topleft)
            else:
                hay_given_to_pig = False  # Reset after displaying the heart

        pygame.display.flip()
        clock.tick(60)



def level_selector_screen(selected_account):
    is_jumping = False  # Flag to indicate if the profile picture is jumping
    jump_frame = 0  # Frame counter for the jump animation
    jump_height = 70  # Maximum height of the jump
    jump_duration = 180  # Total frames for the jump

    # Adjust the position of the back arrow image
    back_arrow_rect = back_arrow_img.get_rect(bottomleft=(20, screen_height - 30))

    while True:
        mouse_pos = pygame.mouse.get_pos()  # Get the current mouse position
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:  # Start jump on space bar press
                    is_jumping = True
                    jump_frame = 0  # Reset the frame counter for the jump
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the back arrow was clicked
                if back_arrow_rect.collidepoint(mouse_pos):
                    game_mode_screen(selected_account)  # Navigate back to the game mode screen
                    return
                # Check if the apple picker portal was clicked
                if apple_portal_rect.collidepoint(mouse_pos):
                    apple_picker_level_screen(selected_account)  # Navigate to the apple picker level screen
                    return
                # Check if the pig care portal was clicked
                if pig_portal_rect.collidepoint(mouse_pos):
                    pig_care_level_screen(selected_account)  # Navigate to the pig care level screen
                    return

        # Update jump logic
        if is_jumping:
            # Smooth jump up and down
            progress = jump_frame / jump_duration
            jump_offset = -4 * jump_height * (progress - 0.5) ** 2 + jump_height
            jump_frame += 1
            if jump_frame >= jump_duration:  # End the jump after the duration
                is_jumping = False
                jump_offset = 0
        else:
            jump_offset = 0

        # Draw the background
        screen.blit(level_selector_bg, (0, 0))

        # Draw the selected account's profile picture with the jump effect
        profile_pic = profile_pics[selected_account["profile_pic"]]  # Get the chosen profile picture
        profile_pic_x, profile_pic_y = screen_width - 437, 400 - jump_offset  # Apply jump offset upwards
        screen.blit(profile_pic, (profile_pic_x, profile_pic_y))

        # Portal positions and dimensions
        apple_portal_x, apple_portal_y = 0, 80
        apple_portal_width, apple_portal_height = 180, 180
        apple_portal_rect = pygame.Rect(apple_portal_x, apple_portal_y, apple_portal_width, apple_portal_height)

        pig_portal_x, pig_portal_y = 200, 101  # Positioned to the right of the apple picker portal
        pig_portal_width, pig_portal_height = 180, 180
        pig_portal_rect = pygame.Rect(pig_portal_x, pig_portal_y, pig_portal_width, pig_portal_height)

        # Hover effect and tooltip for the apple picker portal
        if apple_portal_rect.collidepoint(mouse_pos):  # Check if the mouse is hovering over the apple picker portal
            enlarged_portal = pygame.transform.scale(apple_picker_portal, (200, 200))  # Slightly enlarge the portal
            screen.blit(enlarged_portal, (apple_portal_x, apple_portal_y - 10))  # Move it up slightly
            tooltip_text = tooltip_font.render("Apple Picker", True, (0, 0, 0))  # Tooltip text with black color
            tooltip_rect = tooltip_text.get_rect(center=(apple_portal_x + 120, apple_portal_y + 200))  # Position the tooltip below
            screen.blit(tooltip_text, tooltip_rect)  # Render the tooltip
        else:
            screen.blit(apple_picker_portal, (apple_portal_x, apple_portal_y))  # Regular portal rendering

        # Hover effect and tooltip for the pig care portal
        if pig_portal_rect.collidepoint(mouse_pos):  # Check if the mouse is hovering over the pig care portal
            enlarged_portal = pygame.transform.scale(pig_care_portal, (200, 200))  # Slightly enlarge the portal
            screen.blit(enlarged_portal, (pig_portal_x, pig_portal_y - 10))  # Move it up slightly
            tooltip_text = tooltip_font.render("Piggie Caretaker", True, (0, 0, 0))  # Tooltip text with black color
            tooltip_rect = tooltip_text.get_rect(center=(pig_portal_x + 100, pig_portal_y + 180))  # Position the tooltip below
            screen.blit(tooltip_text, tooltip_rect)  # Render the tooltip
        else:
            screen.blit(pig_care_portal, (pig_portal_x, pig_portal_y))  # Regular portal rendering

        # Draw the back arrow at the bottom left corner
        screen.blit(back_arrow_img, back_arrow_rect)

        pygame.display.flip()


def classroom_screen(selected_account):
    # Adjusted button sizes and positions for a sleeker look
    button_width, button_height = 140, 50
    spacing = 20  # Space between buttons

    # Define button positions
    math_fun_button_rect = pygame.Rect(screen_width // 2 - button_width - spacing - 63, screen_height // 2 - 110, button_width, button_height)
    spelling_bee_button_rect = pygame.Rect(screen_width // 2 - button_width // 2 + 19, screen_height // 2 - 110, button_width, button_height)
    memory_game_button_rect = pygame.Rect(screen_width // 2 + button_width + spacing - 40, screen_height // 2 - 110, button_width, button_height)
    report_card_button_rect = pygame.Rect(screen_width // 2 - button_width // 2 + 17, screen_height // 2 + 60, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check button interactions
                if math_fun_button_rect.collidepoint(mouse_pos):
                    print("Math Fun selected")
                    # Add logic for Math Fun
                elif spelling_bee_button_rect.collidepoint(mouse_pos):
                    print("Spelling Bee selected")
                    # Add logic for Spelling Bee
                elif memory_game_button_rect.collidepoint(mouse_pos):
                    print("Memory Game selected")
                    # Add logic for Memory Game
                elif report_card_button_rect.collidepoint(mouse_pos):
                    print("Report Card selected")
                    # Add logic for Report Card
                elif back_button_rect.collidepoint(mouse_pos):
                    return game_mode_screen(selected_account)

        # Draw the classroom screen background
        screen.blit(classroom_screen_bg, (0, 0))

        # Back button
        back_button_text = button_font.render("Back", True, button_text_color)
        back_button_rect = back_button_text.get_rect(topleft=(15, 560))
        draw_textured_button(screen, back_button_text, back_button_rect, button_color, button_shadow_color)

        # Math Fun button
        math_fun_text = button_font.render("Math Fun", True, button_text_color)
        draw_textured_button(
            screen, math_fun_text, math_fun_button_rect, button_color, button_shadow_color, hover=False
        )

        # Spelling Bee button
        spelling_bee_text = button_font.render("Spelling Bee", True, button_text_color)
        draw_textured_button(
            screen, spelling_bee_text, spelling_bee_button_rect, button_color, button_shadow_color, hover=False
        )

        # Memory Game button
        memory_game_text = button_font.render("Memory", True, button_text_color)
        draw_textured_button(
            screen, memory_game_text, memory_game_button_rect, button_color, button_shadow_color, hover=False
        )

        # Report Card button (different color)
        report_card_text = button_font.render("Report Card", True, (255, 255, 255))  # White text for contrast
        report_card_color = (80, 140, 200)  # Blueish color
        report_card_shadow_color = (60, 110, 160)
        draw_textured_button(
            screen, report_card_text, report_card_button_rect, report_card_color, report_card_shadow_color, hover=False
        )

        pygame.display.flip()


# Function to handle the "Start Learning" screen
def start_learning_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if create_account_rect.collidepoint(mouse_pos):
                    create_account_screen()
                elif choose_account_rect.collidepoint(mouse_pos):
                    choose_account_screen()

        screen.blit(account_screen_bg, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        draw_textured_button(screen, create_account_text, create_account_rect,
                             button_hover_color if create_account_rect.collidepoint(mouse_pos) else button_color,
                             button_shadow_color, hover=create_account_rect.collidepoint(mouse_pos), padding=20)
        draw_textured_button(screen, choose_account_text, choose_account_rect,
                             button_hover_color if choose_account_rect.collidepoint(mouse_pos) else button_color,
                             button_shadow_color, hover=choose_account_rect.collidepoint(mouse_pos), padding=20)
        pygame.display.flip()

# Function to handle creating an account
def create_account_screen():
    name = ""
    selected_pic = None
    profile_pic_rects = [
        profile_pics[0].get_rect(center=(screen_width // 4, int(screen_height * 0.7))),
        profile_pics[1].get_rect(center=(3 * screen_width // 4, int(screen_height * 0.7)))
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_arrow_rect.collidepoint(mouse_pos):
                    return
                for i, rect in enumerate(profile_pic_rects):
                    if rect.collidepoint(mouse_pos):
                        selected_pic = i
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip() and selected_pic is not None:
                    show_popup("Pick a character to play as")
                    accounts.append({"name": name.strip(), "profile_pic": selected_pic})
                    save_accounts()
                    return
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isprintable():
                    name += event.unicode

        screen.blit(create_account_bg, (0, 0))
        instructions = instruction_font.render("Enter your name:", True, (255, 255, 255))
        name_text = button_font.render(name, True, (255, 255, 255))
        screen.blit(instructions, instructions.get_rect(center=(screen_width // 2, screen_height // 2.6)))
        screen.blit(name_text, name_text.get_rect(center=(screen_width // 2, int(screen_height * 0.44))))

        for i, pic in enumerate(profile_pics):
            screen.blit(pic, profile_pic_rects[i])
            if selected_pic == i:
                pygame.draw.rect(screen, (0, 255, 0), profile_pic_rects[i], 4)

        screen.blit(back_arrow_img, back_arrow_rect)
        pygame.display.flip()

# Function to handle choosing an account
def choose_account_screen():
    selected_account = None
    continue_button_rect = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_arrow_rect.collidepoint(mouse_pos):
                    return
                if continue_button_rect and continue_button_rect.collidepoint(mouse_pos):
                    if selected_account:  # Ensure an account is selected
                        game_mode_screen(selected_account)  # Navigate to the game mode screen
                        return
                y_offset = 150
                for account in accounts:
                    account_rect = pygame.Rect(100, y_offset, 200, 100)
                    if account_rect.collidepoint(mouse_pos):
                        selected_account = account
                        break
                    y_offset += 150

        screen.blit(choose_account_bg, (0, 0))

        y_offset = 150
        for account in accounts:
            name_text = button_font.render(account["name"], True, button_text_color)
            profile_pic = profile_pics[account["profile_pic"]]
            screen.blit(profile_pic, (100, y_offset))
            screen.blit(name_text, (250, y_offset + 30))
            if selected_account == account:
                pygame.draw.rect(screen, (0, 255, 0), (100, y_offset, 200, 100), 3)  # Highlight selected account
            y_offset += 150

        if selected_account:
            continue_button_text = button_font.render("Continue", True, button_text_color)
            continue_button_rect = continue_button_text.get_rect(center=(screen_width // 2, screen_height - 100))
            draw_textured_button(screen, continue_button_text, continue_button_rect, button_color, button_shadow_color)

        screen.blit(back_arrow_img, back_arrow_rect)
        pygame.display.flip()


def game_mode_screen(selected_account):
    go_to_class_button_rect = None
    mini_games_button_rect = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_accounts()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if go_to_class_button_rect and go_to_class_button_rect.collidepoint(mouse_pos):
                    # Go to class logic here
                    classroom_screen(selected_account)
                    return
                if mini_games_button_rect and mini_games_button_rect.collidepoint(mouse_pos):
                    # Mini-games logic here
                    level_selector_screen(selected_account)  # Navigate to the game mode screen
                    return

        # Draw the background
        screen.blit(game_mode_bg, (0, 0))

        # Display the "Choose Game Mode" text
        title_text = button_font.render("Choose Game Mode", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen_width // 2 + 30, 116))
        screen.blit(title_text, title_rect)

        # Draw the buttons
        go_to_class_text = button_font.render("Go To Class", True, button_text_color)
        mini_games_text = button_font.render("Mini-Games", True, button_text_color)

        go_to_class_button_rect = go_to_class_text.get_rect(center=(screen_width // 2 + 35, screen_height // 2 - 50))
        mini_games_button_rect = mini_games_text.get_rect(center=(screen_width // 2 + 35, screen_height // 2 + 50))

        draw_textured_button(screen, go_to_class_text, go_to_class_button_rect, button_color, button_shadow_color)
        draw_textured_button(screen, mini_games_text, mini_games_button_rect, button_color, button_shadow_color)

        pygame.display.flip()


# Game loop for the title screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_accounts()
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if start_button_rect.collidepoint(mouse_pos):
                start_learning_screen()

    screen.blit(title_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()
    draw_textured_button(screen, start_button_text, start_button_rect,
                         button_hover_color if start_button_rect.collidepoint(mouse_pos) else button_color,
                         button_shadow_color, hover=start_button_rect.collidepoint(mouse_pos), padding=20)
    draw_textured_button(screen, options_button_text, options_button_rect,
                         button_hover_color if options_button_rect.collidepoint(mouse_pos) else button_color,
                         button_shadow_color, hover=options_button_rect.collidepoint(mouse_pos), padding=20)
    pygame.display.flip()
