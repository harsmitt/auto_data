from .utils import get_alpha

synonym_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'

match_com= '[A-Za-z0-9. - ]*%s[ ,A-Za-z0-9.-]*$'

# d_keywords =['less','deduction','depreciation','amortization','impairment']
#todo need to add and operator between consolidted and balance sheets

check_1 = '[ (A-Za-z0-9. - )]*consolidated*[ (A-Za-z0-9. - )$]'

check_2 = '[ (A-Za-z0-9. - )]*%s*[ (A-Za-z0-9. - )$]'


similar_keyword_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
extended_key = '%s[ ,A-Za-z0-9.-]*$'

equity_key_list =list(map(lambda x: get_alpha(x), ['shareholders-equity', 'stockholders-equity',"stockholders' equity","shareholders' equity"]))

pnl1 = '[ (A-Za-z0-9. - )]*consolidated statement*[ (A-Za-z0-9. - )$]'
pnl2 = '[ (A-Za-z0-9. - )]income|operation|comprehensive loss*[ (A-Za-z0-9. - )$]'
notes_re1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
notes_re2 = '%s[ ,A-Za-z0-9.-]*$'

