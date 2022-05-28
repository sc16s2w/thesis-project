from supar import Parser


if __name__ == '__main__':
    parser = Parser.load('biaffine-dep-en')
    dataset = parser.predict('I saw Sarah with a telescope.', lang='en', prob=True, verbose=False)
    print(dataset[0])
    con = Parser.load('crf-con-en')
    con.predict(['The', 'man','who','is','the','teacher','is','going', 'to','work', '.'], verbose=False)[0].pretty_print()