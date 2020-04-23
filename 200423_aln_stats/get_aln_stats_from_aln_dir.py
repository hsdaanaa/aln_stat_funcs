# aln_stats has functions

# Should raise warning when there are empty comparisons
# should avoid capitalizing sequences
#------------------------------------------------------------
import sys, os, re
import pandas as pd
from itertools import combinations
from utils import get_file_paths_from_dir, substring_delim, cds_to_dict, map_dict_vals
from stats import compare_aln_seqs, count_gap_block_in_sequence, count_aln_gaps, count_str_chars, get_longest_aligned_blocks_between_aligned_seqs
#------------------------------------------------------------
def get_aln_stats_from_path(path_to_aln, gap_char = '-', amb_char = 'N', verbose = 0):
    """takes an input path to an FASTA-formatted alignment of a pair of sequences
    and returns a list containing the names of the alignment file,  
    samples names, and alignment statistics.
    statistics are: 
        - length of the alignment
        - number of aligned sites
        - sequence length of sequence 1 and 2
        - number of mismatches between sequence 1 and 2
        - number of gap blocks (an uninterrupted stretch of gaps)
        - number of gaps
    
    parameters
    ----------
    path_to_aln: str
        path to the input alignment file
    gap_char: str
        character specifying a gap in the sequence    
    verbose: int, 0 or 1
        set to 1 for debugging output
        
    returns
    -------
    list"""
    
    assert os.path.isfile(path_to_aln) == True, 'your input path was not a valid path'
    assert isinstance(gap_char, str), 'your gap character was not a string'
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose must be 0 or 1'
   
    pairwise_comparisons = []
    # reads the alignment into a dictionary, sample names are mapped to sample sequences
    # converts the dictionary into a dataframe
    aln_dict = cds_to_dict(path_to_aln, delim2 = 'lastpos') 
    cds = map_dict_vals(aln_dict, str.upper) # capitalizes sequence characters

    # get combinations 
    sample_pairs = list(combinations(aln_dict.keys(), 2))
    
    for pair in sample_pairs: 
        # extracts the names and sequences of first and second samples 
        id1 = pair[0]
        id2 = pair[1]
        seq1 = aln_dict[id1]
        seq2 = aln_dict[id2]
        if verbose == 1:
            print('current ids: {}, {}'.format(id1, id2))
            print('current seqs: {}, {}'.format(seq1, seq2))

        # extract statistics: alignment length, number of aligned sites and number of mismatches
        aln_len, aln_site_num, site_match, mismatch_num = compare_aln_seqs(seq1, seq2, gap_char = gap_char)
        longest_aln_block = get_longest_aligned_blocks_between_aligned_seqs(seq1, seq2, gap_char = gap_char)
        
        # listing for pair
        pairwise_comparisons.append([os.path.basename(path_to_aln),id1, id2, aln_len,
            aln_site_num, count_str_chars(seq1, [gap_char]), count_str_chars(seq2, [gap_char]), count_str_chars(seq1, [gap_char, amb_char]), count_str_chars(seq2, [gap_char, amb_char]),
         site_match, mismatch_num, longest_aln_block, count_gap_block_in_sequence(seq1, gap_char), count_gap_block_in_sequence(seq2, gap_char),
        count_aln_gaps(seq1, gap_char), count_aln_gaps(seq2, gap_char)])
    
    # outputs list in order described in description
    return pairwise_comparisons
#---------------------------------------------------------------------------------
def get_aln_stats_from_aln_dir(aln_dir_path, gap_char = '-', amb_char = 'N', aln_suffix = '.aln', verbose = 0):
    """takes an path to a directory and a tring that specifies 
    a suffixes of alignment files in the directory. returns a table
    containing the names of each alignment file, its sample names
    and alignment statistics.
    
    parameters 
    ----------
    aln_dir_path: str
        path to an directory containing fasta-formatted alignments
    aln_suffix: str
        a string that specifies the file extension name of each alignment file
    gap_char: str
        character specifying a gap in the sequence    
    verbose: int, 0 or 1
        set to 1 for debugging output
    
    
    returns 
    -------
    pandas.DataFrame"""
    
    assert isinstance(aln_dir_path, str) == True, 'your alignment directory was not a string'
    assert isinstance(aln_suffix, str) == True, 'your input for aln_suffix was not a string'
    assert os.path.isdir(aln_dir_path) == True, 'your input path was not a valid path'
    assert isinstance(gap_char, str), 'your gap character was not a string'
    assert isinstance(verbose, int), 'your input for verbose was not an integer'
    assert verbose in [0,1], 'your input for verbose must be 0 or 1'

    alns = []
    
    aln_paths = get_file_paths_from_dir(aln_dir_path, ext = [aln_suffix])
    
    if verbose == 1: 
        pass
    
    # loop over alignment paths
    # compute statistics and append to a list
    for path in aln_paths:
        alns.append(pd.DataFrame(get_aln_stats_from_path(path, gap_char = gap_char)))

    #return alns
    # convert list of aln statistics into a table
    alns = pd.concat(alns)
    alns.index = range(1, len(alns) + 1)
    alns.columns = ['aln_name', 'sp1_ID', 'sp2_ID', 'aln_len', 'aln_sites', 'sp1_seqlen_w_N', 'sp2_seqlen_w_N','sp1_seqlen_wo_N', 'sp2_seqlen_wo_N', 'matches', 'mismatches', 'longest_aligned_block',
                        'sp1_gap_blocks', 'sp2_gap_blocks', 'sp1_gaps', 'sp2_gaps']
    
    #alns['sp1_5p_exon_endpos'] = alns['sp1_ID'].apply(lambda x: x.split(':')[1])
    #alns['sp2_5p_exon_endpos'] = alns['sp2_ID'].apply(lambda x: x.split(':')[1])

    #alns['sp1_ID'] = alns['sp1_ID'].apply(lambda x: x.split(':')[0])
    #alns['sp2_ID'] = alns['sp2_ID'].apply(lambda x: x.split(':')[0])

    return alns.loc[:, ['aln_name', 'sp1_ID', 'sp2_ID', 'aln_len', 'aln_sites', 'sp1_seqlen_w_N', 'sp2_seqlen_w_N','sp1_seqlen_wo_N', 'sp2_seqlen_wo_N', 'matches',
           'mismatches', 'longest_aligned_block', 'sp1_gap_blocks', 'sp2_gap_blocks', 'sp1_gaps',
           'sp2_gaps']]