package dk.itu.mario.engine.level;

import java.util.Random;
import java.util.*;

//Make any new member variables and functions you deem necessary.
//Make new constructors if necessary
//You must implement mutate() and crossover()


public class MyDNA extends DNA
{
	
	public int numGenes = 0; //number of genes

	// Return a new DNA that differs from this one in a small way.
	// Do not change this DNA by side effect; copy it, change the copy, and return the copy.
	public MyDNA mutate ()
	{
		MyDNA copy = new MyDNA();
		//YOUR CODE GOES BELOW HERE
		String origChrome = this.getChromosome();
    	int index = (int) (Math.random() * origChrome.length());
    	char randChar = (char) ('a' + Math.random() * 26);
    	copy.setChromosome(origChrome.substring(0, index) + randChar + origChrome.substring(index + 1));

		//YOUR CODE GOES ABOVE HERE
		return copy;
	}
	
	// Do not change this DNA by side effect
	public ArrayList<MyDNA> crossover (MyDNA mate)
	{
		ArrayList<MyDNA> offspring = new ArrayList<MyDNA>();
		//YOUR CODE GOES BELOW HERE
		String currChrome = this.getChromosome();
		String currMate = mate.getChromosome();

		Random rand = new Random();
		int breakInt = rand.nextInt(currChrome.length());

		String dna1Chromosome = currChrome.substring(0, breakInt) + currMate.substring(breakInt);
		MyDNA dna1 = new MyDNA();
		dna1.setChromosome(dna1Chromosome);
		offspring.add(dna1);

		String dna2Chromosome = currMate.substring(0, breakInt) + currChrome.substring(breakInt);
		MyDNA dna2 = new MyDNA();
		dna2.setChromosome(dna2Chromosome);
		offspring.add(dna2);
		//YOUR CODE GOES ABOVE HERE
		return offspring;
	}
	
	// Optional, modify this function if you use a means of calculating fitness other than using the fitness member variable.
	// Return 0 if this object has the same fitness as other.
	// Return -1 if this object has lower fitness than other.
	// Return +1 if this objet has greater fitness than other.
	public int compareTo(MyDNA other)
	{
		int result = super.compareTo(other);
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return result;
	}
	
	
	// For debugging purposes (optional)
	public String toString ()
	{
		String s = super.toString();
		//YOUR CODE GOES BELOW HERE
		
		//YOUR CODE GOES ABOVE HERE
		return s;
	}
	
	public void setNumGenes (int n)
	{
		this.numGenes = n;
	}

}

