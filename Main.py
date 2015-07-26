__author__ = 'chengmin'
from Sentiment import *
ComputeSentiment("萬科三季報：手握現金315億")

#encoding=utf-8
import genius
text = u"""昨天,我和施瓦布先生一起与部分企业家进行了交流,大家对中国经济当前、未来发展的态势、走势都十分关心。"""
seg_list = genius.seg_text(
    text,
    use_combine=True,
    use_pinyin_segment=True,
    use_tagging=True,
    use_break=True
)
print('\n'.join(['%s\t%s' % (word.text, word.tagging) for word in seg_list]))