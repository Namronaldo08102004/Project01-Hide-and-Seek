<a id="readme-top"></a>

# Hide and Seek

This project is a simulation that replicates how a player (seeker) would move in order to catch the hiders around maps.

## Key Aspect
- **Difficulties:** Have an increasing difficulty where hiders have more potential to move around.
- **Comprehensive Experience:** A simple UI with Pygame allowing user to easily track how the seeker move around.
- **Score:** Score the run base on the number of steps the seeker took, which is use to evaluate the optimality.

## Implementing Algorithms
The backbone of the project was to base on the A* algorithm. Moreover, we introduced some optimization in choosing the path so that seeker and hiders both can play optimally.

- The trick is, the hider may choose to hide in the corner so we define the heuristic function as `h = d - 0.9 * isCorner` with d is the Manhattan distance.
- On the road, it will prioritize to touch the hider if observed.
- If it cannot find a certain hider, instead of giving up immediately, the seekd will start to move on the next objective (next hider).
- The seeker to choose the move based on the "Nash Theory" in Game Theory.

For more detail on the implementation, please read it in the [Report](DOCUMENT/Report.pdf).

## Levels
In our project, there are **4 levels of difficulties** introduced:
- *Level 1:* One stay-still hider.
- *Level 2:* Mulitple stay-still hiders.
- *Level 3:* Hiders can move around, fleeing from the seeker.
- *Level 4:* Hiders can move the obstacles before the game starts. (Not implemented)


## Contributors
Special thanks to the following contributors for their valuable work on this project:
- [Diep Gia Huy](https://github.com/22127475)
- [@Melios22](https://github.com/Melios22)
- [@Namronaldo08102004](https://github.com/Namronaldo08102004)
- [@buinguyenlanvy](https://github.com/buinguyenlanvy)




## Future Improvements
- Implement more complex algorithms for the seeker to choose more optimal path.
- Add more possibilities for the hiders.
- Integrate into a more seamless system.



## Support the Project
If you find this project useful, please consider giving it a **⭐ star** on GitHub!


<p align="right">
  <a href="#readme-top">⬆️ Back to top</a>
</p>

