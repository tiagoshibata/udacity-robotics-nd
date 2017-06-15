from vision import Vision
import transform

vision = Vision()


def perception_step(Rover):
    # 1) Define source and destination points for perspective transform
    # 2) Apply perspective transform
    # 3) Apply color threshold to identify navigable terrain/obstacles/rock samples
    # 4) Update Rover.vision_image (this will be displayed on left side of screen)
    # Example: Rover.vision_image[:,:,0] = obstacle color-thresholded binary image
    #          Rover.vision_image[:,:,1] = rock_sample color-thresholded binary image
    #          Rover.vision_image[:,:,2] = navigable terrain color-thresholded binary image
    obstacles, rocks, navigable = vision.process(Rover.img)
    Rover.vision_image[:, :, 0] = 255 * obstacles
    Rover.vision_image[:, :, 1] = 255 * rocks
    Rover.vision_image[:, :, 2] = 255 * navigable

    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates
    # 7) Update Rover worldmap (to be displayed on right side of screen)
    # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
    #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
    #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    rover_navigable = transform.image_to_rover(navigable)
    world_navigable_x, world_navigable_y = transform.to_world(*rover_navigable, *Rover.pos, Rover.yaw, 200, 10)
    Rover.worldmap[world_navigable_x, world_navigable_y, 2] += 1

    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
    # Rover.nav_dists = rover_centric_pixel_distances
    # Rover.nav_angles = rover_centric_angles
    dist, angles = transform.to_polar_coords(*rover_navigable)
    Rover.nav_dists = dist
    Rover.nav_angles = angles
    return Rover
