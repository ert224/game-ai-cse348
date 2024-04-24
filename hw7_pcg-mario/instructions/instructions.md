# PCG - Mario

## Mario Level Generation

Procedural content generation is the use of algorithms (procedures) to create novel, and sometimes customized, game content from scratch.
Examples of PCG include generation of levels, maps, tree, cityscapes, weapons, monsters, and quests.
PCG is often used as a design-time tool to roughly sketch out level content to be refined by human designers.
PCG can also be done at run-time to incorporate individual player differences such as skills or preferences.

In this project, we look at run-time PCG to create Mario Bros. game levels customized to individual players’ play styles.
This includes
* learning a model of the player’s play style, and
* using the model to create a custom level.
Fortunately, the first part is already done for you.
You must focus on designing and implementing algorithms that use the player information to create something that will evaluate well.

This project will be using the [2011 IEEE Super Mario Bros. Competition infrastructure (Level Generation Track)](http://www.marioai.org/LevelGeneration).
Unfortunately, the original website is no longer available -- [an internet archive version of the site is here](http://www.marioai.org/LevelGeneration).
The description of the competition and some documentation can be found there.
Note that (from <https://groups.google.com/g/mariocompetition/c/V2W1g-sTAos>)...
> Nintendo owns the rights to the Mario trademark and all of the graphics and does not endorse this framework

![An example mario level](mariolevel.png)

You will write a procedural content generator in the provided Mario Bros. game engine that optimizes level content for different types of players such as those who like to jump, like to collect coins, or like to kill enemies.
You will implement a genetic algorithm to tune the layout of the Mario Bros. level.

### A note on history
The Mario level generation competition is no more.
* A version of [Togelius' original page on the competition is still available](http://julian.togelius.com/mariocompetition2009/)
* In 2019, the Mario AI framework was updated by Ahmed Khalifa and is available on [their github page](https://github.com/amidos2006/Mario-AI-Framework).
    * "Yes, it's true, the Mario AI framework has been around for ten years, and keep being used. For most of its existence, different versions of the framework have supported different functionality, e.g. Robin Baumgarten's A* agent has not easily worked with the same code as the various level generators. This new version finally brings all of this functionality into the same code base, and also adds various bug fixes and a graphical retroification. Gameplay remains the same.
    * "This version of the framework was created by Ahmed Khalifa, based on the original Mario AI Framework by Sergey Karakovskiy, Noor Shaker, and Julian Togelius, which in turn was based on Infinite Mario Bros by Markus Persson. (Or perhaps it came from space.)"
* From ["The VGLC: The Video Game Level Corpus" by Adam James Summerville, Sam Snodgrass, Michael Mateas, Santiago Ontañón](http://arxiv.org/abs/1606.07487)
    * "Levels are a key component of many different video games, and a large body of work has been produced on how to procedurally generate game levels. Recently, Machine Learning techniques have been applied to video game level generation towards the purpose of automatically generating levels that have the properties of the training corpus. Towards that end we have made available a corpora of video game levels in an easy to parse format ideal for different machine learning and other game AI research purposes. "
    * <https://github.com/TheVGLC/TheVGLC>

<hr />

## What you need to know
The Mario Bros. engine is written in Java.
You will find the source code in the src/ directory.

You will modify `MyLevel.java`, `MyDNA.java`, and `MyLevelGenerator.java` to implement a genetic algorithm in order to satisfy a variety of "player profiles".
Each player profile is an evaluation function focused on a specific type of potential player.
You are provided with four player profiles: 
* **Scrooge**: loves coins
* **Jumper**: loves jumping
* **Killer**: loves having to kill enemies
* **CloudClimber**: loves to be high in the sky
* **KillerCollector**: loves killing enemies and collecting coins

Each evaluation function for each player profile returns a value between 0-1 (inclusive) to demonstrate how much that player profile "likes" a given level. 

### dk.itu.mario.engine.level.DNA:

This object contains the chromosome representation used by the genetic algorithm.
It represents an individual in the population.
This is an abstract base class for MyDNA.

Member variables:
* `chromosome`: the default string representation for the DNA.
* `fitness`: the fitness of the individual represented by this DNA.
* `length`: the length of the level to be generated from this DNA. Not used.

Member functions:
* `getGenotype()`: return the genotype string.
* `setGenotype(string)`: set the genotype string.
* `getFitness()`: return the fitness.
* `setFitness(double)`: set the fitness.
* `setLength(int)`: set the level length.
* `getLength()`: return the level length.
* `compareTo(DNA)`: Used by Collections.sort().
    * Return 0 if this object has the same fitness as the argument passed in.
    * Return -1 if this object has lower fitness than the argument passed in.
    * Return +1 if this object has greater fitness than the argument passed in.


### dk.itu.mario.engine.level.MyDNA:

This is a specific version of DNA that will be used for your Mario level generation implementation.
You must complete this class.
You may choose to use the default string-based representation or add new member variables and functions as necessary.

Member functions:
* `mutate()`: Return a copy of this DNA object that has been changed in some small way.
    * Do not change the MyDNA object by side-effect.
    * You should make a copy of the current object, make a change to the copy, and return the copy.
    * **You will complete this function.**
* `crossover(mate)`: Cross this MyDNA object with another MyDNA object passed in.
    * Return one or more children.
    * **You will complete this function.**
* `toString()`: convert this object into a string.
    * By default, this returns the genotype string.
    * However, for debugging purposes you may want to modify this function.
    * **Modifying this function is optional.**
* `compareTo(DNA)`: Used by Collections.sort().
    * Return 0 if this object has the same fitness as the argument passed in.
    * Return -1 if this object has lower fitness than the argument passed in.
    * Return +1 if this object has greater fitness than the argument passed in.
    * **Modifying this function is optional**; it only needs to be modified if MyDNA uses some means of computing fitness other than storing it in the fitness member variable inherited from DNA.


### dk.itu.mario.engine.level.MyLevel:

This object places the blocks of the level.
It converts a MyDNA object into a structure that can be rendered.
In genetic algorithm terms, MyDNA is the genotype and MyLevel is the phenotype, the organisms that manifests when the chromosome is activated.

* `create(dna, type)`: Converts the MyDNA into a level. 
    * **You will complete this function.**
* `setBlock(x,y,byte-block-value)`: Sets the value of the current x,y value with a constant value determining the block type.
    * You can see a list of all of these values in `Level.java` and see examples of this function being called in `MyLevelGenerator.java`
* `setSpriteTemplate(x,y,SpriteTemplate)`: Sets an enemy of the passed in SpriteTemplate class to the `x,y` position.
    * You can see a list of all enemy types in `Enemy.java` and see an example of this function being called in `MyLevelGenerator.java`

In addition, **this class contains a number of extra functions that show examples of how to create complicated level structures**. 

### dk.itu.mario.engine.level.generator.MyLevelGenerator:

This class implements the genetic algorithm.
The basic structure of the genetic algorithm is given, but the details remain to be completed.

* `generateLevel(playerProfile)`: Called by the underlying game engine.
    * Passes in the playerProfile, which contains the fitness evaluation function.
    * This function calls the genetic algorithm and then hands the solution off to MyLevel to create the phenotype level.
* `geneticAlgorithm(playerProfile)`: Genetic algorithm implementation.
    * The playerProfile is the fitness function.
    * This function does not need to be modified, but it relies on a number of functions that must be customized.

See below instructions for the functions in `MyLevelGenerator` that need to be completed.

<hr />

## Instructions
You must implement a genetic algorithm that produces level content that is "liked" by different player profiles as given by the three evaluation functions, `Scrooge`, `Killer`, and `Jumper`.

**Step 1**: Acquire and install [Apache Ant](http://ant.apache.org/).

**Step 2**: In your directory for this homework, build the game engine:

```
> ant
```

**Step 3**: Modify the following files: 
* `/src/dk/itu/mario/engine/level/MyDNA.java`,
* `/src/dk/itu/mario/engine/level/MyLevel.java`, and
* `/src/dk/itu/mario/engine/level/generator/MyLevelGenerator.java`.

Complete the following functions:

`MyDNA`:
* `crossover()`: This function should return one or more new children from combining the object the function is called on and the object passed in.
* `mutate()`: This function should return a single MyDNA instance, which is a copy of the object the function is called on. This copy is randomly modified in some small way and the original should not be modified by side-effect.
* `toString()`: optional (for debugging purposes). The default is to return the default chromosome string, but if the MyDNA implementation is more complex, this will need to be altered to provide useful information.

You can create new member variables and functions as necessary to give the genotype representation the complexity needed to represent Super Mario Bros. levels.
At a minimum, you will want to define a string symbol language that represents level elements that can be produced by MyLevel.

`MyLevel`:
* `create(dna, type)`: This function should take a MyDNA object and translate the genotype into playable level through the use of `setBlock()` calls. That is, it should read the `MyDNA` genotype representation and create the phenotype.

If the genotype uses a default chromosome string, then `create()` *parses* the string and translates elements in the string into `setBlock()` calls.
You may make any new member functions or member variables necessary.

`MyLevelGenerator`:
* `getPopulationSize()`: returns a number, the maximum population size. This function needs only set the return value.
* `numberOfCrossovers()`: returns a number, the number of times crossover will occur per iteration. This function needs only set the return value.
* `terminate()`: Return true if the search is complete. The population and the number of iterations is passed in.
* `generateRandomIndividual()`: Create a new individual with random configuration. 
* `selectIndividualsForMutation()`: given a population, select and return an ArrayList of individuals that will undergo mutation.
* `pickIndividualForCrossover()`: given a population, pick a single individual that will undergo crossover. The excludeMe parameter is an individual that should NOT be picked (this prevents the same individual from being picked twice).
* `competeWithParentsOnly()`: return true if the population will be reduced by competing children against parents (i.e., use `competeWithParents()`). Return false if the population will be reduced by competing all individuals against all other individuals (i.e., use `globalCompetition()`).
* `competeWithParents()`: return a population of the proper size by testing whether each child is more fit than its parents. The original population, the population after mutations and crossover, and a hash that gives the parents of each individual.
* `globalCompetition()`: returns a population of the proper size by selecting the most fit individuals from the old population and the new population.
* `evaluateFitness()`: optional, can use this as is or make any changes necessary.
* `postProcess()`: optional, use this to perform any additional processes on the final solution DNA.


**Step 4**: Run your level generator from the homework directory: 

To run the codebase, you must first compile any changes you've made with the command `ant` in the parent directory.
Then, if the code compiled correctly, you can run the game by calling (with "<Profile_Name>" replaced appropriately): 

```
> java -cp bin dk.itu.mario.engine.PlayCustomized <Profile_Name>;
```

With the five player profiles you have access to, for example:

```
> java -cp bin dk.itu.mario.engine.PlayCustomized Scrooge
> java -cp bin dk.itu.mario.engine.PlayCustomized Jumper
> java -cp bin dk.itu.mario.engine.PlayCustomized Killer
> java -cp bin dk.itu.mario.engine.PlayCustomized CloudClimber
> java -cp bin dk.itu.mario.engine.PlayCustomized KillerCollector
```

When you run the application, an image (`output_image.png`) will be generated in the parent directory which shows the entire generated level. 
It will also drop a Java GUI window which allows you to play through the level using the `arrow keys`, `a` to run, and `space bar` to jump.

If you die 3 times, Mario will respawn at the top of the screen and fly, allowing you to see the entire level.

<hr />

## Grading
Submissions will be graded as follows:

* **6 points**: your code generates levels that score > 0.8 for 4 test player profiles (Scrooge, Killer, CloudClimber, Jumper) and 2 additional "hybrid" player profiles that are not provided (1 point per player profile, with the average score from 5 levels)
* **3 points**: all of the generated levels should be playable (0.1 for each level generated). Playability will be evaluated by an A* agent that can play a perfect game.
* **1 point**: create levels that do not violate any Mario conventions. Power blocks should all be accessible, no "floating" blocks or enemies, and no broken pipes.

<hr />

## Hints
Make sure that `MyLevel.create()` is linear time, or close to it.
It will need to be called to turn a genotype into phenotype every time an individual is created (via mutation or crossover) and evaluated.

You may wish to create member variables in `MyGenerateLevel` to keep track of the global fitness of the population and how it has changed over time.
You can use this to terminate the search if the search is approaching an asymptote or if the global fitness (or max fitness) hasn't changed in a while.

<hr />

## Submission

To submit your solution, upload your modified `MyDNA.java`, `MyLevel.java`, and `MyLevelGenerator.java`.

DO NOT upload the entire game engine.