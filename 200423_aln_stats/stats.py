### functions for comparing a pair of sequences and also computing statistics for sequences in alignments (sequence length, gap opening and gap number, mismatches, number of aligned sites)
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import re
#-------------------------------------------------------------------------------------------
# if you're counting gaps, should aligned sites stay the same or exclude 'Ns'
def compare_aln_seqs(sequence1, sequence2, gap_char = '-', amb_char = 'N', verbose = 0):
    """takes a pair of aligned sequences and a string indicating the gap character 
    and returns: a. the length of the alignment b. the number of aligned sites and c. the number of 
    mismatches between the two sequences
    
    parameters:
    ----------
    sequence1: str
        first sequence 
    sequence2: str
        second sequence
    gap_char: str
        character that specifies a gap in a sequence
    amb_chars: list
        ambigous characters in the sequence
    verbose: 0,1
        set to 1 for debugging output
        
    returns 
    -------
    tuple"""
    
    # confirming inputs are valid and expected 
    assert isinstance(sequence1, str) and isinstance(sequence2, str), 'one or both your sequences were not strings'
    assert len(sequence1) == len(sequence2), 'your input sequences were not the same length'
    assert isinstance(gap_char, str), 'your gap character was not a string'
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose must be 0 or 1'
    
    # to count number of aligned sites and mismatches
    site_match = 0
    aln_mismatch = 0
    aligned_sites = 0
    # loop over both sequences by index 
    for index in range(1, len(sequence1) + 1):
        seq1_char = sequence1[index - 1]
        seq2_char = sequence2[index - 1]
        if verbose == 1: 
            print('current alignment position: {}'.format(index))
            print('nucleotide pair to compare: {}, {}'.format(seq1_char, seq2_char))
            print('\n')
            
        # check if site pairs are non-gaps; if true, count as aligned site else do nothing
        # also, if site pairs are non-gaps and dissimilar, count as a mismatch
        if not gap_char in set([seq1_char, seq2_char]):
            aligned_sites +=1
        
        if seq1_char != seq2_char:
            if not amb_char in set([seq1_char, seq2_char]):
                aln_mismatch +=1
        else:
            site_match +=1
        
        if verbose == 1: 
            print('current aligned site count {}'.format(site_match))
            print('current mismatch counts: {}'.format(aln_mismatch))
            print('\n')

    return len(sequence1), aligned_sites, site_match,  aln_mismatch
#------------------------------------------------------------
def count_str_chars(str_var, strs_to_exclude = None, verbose = 0):
    """takes an input string and a list of strings and
    returns the length of the string, discounting
    the counts for any strings that appear in the list. 
    the function default counts all charaters
    
    parameters
    ----------
    str_var: str
        input string
    str_to_exclude: list
        list of charcaters to exclude when counting
    verbose: int, 0, 1
        set to 1 for debugging output 
    
    returns 
    -------
    int"""
       
    assert isinstance(str_var, str), 'your input string was not a string type. Got: {}'.format(type(str_var))
    assert isinstance(strs_to_exclude, list), 'your list of strings to exlude was not a list type. Got: {}'.format(type(strs_to_exclude))
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose must be 0 or 1'
    
    if not strs_to_exclude == None:
        assert set([type(i) == str for i in strs_to_exclude]) == {True}, 'one or more of your list of strings to exclude was not a string type'
    
    target_chars = [i for i in str_var if not i in strs_to_exclude]
    
    return len(target_chars)
#------------------------------------------------------------
def count_gap_block_in_sequence(sequence, gap_char = '-', verbose = 0):
    """takes an input sequence and and a gap character
    and returns the number of gap blocks in the sequence. 
    a gap block is an uninterrupted strech of gaps in the sequence
    
    paraneters
    ----------
    sequence: str
        input sequence
    gap_char: str
        character specifying a gap in the sequence
    verbose: int, 0, 1
        set to 1 for debugging output
        
    return 
    ------
    int"""
    
    # confirming inputs are valid and expected 
    
    assert isinstance(sequence, str),'your sequence was not a string'
    assert isinstance(gap_char, str), 'your gap character was not a string'
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose must be 0 or 1'
    
    pattern_to_catch = '{}+'.format(gap_char)
    extracted_pattern_matches = re.findall(pattern_to_catch, sequence)
    
    if verbose == 1: 
        print('pattern_to_match: {}'.format(pattern_to_catch))
        print('pattern matches: {}'.format(extracted_pattern_matches))
        print('number of matches = {}:'.format(len(extracted_pattern_matches)))
        
        
    return len(extracted_pattern_matches)
#------------------------------------------------------------
def count_aln_gaps(sequence, gap_char = '-'):
    """takes an input sequence and and a gap character
    and returns the number of gaps in the sequence. 
    
    paraneters
    ----------
    sequence: str
        input sequence
    gap_char: str
        character specifying a gap in the sequence
    verbose: int, 0, 1
        set to 1 for debugging output
        
    return 
    ------
    int"""
    
    # confirming inputs are valid and expected 
    assert isinstance(sequence, str), 'your sequence was not a string'
    assert isinstance(gap_char, str), 'your gap character was not a string'
   
    return sequence.count(gap_char)
#--------------------------------------------------------------
# note
# ----
# code test, expeected number of aligned blocks is gap openings + 1
def get_longest_aligned_blocks_between_aligned_seqs(seq1, seq2, gap_char = '-', verbose = 0):
    """takes two aligned sequences and returns the longest aligned 
    block between the two sequences the gap_char specifies the 
    gap character in the alignment. 
    
    parameters
    ----------
    seq1: str
        first sequence in the alignment
    seq2: str
        second sequence in the alignment
    gap_char: str
        character that specifies a gap character in the alignment
    verbose: 0,1
        set to 1 for debugging output 
        
    return 
    ------
    int"""
    
    assert isinstance(seq1, str), 'the first sequence was not a string type'
    assert isinstance(seq1, str), 'the second sequence  was not a string type'
    assert isinstance(gap_char, str), 'the gap character was not a string type'
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose can only 0 or 1'
    
    
    segments = []
    temp_str_pair = []
    
    # creates a sequence of paired tuples, the
    # tuples contain the nucleotides as the ith position 
    # of both sequences in the alignmend 
    paired_seq_nucs = list(zip(seq1,seq2))
    if verbose == 1: 
        print('paired tuple sequence of ith positions of sequence pair: {}'.format(paired_seq_nucs))
        
    # loops over the list of paired tuples
    # and appends the tuple to a temporary list, if a gap is encountered
    # in any of the tuples, temporary list is appended to another list then
    # emptied, note that the temporary list is consists of 1 aligned block. 
    for pair in paired_seq_nucs:
        
        # presence of a gap means the previous 
        if gap_char in pair: 
            segments.append(temp_str_pair)
            if verbose == 1: 
                print('aligned block to append: {}'.format(temp_str_pair))
                print('current aligned blocks: {}'.format(segments))
                
            temp_str_pair = []
            
        else:
            temp_str_pair.append(pair)
        
        
     
    segments.append(temp_str_pair)
    if verbose == 1: 
            print('current block list: {}'.format([i for i in segments if len(i) > 0]))
            print('current block total: {}'.format(len([i for i in segments if len(i) > 0])))
            
    if verbose == 1: 
        print('aligned blocks: {}'.format([i for i in segments if len(i) > 0]))
        print('aligned block lengths: {}'.format([len(i) for i in segments if len(i) > 0]))
        print('max aligned block length: {}'.format(max([len(i) for i in segments if len(i) > 0])))
        
    
    return max([len(i) for i in segments if len(i) > 0])
#------------------------------------------------------------