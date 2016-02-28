# Gradual Learning Algorithm for Harmonic Grammar

## Description
Implementation of the Gradual Learning Algorithm for Harmonic Grammar. Used to learn syllable types and model acquisition of syllable structure.

## Usage
Clone the repository
```
$ git clone git@github.com:connormcl/harmonic-grammar.git
```
Switch to the project directory
```
$ cd harmonic-grammar
```
Run the Python script
```
$ python HGlearn.py GRAMMAR DATA UNI ITER RATE
```
* UNI: 1 or 0
  * if 1 initial weights should be all 1s
  * if 0 initial weights should be 10 for markedness constraints and 1 for faithfulness constraints
* ITER - an integer specifying how many iterations to run
* RATE - a decimal specifying the learning rate

## More information
Completed as a part of **LING 227: Language and Computation** taught by  Claire Moore-Cantwell during Fall 2015

For more information on the Gradual Learning Algorithm, please visit http://web.stanford.edu/dept/linguistics/linginst/nsf-workshop/PaterHandout.pdf
