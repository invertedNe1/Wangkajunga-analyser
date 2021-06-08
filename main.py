# hfst-lookup src/analyser-gt-desc.hfstol < ~/Desktop/test_w_words | cut -f2 > ~/Desktop/test_w_words_output
# hfst-lookup src/analyser-gt-desc.hfstol < /home/hoopdriver/PycharmProjects/Wangkajunga_analysis/text_files/forms | cut -f2 > /home/hoopdriver/PycharmProjects/Wangkajunga_analysis/text_files/forms_outputs
from os import path
import subprocess
import sys


def split_tags(gold_standard):
    split_gold_standard = gold_standard.split('+')
    if split_gold_standard[0].startswith('Directional'):  # the only kinds of prefixes are 'Directional'
        lemma = split_gold_standard[1]
    else:
        lemma = split_gold_standard[0]
    tag = None  # non-inflecting English and Creole words not given a tag in gold-standard
    tags = []  # store (form - lemma), for grouping multi-tag morphemes
    properly_split_gold_standard = []  # used for storing sorted tags
    if len(split_gold_standard) == 1:
        pass
    elif len(split_gold_standard) == 2:
        tag = split_gold_standard[1]
        tags = split_gold_standard[1:]
    elif len(split_gold_standard) > 2:
        if split_gold_standard[0].startswith('Directional'):
            tag = split_gold_standard[2]
        else:
            tag = split_gold_standard[1]
            tags = split_gold_standard[1:]
    length = len(tags)
    count = 0
    while count < length:
        if (length - count) > 3:
            temp_tag = tags[count] + tags[count + 1] + tags[count + 2] + tags[count + 3]
            if temp_tag in marker_list_no_plus:
                properly_split_gold_standard.append(temp_tag)
                count += 4
            else:
                temp_tag = tags[count] + tags[count + 1] + tags[count + 2]
                if temp_tag in marker_list_no_plus:
                    properly_split_gold_standard.append(temp_tag)
                    count += 3
                else:
                    temp_tag = tags[count] + tags[count + 1]
                    if temp_tag in marker_list_no_plus:
                        properly_split_gold_standard.append(temp_tag)
                        count += 2
                    else:
                        temp_tag = tags[count]
                        if temp_tag in marker_list_no_plus:
                            properly_split_gold_standard.append(temp_tag)
                            count += 1
                        else:  # error message, hopefully with some useful info
                            print("temp_tag: " + temp_tag + " not in marker_list... " + form + " " + gold_standard)
                            continue
        elif (length - count) > 2:
            temp_tag = tags[count] + tags[count + 1] + tags[count + 2]
            if temp_tag in marker_list_no_plus:
                properly_split_gold_standard.append(temp_tag)
                count += 3
            else:
                temp_tag = tags[count] + tags[count + 1]
                if temp_tag in marker_list_no_plus:
                    properly_split_gold_standard.append(temp_tag)
                    count += 2
                else:
                    temp_tag = tags[count]
                    if temp_tag in marker_list_no_plus:
                        properly_split_gold_standard.append(temp_tag)
                        count += 1
                    else:
                        print("temp_tag: " + temp_tag + " not in marker_list... " + form + " " + gold_standard)
                        continue
        elif (length - count) > 1:
            temp_tag = tags[count] + tags[count + 1]
            if temp_tag in marker_list_no_plus:
                properly_split_gold_standard.append(temp_tag)
                count += 2
            else:
                temp_tag = tags[count]
                if temp_tag in marker_list_no_plus:
                    properly_split_gold_standard.append(temp_tag)
                    count += 1
                else:
                    print("temp_tag: " + temp_tag + " not in marker_list... " + form + " " + gold_standard)
                    continue
        elif (length - count) == 1:
            temp_tag = tags[count]
            if temp_tag in marker_list_no_plus:
                properly_split_gold_standard.append(temp_tag)
                count += 1
            else:
                print("temp_tag: " + temp_tag + " not in marker_list... " + form + " " + gold_standard)
                continue

    # print(properly_split_gold_standard)
    return properly_split_gold_standard, lemma, tag


if __name__ == '__main__':
    word_entries = []
    temp_list_possible_markers = []  # rename when working
    marker_list_with_plus = ["N", "N+Sem/Temp", "N+Sem/Spat", "N+Prop+Sem/Mal", "N+Prop+Sem/Fem", "N+Prop+Sem/Plc", "N+Prop", "V", "V+IV", "V+TV", "CC", "Dem", "Pcle", "Interj", "Abs", "Erg", "Dat", "Abl", "Gen", "Loc", "Perl", "All", "Avoid", "Der/Hav", "Der/Thing", "Der/Priv", "Der/Int", "Der/Want", "Der/Asst", "Der/Temp", "Der/Dwell", "Der/Side", "Der/Type", "Der/Sim", "Der/Contr", "Der/Mod", "Der/Big", "Der/Anoth", "Der/Very", "Der/Num", "Der/Dual", "Der/Few", "Der/Pl", "Der/Grp", "Der/Pair", "Der/Only", "Der/Foc", "Der/SpatAbl", "Der/SpatAll", "Der/TempLoc", "Inch", "Redpl", "Grp", "Compl", "Warn", "Act", "Caus/Make", "Caus/PutTo", "Trel", "Pron/Clt+1Sg+Subj", "Pron/Clt+2Sg+Subj", "Pron/Clt+3Sg+Subj", "Pron/Clt+1Du+Incl+Subj", "Pron/Clt+1Du+Excl+Subj", "Pron/Clt+1Pl+Incl+Subj", "Pron/Clt+1Pl+Excl+Subj", "Pron/Clt+2Du+Subj", "Pron/Clt+2Pl+Subj", "Pron/Clt+3Du+Subj", "Pron/Clt+3Pl+Subj", "Pron/Clt+1Sg+Abs", "Pron/Clt+2Sg+Abs", "Pron/Clt+3Sg+Abs", "Pron/Clt+1Du+Incl+Abs", "Pron/Clt+1Du+Excl+Abs", "Pron/Clt+1Pl+Incl+Abs", "Pron/Clt+1Pl+Excl+Abs", "Pron/Clt+2Du+Abs", "Pron/Clt+2Pl+Abs", "Pron/Clt+3Du+Abs", "Pron/Clt+3Pl+Abs", "Pron/Clt+1Sg+Dat", "Pron/Clt+2Sg+Dat", "Pron/Clt+3Sg+Dat", "Pron/Clt+1Du+Incl+Dat", "Pron/Clt+1Du+Excl+Dat", "Pron/Clt+1Pl+Incl+Dat", "Pron/Clt+1Pl+Excl+Dat", "Pron/Clt+2Du+Dat", "Pron/Clt+2Pl+Dat", "Pron/Clt+3Du+Dat", "Pron/Clt+3Pl+Dat", "Pron/Clt+1Sg+Acs", "Pron/Clt+2Sg+Acs", "Pron/Clt+3Sg+Acs", "Pron/Clt+1Du+Incl+Acs", "Pron/Clt+1Du+Excl+Acs", "Pron/Clt+1Pl+Incl+Acs", "Pron/Clt+1Pl+Excl+Acs", "Pron/Clt+2Du+Acs", "Pron/Clt+2Pl+Acs", "Pron/Clt+3Du+Acs", "Pron/Clt+3Pl+Acs", "Pron/Clt+1Sg+Abl", "Pron/Clt+2Sg+Abl", "Pron/Clt+3Sg+Abl", "Pron/Clt+1Du+Incl+Abl", "Pron/Clt+1Du+Excl+Abl", "Pron/Clt+1Pl+Incl+Abl", "Pron/Clt+1Pl+Excl+Abl", "Pron/Clt+2Du+Abl", "Pron/Clt+2Pl+Abl", "Pron/Clt+3Du+Abl", "Pron/Clt+3Pl+Abl", "Pron/Clt+Refl", "Pa", "Clt/Foc", "Clt/Prob", "Clt/contrary_to_expectation", "Clt/really", "Clt/Cert", "Clt/Rep", "Clt/Dub", "Clt/Emph", "Clt/while", "Clt/when", "Clt/then", "Voc", "SentMod", "Dem/ngula", "Dem/pa", "Dem/na", "Dem/janu", "Dem/janulu", "Nomz", "Ser", "Prs", "Perf+Imprt", "Perf+PstNar", "Perf+Pst", "Perf+Fut", "Imperf", "Pst", "PstHbt", "Fut", "Imprt", "Irr", "Admon", "Avoid", "Oblig", "Hyp", "Char", "Int", "Unr", "Purp", "Contr", "Directional/away",
"Directional/around", "Directional/towards", "as.well", "u", "get.up", "Foc", "Pron+Interr", "Pron+Indef", "Pron+Pers", "?"]
    marker_list_no_plus = ["N", "NSem/Temp", "NSem/Spat", "NPropSem/Mal", "NPropSem/Fem", "NPropSem/Plc", "NProp", "V", "VIV", "VTV", "CC", "Dem", "Pcle", "Interj", "Abs", "Erg", "Dat", "Abl", "Gen", "Loc", "Perl", "All", "Avoid", "Der/Hav", "Der/Thing", "Der/Priv", "Der/Int", "Der/Want", "Der/Asst", "Der/Temp", "Der/Dwell", "Der/Side", "Der/Type", "Der/Sim", "Der/Contr", "Der/Mod", "Der/Big", "Der/Anoth", "Der/Very", "Der/Num", "Der/Dual", "Der/Few", "Der/Pl", "Der/Grp", "Der/Pair", "Der/Only", "Der/Foc", "Der/SpatAbl", "Der/SpatAll", "Der/TempLoc", "Inch", "Redpl", "Grp", "Compl", "Warn", "Act", "Caus/Make", "Caus/PutTo", "Trel", "Pron/Clt1SgSubj", "Pron/Clt2SgSubj", "Pron/Clt3SgSubj", "Pron/Clt1DuInclSubj", "Pron/Clt1DuExclSubj", "Pron/Clt1PlInclSubj", "Pron/Clt1PlExclSubj", "Pron/Clt2DuSubj", "Pron/Clt2PlSubj", "Pron/Clt3DuSubj", "Pron/Clt3PlSubj", "Pron/Clt1SgAbs", "Pron/Clt2SgAbs", "Pron/Clt3SgAbs", "Pron/Clt1DuInclAbs", "Pron/Clt1DuExclAbs", "Pron/Clt1PlInclAbs", "Pron/Clt1PlExclAbs", "Pron/Clt2DuAbs", "Pron/Clt2PlAbs", "Pron/Clt3DuAbs", "Pron/Clt3PlAbs", "Pron/Clt1SgDat", "Pron/Clt2SgDat", "Pron/Clt3SgDat", "Pron/Clt1DuInclDat", "Pron/Clt1DuExclDat", "Pron/Clt1PlInclDat", "Pron/Clt1PlExclDat", "Pron/Clt2DuDat", "Pron/Clt2PlDat", "Pron/Clt3DuDat", "Pron/Clt3PlDat", "Pron/Clt1SgAcs", "Pron/Clt2SgAcs", "Pron/Clt3SgAcs", "Pron/Clt1DuInclAcs", "Pron/Clt1DuExclAcs", "Pron/Clt1PlInclAcs", "Pron/Clt1PlExclAcs", "Pron/Clt2DuAcs", "Pron/Clt2PlAcs", "Pron/Clt3DuAcs", "Pron/Clt3PlAcs", "Pron/Clt1SgAbl", "Pron/Clt2SgAbl", "Pron/Clt3SgAbl", "Pron/Clt1DuInclAbl", "Pron/Clt1DuExclAbl", "Pron/Clt1PlInclAbl", "Pron/Clt1PlExclAbl", "Pron/Clt2DuAbl", "Pron/Clt2PlAbl", "Pron/Clt3DuAbl", "Pron/Clt3PlAbl", "Pron/CltRefl", "Pa", "Clt/Foc", "Clt/Prob", "Clt/contrary_to_expectation", "Clt/really", "Clt/Cert", "Clt/Rep", "Clt/Dub", "Clt/Emph", "Clt/while", "Clt/when", "Clt/then", "Voc", "SentMod", "Dem/ngula", "Dem/pa", "Dem/na", "Dem/janu", "Dem/janulu", "Nomz", "Ser", "Prs", "PerfImprt", "PerfPstNar", "PerfPst", "PerfFut", "Imperf", "Pst", "PstHbt", "Fut", "Imprt", "Irr", "Admon", "Avoid", "Oblig", "Hyp", "Char", "Int", "Unr", "Purp", "Contr", "Directional/away",
"Directional/around", "Directional/towards", "as.well", "u", "get.up", "Foc", "PronInterr", "PronIndef", "PronPers", "?"]
    f = open("text_files//texts_gold_standard", "r")
    # parse texts_gold_standard and add each word with some of its features to an array for storage
    for line in f:
        if line.startswith('*'):  # header for new text
            continue
        if line == '\n':
            line = f.readline()
            if line.startswith('*'):
                continue
            form = line.strip()
            line = f.readline()
            gold_standard = line.strip()

            properly_split_gold_standard, lemma, tag = split_tags(gold_standard)

            # for marker in split_gold_standard:
            #     if marker not in temp_list_possible_markers and not marker == lemma:
            #        temp_list_possible_markers.append(marker)

            num_markers = 0  # for many english words with no tags
            if len(properly_split_gold_standard) > 0:
                num_markers = len(properly_split_gold_standard) - 1  # remove tag from count
            line = f.readline()  # skip line that is ---
            line = f.readline()
            translation = line.strip()
            word_entries.append([form, lemma, tag, num_markers, properly_split_gold_standard, translation, gold_standard])
        else:
            pass
    # for marker in temp_list_possible_markers:
    #     print(marker)
    # print(len(temp_list_possible_markers))
    # print(marker for marker in temp_list_possible_markers)
    f.close()

    # print(len(word_entries))
    for item in word_entries:
        pass
    #      print(item[0])

    # write the form elements of word_entries to a new file "forms"
    g = open("text_files//forms", 'w')
    for item in word_entries:
        g.write(item[0] + '\n')
    g.close()

    # add outputs in file "forms_outputs" to new array
    h = open("text_files//forms_outputs", 'r')
    word_outputs = []
    word_output = []
    for line in h:
        if not line == '\n':
            word_output.append(line.strip())
        else:
            word_outputs.append(word_output)
            word_output = []
    word_outputs.append(word_output)  # add last array (last line in file is not empty)
    # for item in word_outputs:
    #     print(item)
    #     print(len(item))

    # analysis
    # initialise variables that will be used for statistics
    total = 0
    total_correct = 0
    total_overgeneration = 0
    total_overgeneration_correct = 0
    nouns_total = 0
    nouns_correct = 0
    nouns_overgeneration = 0
    nouns_overgeneration_correct = 0
    nouns_num_tags = 0
    verbs_total = 0
    verbs_correct = 0
    verbs_overgeneration = 0
    verbs_overgeneration_correct = 0
    verbs_num_tags = 0
    particles_total = 0
    particles_correct = 0
    particles_overgeneration = 0
    particles_overgeneration_correct = 0
    particles_num_tags = 0
    interjections_total = 0
    interjections_correct = 0
    interjections_overgeneration = 0
    interjections_overgeneration_correct = 0
    interjections_num_tags = 0
    conjunctions_total = 0
    conjunctions_correct = 0
    conjunctions_overgeneration = 0
    conjunctions_overgeneration_correct = 0
    conjunctions_num_tags = 0
    demonstratives_total = 0
    demonstratives_correct = 0
    demonstratives_overgeneration = 0
    demonstratives_overgeneration_correct = 0
    demonstratives_num_tags = 0
    pronouns_total = 0
    pronouns_correct = 0
    pronouns_overgeneration = 0
    pronouns_overgeneration_correct = 0
    pronouns_num_tags = 0
    eng_or_creole_total = 0
    eng_or_creole_correct = 0
    eng_or_creole_overgeneration = 0
    eng_or_creole_overgeneration_correct = 0
    incorrect_number_affixes = 0
    incorrect_number_correctly_guessed_affixes = 0
    incorrect_overgeneration_guessed_affixes = 0

    most_correct_form_matchable_count = 0
    new_list = []  # stores 'most_correct' forms for incorrect words
    for word, outputs in zip(word_entries, word_outputs):
        total += 1
        total_overgeneration += len(outputs)
        if word[2] == 'N':
            nouns_total += 1
            nouns_overgeneration += len(outputs)
            nouns_num_tags += word[3]
        elif word[2] == 'V':
            verbs_total += 1
            verbs_overgeneration += len(outputs)
            verbs_num_tags += word[3]
        elif word[2] == 'Pcle':
            particles_total += 1
            particles_overgeneration += len(outputs)
            particles_num_tags += word[3]
        elif word[2] == 'Interj':
            interjections_total += 1
            interjections_overgeneration += len(outputs)
            interjections_num_tags += word[3]
        elif word[2] == 'CC':
            conjunctions_total += 1
            conjunctions_overgeneration += len(outputs)
            conjunctions_num_tags += word[3]
        elif word[2] == 'Dem':
            demonstratives_total += 1
            demonstratives_overgeneration += len(outputs)
            demonstratives_num_tags += word[3]
        elif word[2] == 'Pron':
            pronouns_total += 1
            pronouns_overgeneration += len(outputs)
            pronouns_num_tags += word[3]
        elif word[2] is None:
            eng_or_creole_total += 1
            eng_or_creole_overgeneration += len(outputs)

        correct = False  # tracker to see if there is a matching form
        most_correct_output_so_far = None
        most_correct_num_correct_tags = 0
        most_correct_num_total_tags = 0
        total_tags = len(word[4])
        for output in outputs:
            split_output, lemma, tag = split_tags(output)
            correct_tags = 0
            total_output_tags = len(split_output)
            for tag in split_output:
                if tag in word[4]:
                    correct_tags += 1
            if correct_tags > most_correct_num_correct_tags:
                most_correct_num_correct_tags = correct_tags
                most_correct_output_so_far = output
                most_correct_num_total_tags = total_output_tags
            elif correct_tags == most_correct_num_correct_tags and total_output_tags < most_correct_num_total_tags:
                most_correct_num_correct_tags = correct_tags
                most_correct_output_so_far = output
                most_correct_num_total_tags = total_output_tags
            if output == word[6]:
                correct = True
                total_correct += 1
                total_overgeneration_correct += len(outputs)
                if word[2] == 'N':
                    nouns_correct += 1
                    nouns_overgeneration_correct += len(outputs)
                elif word[2] == 'V':
                    verbs_correct += 1
                    verbs_overgeneration_correct += len(outputs)
                elif word[2] == 'Pcle':
                    particles_correct += 1
                    particles_overgeneration_correct += len(outputs)
                elif word[2] == 'Interj':
                    interjections_correct += 1
                    interjections_overgeneration_correct += len(outputs)
                elif word[2] == 'CC':
                    conjunctions_correct += 1
                    conjunctions_overgeneration_correct += len(outputs)
                elif word[2] == 'Dem':
                    demonstratives_correct += 1
                    demonstratives_overgeneration_correct += len(outputs)
                elif word[2] == 'Pron':
                    pronouns_correct += 1
                    pronouns_overgeneration_correct += len(outputs)
                elif word[2] is None:
                    eng_or_creole_correct += 1
                    eng_or_creole_overgeneration_correct += len(outputs)
                continue
            else:
                pass
                # if word[2] == 'Dem':
                #     print("no matching forms for: " + word[0] + "\t" + word[6] + '\t' + output)
        if not correct and most_correct_num_correct_tags > 0:
            most_correct_form_matchable_count += 1
            incorrect_number_affixes += total_tags
            incorrect_number_correctly_guessed_affixes += most_correct_num_correct_tags
            incorrect_overgeneration_guessed_affixes += most_correct_num_total_tags
            print("no matching forms for: " + word[0] + '\t' + word[6])
    # # print analysis
    print('total: ' + str(total))
    print('total correct: ' + str(total_correct) + '\t' + '(' + str(round(total_correct/total*100, 2)) + '%)')
    print('total overgeneration avg: ' + str(round(total_overgeneration/total, 2)))
    print('total overgeneration correct avg: ' + str(round(total_overgeneration_correct/total_correct, 2)))
    print('nouns total: ' + str(nouns_total))
    print('nouns correct: ' + str(nouns_correct) + '\t' + '(' + str(round(nouns_correct/nouns_total*100, 2)) + '%)')
    print('nouns overgeneration avg: ' + str(round(nouns_overgeneration/nouns_total, 2)))
    print('nouns overgeneration correct avg: ' + str(round(nouns_overgeneration_correct/nouns_correct, 2)))
    print('nouns affixes avg: ' + '\t' + str(round(nouns_num_tags/nouns_total, 2)))
    print('verbs total: ' + str(verbs_total))
    print('verbs correct: ' + str(verbs_correct) + '\t' + '(' + str(round(verbs_correct/verbs_total*100, 2)) + '%)')
    print('verbs overgeneration avg: ' + str(round(verbs_overgeneration/verbs_total, 2)))
    print('verbs overgeneration correct avg: ' + str(round(verbs_overgeneration_correct/verbs_correct, 2)))
    print('verbs affixes avg: ' + '\t' + str(round(verbs_num_tags/verbs_total, 2)))
    print('particles total: ' + str(particles_total))
    print('particles correct: ' + str(particles_correct) + '\t' + '(' + str(round(particles_correct/particles_total*100, 2)) + '%)')
    print('particles overgeneration avg: ' + str(round(particles_overgeneration/particles_total, 2)))
    print('particles overgeneration correct avg: ' + str(round(particles_overgeneration_correct/particles_correct, 2)))
    print('particles affixes avg: ' + '\t' + str(round(particles_num_tags/particles_total, 2)))
    print('interjections total: ' + str(interjections_total))
    print('interjections correct: ' + str(interjections_correct) + '\t' + '(' + str(round(interjections_correct/interjections_total*100, 2)) + '%)')
    print('interjections overgeneration avg: ' + str(round(interjections_overgeneration/interjections_total, 2)))
    print('interjections overgeneration correct avg: ' + str(round(interjections_overgeneration_correct/interjections_correct, 2)))
    print('interjections affixes avg: ' + '\t' + str(round(interjections_num_tags/interjections_total, 2)))
    print('conjunctions total: ' + str(conjunctions_total))
    print('conjunctions correct: ' + str(conjunctions_correct) + '\t' + '(' + str(round(conjunctions_correct / conjunctions_total*100, 2)) + '%)')
    print('conjunctions overgeneration avg: ' + str(round(conjunctions_overgeneration/conjunctions_total, 2)))
    print('conjunctions overgeneration correct avg: ' + str(round(conjunctions_overgeneration_correct/ conjunctions_correct, 2)))
    print('conjunctions affixes avg: ' + '\t' + str(round(conjunctions_num_tags/conjunctions_total, 2)))
    print('demonstratives total: ' + str(demonstratives_total))
    print('demonstratives correct: ' + str(demonstratives_correct) + '\t' + '(' + str(round(demonstratives_correct/demonstratives_total*100, 2)) + '%)')
    print('demonstratives overgeneration avg: ' + str(round(demonstratives_overgeneration/demonstratives_total, 2)))
    print('demonstratives overgeneration correct avg: ' + str(round(demonstratives_overgeneration_correct/demonstratives_correct, 2)))
    print('demonstratives affixes avg: ' + '\t' + str(round(demonstratives_num_tags / demonstratives_total, 2)))
    print('pronouns total: ' + str(pronouns_total))
    print('pronouns correct: ' + str(pronouns_correct) + '\t' + '(' + str(round(pronouns_correct/pronouns_total*100, 2)) + '%)')
    print('pronouns overgeneration avg: ' + str(round(pronouns_overgeneration/demonstratives_total, 2)))
    print('pronouns overgeneration correct avg: ' + str(round(pronouns_overgeneration_correct/pronouns_correct, 2)))
    print('pronouns affixes avg: ' + '\t' + str(round(pronouns_num_tags / pronouns_total, 2)))
    print('eng or creole total: ' + str(eng_or_creole_total))
    print('eng or creole correct: ' + str(eng_or_creole_correct) + '\t' + '(' + str(round(eng_or_creole_correct/eng_or_creole_total*100, 2)) + '%)')
    print('eng or creole overgeneration: ' + str(round(eng_or_creole_overgeneration/eng_or_creole_total, 2)))
    print('eng or creole overgeneration correct: ' + str(round(eng_or_creole_overgeneration_correct/eng_or_creole_correct, 2)))
    print('percent correctly guessed affixes of most-correct incorrect form: ' + str(round(incorrect_number_correctly_guessed_affixes / incorrect_number_affixes*100, 2)))
    print('avg overgeneration of most-correct incorrect forms: ' + str(round(incorrect_overgeneration_guessed_affixes / incorrect_number_affixes*100, 2)))
    print('incorrect number correctly guessed affixes: ' + str(incorrect_number_correctly_guessed_affixes))
    print('incorrect number affixes: ' + str(incorrect_number_affixes))
    print('incorrect overgeneration guessed affixes: ' + str(incorrect_overgeneration_guessed_affixes))
    print('most correct matchable forms: ' + str(most_correct_form_matchable_count))