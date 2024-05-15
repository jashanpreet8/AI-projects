import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait
    """
    names = list(people.keys())
    for name in names:
        child = people[name]['name']
        mother = people[name]['mother']
        father = people[name]['father']

    if mother in one_gene:
        mother_gene = 1
    elif mother in two_genes:
        mother_gene = 2
    else:
        mother_gene = 0

    if father in one_gene:
        father_gene = 1
    elif mother in two_genes:
        father_gene = 2
    else:
        father_gene = 0


    if mother not in (one_gene, two_genes):
        prob_0_gene = PROBS['gene'][0]
        if mother in have_trait:
            trait_0_gene = PROBS['trait'][0][True]
            probability_0 = prob_0_gene*trait_0_gene
            return probability_0
        else:
            trait_0_gene = PROBS['trait'][0][False]
            probability_0 = prob_0_gene * trait_0_gene
            return probability_0

    if father not in (one_gene, two_genes):
        prob_0_gene = PROBS['gene'][0]
        if father in have_trait:
            trait_0_gene = PROBS['trait'][0][True]
            probability_0 = prob_0_gene * trait_0_gene
            return probability_0
        else:
            trait_0_gene = PROBS['trait'][0][False]
            probability_0 = prob_0_gene * trait_0_gene
            return probability_0

    for indi in one_gene:
        if indi == child:
            if mother_gene == 0 or father_gene == 0:
                prob_get0 = PROBS['mutation']
                prob_get1 = 1-PROBS['mutation']
                probability = prob_get0*prob_get0 + prob_get1*prob_get1
                if indi in have_trait:
                    trait_one_gene = PROBS['trait'][1][True]
                    probability_1 = probability * trait_one_gene
                    return probability_1
                else:
                    trait_one_gene = PROBS['traits'][1][False]
                    probability_1 = probability * trait_one_gene
                    return probability_1
            else:
                prob_get1 = PROBS['gene'][1]
                prob_get2 = PROBS['gene'][1]
                probability = prob_get1*prob_get1 + prob_get2*prob_get2
                if indi in have_trait:
                    trait_one_gene = PROBS['trait'][1][True]
                    probability_1 = probability * trait_one_gene
                    return probability_1
                else:
                    trait_one_gene = PROBS['traits'][1][False]
                    probability_1 = probability * trait_one_gene
                    return probability_1

        else:
            prob_one_gene = PROBS['gene'][1]
            if indi in have_trait:
                trait_one_gene = PROBS['trait'][1][True]
                probability_1 = prob_one_gene * trait_one_gene
                return probability_1
            else:
                trait_one_gene = PROBS['traits'][1][False]
                probability_1 = prob_one_gene * trait_one_gene
                return probability_1


    for indi in two_genes:
        if indi == child:
            if mother_gene == 0 or father_gene == 0:
                prob_get1 = PROBS['mutation']
                prob_get2 = 1-PROBS['mutation']
                probability = prob_get1*prob_get1 + prob_get2*prob_get2
                if indi in have_trait:
                    trait_two_gene = PROBS['trait'][2][True]
                    probability_2 = probability * trait_two_gene
                    return probability_2
                else:
                    trait_two_gene = PROBS['traits'][1][False]
                    probability_2 = probability * trait_two_gene
                    return probability_2
            else:
                prob_get1 = PROBS['gene'][1]
                prob_get2 = PROBS['gene'][1]
                probability = prob_get1*prob_get1 + prob_get2*prob_get2
                if indi in have_trait:
                    trait_two_gene = PROBS['trait'][2][True]
                    probability_2 = probability * trait_two_gene
                    return probability_2
                else:
                    trait_two_gene = PROBS['traits'][1][False]
                    probability_2 = probability * trait_two_gene
                    return probability_2
        else:
            prob_two_genes = PROBS['gene'][2]
            if indi in have_trait:
                trait_two_genes = PROBS['trait'][2][True]
                probability_2 = prob_two_genes * trait_two_genes
                return probability_2
            else:
                trait_two_genes = PROBS['traits'][2][False]
                probability_2 = prob_two_genes * trait_two_genes
                return probability_2


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    names = list(probabilities.keys())
    for name in names:
        if name in one_gene:
            probabilities[name]['gene'][1] += p
        elif name in two_genes:
            probabilities[name]['gene'][2] += p
        else:
            probabilities[name]['gene'][0] += p

        if name in have_trait:
            probabilities[name]["trait"][True] += p
        else:
            probabilities[name]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    names = list(probabilities.keys())
    for name in names:
        a = probabilities[name]["gene"][0]
        b = probabilities[name]["gene"][1]
        c = probabilities[name]["gene"][2]

        x = probabilities[name]["trait"][True]
        y = probabilities[name]["trait"][False]

        genes_sum = a+b+c
        probabilities[name]['gene'][0] = a/genes_sum
        probabilities[name]["gene"][1] = b/genes_sum
        probabilities[name]["gene"][2] = c/genes_sum

        traits_sum = x+y
        probabilities[name]["trait"][True] = x/traits_sum
        probabilities[name]["trait"][False] = y/traits_sum


if __name__ == "__main__":
    main()
