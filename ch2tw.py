from opencc import OpenCC

cc = OpenCC('s2twp')
text = '他对女人的厌恶近乎神经质'

print(cc.convert(text))