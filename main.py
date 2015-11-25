import os
import sys
import pygame
from buffalo import utils
import menu
import profile_creation
import profile_selection

def main():
    while not utils.end:
        utils.scene.logic()
        utils.scene.update()
        utils.scene.render()
        utils.delta = utils.clock.tick( utils.FRAMES_PER_SECOND )

if __name__ == "__main__":
    if not utils.init(caption="Simple Kingdom Simulator", fullscreen=True,):
        print("Buffalo failed to initialize")
        pygame.quit()
        sys.exit()

    profiles = next(os.walk("profiles"))[2]
    if len(profiles) == 0:
        # Go to the profile creation Scene
        utils.set_scene(profile_creation.Profile_Creation())
    elif len(profiles) == 1:
        # Load the only profile and go straight to the main menu
        utils.set_scene(menu.Menu(profiles[0], load=True))
    elif len(profiles) > 1:
        # Go to the profile selection Scene
        utils.set_scene(profile_selection.Profile_Selection())
    main()
    pygame.quit()
