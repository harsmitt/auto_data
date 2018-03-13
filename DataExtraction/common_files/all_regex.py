from .utils import get_alpha

synonym_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'

match_com= '[A-Za-z0-9. - ]*%s[ ,A-Za-z0-9.-]*$'

d_keywords =['less','deduction','depreciation','amortization','impairment']

balance_sheet = '[ (A-Za-z0-9. - )]*consolidated balance (sheets|sheet) *[ (A-Za-z0-9. - )$]'



similar_keyword_re = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
extended_key = '% s[ ,A-Za-z0-9.-]*$'

equity_key_list =list(map(lambda x: get_alpha(x), ['shareholders-equity', 'stockholders-equity',"stockholders' equity","shareholders' equity"]))

pnl1 = '[ (A-Za-z0-9. - )]statements of *[ (A-Za-z0-9. - )$]'
pnl2 = '[ (A-Za-z0-9. - )]income|operation|opreations*[ (A-Za-z0-9. - )$]'
notes_re1 = '[A-Za-z0-9. - ]* %s[ ,A-Za-z0-9.-]*$'
notes_re2 = '%s[ ,A-Za-z0-9.-]*$'
