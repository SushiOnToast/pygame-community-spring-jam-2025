import pygame

def import_character_sprites(sheet, frame_width, frame_height):
    animations = {
        'down_idle': [], 'down': [],
        'up_idle': [], 'up': [],
        'left_idle': [], 'left': [],
        'right_idle': [], 'right': []
    }

    directions = ['down', 'up', 'left', 'right']

    for i, direction in enumerate(directions):
        for j in range(4):  # 1 idle + 3 move frames
            frame = sheet.subsurface(pygame.Rect(
                j * frame_width, i * frame_height, frame_width, frame_height))
            
            # Create a mask for the frame to detect non-transparent pixels
            mask = pygame.mask.from_surface(frame)
            
            # Get the bounding box of the non-transparent pixels
            bounding_box = mask.get_bounding_rects()[0]
            
            if bounding_box.width > 0 and bounding_box.height > 0:
                # Crop the surface based on the bounding box
                cropped_frame = frame.subsurface(bounding_box)
            else:
                # If the mask has no non-transparent pixels, use the original frame
                cropped_frame = frame

            # Append the cropped frame to the corresponding animation list
            if j == 0:
                animations[f"{direction}_idle"].append(cropped_frame)
            else:
                animations[f"{direction}"].append(cropped_frame)

    return animations
