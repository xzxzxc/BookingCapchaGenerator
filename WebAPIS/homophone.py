# The code snippet bellow taken from https://github.com/ecthros/uncaptcha
#
# Apply both layers of phonetic mapping
# More complex mapping, where homophones and near-homophones are used in conjunction
# Heigher weights are given to words that are phonetically close to a digit


def text_to_num(num):
    num = num.strip()

    digits = list()
    ########## SECOND LAYER MAPPING ##########
    # These match correspond to near homophone matches
    if num in ["one", "1", "juan", "Warren", "fun", "who won"]:
        digits.append(1)
    if num in ["to", "two", "too", "2", "who", "true", "do", "so", "you", "hello", "lou"] or num.endswith("ew") or num.endswith("do"):
        digits.append(2)
    if num in ["during", "three", "3", "tree", "free", "siri", "very", "be", "wes", "we", "really", "hurry"] or "ee" in num:
        digits.append(3)
    if num in ["four", "for", "fourth", "4", "oar", "or", "more", "porn"] or "oor" in num:
        digits.append(4)
    if num in ["five", "5", "hive", "fight", "fifth", "why", "find"] or "ive" in num:
        digits.append(5)
    if num in ["six", "6", "sex", "big", "sic", "set", "dicks", "it", "thank"] or num.endswith("icks") or num.endswith("ick") or num.endswith("inks") or num.endswith("ex"):
        digits.append(6)
    if num in ["get in", "seven", "7", "heaven", "Frozen", "Allen", "send","weather", "that in", "ten"] or "ven" in num:
        digits.append(7)
    if num in ["eight hundred", "o. k.", "eight", "8", "hate", "fate", "hey", "it", "they", "a", "A", "they have", "then"] or "ate" in num:
        digits.append(8)
    if num in ["yeah I", "no", "nine", "i'm", "9", "mine", "brian", "now i", "no i", "no I", "during", "now I", "no", "night", "eyes", "none", "non", "bind", "nice", "no i'm"] or "ine" in num:
        digits.append(9)
    if num in ["a hero", "the euro", "the hero", "Europe", "yeah well", "the o.", "hey oh", "zero", "hero", "0", "yeah","here", "well", "yeah well", "euro", "yo", "hello", "arrow", "Arrow", "they don't", "girl", "bill", "you know"] or "ero" in num:
        digits.append(0)
    if num in ["hi", "i", "I", "bye", "by", "buy"]:
        digits.append(5)
        digits.append(9)
    # Combine the output of the filters
    res = f'<{" or ".join([str(x) for x in digits])}>'
    if not digits:
        return num
    else:
        return res
