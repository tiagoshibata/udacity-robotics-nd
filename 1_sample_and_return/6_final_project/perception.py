from vision import Vision
import transform

vision = Vision()


def perception_step(Rover):
    obstacle, rock, navigable = vision.process(Rover.img)
    Rover.vision_image[:, :, 0] = 255 * obstacle
    Rover.vision_image[:, :, 1] = 255 * rock
    Rover.vision_image[:, :, 2] = 255 * navigable

    # 5) Convert map image pixel values to rover-centric coords
    # 6) Convert rover-centric pixel values to world coordinates
    # 7) Update Rover worldmap (to be displayed on right side of screen)
    # Example: Rover.worldmap[obstacle_y_world, obstacle_x_world, 0] += 1
    #          Rover.worldmap[rock_y_world, rock_x_world, 1] += 1
    #          Rover.worldmap[navigable_y_world, navigable_x_world, 2] += 1
    rover_navigable = transform.image_to_rover(navigable)
    if (Rover.pitch > 356 or Rover.pitch < 4) and (Rover.roll > 356 or Rover.roll < 4):
        world_navigable_x, world_navigable_y = transform.to_world(*rover_navigable, *Rover.pos, Rover.yaw, 200, 10)
        Rover.worldmap[world_navigable_y, world_navigable_x, 2] += 10

        rover_obstacle = transform.image_to_rover(obstacle)
        world_obstacle_x, world_obstacle_y = transform.to_world(*rover_obstacle, *Rover.pos, Rover.yaw, 200, 10)
        Rover.worldmap[world_obstacle_y, world_obstacle_x, 0] += 1
        Rover.worldmap[world_obstacle_y, world_obstacle_x, 2] -= 0.5

    # 8) Convert rover-centric pixel positions to polar coordinates
    # Update Rover pixel distances and angles
    # Rover.nav_dists = rover_centric_pixel_distances
    # Rover.nav_angles = rover_centric_angles
    dist, angles = transform.to_polar_coords(*rover_navigable)
    Rover.nav_dists = dist
    Rover.nav_angles = angles
    return Rover
